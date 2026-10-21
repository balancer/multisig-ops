-- BIP-928 tetuBAL snapshot (forum post block) + look-through
-- ETH 25977785 / Polygon 93806051 / 50% share / >10 BAL @50%
-- Look-through: xtetuBAL vault, both tetuBAL-BPT pools, gauges,
--               GaugeDepositor → Tetu BPT vaults
-- Expected: bal_behind ≈ 2,791,186.14 · 50% per tetuBAL ≈ 2.53896

WITH params AS (
  SELECT
    DATE '2026-09-14' AS snap_date,
    CAST(25977785 AS bigint) AS eth_block,
    CAST(93806051 AS bigint) AS poly_block,
    0x9cc56fa7734da21ac88f6a816af10c5b898596ce AS bal_locker,
    0x5c6ee304399dbdb9c8ef030ab642b10820db8f56 AS bpt_80_20,
    0xba100000625a3754423978a60c9317c58a424e3d AS bal,
    0x7fc9e0aa043787bfad28e29632ada302c790ce33 AS tetubal,
    0xdade618e95f5e51198c69ba0a9cc3033874fa643 AS xtetu_strategy,
    0x915e49f7cd8b2b5763759c23d9463a74d5b5c1d5 AS xtetu_vault,
    0xba12222222228d8ba445958a75a0704d566bf2c8 AS bal_vault,
    0x7af62c1ebf97034b7542ccec13a2e79bbcf34380 AS old_pool,
    0xb797adfb7b268faeaa90cadbfed464c76ee599cd AS new_pool,
    0xe42d1087c84902ceca43c9887259eb611cfd58ca AS old_gauge,
    0x608f2b6f31c102ad4b956761956e2362e2ba8941 AS new_gauge,
    0x1f46804e2d4b11ce7a61e36720df316b7343b023 AS gauge_depositor,
    0xe4f7ed41e2461f162c9409015874716a1e96776f AS old_bpt_vault,
    0xbd06685a0e7ebd7c92fc84274b297791f3997ed3 AS new_bpt_vault,
    0.5 AS fraction,
    10.0 AS min_bal_50pct
),

-- ---------- ETH: BAL behind BalLocker ----------
locker_locked_bpt AS (
  SELECT
    (
      COALESCE((
        SELECT SUM(CAST(value AS DOUBLE))
        FROM balancer_ethereum.VotingEscrow_evt_Deposit d
        CROSS JOIN params p
        WHERE d.provider = p.bal_locker
          AND d.evt_block_number <= p.eth_block
      ), 0)
      - COALESCE((
        SELECT SUM(CAST(value AS DOUBLE))
        FROM balancer_ethereum.VotingEscrow_evt_Withdraw w
        CROSS JOIN params p
        WHERE w.provider = p.bal_locker
          AND w.evt_block_number <= p.eth_block
      ), 0)
    ) / 1e18 AS locked_bpt
),

bpt_supply AS (
  SELECT
    SUM(
      CASE
        WHEN "from" = 0x0000000000000000000000000000000000000000 THEN CAST(value AS DOUBLE)
        WHEN "to" = 0x0000000000000000000000000000000000000000 THEN -CAST(value AS DOUBLE)
        ELSE 0
      END
    ) / 1e18 AS bpt_supply
  FROM erc20_ethereum.evt_Transfer t
  CROSS JOIN params p
  WHERE t.contract_address = p.bpt_80_20
    AND t.evt_block_number <= p.eth_block
),

bal_in_pool AS (
  SELECT token_balance AS bal_in_pool
  FROM balancer.liquidity l
  CROSS JOIN params p
  WHERE l.blockchain = 'ethereum'
    AND l.pool_address = p.bpt_80_20
    AND l.token_address = p.bal
    AND l.day <= p.snap_date
  ORDER BY l.day DESC
  LIMIT 1
),

macro AS (
  SELECT
    l.locked_bpt,
    s.bpt_supply,
    b.bal_in_pool,
    b.bal_in_pool * l.locked_bpt / s.bpt_supply AS bal_behind_locker,
    b.bal_in_pool * l.locked_bpt / s.bpt_supply * p.fraction AS bal_behind_50pct
  FROM locker_locked_bpt l
  CROSS JOIN bpt_supply s
  CROSS JOIN bal_in_pool b
  CROSS JOIN params p
),

