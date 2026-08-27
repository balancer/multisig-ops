# Disable Deprecated V3 Liquidity Bootstrapping Pool Factories

## Summary

Safe Transaction Builder payloads to disable **deprecated** V3 LBP factories only:

| Version | Deployment task | Status |
|---|---|---|
| v1 | [`20250307-v3-liquidity-bootstrapping-pool`](https://github.com/balancer/balancer-deployments/tree/master/v3/deprecated/20250307-v3-liquidity-bootstrapping-pool) | deprecated |
| v2 | [`20250701-v3-liquidity-bootstrapping-pool-v2`](https://github.com/balancer/balancer-deployments/tree/master/v3/deprecated/20250701-v3-liquidity-bootstrapping-pool-v2) | deprecated |
| v3 | [`20251219-v3-liquidity-bootstrapping-pool-v3`](https://github.com/balancer/balancer-deployments/tree/master/v3/deprecated/20251219-v3-liquidity-bootstrapping-pool-v3) | deprecated |

**Excluded:** v4, FixedPriceLBPoolFactory, and Sepolia.

**21 factories across 10 networks** (63 transactions).

## Which versions exist on which chains

Not every deprecated version was deployed everywhere:

| Network | v1 | v2 | v3 |
|---|---|---|---|
| mainnet | yes | yes | yes |
| arbitrum | yes | yes | yes |
| base | yes | yes | yes |
| gnosis | yes | yes | yes |
| hyperevm | yes | yes | yes |
| plasma | — | yes | yes |
| optimism | yes | — | — |
| avalanche | yes | — | — |
| monad | — | — | yes |
| xlayer | — | — | yes |

- **v1+v2+v3:** mainnet, arbitrum, base, gnosis, hyperevm
- **v2+v3 only (no v1):** plasma
- **v1 only:** optimism, avalanche
- **v3 only (no v1/v2):** monad, xlayer

## Payload locations

| Network | Path | Executing safe |
|---|---|---|
| mainnet | [`BIPs/2026-W35/BIP-918-disable-deprecated-v3-lbp-factories-mainnet.json`](../../BIPs/2026-W35/BIP-918-disable-deprecated-v3-lbp-factories-mainnet.json) | DAO Multisig |
| All other networks below | this directory (`disable-v3-lbp-factories-<network>.json`) | Omnisig |

## Technical Specification

For each factory: `grantRole(actionId)` → `disable()` → `revokeRole(actionId)` (same pattern as BIP-914).

### HyperEVM v1 action ID

HyperEVM v1 factory `0x013D4382F291be5688AFBcc741Ee8A24C66B2C92` has on-chain:

```text
getActionId(disable()) = 0x8a09a4e6ece4d90d1e061f59a0083a9ea8b51542e5c17d1533148b57910e2c67
```

That value was **queried on-chain** because `action-ids/hyperevm/action-ids.json` in `balancer-deployments` has **never** contained task `20250307-v3-liquidity-bootstrapping-pool` (checked across hyperevm action-ids history). The factory *is* recorded in `addresses/hyperevm.json` and `output/hyperevm.json`, but its action IDs were never generated/backfilled into the hyperevm action-ids file (likely skipped when HyperEVM action-ids were first produced, after v1 was already deprecated).

CI reports resolve roles via `bal_addresses` / deployments action-ids, so this role will show as unresolved / N/A for HyperEVM even though `getActionId` on the live factory returns it. Same class of gap as BIP-914’s overwritten oracle factories that were also missing from action-ids.

## Executing Safes

| Network | Safe | Address | Authorizer |
|---|---|---|---|
| mainnet | DAO Multisig | `0x10A19e7eE7d7F8a52822f6817de8ea18204F2e4f` | `0xA331D84eC860Bf466b4CdCcFb4aC09a1B43F3aE6` |
| optimism | Omnisig | `0x9ff471F9f98F42E5151C7855fD1b5aa906b1AF7e` | `0xA331D84eC860Bf466b4CdCcFb4aC09a1B43F3aE6` |
| gnosis | Omnisig | `0x9ff471F9f98F42E5151C7855fD1b5aa906b1AF7e` | `0xA331D84eC860Bf466b4CdCcFb4aC09a1B43F3aE6` |
| monad | Omnisig | `0x9ff471F9f98F42E5151C7855fD1b5aa906b1AF7e` | `0xE39B5e3B6D74016b2F6A9673D7d7493B6DF549d5` |
| xlayer | Omnisig | `0x9ff471F9f98F42E5151C7855fD1b5aa906b1AF7e` | `0xE39B5e3B6D74016b2F6A9673D7d7493B6DF549d5` |
| hyperevm | Omnisig | `0x9ff471F9f98F42E5151C7855fD1b5aa906b1AF7e` | `0x85a80afee867aDf27B50BdB7b76DA70f1E853062` |
| base | Omnisig | `0x9ff471F9f98F42E5151C7855fD1b5aa906b1AF7e` | `0x809B79b53F18E9bc08A961ED4678B901aC93213a` |
| plasma | Omnisig | `0x9ff471F9f98F42E5151C7855fD1b5aa906b1AF7e` | `0xE39B5e3B6D74016b2F6A9673D7d7493B6DF549d5` |
| arbitrum | Omnisig | `0x9ff471F9f98F42E5151C7855fD1b5aa906b1AF7e` | `0xA331D84eC860Bf466b4CdCcFb4aC09a1B43F3aE6` |
| avalanche | Omnisig | `0x9ff471F9f98F42E5151C7855fD1b5aa906b1AF7e` | `0xA331D84eC860Bf466b4CdCcFb4aC09a1B43F3aE6` |

## Factories by Network

### mainnet (chainId 1) — 3 factories / 9 txs

| Factory | Address | `disable()` actionId |
|---|---|---|
| LBPoolFactory v1 | `0x4eff2d77D9fFbAeFB4b141A3e494c085b3FF4Cb5` | `0xcaf85986241f9906113741c5e12e9d1d7a67832f717d4ed507beb522e69334b1` |
| LBPoolFactory v2 | `0x02916d8F0891309806FCb347Bf4191692cbDDcAF` | `0xec386230b43d2777141af97e47dae057801371989fd72e32faacec52147502db` |
| LBPoolFactory v3 | `0xD5584b37D1845fFeD958C2d94bC675603DdCce68` | `0x72fd4963dcf180d1df4e653ff72a27ca0c9e8943829fa0a6de70f3dde5a0c7ed` |

Payload: [`BIPs/2026-W35/BIP-918-disable-deprecated-v3-lbp-factories-mainnet.json`](../../BIPs/2026-W35/BIP-918-disable-deprecated-v3-lbp-factories-mainnet.json)

### optimism (chainId 10) — 1 factory / 3 txs

| Factory | Address | `disable()` actionId |
|---|---|---|
| LBPoolFactory v1 | `0xC1A64500E035D9159C8826E982dFb802003227f0` | `0x63917ea03eefb14da2515f5d2ec64da1d52edecca471b857d62e2fe7bb62660f` |

Payload: [`disable-v3-lbp-factories-optimism.json`](./disable-v3-lbp-factories-optimism.json)

### gnosis (chainId 100) — 3 factories / 9 txs

| Factory | Address | `disable()` actionId |
|---|---|---|
| LBPoolFactory v1 | `0x6eE18fbb1BBcC5CF700cD75ea1aef2bb21e3cB3F` | `0x6febf9f238dc2ec20e86da0ec49412a1a4d6f6a3a5de38e57a31d7f05dd323f8` |
| LBPoolFactory v2 | `0x53EFf5068A1A3b39a9157DA6eF5A18d555c479eF` | `0xa58fd4a4bf957636db02af34ea4f6b78cc0dc1a1246aa3314baf7f972d0c9ee9` |
| LBPoolFactory v3 | `0x2FAa140F90f76eeEEBC191f4eF4b2634be1E4e91` | `0x063cae26eb3f9aaad18da492e015286aa80679463c4eed391ec4559ff072e940` |

Payload: [`disable-v3-lbp-factories-gnosis.json`](./disable-v3-lbp-factories-gnosis.json)

### monad (chainId 143) — 1 factory / 3 txs

| Factory | Address | `disable()` actionId |
|---|---|---|
| LBPoolFactory v3 | `0xa3b370092aeb56770B23315252aB5E16DAcBF62B` | `0x544c6420e7cdee475b31065882694ecf59beaee0baf58f5d68d87f1a08039e8b` |

Payload: [`disable-v3-lbp-factories-monad.json`](./disable-v3-lbp-factories-monad.json)

### xlayer (chainId 196) — 1 factory / 3 txs

| Factory | Address | `disable()` actionId |
|---|---|---|
| LBPoolFactory v3 | `0xa3b370092aeb56770B23315252aB5E16DAcBF62B` | `0x544c6420e7cdee475b31065882694ecf59beaee0baf58f5d68d87f1a08039e8b` |

Payload: [`disable-v3-lbp-factories-xlayer.json`](./disable-v3-lbp-factories-xlayer.json)

### hyperevm (chainId 999) — 3 factories / 9 txs

| Factory | Address | `disable()` actionId |
|---|---|---|
| LBPoolFactory v1 | `0x013D4382F291be5688AFBcc741Ee8A24C66B2C92` | `0x8a09a4e6ece4d90d1e061f59a0083a9ea8b51542e5c17d1533148b57910e2c67` (on-chain; missing from action-ids) |
| LBPoolFactory v2 | `0xa1D0791a41318c775707C56eAe247AF81a05322C` | `0x668986fc2832f58b18f6dbb6bd3930239eb176f8c74768d3386c75061f84eabd` |
| LBPoolFactory v3 | `0xd22eecBB495380Ef52b1CCeF1cA594979885D484` | `0xe3ac7b0854230587876d79e6d6fd0b1667117a72c169379e4c47a1b2a5d53b00` |

Payload: [`disable-v3-lbp-factories-hyperevm.json`](./disable-v3-lbp-factories-hyperevm.json)

### base (chainId 8453) — 3 factories / 9 txs

| Factory | Address | `disable()` actionId |
|---|---|---|
| LBPoolFactory v1 | `0x662112B8CB18889e81459b92CA0f894a2ef2c1B8` | `0xb4abfdf0a490599e9a35cfefa92ed81b15bcf767a883899f9aaf250dd67fa6ed` |
| LBPoolFactory v2 | `0x0b11209B8c5E821b18dED147583b8978c3E63911` | `0x3f6401a12ca8f8048783a6e5b059877235fcf452f62691cbcbe45ebe6bf3c217` |
| LBPoolFactory v3 | `0x6eE18fbb1BBcC5CF700cD75ea1aef2bb21e3cB3F` | `0x6febf9f238dc2ec20e86da0ec49412a1a4d6f6a3a5de38e57a31d7f05dd323f8` |

Payload: [`disable-v3-lbp-factories-base.json`](./disable-v3-lbp-factories-base.json)

### plasma (chainId 9745) — 2 factories / 6 txs

| Factory | Address | `disable()` actionId |
|---|---|---|
| LBPoolFactory v2 | `0x0f08eEf2C785AA5e7539684aF04755dEC1347b7c` | `0xc4947a848de6cca284acda6c460b475a939b9ad4ed6361cb81514fb0c723493e` |
| LBPoolFactory v3 | `0x3BEb058DE1A25dd24223fd9e1796df8589429AcE` | `0xfd7d049f57516387fe0b442e1455675b11c641859ce76b39f121f650f51650ac` |

Payload: [`disable-v3-lbp-factories-plasma.json`](./disable-v3-lbp-factories-plasma.json)

### arbitrum (chainId 42161) — 3 factories / 9 txs

| Factory | Address | `disable()` actionId |
|---|---|---|
| LBPoolFactory v1 | `0x4BB42f71CAB7Bd13e9f958dA4351B9fa2d3A42FF` | `0x2cb59d35a7a1b89d4ca6e466034d4d7bba7efe0e0dbb3bbe125e78def0cbdac1` |
| LBPoolFactory v2 | `0x8D217CB74f675B46cC2767C8cF0aAB53BE1c4818` | `0x420e98f887204e24065ca464f7424e10e354754d5a9fa42b526de06cdefb61ec` |
| LBPoolFactory v3 | `0xF9309a99836b5F07a2440c177C049b0f0A9A2c33` | `0x9cfdab4beadfcae7d0f179599ccd11866e01cf1ee5c21374f6261d4c8338d914` |

Payload: [`disable-v3-lbp-factories-arbitrum.json`](./disable-v3-lbp-factories-arbitrum.json)

### avalanche (chainId 43114) — 1 factory / 3 txs

| Factory | Address | `disable()` actionId |
|---|---|---|
| LBPoolFactory v1 | `0x3BEb058DE1A25dd24223fd9e1796df8589429AcE` | `0xfd7d049f57516387fe0b442e1455675b11c641859ce76b39f121f650f51650ac` |

Payload: [`disable-v3-lbp-factories-avalanche.json`](./disable-v3-lbp-factories-avalanche.json)
