# BIP-XXX: BAL Tokenomics Revamp — Payloads

## 1. Zero All Gauge Type Weights (Halt BAL Emissions)

Instead of killing individual gauges, all gauge type weights are set to 0 on the GaugeController. This stops new BAL from being minted while allowing existing unclaimed BAL to still be claimed.

**File:** `BIP-XXX-zero-gauge-type-weights.json`
**Safe:** `0x10A19e7eE7d7F8a52822f6817de8ea18204F2e4f` (DAO multisig)
**Entrypoint:** `0xf5dECDB1f3d1ee384908Fbe16D2F0348AE43a9eA` (AuthorizerAdaptorEntrypoint)
**Target:** `0xC128468b7Ce63eA702C1f104D55A2566b13D3ABD` (GaugeController)
**Function:** `change_type_weight(int128, uint256)` (`0xdb1ca260`)
**Transactions:** 5

| Type ID | Name | Active Gauges | Current Weight | New Weight |
|---------|------|---------------|----------------|------------|
| 1 | veBAL | 0 | 1 | 0 |
| 2 | Ethereum | 160 | 1 | 0 |
| 3 | Polygon | 3 | 1 | 0 |
| 4 | Arbitrum | 2 | 1 | 0 |
| 5 | Optimism | 0 | 1 | 0 |

## 2. V3 Swap Fee Reduction (50% -> 25%)

Separate per-chain payloads reduce the V3 global protocol swap fee from 50% to 25% and propagate to all existing pools.

**Safe:** `0x9ff471F9f98F42E5151C7855fD1b5aa906b1AF7e` (Omni)

| Chain | File | Txs |
|-------|------|-----|
| Mainnet (part 1) | `BIP-XXX-reduce-v3-swap-fee-mainnet-part1.json` | 151 (1 global + 150 pools) |
| Mainnet (part 2) | `BIP-XXX-reduce-v3-swap-fee-mainnet-part2.json` | 200 pools |
| Mainnet (part 3) | `BIP-XXX-reduce-v3-swap-fee-mainnet-part3.json` | 200 pools |
| Mainnet (part 4) | `BIP-XXX-reduce-v3-swap-fee-mainnet-part4.json` | 200 pools |
| Mainnet (part 5) | `BIP-XXX-reduce-v3-swap-fee-mainnet-part5.json` | 200 pools |
| Mainnet (part 6) | `BIP-XXX-reduce-v3-swap-fee-mainnet-part6.json` | 200 pools |
| Mainnet (part 7) | `BIP-XXX-reduce-v3-swap-fee-mainnet-part7.json` | 28 pools |
| Arbitrum | `BIP-XXX-reduce-v3-swap-fee-arbitrum.json` | 76 (1 global + 75 pools) |
| Base | `BIP-XXX-reduce-v3-swap-fee-base.json` | 308 (1 global + 307 pools) |
| Gnosis | `BIP-XXX-reduce-v3-swap-fee-gnosis.json` | 44 (1 global + 43 pools) |
| Avalanche | `BIP-XXX-reduce-v3-swap-fee-avalanche.json` | 46 (1 global + 45 pools) |
| HyperEVM | `BIP-XXX-reduce-v3-swap-fee-hyperevm.json` | 34 (1 global + 33 pools) |
| Plasma | `BIP-XXX-reduce-v3-swap-fee-plasma.json` | 39 (1 global + 38 pools) |
| Monad | `BIP-XXX-reduce-v3-swap-fee-monad.json` | 20 (1 global + 19 pools) |
| X Layer | `BIP-XXX-reduce-v3-swap-fee-xlayer.json` | 3 (1 global + 2 pools) |

Each payload calls `setGlobalProtocolSwapFeePercentage(250000000000000000)` followed by `updateProtocolSwapFeePercentage(pool)` for every V3 pool on that chain via the ProtocolFeeController v2.

Mainnet split into 7 parts due to block gas limit (~30M). Part 1 must execute first (contains the global fee change). 3 pools excluded due to transfer-restricted tokens (CMTDE_V3, fake USDT).