-- ---------- Polygon: last balance at/before snapshot ----------
token_balances AS (
  SELECT
    token_address,
    address,
    balance
  FROM (
    SELECT
      u.token_address,
      u.address,
      u.balance,
      ROW_NUMBER() OVER (
        PARTITION BY u.token_address, u.address
        ORDER BY u.block_number DESC, u.timestamp DESC
      ) AS rn
    FROM balances_polygon.updates u
    CROSS JOIN params p
    WHERE u.block_date <= p.snap_date
      AND u.block_number <= p.poly_block
      AND u.token_address IN (
        p.tetubal,
        p.xtetu_vault,
        p.old_pool,
        p.new_pool,
        p.old_gauge,
        p.new_gauge,
        p.old_bpt_vault,
        p.new_bpt_vault
      )
  )
  WHERE rn = 1
    AND balance > 0
),

tetubal_raw AS (
  SELECT address, balance AS amt
  FROM token_balances tb
  CROSS JOIN params p
  WHERE tb.token_address = p.tetubal
),

xtetu_shares AS (
  SELECT address, balance AS shares
  FROM token_balances tb
  CROSS JOIN params p
  WHERE tb.token_address = p.xtetu_vault
),

old_bpt_vault_shares AS (
  SELECT address, balance AS shares
  FROM token_balances tb
  CROSS JOIN params p
  WHERE tb.token_address = p.old_bpt_vault
),

new_bpt_vault_shares AS (
  SELECT address, balance AS shares
  FROM token_balances tb
  CROSS JOIN params p
  WHERE tb.token_address = p.new_bpt_vault
),

old_gauge_bals AS (
  SELECT address, balance AS amt
  FROM token_balances tb
  CROSS JOIN params p
  WHERE tb.token_address = p.old_gauge
),

new_gauge_bals AS (
  SELECT address, balance AS amt
  FROM token_balances tb
  CROSS JOIN params p
  WHERE tb.token_address = p.new_gauge
),

old_pool_bpt AS (
  SELECT address, balance AS amt
  FROM token_balances tb
  CROSS JOIN params p
  WHERE tb.token_address = p.old_pool
    AND address <> p.bal_vault   -- drop composable phantom BPT in Vault
),

new_pool_bpt AS (
  SELECT address, balance AS amt
  FROM token_balances tb
  CROSS JOIN params p
  WHERE tb.token_address = p.new_pool
),

-- tetuBAL sitting in each Balancer pool (via Vault)
pool_tetubal AS (
  SELECT
    MAX(CASE WHEN l.pool_address = p.old_pool THEN l.token_balance END) AS old_pool_tetu,
    MAX(CASE WHEN l.pool_address = p.new_pool THEN l.token_balance END) AS new_pool_tetu
  FROM (
    SELECT
      l.pool_address,
      l.token_balance,
      ROW_NUMBER() OVER (
        PARTITION BY l.pool_address
        ORDER BY l.day DESC
      ) AS rn
    FROM balancer.liquidity l
    CROSS JOIN params p
    WHERE l.blockchain = 'polygon'
      AND l.token_address = p.tetubal
      AND l.pool_address IN (p.old_pool, p.new_pool)
      AND l.day <= p.snap_date
  ) l
  CROSS JOIN params p
  WHERE rn = 1
),

-- ---------- Look-through claims (tetuBAL units) ----------
-- 1) Direct tetuBAL, skipping wrappers that are looked through
direct_claims AS (
  SELECT t.address, t.amt
  FROM tetubal_raw t
  CROSS JOIN params p
  WHERE t.address NOT IN (p.xtetu_strategy, p.bal_vault, p.new_bpt_vault)
),

-- 2) xtetuBAL strategy → vault shareholders (1:1 PPFS)
xtetu_claims AS (
  SELECT
    s.address,
    s.shares * COALESCE(st.amt, 0) / NULLIF(SUM(s.shares) OVER (), 0) AS amt
  FROM xtetu_shares s
  CROSS JOIN params p
  LEFT JOIN tetubal_raw st
    ON st.address = p.xtetu_strategy
),

-- 3) new BPT vault's own tetuBAL balance → its shareholders
new_vault_tetu_claims AS (
  SELECT
    s.address,
    s.shares * COALESCE(nv.amt, 0) / NULLIF(SUM(s.shares) OVER (), 0) AS amt
  FROM new_bpt_vault_shares s
  CROSS JOIN params p
  LEFT JOIN tetubal_raw nv
    ON nv.address = p.new_bpt_vault
),

-- 4) Old pool BPT → effective holders (gauge → GaugeDepositor → old BPT vault)
old_gauge_eff_bpt AS (
  SELECT
    CASE
      WHEN g.address = p.gauge_depositor THEN NULL  -- handled below
      ELSE g.address
    END AS address,
    CASE
      WHEN g.address = p.gauge_depositor THEN 0
      ELSE g.amt
    END AS amt,
    SUM(CASE WHEN g.address = p.gauge_depositor THEN g.amt ELSE 0 END) OVER () AS depositor_amt
  FROM old_gauge_bals g
  CROSS JOIN params p
),

