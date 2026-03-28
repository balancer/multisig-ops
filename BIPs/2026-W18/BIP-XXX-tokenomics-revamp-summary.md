# BIP-XXX: Kill All Gauges (veBAL Sunset)

As part of the BAL Tokenomics Revamp, all active gauges are killed to halt BAL emissions.

**Total gauges to kill: 165**
**Safe:** `0x9ff471F9f98F42E5151C7855fD1b5aa906b1AF7e` (Omni)
**Entrypoint:** `0xf5dECDB1f3d1ee384908Fbe16D2F0348AE43a9eA` (AuthorizerAdaptorEntrypoint)
**Function:** `killGauge()` (`0xab8f0945`)

## Summary by Chain

| Chain | Count |
|-------|-------|
| ARBITRUM | 27 |
| AVALANCHE | 11 |
| BASE | 23 |
| GNOSIS | 11 |
| MAINNET | 71 |
| OPTIMISM | 10 |
| POLYGON | 12 |

## Full Gauge List

| # | Root Gauge Address | Chain | Pool Symbol | Tokens |
|---|-------------------|-------|-------------|--------|
| 1 | `0xc4b6cc9a444337b1cb8cbbdd9de4d983f609c391` | ARBITRUM | 2BTC | WBTC, tBTC |
| 2 | `0x75ba7f8733c154302cbe2e19fe3ec417e0679833` | ARBITRUM | 2CLP-AUSDC-USDC | waUSDCn, USDC |
| 3 | `0xf937bf168b33d8d10d555e9a039ec1b8e4c543d1` | ARBITRUM | 2CLP-AUSDT-USDT | waUSDT, USDT |
| 4 | `0x175407b4710b5a1cb67a37c76859f17fb2ff6672` | ARBITRUM | 55auraBal-45wsteth | auraBAL, wstETH |
| 5 | `0x98fbf8fc81edc411a53db921ab0eb82d97a6f123` | ARBITRUM | 80PRF-20WETH | PRF, WETH |
| 6 | `0xdb7981655db66aa9bd489c76323b88bd1545c7ab` | ARBITRUM | Aave GHO-USDai | USDai, waArbGHO |
| 7 | `0x9b237fa1958e3022464343137738926d38815801` | ARBITRUM | Aave GHO/USDT/USDC | waArbUSDCn, waArbUSDT, waArbGHO |
| 8 | `0xb2fcad9fd42affd0a90a996a1dede4427435e5f8` | ARBITRUM | Aave wstETH-wETH | waArbWETH, waArbwstETH |
| 9 | `0xca318253bb460e08ca33fd22574e7f70217130f5` | ARBITRUM | Aave wstETH/ezETH | waArbezETH, waArbwstETH |
| 10 | `0xac3b3fff577561c58f126e4f6375f56476dd9fdb` | ARBITRUM | Balancer rETH-Aave wETH | waArbWETH, rETH |
| 11 | `0x7e123ad65cc842ab93bf2dc79a8eade8975bd3cb` | ARBITRUM | ECLP-GYD-AUSDT | waUSDT, GYD |
| 12 | `0xc11442cdbe8901b36aeb7be7f3f95b6a8ade394e` | ARBITRUM | ECLP-wstETH-GYD | wstETH, GYD |
| 13 | `0x7f49d37d0da53a4899bc0ba916f59ec9d4e6d1e2` | ARBITRUM | EURe-Aave USDC | EURe, waArbUSDCn |
| 14 | `0x1a965ea559364fb5667985b26899644712c81b18` | ARBITRUM | Gyro eBTC- Aave weETH | eBTC, waArbweETH |
| 15 | `0x72e7d4b2925a33a8f57e4b080eeac4fa778a5729` | ARBITRUM | Gyro eBTC-Aave USDCn | eBTC, waArbUSDCn |
| 16 | `0x8135d6abfd42707a87a7b94c5cfa3529f9b432ad` | ARBITRUM | RDNT-WETH | RDNT, WETH |
| 17 | `0x088040aa3e8fdf780829c07f8cc53fa8a8f07fa9` | ARBITRUM | Surge eBTC-Aave WBTC | waArbWBTC, eBTC |
| 18 | `0x2d1c51eab8b3c2287ba26061c0e339da3b15b955` | ARBITRUM | Surge orbETH-Aave wETH | waArbWETH, orbETH |
| 19 | `0xeb312b0d7795743c3de905bc09c0d62aa180a7a6` | ARBITRUM | Surge sUSDX USDX aUSDT | sUSDX, waArbUSDT, USDX |
| 20 | `0xc77ac1ae3434260baefce0e23582c1249392d12d` | ARBITRUM | Surge yUSD-Aave USDC | yUSD, waArbUSDCn |
| 21 | `0x41de33d3b227677af277b6c29cb2545195df508c` | ARBITRUM | USDe/USDC | USDe, USDC |
| 22 | `0x6f7f4e708d54e314892df3d6960e1dd987f75141` | ARBITRUM | eeUSDC-yUSND | yUSND, eeUSDC |
| 23 | `0x0fc6169f74b1d0bbe7a269c1ee8d92edb58b1ade` | ARBITRUM | osETH-WETH | waArbWETH, osETH |
| 24 | `0x3c982431ffde3447a2086495631d1af27bd5686d` | ARBITRUM | reCLAMM-AAVE-WETH | WETH, AAVE |
| 25 | `0x1c5007af9907ac83f6d391b18f28fb2f5f8c9493` | ARBITRUM | sUSDe/USDe | sUSDe, USDe |
| 26 | `0xb4db5e1098b5a40ce4b36c9ebfef23a54e50db65` | ARBITRUM | tETH-Aave weETH | tETH, waArbweETH |
| 27 | `0x9172ad6a79cd6a25f60b1312262ec51219e05f6d` | ARBITRUM | yUSD-AaveUSDC | waArbUSDCn, yUSD |
| 28 | `0xd3ea1345352047bd039bac9d4177c883e06d449d` | AVALANCHE | Aave GHO/USDT/USDC | waAvaUSDT, waAvaGHO, waAvaUSDC |
| 29 | `0xb2a8f0f477aae4d78ea78d85234233285c91bb08` | AVALANCHE | Aave USDT/USDC/AUSD | waAvaAUSD, waAvaUSDT, waAvaUSDC |
| 30 | `0x608f2b6f31c102ad4b956761956e2362e2ba8941` | AVALANCHE | Aave wAVAX/BTC.b | waAvaBTC.b, waAvaWAVAX |
| 31 | `0x0aea1abc694a3608c8ac5f131d8310f95039111a` | AVALANCHE | Aave wAVAX/wETH.e | waAvaWAVAX, waAvaWETH |
| 32 | `0xd43fc9340adbff1c0c28db7a5fb554f736d256fa` | AVALANCHE | Euler Re7 savUSD-AUSD-USDC | eAUSD-2, eUSDC-2, esavUSD-2 |
| 33 | `0xd42fae61a6d0f8466b9e790db921c3469d5bef55` | AVALANCHE | Gyro AAVE WAVAX-USDC | waAvaWAVAX, waAvaUSDC |
| 34 | `0xa7165e1e3defe55dada5c4289268d57faba6dad2` | AVALANCHE | Surge eK3 savUSD-USDT | esavUSD-3, eUSDt-3 |
| 35 | `0x1f0ee42d005b89814a01f050416b28c3142ac900` | AVALANCHE | USDp-mevUSDC | mevUSDC, USDp |
| 36 | `0x5c13c3b72b031b6405046c319b2d840d3c1403c7` | AVALANCHE | aWAVAX-aSAVAX-ggAVAX | waAvaSAVAX, ggAVAX, waAvaWAVAX |
| 37 | `0xf53b66d40d166eb8f6e33ba2cd4af35c81a4c6c2` | AVALANCHE | tAVAX-waAvaSAVAX | tAVAX, waAvaSAVAX |
| 38 | `0x219b3a4a2d2351582277a87048995034ca7e9aef` | AVALANCHE | upAUSD-savUSD-sdeUSD | savUSD, upAUSD, sdeUSD |
| 39 | `0x156cc29c8dfa80821ed240c3ca4ba85103e10f2b` | BASE |  50tBTC-50USD | tBTC, USDbC |
| 40 | `0x5b5bad6a124c5f45b4289908ba15ff0047928648` | BASE | 20WETH-80IMO | WETH, IMO |
| 41 | `0x5faa5dbe07e4473819d22bb6f5d8179817305d71` | BASE | 30waBasUSDC-70FYNI | FYNI, waBasUSDC |
| 42 | `0xfcce9b5c1e8d56d9fc6dcbb706acc51dd03fe9f1` | BASE | 80PRL-20WETH | WETH, PRL |
| 43 | `0x1b7e33186c7e9c337508bb65ea9dc498ab14fcae` | BASE | Aave GHO-USR | USR, waBasGHO |
| 44 | `0x1da19f38eb6f2c22199dc0848118b26095c29aed` | BASE | Aave USDC-Aave GHO | waBasGHO, waBasUSDC |
| 45 | `0x86c44de72ec88d205e63c2af8d577659319c7a7f` | BASE | Aave wstETH-ezETH | waBaswstETH, waBasezETH |
| 46 | `0x0855e486ee80ff0ec7c913ec0588a7cbf2b8e89c` | BASE | Aave wstETH-wETH | waBaswstETH, waBasWETH |
| 47 | `0xa9390f0e0fd42d3a53a5ba8ed2a381ba29a2ed8e` | BASE | BAL-AURA-waBasUSDC | AURA, BAL, waBasUSDC |
| 48 | `0xaa23fc5fafba846f07181761903fb9350e954c34` | BASE | BTF:BMACRO | WETH, USDC, AERO, cbBTC |
| 49 | `0x31ccb4e5005fd37005523e6e3f1d084f9abe25b6` | BASE | Balancer rETH-Aave wETH | rETH, waBasWETH |
| 50 | `0x3143f29f2d541b03d8526c265a54fbc727da6565` | BASE | ECLP-WETH-USDC | WETH, USDC |
| 51 | `0x17c67ca47d472d16fbc09f0a0408edee22180cee` | BASE | ECLP-weETH-wstETH | weETH, wstETH |
| 52 | `0xf81d677abac5ac56c7c6386f85f2720badc6eb4c` | BASE | ExtraFi-exUSDC-exUSR | wexBaseUSDC, wexBaseUSR |
| 53 | `0xb1e8ec305b0b29097a117cafc9721a553533e54c` | BASE | Surge Aave EURC-GHO | waBasEURC, waBasGHO |
| 54 | `0x9604a525630e7d9d72d804bdcb678862bab1971c` | BASE | Surge Aave wstETH-fWETH | waBaswstETH, fWETH |
| 55 | `0x0d3f5d4022279c536a53aaa6bb8c225a0226d168` | BASE | Surge yUSD-Aave USDC | yUSD, waBasUSDC |
| 56 | `0x5a65665161a2b231fd1bb22fbebfa1cb624bdbc3` | BASE | Surge yUSD-Aave USDC | yUSD, waBasUSDC |
| 57 | `0xc9fffc7d9810d2a3deee7de70e2fb41781a5d779` | BASE | USDp-USDC | USDp, USDC |
| 58 | `0x533382463506f3b513ebbe9f2be7fbb49ccaef25` | BASE | USDp-frxUSD | USDp, frxUSD |
| 59 | `0x67313e858fb87cc4b30ad56b6b461d7450738950` | BASE | axlBAL/BAL | axlBAL, BAL |
| 60 | `0xb145b0ef7dfd7e02b181f4c9a880e8aeced9bcf3` | BASE | axlETH/ETH | WETH, axlETH |
| 61 | `0x53d051f583d418de6512db1bde281957f043937b` | BASE | smUSDC-sUSDS | sUSDS, smUSDC |
| 62 | `0xc61e7e858b5a60122607f5c7df223a53b01a1389` | GNOSIS | 50COW-50GNO | COW, GNO |
| 63 | `0x40b04058ff35fd3164e6cc66c4e6398c1e5e68c8` | GNOSIS | 50waWstETH-50waGNO | waGnowstETH, waGnoGNO |
| 64 | `0x2041f8a758a0266e1b9272fcd4b1f1c37b67d5da` | GNOSIS | B-50sDAI-50wstETH | wstETH, sDAI |
| 65 | `0x64fced4684f4b065e6b900c4e99a0cbacc5e5fe1` | GNOSIS | B-50wstETH-25BAL-25AURA | AURA, wstETH, BAL |
| 66 | `0x93ae6971f03ce890fa4e9274ab441477b84dae5f` | GNOSIS | B-50wstETH-50COW | COW, wstETH |
| 67 | `0xb1af0d75aeea1c13c450ffc7e12083072daf41eb` | GNOSIS | B-50wstETH-50GNO | wstETH, GNO |
| 68 | `0x7632c11c49e6091504bb0395c0c81c8be48f4a8c` | GNOSIS | BRLA-sDAI | sDAI, BRLA |
| 69 | `0xc0b75da8e6f6403804efefde3101b02276c5f8ea` | GNOSIS | ECLP-sDAI-USDC.e-rh | sDAI, waUSDCn |
| 70 | `0x6d060a785530cb13795b3c5a43320c462811d43b` | GNOSIS | ECLP-wstETH-WETH | WETH, wstETH |
| 71 | `0x5c36197a631649441649028110fa503a3be00162` | GNOSIS | aGNO/sDAI | waGnoGNO, sDAI |
| 72 | `0xfd151734ffc9a4a55c50fed4b66c15b06bbb390b` | GNOSIS | waWstETH-waWETH | waGnoWETH, waGnowstETH |
| 73 | `0x47c56a900295df5224ec5e6751dc31eb900321d5` | MAINNET | 20WETH-80WNCG | WETH, WNCG |
| 74 | `0x54839a2fe079a21311127f3d811ec8c7afd0a2e9` | MAINNET | 50-ZCHF-50-svZCHF | ZCHF, svZCHF |
| 75 | `0x57ab3b673878c3feab7f8ff434c40ab004408c4c` | MAINNET | 50COW-50GNO | GNO, COW |
| 76 | `0x7c777eea1dc264e71e567fcc9b6ddaa9064eff51` | MAINNET | 50COW-50WETH | WETH, COW |
| 77 | `0x275df57d2b23d53e20322b4bb71bf1dcb21d0a00` | MAINNET | 50WETH-50AURA | WETH, AURA |
| 78 | `0xf7b0751fea697cf1a541a5f57d11058a8fb794ee` | MAINNET | 50wstETH-50ACX | ACX, wstETH |
| 79 | `0x8fb6ef455dcb9cf747576ff36196a4c4535b81d6` | MAINNET | 60-GOLD-40-wstETH | wstETH, GOLD |
| 80 | `0x4eb7c7fd67b9b2c24d9ff1601ccda5a01bd40c7f` | MAINNET | 75SDEX25AaveLidoETH | waEthLidoWETH, SDEX |
| 81 | `0x6732ed78bf1d8afa3ef03f1ead302d21b0b2b1ff` | MAINNET | 80-ixEdel-20-USDC | USDC, ixEdel |
| 82 | `0x2f534f93928b99a4759a5c6a75a61b34132a06ff` | MAINNET | 80ALCX-20WETH | WETH, ALCX |
| 83 | `0x24b7aeeefdb612d43f018cbc9c325680f61ec96d` | MAINNET | 80GEM-20WETH | GEM, WETH |
| 84 | `0x30fb447441195a5b72a382ef14c5865c0fc1a9aa` | MAINNET | 80PRL-20WETH | PRL, WETH |
| 85 | `0xcc6a23446f6388d78f3037bd55f2eb820352d982` | MAINNET | 80T-20TBTC | tBTC, T |
| 86 | `0xdbd4dd2d5e0b927022c2be8d493f20e79e60c2e7` | MAINNET | 80TREE-20AavePrimeWETH | waEthLidoWETH, TREE |
| 87 | `0x5b79494824bc256cd663648ee1aad251b32693a9` | MAINNET | 80USH-20unshETH | unshETH, USH |
| 88 | `0x9fdd52efeb601e4bc78b89c6490505b8ac637e9f` | MAINNET | Aave GHO/USDT/USDC | waEthUSDT, Aave Prime GHO, waEthUSDC |
| 89 | `0x4b891340b51889f438a03dc0e8aaafb0bc89e7a6` | MAINNET | Aave Lido wETH-wstETH | waEthLidoWETH, waEthLidowstETH |
| 90 | `0x6c0a4550c575c917435f228d36939125a437a98b` | MAINNET | Aave PyUSD-Lido GHO | Aave Core pyUSD, Aave Prime GHO |
| 91 | `0xeec405b834c90b59122bcc2357f27110b2adb4b7` | MAINNET | Aave USDC-USDT | waEthUSDT, waEthUSDC |
| 92 | `0xb78543e00712c3abba10d0852f6e38fde2aaba4d` | MAINNET | B-80BAL-20WETH | BAL, WETH |
| 93 | `0x80cd37a62a8a58c4cbf64003410c5ccc4d01519f` | MAINNET | B-KAI-WETH-WEIGHTED | KAI, WETH |
| 94 | `0x0312aa8d0ba4a1969fddb382235870bf55f7f242` | MAINNET | B-auraBAL-STABLE | B-80BAL-20WETH, auraBAL |
| 95 | `0x5bbaed1fadc08c5fb3e4ae3c8848777e2da77103` | MAINNET | B-csUSDC-csUSDL | csUSDC, csUSDL |
| 96 | `0x4fd03b8c15e70e6b3413e4d2ff3825a19746e78b` | MAINNET | B-kaiAURA-AURA-WEIGHTED | AURA, kaiAURA |
| 97 | `0xdc2df969ee5e66236b950f5c4c5f8abe62035df2` | MAINNET | B-sdBAL-STABLE | B-80BAL-20WETH, sdBal |
| 98 | `0x2d42910d826e5500579d121596e98a6eb33c0a1b` | MAINNET | B-wjAura-wETH | wjAURA, WETH |
| 99 | `0x56124eb16441a1ef12a4ccaeabdd3421281b795a` | MAINNET | BAL-20WETH-80LIT | WETH, LIT |
| 100 | `0x093e02dec0b5a40c03d84ecda6058ad91436923f` | MAINNET | BTFSH | WBTC, PAXG, USDC |
| 101 | `0xd0f4829f6ccb2df530445519d8d84d1e715f6391` | MAINNET | DVstETH-Prime wstETH | DVstETH, waEthLidowstETH |
| 102 | `0x9c1a157cf8b242f67b3c950eda9a30b320bde9cd` | MAINNET | ECLP-GYD-USDC | USDC, GYD |
| 103 | `0xfc7d964f1676831d8105506b1f0c3b3e2b55c467` | MAINNET | ECLP-GYD-USDT | USDT, GYD |
| 104 | `0xfc3f916c28f32deba1cc04b1f6011f28a691134c` | MAINNET | ECLP-GYD-sDAI | sDAI, GYD |
| 105 | `0x146b6030e6d6a6398b918e9854652a71c9537180` | MAINNET | ECLP-sUSDe-GYD | sUSDe, GYD |
| 106 | `0xa00db7d9c465e95e4aa814a9340b9a161364470a` | MAINNET | ECLP-stdeUSD-deUSD | deUSD, sdeUSD |
| 107 | `0xf2c203a264dc05942cfbaea16f712b2106c2fb02` | MAINNET | ECLP-ynETH-wstETH | ynETH, wstETH |
| 108 | `0x1f3a4c8115629c33a28bf2f97f22d31d256317f6` | MAINNET | ETHx waWETH | waEthWETH, ETHx |
| 109 | `0x8e891a7b048a594592e9f0de70dc223143b4f1e6` | MAINNET | QI BPT | QI, WETH |
| 110 | `0xf22bbdad6b3dd9314bdf97724df32b09ff95c216` | MAINNET | RDNT-WETH | RDNT, WETH |
| 111 | `0x15c84754c7445d0df6c613f1490ca07654347c1b` | MAINNET | STG/USDC | USDC, STG |
| 112 | `0xf6a9bbb5d9733fa6f77120683636061bc26e7e85` | MAINNET | ShezUSD-sDAI | ShezUSD, sDAI |
| 113 | `0x8f1e24671e90bb3e43adaedf79a5c6e42ed74f72` | MAINNET | Steak USDR-USDQ-USDT | steakUSDTlite, steakUSDR, steakUSDQ |
| 114 | `0x1cce9d493224a19fcb5f7fbade8478630141cb54` | MAINNET | Surge Fluid wstETH-wETH | fwstETH, fWETH |
| 115 | `0x52d28dff7759ca78978954ebabf87481bd5cf8f0` | MAINNET | Surge USDf-aGHO | Aave Prime GHO, USDf |
| 116 | `0x6b8b1376f7e2a9ada08d0b8bacf5e0bad8b9b4ea` | MAINNET | Surge inwstETHs-gtWETHe | gtWETHe, inwstETHs |
| 117 | `0x2a42644c1d3e1b4fe6d01fdbc995fc402694a49f` | MAINNET | Surge sUSDX USDX aUSDT | sUSDX, waEthUSDT, USDX |
| 118 | `0xb1efe3b01d5cf28bd923de3e5a567621588f435a` | MAINNET | Surge siUSD-sUSDe | sUSDe, siUSD |
| 119 | `0xd5a0eb558d62780b10ecc202d0049b89f6145073` | MAINNET | Surge tETH-Lido wstETH | waEthLidowstETH, tETH |
| 120 | `0x9798995a042973d9705a4f0fea691a4541d13b43` | MAINNET | Surge wUSDN-Prime GHO | WUSDN, Aave Prime GHO |
| 121 | `0x5a099e2c2a41a5a0ad99e4971c711400eeef34db` | MAINNET | TrustlessMaxi | BOLD, WUSDN |
| 122 | `0xc4e72abe8a32fd7d7ba787e1ec860ecb8c0b333c` | MAINNET | USDC/WETH/L | USDC, WETH |
| 123 | `0xa67fbb1e751e0c6ecd9a213c960a11fd4b3b691d` | MAINNET | aUSDC-USP | USP, waEthUSDC |
| 124 | `0x3d45d7d8eea466829292430d5cb5c2a44b3b0502` | MAINNET | baoBTC-tBTC | tBTC, baoBTC |
| 125 | `0xac681deb529b49b5a563fbf0dcccb95d5bb7cdb0` | MAINNET | iUSD-Aave GHO | iUSD, Aave Prime GHO |
| 126 | `0x3b163ca3875e91c580bdec0ce9c97d4ef6501f20` | MAINNET | inwstETHs-waEthLidowstETH | waEthLidowstETH, inwstETHs |
| 127 | `0xc77fc22917501d7d299f27be9847077b6fcbde53` | MAINNET | ixAQUA | XAUt, waEthUSDT, cbBTC, ixEdel, svZCHF |
| 128 | `0x6baed4cd5833b47095b9a8ba65d4529ea37d32e2` | MAINNET | ixFORUM | SKY, LDO, sUSDS, ixEdel, svZCHF |
| 129 | `0xd3a3848c5d445d9ab4bd78346ec674031d0713fa` | MAINNET | ixSTRATA | LINK, AAVE, Aave Prime GHO, ixEdel, svZCHF |
| 130 | `0x7a59af3a8650edc8ebe6d79162a2aa97f2b98aac` | MAINNET | kaiAURA-AURA | AURA, kaiAURA |
| 131 | `0xcf72a84edaae931385e84fb4c2edee07a32822a6` | MAINNET | msUSD-USDC | msUSD, USDC |
| 132 | `0x5241b61045afb7bc7e031bfe4931ef4bd614d5ec` | MAINNET | msUSD-iUSD | iUSD, msUSD |
| 133 | `0x42d9ee7049f5dc573fe08330a3597af17437ebb6` | MAINNET | msY-msUSD | msUSD, msY |
| 134 | `0x70a1c01902dab7a45dca1098ca76a8314dd8adba` | MAINNET | osETH-waWETH | waEthWETH, osETH |
| 135 | `0x3a51bdf9013633ae934a3630db96f09ae4c5814a` | MAINNET | pxETH-gtWETHe | pxETH, gtWETHe |
| 136 | `0x62a66eb9abf7a788f48d0ce7c0c065df9e09da19` | MAINNET | rETH-waEthWETH | waEthWETH, rETH |
| 137 | `0x3612493e894c251d57bf24f837d2d05493dd6a24` | MAINNET | rETH-xrETH | rETH, xrETH |
| 138 | `0x6ba97c44aecf7cc15b05947c172a6d797ce96693` | MAINNET | reCLAMM-AAVE-WETH | AAVE, WETH |
| 139 | `0xcbc0a61e99fe3adba90bead3738446952bcb8002` | MAINNET | rsETH-hgETH | rsETH, hgETH |
| 140 | `0x04202b147eae6f5f50cbf72d0b8e9459c57b15e6` | MAINNET | rstETH-Lido wstETH | waEthLidowstETH, rstETH |
| 141 | `0x09afec27f5a6201617aad014ceea8deb572b0608` | MAINNET | sNOTE-BPT | WETH, NOTE |
| 142 | `0x95d260ac86b58d458187c819f87aad2c7c4203ef` | MAINNET | waUSDe-waUSDT | waEthUSDe, waEthUSDT |
| 143 | `0xb5bd58c733948e3d65d86ba9604e06e5da276fd1` | MAINNET | wstETH/rETH/L | wstETH, rETH |
| 144 | `0x132296d1dfd10ba55b565c4cfe49d350617a2a2b` | OPTIMISM | BPT-OPARA | OP, PSP |
| 145 | `0xd0b6787589d33b4f7aa5a27f36497e091e78a2ad` | OPTIMISM | BPT-RESERVE | USDC.e, ERN |
| 146 | `0x1ce5bf7e6c16c567defd625e0911bfd0fc7f2d7d` | OPTIMISM | BPT-ROAD | WETH, OP, USDC.e |
| 147 | `0xd606ea6f6d93d90efafc7d21972353fb98205eb8` | OPTIMISM | Balancer rETH-Aave wETH | waOptWETH, rETH |
| 148 | `0x730a168cf6f501cf302b803ffc57ff3040f378bf` | OPTIMISM | ECLP-wstETH-WETH | wstETH, WETH |
| 149 | `0x91bec9e7867635487668b3df73971456a6a5f2fa` | OPTIMISM | bpt-50sfrxUSD-50waOptWETH | waOptWETH, sfrxUSD |
| 150 | `0x2fb78cd279fd613891fdac2681444ad3541c31b2` | OPTIMISM | bpt-wrsETH-waOptWETH | waOptWETH, wrsETH |
| 151 | `0xeadb24ebe7348f716780c162c56b61bef8283455` | OPTIMISM | eclp-sfrxETH-waOptWETH | sfrxETH, waOptWETH |
| 152 | `0xab39b84287769481d7d004e17ac3875248d3c631` | OPTIMISM | eclp-sfrxUSD-waOptUSDCn | waOptUSDCn, sfrxUSD |
| 153 | `0x6ddedcdb545e04927b2aba21778a790a3318e3cb` | OPTIMISM | ss-sfrxETH-rETH-wstETH | sfrxETH, waOptrETH, waOptwstETH |
| 154 | `0x852580e3e1c0fd35de426c5481670c1772525265` | POLYGON | 2CHF (VCHF) | jCHF, VCHF |
| 155 | `0x16289f675ca54312a8fcf99341e7439982888077` | POLYGON | 2eur (PAR) | jEUR, PAR |
| 156 | `0x1f5cb5b832f27e24a3b0ad4b837d3ed26ff7ac6e` | POLYGON | 80TETU-20USDC | TETU, USDC |
| 157 | `0x8e4debfb047efcf6501665160739818e90ed621f` | POLYGON | ECLP-GYD-AUSDT | waUSDT, GYD |
| 158 | `0x7f5a5c80ceeb1c91718a71030f67788f3810be98` | POLYGON | ECLP-PAR-EUROe | EUROe, PAR |
| 159 | `0x9b2defbf22be1ccd63f36dadf69842feb5e7b8df` | POLYGON | ECLP-PAR-EURe | EURe, PAR |
| 160 | `0x87306f713eab296f87ca4519295668fb4bd51f04` | POLYGON | ECLP-paUSD-USDC-rh | waUSDCn, paUSD |
| 161 | `0x9fbfcb0547dc7d57258b8cf57a57624c6c3a61a1` | POLYGON | LP-COPM-USDC | COPM, USDC |
| 162 | `0xa532f5aafb0b268d873443d621521ee0eeb8a6d3` | POLYGON | LP-TXAG-USDC | USDC, TXAG |
| 163 | `0x2b7bd050d7e0341fb49ff96f32ea59bd8087d487` | POLYGON | LP-XSGD-USDC | USDC, XSGD |
| 164 | `0xd1177e2157a7fd6a0484b79f8e50e8a9305f8063` | POLYGON | tetuBAL-BALWETH | 20WETH-80BAL, tetuBAL |
| 165 | `0xf6a814ed60653cb0e36da247b01e6309318328d4` | POLYGON | tetuBAL-BALWETH | 20WETH-80BAL, tetuBAL |

## V3 Swap Fee Reduction (50% -> 25%)

Separate per-chain payloads reduce the V3 global protocol swap fee from 50% to 25% and propagate to all existing pools:

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

