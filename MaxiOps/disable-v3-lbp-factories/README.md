# Disable V3 Liquidity Bootstrapping Pool Factories

## Summary

Prepared Safe Transaction Builder payloads to disable all currently deployed V3 LBP factories, including:

| Version | Deployment task | Status in deployments repo |
|---|---|---|
| v1 | [`20250307-v3-liquidity-bootstrapping-pool`](https://github.com/balancer/balancer-deployments/tree/master/v3/deprecated/20250307-v3-liquidity-bootstrapping-pool) | deprecated |
| v2 | [`20250701-v3-liquidity-bootstrapping-pool-v2`](https://github.com/balancer/balancer-deployments/tree/master/v3/deprecated/20250701-v3-liquidity-bootstrapping-pool-v2) | deprecated |
| v3 | [`20251219-v3-liquidity-bootstrapping-pool-v3`](https://github.com/balancer/balancer-deployments/tree/master/v3/deprecated/20251219-v3-liquidity-bootstrapping-pool-v3) | deprecated |
| v4 | [`20260501-v3-liquidity-bootstrapping-pool-v4`](https://github.com/balancer/balancer-deployments/tree/master/v3/tasks/20260501-v3-liquidity-bootstrapping-pool-v4) | active |
| fixed-price | [`20251205-v3-fixed-price-lbp`](https://github.com/balancer/balancer-deployments/tree/master/v3/tasks/20251205-v3-fixed-price-lbp) | active |

On-chain `isDisabled()` was `false` for all factories at payload creation time.

**Do not execute until the replacement LBP factories are deployed.** These payloads permanently stop new pool creation from the listed factories.

## Technical Specification

For each factory, the executing safe performs the same 3-step Authorizer pattern used in BIP-914:

1. `grantRole(actionId, account)` on the Authorizer
2. `disable()` on the factory
3. `revokeRole(actionId, account)` on the Authorizer

`disable()` action IDs were taken from `balancer-deployments` action-ids (and verified on-chain via `getActionId(0x2f2770db)`). HyperEVM v1 was missing from action-ids and was queried on-chain.

## Executing Safes

Executing safes are the current Authorizer `DEFAULT_ADMIN_ROLE` holders (verified on-chain), so `grantRole` / `revokeRole` can succeed:

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
| sepolia | balancer_labs | `0x4F99ccB28e78886BEb4d08880e6555896ad7FDd8` | `0xA331D84eC860Bf466b4CdCcFb4aC09a1B43F3aE6` |

Note: unlike BIP-914 (which routed several L2 payloads through DAO safes), only **mainnet** currently has the DAO as Authorizer admin. All other listed production networks use the **Omnisig**. Sepolia uses **balancer_labs**.

## Factories by Network

### mainnet (chainId 1) — 5 factories / 15 txs

| Factory | Address | `disable()` actionId |
|---|---|---|
| LBPoolFactory v1 | `0x4eff2d77D9fFbAeFB4b141A3e494c085b3FF4Cb5` | `0xcaf85986241f9906113741c5e12e9d1d7a67832f717d4ed507beb522e69334b1` |
| LBPoolFactory v2 | `0x02916d8F0891309806FCb347Bf4191692cbDDcAF` | `0xec386230b43d2777141af97e47dae057801371989fd72e32faacec52147502db` |
| LBPoolFactory v3 | `0xD5584b37D1845fFeD958C2d94bC675603DdCce68` | `0x72fd4963dcf180d1df4e653ff72a27ca0c9e8943829fa0a6de70f3dde5a0c7ed` |
| LBPoolFactory v4 | `0x6642863979e66d995717A2B836A121700595069A` | `0x2f9da633af72e79ee363d063d4a1793f03d08d19cbab7d6b126e9dbc6e533360` |
| FixedPriceLBPoolFactory | `0xeb1AA94421aEcFB1dc17dDB1068E4609c4bE8758` | `0x9117651d3db1f75e5aba050b30b85baf13b7a0821a9ce8b3118f8ca4b7033046` |

Payload: [`disable-v3-lbp-factories-mainnet.json`](./disable-v3-lbp-factories-mainnet.json)

### optimism (chainId 10) — 2 factories / 6 txs

| Factory | Address | `disable()` actionId |
|---|---|---|
| LBPoolFactory v1 | `0xC1A64500E035D9159C8826E982dFb802003227f0` | `0x63917ea03eefb14da2515f5d2ec64da1d52edecca471b857d62e2fe7bb62660f` |
| LBPoolFactory v4 | `0x6642863979e66d995717A2B836A121700595069A` | `0x2f9da633af72e79ee363d063d4a1793f03d08d19cbab7d6b126e9dbc6e533360` |

Payload: [`disable-v3-lbp-factories-optimism.json`](./disable-v3-lbp-factories-optimism.json)

### gnosis (chainId 100) — 5 factories / 15 txs

| Factory | Address | `disable()` actionId |
|---|---|---|
| LBPoolFactory v1 | `0x6eE18fbb1BBcC5CF700cD75ea1aef2bb21e3cB3F` | `0x6febf9f238dc2ec20e86da0ec49412a1a4d6f6a3a5de38e57a31d7f05dd323f8` |
| LBPoolFactory v2 | `0x53EFf5068A1A3b39a9157DA6eF5A18d555c479eF` | `0xa58fd4a4bf957636db02af34ea4f6b78cc0dc1a1246aa3314baf7f972d0c9ee9` |
| LBPoolFactory v3 | `0x2FAa140F90f76eeEEBC191f4eF4b2634be1E4e91` | `0x063cae26eb3f9aaad18da492e015286aa80679463c4eed391ec4559ff072e940` |
| LBPoolFactory v4 | `0x6642863979e66d995717A2B836A121700595069A` | `0x2f9da633af72e79ee363d063d4a1793f03d08d19cbab7d6b126e9dbc6e533360` |
| FixedPriceLBPoolFactory | `0xD9E91f7aD501929b089992842a3f193795E6479e` | `0x8cb3d0b6606d6e551685018bd40ddf3428101d6e75fb95cdf7f5e7b322e8fccd` |

Payload: [`disable-v3-lbp-factories-gnosis.json`](./disable-v3-lbp-factories-gnosis.json)

### monad (chainId 143) — 3 factories / 9 txs

| Factory | Address | `disable()` actionId |
|---|---|---|
| LBPoolFactory v3 | `0xa3b370092aeb56770B23315252aB5E16DAcBF62B` | `0x544c6420e7cdee475b31065882694ecf59beaee0baf58f5d68d87f1a08039e8b` |
| LBPoolFactory v4 | `0x6642863979e66d995717A2B836A121700595069A` | `0x2f9da633af72e79ee363d063d4a1793f03d08d19cbab7d6b126e9dbc6e533360` |
| FixedPriceLBPoolFactory | `0xe2fa4e1d17725e72dcdAfe943Ecf45dF4B9E285b` | `0x740f4332364e3e7815877d3129b935f10ce37584e973ed33b93e793000a1c263` |

Payload: [`disable-v3-lbp-factories-monad.json`](./disable-v3-lbp-factories-monad.json)

### xlayer (chainId 196) — 3 factories / 9 txs

| Factory | Address | `disable()` actionId |
|---|---|---|
| LBPoolFactory v3 | `0xa3b370092aeb56770B23315252aB5E16DAcBF62B` | `0x544c6420e7cdee475b31065882694ecf59beaee0baf58f5d68d87f1a08039e8b` |
| LBPoolFactory v4 | `0xDE3d3d70Cc85a456f2D2569Ddec1ba38fA144837` | `0x4be9c29c0ff87c4564b34dc925f347d1f61d65719c8dcb2de9b8399f788774c0` |
| FixedPriceLBPoolFactory | `0xC1A64500E035D9159C8826E982dFb802003227f0` | `0x63917ea03eefb14da2515f5d2ec64da1d52edecca471b857d62e2fe7bb62660f` |

Payload: [`disable-v3-lbp-factories-xlayer.json`](./disable-v3-lbp-factories-xlayer.json)

### hyperevm (chainId 999) — 5 factories / 15 txs

| Factory | Address | `disable()` actionId |
|---|---|---|
| LBPoolFactory v1 | `0x013D4382F291be5688AFBcc741Ee8A24C66B2C92` | `0x8a09a4e6ece4d90d1e061f59a0083a9ea8b51542e5c17d1533148b57910e2c67` |
| LBPoolFactory v2 | `0xa1D0791a41318c775707C56eAe247AF81a05322C` | `0x668986fc2832f58b18f6dbb6bd3930239eb176f8c74768d3386c75061f84eabd` |
| LBPoolFactory v3 | `0xd22eecBB495380Ef52b1CCeF1cA594979885D484` | `0xe3ac7b0854230587876d79e6d6fd0b1667117a72c169379e4c47a1b2a5d53b00` |
| LBPoolFactory v4 | `0x6642863979e66d995717A2B836A121700595069A` | `0x2f9da633af72e79ee363d063d4a1793f03d08d19cbab7d6b126e9dbc6e533360` |
| FixedPriceLBPoolFactory | `0xAE563E3f8219521950555F5962419C8919758Ea2` | `0xf3bfbb6eabf20290d4cb2ef46f2bb0912e1e2a204fd7eeffec2eba4d63c58583` |

Payload: [`disable-v3-lbp-factories-hyperevm.json`](./disable-v3-lbp-factories-hyperevm.json)

### base (chainId 8453) — 5 factories / 15 txs

| Factory | Address | `disable()` actionId |
|---|---|---|
| LBPoolFactory v1 | `0x662112B8CB18889e81459b92CA0f894a2ef2c1B8` | `0xb4abfdf0a490599e9a35cfefa92ed81b15bcf767a883899f9aaf250dd67fa6ed` |
| LBPoolFactory v2 | `0x0b11209B8c5E821b18dED147583b8978c3E63911` | `0x3f6401a12ca8f8048783a6e5b059877235fcf452f62691cbcbe45ebe6bf3c217` |
| LBPoolFactory v3 | `0x6eE18fbb1BBcC5CF700cD75ea1aef2bb21e3cB3F` | `0x6febf9f238dc2ec20e86da0ec49412a1a4d6f6a3a5de38e57a31d7f05dd323f8` |
| LBPoolFactory v4 | `0x6642863979e66d995717A2B836A121700595069A` | `0x2f9da633af72e79ee363d063d4a1793f03d08d19cbab7d6b126e9dbc6e533360` |
| FixedPriceLBPoolFactory | `0xb96524227c4B5Ab908FC3d42005FE3B07abA40E9` | `0x54ed747f10bf74fca2a1110cb69c6328e2fb5025039aede2933d04dfc21abd11` |

Payload: [`disable-v3-lbp-factories-base.json`](./disable-v3-lbp-factories-base.json)

### plasma (chainId 9745) — 4 factories / 12 txs

| Factory | Address | `disable()` actionId |
|---|---|---|
| LBPoolFactory v2 | `0x0f08eEf2C785AA5e7539684aF04755dEC1347b7c` | `0xc4947a848de6cca284acda6c460b475a939b9ad4ed6361cb81514fb0c723493e` |
| LBPoolFactory v3 | `0x3BEb058DE1A25dd24223fd9e1796df8589429AcE` | `0xfd7d049f57516387fe0b442e1455675b11c641859ce76b39f121f650f51650ac` |
| LBPoolFactory v4 | `0x6642863979e66d995717A2B836A121700595069A` | `0x2f9da633af72e79ee363d063d4a1793f03d08d19cbab7d6b126e9dbc6e533360` |
| FixedPriceLBPoolFactory | `0xEAedc32a51c510d35ebC11088fD5fF2b47aACF2E` | `0x34f66ef5706b2abf916d3f719040884c962d3a419b90ec8af8fb2c1f6ea4e313` |

Payload: [`disable-v3-lbp-factories-plasma.json`](./disable-v3-lbp-factories-plasma.json)

### arbitrum (chainId 42161) — 5 factories / 15 txs

| Factory | Address | `disable()` actionId |
|---|---|---|
| LBPoolFactory v1 | `0x4BB42f71CAB7Bd13e9f958dA4351B9fa2d3A42FF` | `0x2cb59d35a7a1b89d4ca6e466034d4d7bba7efe0e0dbb3bbe125e78def0cbdac1` |
| LBPoolFactory v2 | `0x8D217CB74f675B46cC2767C8cF0aAB53BE1c4818` | `0x420e98f887204e24065ca464f7424e10e354754d5a9fa42b526de06cdefb61ec` |
| LBPoolFactory v3 | `0xF9309a99836b5F07a2440c177C049b0f0A9A2c33` | `0x9cfdab4beadfcae7d0f179599ccd11866e01cf1ee5c21374f6261d4c8338d914` |
| LBPoolFactory v4 | `0x6b7DEd11F15D6AB9959c29cEd3Cd101D69A14c35` | `0x547f0f109bf2934c5c301cb9ec94fbaac37c2c3c51fc3047d90c714cd5b17f27` |
| FixedPriceLBPoolFactory | `0x7f246E7Bab4CdC8C7AB41EaDA8290009a5b26E0D` | `0x563e4481a97a41cdd413da1f83ac6635161c37618c79f5212599f5d564353f36` |

Payload: [`disable-v3-lbp-factories-arbitrum.json`](./disable-v3-lbp-factories-arbitrum.json)

### avalanche (chainId 43114) — 2 factories / 6 txs

| Factory | Address | `disable()` actionId |
|---|---|---|
| LBPoolFactory v1 | `0x3BEb058DE1A25dd24223fd9e1796df8589429AcE` | `0xfd7d049f57516387fe0b442e1455675b11c641859ce76b39f121f650f51650ac` |
| LBPoolFactory v4 | `0x6642863979e66d995717A2B836A121700595069A` | `0x2f9da633af72e79ee363d063d4a1793f03d08d19cbab7d6b126e9dbc6e533360` |

Payload: [`disable-v3-lbp-factories-avalanche.json`](./disable-v3-lbp-factories-avalanche.json)

### sepolia (chainId 11155111) — 5 factories / 15 txs

| Factory | Address | `disable()` actionId |
|---|---|---|
| LBPoolFactory v1 | `0xA714753434481DbaBf7921963f18190636eCde69` | `0xb490583a5207c0875ec6bcc27ce2607b53142dc2ad5852e8476477429ff06260` |
| LBPoolFactory v2 | `0xE92cF5185384f53B2af74A2eBA62ba3A9C0ED65B` | `0x87718798d7b3fba119fbf388701396c35009cf180dcdcc0ce48653017185674a` |
| LBPoolFactory v3 | `0x7fed0fd2843232973eE2F61120e9D9C5eB78Cb16` | `0x4b362040436c8b495a8424d2a1081300c6e4653c003541d31c8d4e409db7435d` |
| LBPoolFactory v4 | `0x4b32854C043c70548879921b9A1880D8f8C583d0` | `0x14e633b9c27287c8ffac0d056e7e3afe84d72ebd769ca3214b3ea14b7bb5e095` |
| FixedPriceLBPoolFactory | `0x57Ef4cB125d1c690dF98118281090b7CdC7b9F85` | `0x3e54e84f69e39ee0118535e3189370750c02371414e7dfaf80e9e196c80f7fb5` |

Payload: [`disable-v3-lbp-factories-sepolia.json`](./disable-v3-lbp-factories-sepolia.json)

## Payload Files

- [`disable-v3-lbp-factories-mainnet.json`](./disable-v3-lbp-factories-mainnet.json) — 5 factories, 15 transactions
- [`disable-v3-lbp-factories-optimism.json`](./disable-v3-lbp-factories-optimism.json) — 2 factories, 6 transactions
- [`disable-v3-lbp-factories-gnosis.json`](./disable-v3-lbp-factories-gnosis.json) — 5 factories, 15 transactions
- [`disable-v3-lbp-factories-monad.json`](./disable-v3-lbp-factories-monad.json) — 3 factories, 9 transactions
- [`disable-v3-lbp-factories-xlayer.json`](./disable-v3-lbp-factories-xlayer.json) — 3 factories, 9 transactions
- [`disable-v3-lbp-factories-hyperevm.json`](./disable-v3-lbp-factories-hyperevm.json) — 5 factories, 15 transactions
- [`disable-v3-lbp-factories-base.json`](./disable-v3-lbp-factories-base.json) — 5 factories, 15 transactions
- [`disable-v3-lbp-factories-plasma.json`](./disable-v3-lbp-factories-plasma.json) — 4 factories, 12 transactions
- [`disable-v3-lbp-factories-arbitrum.json`](./disable-v3-lbp-factories-arbitrum.json) — 5 factories, 15 transactions
- [`disable-v3-lbp-factories-avalanche.json`](./disable-v3-lbp-factories-avalanche.json) — 2 factories, 6 transactions
- [`disable-v3-lbp-factories-sepolia.json`](./disable-v3-lbp-factories-sepolia.json) — 5 factories, 15 transactions

