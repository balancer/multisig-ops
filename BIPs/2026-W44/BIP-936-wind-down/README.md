# BIP-936 post-vote queue (factory disables + pause grants)

Snapshot: [`0x47126e…3563`](https://snapshot.org/#/s:balancer.eth/proposal/0x47126e7bd8e02a63ee7022e32c01ec2884a4443c770b9533621391b001663563)

**BIP-936 passed** (closed, ~6.31M yes, quorum met) at vote end **19:00 Europe/Amsterdam, 27 Oct 2026**.

### Queuing

| Target | How |
|--------|-----|
| Omni (all live omni-admin chains) | JSON copies in `OmniAutoOps/BIP-936-*.json` — auto-upload on merge to `main` via `auto_upload_payloads.yaml` |
| Ethereum DAO | Import `BIP-936-mainnet.json` in Safe Tx Builder ([queue](https://app.safe.global/transactions/queue?safe=eth:0x10A19e7eE7d7F8a52822f6817de8ea18204F2e4f)). Auto-upload only proposes via the omni nested safe, not the DAO. |
| BSC 6-of-11 | Import `BIP-936-bsc.json` ([safe](https://app.safe.global/home?safe=bnb:0x58099b94e660bBe19848547F6c5d76DcA7282E45)). Optional / non-blocking. |

## Shape (agreed)

| Chain set | Safe | Contents |
|-----------|------|----------|
| Ethereum | DAO `0x10A19e7eE7d7F8a52822f6817de8ea18204F2e4f` | Factory `disable()` (+ self-`grantRole` where needed) + V2 pause/recovery grants + V3 `pausePool` grant |
| Live omni-admin chains | Omni `0x9ff471F9f98F42E5151C7855fD1b5aa906b1AF7e` | Same pattern |
| BSC | `0x58099b94e660bBe19848547F6c5d76DcA7282E45` (6-of-11) | Parallel / non-blocking |

Grants are `grantRole(actionId, account)` only. Pause EOA (gosuto): `0x4BC8121278056BFCaC2BD14D455659224d6dDf48`.

- V2: one `pause`/`setPaused` role and one `enableRecoveryMode` role **per factory**
- V3: one `pausePool` role **per chain** (vault action id)
- Role revokes wait until **1 Dec**
- Partner / extension pools (21) are **not** in this batch; Friday pause scripts skip them

Fraxtal and Mode: no enabled factories and no V3 vault pause action — nothing to queue.

## Rebuild

```bash
export DRPC_KEY=...   # or DRPC_API_KEY
python3 tools/python/wind_down/build_bip936_post_vote_queue.py
```

## Files

See `summary.json` for per-chain tx counts and factory lists. Each `BIP-936-<chain>.json` is Safe Transaction Builder format; matching `.notes.txt` lists call intent in order.