old_depositor_to_vault AS (
  SELECT
    s.address,
    s.shares * d.depositor_amt / NULLIF(SUM(s.shares) OVER (), 0) AS amt
  FROM old_bpt_vault_shares s
  CROSS JOIN (SELECT MAX(depositor_amt) AS depositor_amt FROM old_gauge_eff_bpt) d
),

old_eff_bpt AS (
  SELECT address, amt FROM old_pool_bpt CROSS JOIN params p WHERE address <> p.old_gauge
  UNION ALL
  SELECT address, amt FROM old_gauge_eff_bpt WHERE address IS NOT NULL AND amt > 0
  UNION ALL
  SELECT address, amt FROM old_depositor_to_vault WHERE amt > 0
),

old_pool_claims AS (
  SELECT
    e.address,
    e.amt * pt.old_pool_tetu / NULLIF(SUM(e.amt) OVER (), 0) AS amt
  FROM old_eff_bpt e
  CROSS JOIN pool_tetubal pt
),

-- 5) New pool BPT → effective holders (gauge → GaugeDepositor → new BPT vault)
new_gauge_eff_bpt AS (
  SELECT
    CASE
      WHEN g.address = p.gauge_depositor THEN NULL
      ELSE g.address
    END AS address,
    CASE
      WHEN g.address = p.gauge_depositor THEN 0
      ELSE g.amt
    END AS amt,
    SUM(CASE WHEN g.address = p.gauge_depositor THEN g.amt ELSE 0 END) OVER () AS depositor_amt
  FROM new_gauge_bals g
  CROSS JOIN params p
),

new_depositor_to_vault AS (
  SELECT
    s.address,
    s.shares * d.depositor_amt / NULLIF(SUM(s.shares) OVER (), 0) AS amt
  FROM new_bpt_vault_shares s
  CROSS JOIN (SELECT MAX(depositor_amt) AS depositor_amt FROM new_gauge_eff_bpt) d
),

new_eff_bpt AS (
  SELECT address, amt FROM new_pool_bpt CROSS JOIN params p WHERE address <> p.new_gauge
  UNION ALL
  SELECT address, amt FROM new_gauge_eff_bpt WHERE address IS NOT NULL AND amt > 0
  UNION ALL
  SELECT address, amt FROM new_depositor_to_vault WHERE amt > 0
),

new_pool_claims AS (
  SELECT
    e.address,
    e.amt * pt.new_pool_tetu / NULLIF(SUM(e.amt) OVER (), 0) AS amt
  FROM new_eff_bpt e
  CROSS JOIN pool_tetubal pt
),

all_claims AS (
  SELECT address, amt FROM direct_claims
  UNION ALL
  SELECT address, amt FROM xtetu_claims
  UNION ALL
  SELECT address, amt FROM new_vault_tetu_claims
  UNION ALL
  SELECT address, amt FROM old_pool_claims
  UNION ALL
  SELECT address, amt FROM new_pool_claims
),

economic AS (
  SELECT
    address,
    SUM(amt) AS tetubal
  FROM all_claims
  CROSS JOIN params p
  WHERE address NOT IN (
    p.xtetu_strategy,
    p.bal_vault,
    p.xtetu_vault,
    p.old_pool,
    p.new_pool,
    p.old_gauge,
    p.new_gauge,
    p.gauge_depositor,
    p.old_bpt_vault,
    p.new_bpt_vault
  )
  GROUP BY 1
  HAVING SUM(amt) > 0
),

entitled AS (
  SELECT
    e.address,
    e.tetubal,
    e.tetubal / SUM(e.tetubal) OVER () * m.bal_behind_locker AS bal_100pct,
    e.tetubal / SUM(e.tetubal) OVER () * m.bal_behind_50pct AS bal_50pct
  FROM economic e
  CROSS JOIN macro m
)

SELECT
  ROW_NUMBER() OVER (ORDER BY e.bal_50pct DESC) AS rank,
  e.address,
  e.tetubal,
  e.bal_100pct,
  e.bal_50pct,
  m.locked_bpt,
  m.bal_behind_locker,
  m.bal_behind_50pct
FROM entitled e
CROSS JOIN macro m
CROSS JOIN params p
WHERE e.bal_50pct > p.min_bal_50pct
ORDER BY e.bal_50pct DESC
