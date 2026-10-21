-- BIP-928 tetuBAL snapshot (forum post block)
-- ETH 25977785 / Polygon 93806051 / 50% share / >10 BAL @50%
-- Direct Polygon tetuBAL balances only (no pool/vault look-through).
-- Off-chain look-through table: discourse.md in this folder.
-- Expected: bal_behind ≈ 2,791,186.14 · 50% per tetuBAL ≈ 2.53896

WITH params AS (
  SELECT
    DATE '2026-09-14' AS snap_date,
    CAST(25977785 AS bigint) AS eth_block,
    CAST(93806051 AS bigint) AS poly_block,
    0x9cc56fa7734da21ac88f6a816af10c5b898596ce AS bal_locker,
    0xc128a9954e6c874ea3d62ce62b468ba073093f25 AS voting_escrow,
    0x5c6ee304399dbdb9c8ef030ab642b10820db8f56 AS bpt_80_20,
    0xba100000625a3754423978a60c9317c58a424e3d AS bal,
    0x7fc9e0aa043787bfad28e29632ada302c790ce33 AS tetubal,
    0.5 AS fraction,
    10.0 AS min_bal_50pct
),

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

tetubal_holders AS (
  SELECT
    address,
    balance AS tetubal
  FROM (
    SELECT
      u.address,
      u.balance,
      ROW_NUMBER() OVER (
        PARTITION BY u.address
        ORDER BY u.block_number DESC, u.timestamp DESC
      ) AS rn
    FROM balances_polygon.updates u
    CROSS JOIN params p
    WHERE u.token_address = p.tetubal
      AND u.block_date <= p.snap_date
      AND u.block_number <= p.poly_block
  )
  WHERE rn = 1
    AND balance > 0
),

entitled AS (
  SELECT
    h.address,
    h.tetubal,
    h.tetubal / SUM(h.tetubal) OVER () * m.bal_behind_locker AS bal_100pct,
    h.tetubal / SUM(h.tetubal) OVER () * m.bal_behind_50pct AS bal_50pct
  FROM tetubal_holders h
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
