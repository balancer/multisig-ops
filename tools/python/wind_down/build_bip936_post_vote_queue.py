#!/usr/bin/env python3
"""
BIP-936 post-vote Safe queue builder.

Builds factory-disable + pause/recovery grant payloads per agreed wind-down shape:
  - Ethereum → DAO safe
  - Other live omni-admin chains → omni safe
  - BSC → separate 6-of-11 (optional / non-blocking)

Grants are grantRole(actionId, account) only (no where).
V2: one pause role + one enableRecoveryMode role per factory.
V3: one pausePool role per chain (vault action id) to the pause EOA.

Does NOT submit to Safe — queue only after BIP-936 has passed.
"""

from __future__ import annotations

import csv
import json
import os
import subprocess
import time
import urllib.request
import ssl
from collections import defaultdict
from pathlib import Path
from typing import Any

from eth_utils import keccak

ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "BIPs" / "2026-W44" / "BIP-936-wind-down"
CACHE = Path("/tmp/bal")
CACHE.mkdir(parents=True, exist_ok=True)

DRPC_KEY = os.environ.get("DRPC_KEY") or os.environ.get("DRPC_API_KEY")
assert DRPC_KEY, "DRPC_KEY (or DRPC_API_KEY) required"

DAO = "0x10A19e7eE7d7F8a52822f6817de8ea18204F2e4f"
OMNI = "0x9ff471F9f98F42E5151C7855fD1b5aa906b1AF7e"
BSC_SAFE = "0x58099b94e660bBe19848547F6c5d76DcA7282E45"
GOSUTO = "0x4BC8121278056BFCaC2BD14D455659224d6dDf48"

NETWORK = {
    "mainnet": "ethereum",
    "arbitrum": "arbitrum",
    "base": "base",
    "avalanche": "avalanche",
    "gnosis": "gnosis",
    "optimism": "optimism",
    "polygon": "polygon",
    "fraxtal": "fraxtal",
    "mode": "mode",
    "zkevm": "polygon-zkevm",
    "hyperevm": "hyperliquid",
    "monad": "monad",
    "plasma": "plasma",
    "bsc": "bsc",
    "xlayer": "xlayer",
}

CHAIN_ID = {
    "mainnet": "1",
    "arbitrum": "42161",
    "base": "8453",
    "avalanche": "43114",
    "gnosis": "100",
    "optimism": "10",
    "polygon": "137",
    "fraxtal": "252",
    "mode": "34443",
    "zkevm": "1101",
    "hyperevm": "999",
    "monad": "143",
    "plasma": "9745",
    "bsc": "56",
    "xlayer": "196",
}

SHEET_CHAIN = {
    "Ethereum": "mainnet",
    "Arbitrum": "arbitrum",
    "Base": "base",
    "Avalanche": "avalanche",
    "Gnosis": "gnosis",
    "Optimism": "optimism",
    "Polygon": "polygon",
    "BSC": "bsc",
    "Fraxtal": "fraxtal",
    "Mode": "mode",
    "Polygon zkEVM": "zkevm",
}

# Forum BIP-936 mainnet untracked / extra V3 factories (Balancer-code, enabled).
MAINNET_EXTRA_FACTORIES = [
    {
        "task": "untracked-reclamm",
        "contract": "ReClammPoolFactory",
        "address": "0x312600bc7645E47a4926dc658827398AF070D431",
        "proto": "v3",
    },
    {
        "task": "untracked-reclamm",
        "contract": "ReClammPoolFactory",
        "address": "0x7fA49Df302a98223d98D115fc4FCD275576f6faA",
        "proto": "v3",
    },
    {
        "task": "untracked-akron",
        "contract": "AkronWeightedPoolFactory",
        "address": "0x83Fa05e5a37f9C10F4B729EC80F7D38290313596",
        "proto": "v3",
    },
    {
        "task": "untracked-stable-surge",
        "contract": "StableSurgePoolFactory",
        "address": "0x92bad7860B85811E422eCaEAF38a672F8925fcfb",
        "proto": "v3",
    },
    {
        "task": "untracked-reclamm",
        "contract": "ReClammPoolFactory",
        "address": "0xCF7608f0136DB42FDEC021f755BD66406F29158c",
        "proto": "v3",
    },
    {
        "task": "untracked-quantamm",
        "contract": "QuantAMMWeightedPoolFactory",
        "address": "0xD5c43063563f9448cE822789651662cA7DcD5773",
        "proto": "v3",
    },
]

CTX = ssl.create_default_context()


def cast_sig(sig: str) -> str:
    return subprocess.check_output(["cast", "sig", sig], text=True).strip()


SEL_IS_DISABLED = cast_sig("isDisabled()")
SEL_DISABLE = cast_sig("disable()")
SEL_PAUSE = cast_sig("pause()")
SEL_SET_PAUSED = cast_sig("setPaused(bool)")
SEL_ENABLE_RECOVERY = cast_sig("enableRecoveryMode()")
SEL_HAS_ROLE = cast_sig("hasRole(bytes32,address)")
SEL_GET_ACTION_ID = cast_sig("getActionId(bytes4)")


def admin_for(chain: str) -> str:
    if chain == "mainnet":
        return DAO
    if chain == "bsc":
        return BSC_SAFE
    return OMNI


def safe_for(chain: str) -> str:
    return admin_for(chain)


def action_id_for(factory: str, selector4: str) -> str:
    """Balancer Authentication: keccak256(bytes32(uint160(disambiguator)) || bytes4)."""
    packed = factory[2:].lower().rjust(64, "0") + selector4[2:].lower()
    return "0x" + keccak(bytes.fromhex(packed)).hex()


def rpc_url(chain: str) -> str:
    return f"https://lb.drpc.org/ogrpc?network={NETWORK[chain]}&dkey={DRPC_KEY}"


def eth_calls(chain: str, calls: list[tuple[str, str]], chunk: int = 40) -> list[str | None]:
    out: list[str | None] = []
    for i in range(0, len(calls), chunk):
        batch = calls[i : i + chunk]
        payload = [
            {
                "jsonrpc": "2.0",
                "id": j,
                "method": "eth_call",
                "params": [{"to": to, "data": data}, "latest"],
            }
            for j, (to, data) in enumerate(batch)
        ]
        req = urllib.request.Request(
            rpc_url(chain),
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=90, context=CTX) as r:
            j = json.loads(r.read())
        if isinstance(j, dict):
            raise RuntimeError(j)
        by_id = {item["id"]: item for item in j}
        for jid in range(len(batch)):
            item = by_id[jid]
            out.append(None if "error" in item else item.get("result"))
    return out


def pad32(hex_or_addr: str) -> str:
    h = hex_or_addr[2:] if hex_or_addr.startswith("0x") else hex_or_addr
    return h.rjust(64, "0")


def has_role_data(role: str, account: str) -> str:
    return SEL_HAS_ROLE + pad32(role) + pad32(account)


def get_action_id_data(selector4: str) -> str:
    # bytes4 left-aligned in ABI word
    return SEL_GET_ACTION_ID + selector4[2:].ljust(64, "0")


def fetch_json(url: str, dest: Path) -> dict:
    if dest.exists() and dest.stat().st_size > 0:
        return json.loads(dest.read_text())
    req = urllib.request.Request(url, headers={"User-Agent": "balancer-wind-down"})
    with urllib.request.urlopen(req, timeout=60, context=CTX) as r:
        data = r.read()
    dest.write_bytes(data)
    return json.loads(data)


def ensure_sources() -> None:
    (CACHE / "action-ids").mkdir(parents=True, exist_ok=True)
    (CACHE / "addresses").mkdir(parents=True, exist_ok=True)
    for chain in NETWORK:
        fetch_json(
            f"https://raw.githubusercontent.com/balancer/balancer-deployments/master/action-ids/{chain}/action-ids.json",
            CACHE / "action-ids" / f"{chain}.json",
        )
        fetch_json(
            f"https://raw.githubusercontent.com/balancer/balancer-deployments/master/addresses/{chain}.json",
            CACHE / "addresses" / f"{chain}.json",
        )
    book_path = CACHE / "addressbook.json"
    if not book_path.exists():
        fetch_json(
            "https://raw.githubusercontent.com/balancer/bal_addresses/main/outputs/addressbook.json",
            book_path,
        )
    sheet_path = Path("/tmp/bip936_sheet.csv")
    if not sheet_path.exists():
        req = urllib.request.Request(
            "https://docs.google.com/spreadsheets/d/1xhTPdaDClz0KP9XgrVo1z7QlIucXwoX9_LszxhQf3nc/export?format=csv",
            headers={"User-Agent": "balancer-wind-down"},
        )
        with urllib.request.urlopen(req, timeout=60, context=CTX) as r:
            sheet_path.write_bytes(r.read())


def get_authorizer(chain: str) -> str:
    book = json.loads((CACHE / "addressbook.json").read_text())
    ch = book["active"][chain]
    for task in (
        "20210418-authorizer",
        "20250127-v3-contracts-deployment",
        "20241204-v3-vault",
    ):
        if task in ch and isinstance(ch[task], dict) and "Authorizer" in ch[task]:
            return ch[task]["Authorizer"]
    for contracts in ch.values():
        if isinstance(contracts, dict) and "Authorizer" in contracts:
            return contracts["Authorizer"]
    raise KeyError(f"No Authorizer for {chain}")


def is_pool_factory(task: str, name: str) -> bool:
    joined = f"{task}/{name}".lower()
    skip = [
        "lp-oracle",
        "oracle-factory",
        "rate-provider",
        "wrapped-token",
        "wrapped-bpt",
        "balancer-contract-registry",
        "child-chain",
        "gauge",
        "hook-factory",
        "router",
        "buffer",
        "mock",
        "test",
        "permit2",
        "protocol-fee",
    ]
    if any(x in joined for x in skip):
        return False
    if "Factory" not in name:
        return False
    return any(
        x in name
        for x in (
            "PoolFactory",
            "LinearPool",
            "ManagedPool",
            "LBPool",
            "LiquidityBootstrapping",
        )
    ) or (name.endswith("Factory") and "Pool" in name)


def find_pool_action(aids_task: dict | None, keys: list[str]) -> dict | None:
    if not aids_task:
        return None
    for cname, meta in aids_task.items():
        if not isinstance(meta, dict) or "Factory" in cname:
            continue
        amap = meta.get("actionIds") or {}
        for k in keys:
            if k in amap:
                return {
                    "actionId": amap[k],
                    "contract": cname,
                    "function": k,
                    "useAdaptor": meta.get("useAdaptor"),
                }
    return None


def collect_candidates() -> dict[str, list[dict]]:
    ensure_sources()
    by_chain: dict[str, dict[str, dict]] = defaultdict(dict)

    for chain in NETWORK:
        addrs = json.loads((CACHE / "addresses" / f"{chain}.json").read_text())
        aids = json.loads((CACHE / "action-ids" / f"{chain}.json").read_text())
        for task, meta in addrs.items():
            if not isinstance(meta, dict):
                continue
            for c in meta.get("contracts") or []:
                name, addr = c.get("name"), c.get("address")
                if not name or not addr or not is_pool_factory(task, name):
                    continue
                ameta = (aids.get(task) or {}).get(name) or {}
                action_ids = ameta.get("actionIds") or {}
                ver = (meta.get("version") or "").lower()
                proto = "v3" if ver == "v3" or "v3-" in task else "v2"
                pause = find_pool_action(aids.get(task), ["pause()", "setPaused(bool)"])
                recovery = find_pool_action(aids.get(task), ["enableRecoveryMode()"])
                by_chain[chain][addr.lower()] = {
                    "task": task,
                    "contract": name,
                    "address": addr,
                    "status": meta.get("status"),
                    "version": meta.get("version"),
                    "proto": proto,
                    "disableActionId": action_ids.get("disable()"),
                    "pause": pause,
                    "recovery": recovery,
                    "source": "deployments",
                }

    # Sheet-enabled V2 factories (fill gaps e.g. LBPs)
    sheet = Path("/tmp/bip936_sheet.csv")
    if sheet.exists():
        for row in csv.DictReader(sheet.open()):
            if row.get("state") != "enabled":
                continue
            chain = SHEET_CHAIN.get(row["chain"])
            if not chain:
                continue
            addr = row["address"]
            key = addr.lower()
            if key not in by_chain[chain]:
                by_chain[chain][key] = {
                    "task": row["task"],
                    "contract": row["contract"],
                    "address": addr,
                    "status": row.get("repo_status"),
                    "version": None,
                    "proto": "v3" if "v3-" in row["task"] else "v2",
                    "disableActionId": None,
                    "pause": None,
                    "recovery": None,
                    "source": "sheet",
                }

    # Mainnet forum extras
    for extra in MAINNET_EXTRA_FACTORIES:
        key = extra["address"].lower()
        if key not in by_chain["mainnet"]:
            by_chain["mainnet"][key] = {
                **extra,
                "status": "UNTRACKED",
                "version": "v3",
                "disableActionId": None,
                "pause": None,
                "recovery": None,
                "source": "forum-extra",
            }

    return {c: list(m.values()) for c, m in by_chain.items()}


def enrich_onchain(candidates: dict[str, list[dict]]) -> dict[str, list[dict]]:
    enabled: dict[str, list[dict]] = {}
    for chain, factories in candidates.items():
        if not factories:
            enabled[chain] = []
            continue
        outs = eth_calls(chain, [(f["address"], SEL_IS_DISABLED) for f in factories])
        keep = []
        missing_disable_aid = []
        for f, out in zip(factories, outs):
            if out is None or out == "0x" or len(out) < 66:
                f["onchain"] = "call_failed"
                continue
            if int(out, 16) != 0:
                f["onchain"] = "disabled"
                continue
            f["onchain"] = "enabled"
            f["isDisabled"] = False
            if not f.get("disableActionId"):
                missing_disable_aid.append(f)
            keep.append(f)

        # Resolve disable action ids via getActionId(disable())
        if missing_disable_aid:
            outs2 = eth_calls(
                chain,
                [(f["address"], get_action_id_data(SEL_DISABLE)) for f in missing_disable_aid],
            )
            for f, out in zip(missing_disable_aid, outs2):
                if out and len(out) >= 66:
                    f["disableActionId"] = out
                    f["disableActionIdSource"] = "onchain-getActionId"
                else:
                    # fallback compute with factory as disambiguator
                    f["disableActionId"] = action_id_for(f["address"], SEL_DISABLE)
                    f["disableActionIdSource"] = "computed"

        # Fill pause/recovery action ids for V2
        for f in keep:
            if f["proto"] != "v2":
                continue
            if not f.get("pause"):
                # Prefer pause(); LBPs / very old use setPaused(bool)
                task = f["task"]
                prefer_set = "no-protocol-fee-lbp" in task or task.startswith("2021")
                sel = SEL_SET_PAUSED if prefer_set else SEL_PAUSE
                fn = "setPaused(bool)" if prefer_set else "pause()"
                f["pause"] = {
                    "actionId": action_id_for(f["address"], sel),
                    "function": fn,
                    "source": "computed",
                }
            if not f.get("recovery"):
                # Only add if factory era likely supports recovery (post ~2022)
                if f["task"][:4].isdigit() and int(f["task"][:4]) >= 2022:
                    f["recovery"] = {
                        "actionId": action_id_for(f["address"], SEL_ENABLE_RECOVERY),
                        "function": "enableRecoveryMode()",
                        "source": "computed",
                    }

        # hasRole checks for disable (admin) and grants (gosuto)
        authorizer = get_authorizer(chain)
        admin = admin_for(chain)
        role_calls = []
        role_meta = []
        for f in keep:
            f["authorizer"] = authorizer
            f["admin"] = admin
            if f.get("disableActionId"):
                role_calls.append((authorizer, has_role_data(f["disableActionId"], admin)))
                role_meta.append(("adminHasDisable", f))
            if f["proto"] == "v2" and f.get("pause"):
                role_calls.append(
                    (authorizer, has_role_data(f["pause"]["actionId"], GOSUTO))
                )
                role_meta.append(("gosutoHasPause", f))
            if f["proto"] == "v2" and f.get("recovery"):
                role_calls.append(
                    (authorizer, has_role_data(f["recovery"]["actionId"], GOSUTO))
                )
                role_meta.append(("gosutoHasRecovery", f))

        if role_calls:
            role_outs = eth_calls(chain, role_calls)
            for (field, f), out in zip(role_meta, role_outs):
                f[field] = bool(out and int(out, 16) != 0)

        enabled[chain] = keep
        print(
            f"{chain:10} enabled={len(keep):3} "
            f"(need disable grant: {sum(1 for f in keep if f.get('disableActionId') and not f.get('adminHasDisable'))})"
        )
    return enabled


def v3_pause_action_id(chain: str) -> dict | None:
    aids = json.loads((CACHE / "action-ids" / f"{chain}.json").read_text())
    for task, contracts in aids.items():
        for cname, meta in (contracts or {}).items():
            if not isinstance(meta, dict):
                continue
            amap = meta.get("actionIds") or {}
            if "pausePool(address)" in amap and cname in (
                "VaultAdmin",
                "Vault",
                "VaultExtension",
            ):
                return {
                    "task": task,
                    "contract": cname,
                    "actionId": amap["pausePool(address)"],
                }
    for task, contracts in aids.items():
        for cname, meta in (contracts or {}).items():
            if not isinstance(meta, dict):
                continue
            amap = meta.get("actionIds") or {}
            if "pausePool(address)" in amap:
                return {
                    "task": task,
                    "contract": cname,
                    "actionId": amap["pausePool(address)"],
                }
    return None


GRANT_ROLE_METHOD = {
    "inputs": [
        {"internalType": "bytes32", "name": "role", "type": "bytes32"},
        {"internalType": "address", "name": "account", "type": "address"},
    ],
    "name": "grantRole",
    "payable": False,
}

DISABLE_METHOD = {
    "inputs": [],
    "name": "disable",
    "payable": False,
}


def tx_grant(authorizer: str, role: str, account: str) -> dict:
    return {
        "to": authorizer,
        "value": "0",
        "data": None,
        "contractMethod": GRANT_ROLE_METHOD,
        "contractInputsValues": {"role": role, "account": account},
    }


def tx_disable(factory: str) -> dict:
    return {
        "to": factory,
        "value": "0",
        "data": None,
        "contractMethod": DISABLE_METHOD,
        "contractInputsValues": {},
    }


def build_payload(chain: str, factories: list[dict]) -> dict | None:
    authorizer = get_authorizer(chain)
    admin = admin_for(chain)
    safe = safe_for(chain)
    txs: list[dict] = []
    notes: list[str] = []

    # 1) Factory disables (grant self if needed, then disable)
    disableable = [f for f in factories if f.get("disableActionId")]
    for f in sorted(disableable, key=lambda x: (x["proto"], x["task"], x["address"])):
        if not f.get("adminHasDisable"):
            txs.append(tx_grant(authorizer, f["disableActionId"], admin))
            notes.append(
                f"grant disable {f['task']}/{f['contract']} -> {admin}"
            )
        txs.append(tx_disable(f["address"]))
        notes.append(f"disable {f['task']}/{f['contract']} {f['address']}")

    no_disable = [f for f in factories if not f.get("disableActionId")]
    for f in no_disable:
        notes.append(
            f"SKIP disable (no action id): {f['task']}/{f['contract']} {f['address']}"
        )

    # 2) V2 pause + recovery grants to gosuto (one role per factory each)
    for f in sorted(
        [x for x in factories if x["proto"] == "v2"],
        key=lambda x: (x["task"], x["address"]),
    ):
        if f.get("pause") and not f.get("gosutoHasPause"):
            txs.append(tx_grant(authorizer, f["pause"]["actionId"], GOSUTO))
            notes.append(
                f"grant {f['pause'].get('function','pause')} {f['task']} -> gosuto"
            )
        if f.get("recovery") and not f.get("gosutoHasRecovery"):
            txs.append(tx_grant(authorizer, f["recovery"]["actionId"], GOSUTO))
            notes.append(f"grant enableRecoveryMode {f['task']} -> gosuto")

    # 3) V3 pausePool grant (one per chain)
    v3 = v3_pause_action_id(chain)
    if v3:
        # check gosuto already has it
        out = eth_calls(
            chain, [(authorizer, has_role_data(v3["actionId"], GOSUTO))]
        )[0]
        has = bool(out and int(out, 16) != 0)
        if not has:
            txs.append(tx_grant(authorizer, v3["actionId"], GOSUTO))
            notes.append(
                f"grant V3 pausePool ({v3['task']}/{v3['contract']}) -> gosuto"
            )
        else:
            notes.append("gosuto already has V3 pausePool")
    else:
        notes.append("no V3 pausePool action id on this chain")

    if not txs:
        return None

    payload = {
        "version": "1.0",
        "chainId": CHAIN_ID[chain],
        "createdAt": int(time.time() * 1000),
        "meta": {
            "name": f"BIP-936 post-vote: factory disables + pause grants ({chain})",
            "description": (
                "Queue only after BIP-936 passes. Disables enabled pool factories; "
                "grants V2 pause/recovery per factory and V3 pausePool per chain to "
                f"gosuto {GOSUTO}. Role revokes wait until 1 Dec."
            ),
            "txBuilderVersion": "1.16.5",
            "createdFromSafeAddress": safe,
            "createdFromOwnerAddress": "",
            "checksum": "",
        },
        "transactions": txs,
    }
    return {"payload": payload, "notes": notes, "tx_count": len(txs)}


def main() -> None:
    print("Collecting factory candidates...")
    candidates = collect_candidates()
    print("Checking on-chain isDisabled + roles...")
    enabled = enrich_onchain(candidates)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summary = {
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "pause_eoa": GOSUTO,
        "safes": {"mainnet": DAO, "omni": OMNI, "bsc": BSC_SAFE},
        "chains": {},
        "do_not_queue_until": "BIP-936 Snapshot closed + passed",
        "snapshot": "0x47126e7bd8e02a63ee7022e32c01ec2884a4443c770b9533621391b001663563",
    }

    # Prefer live chains first; BSC last / optional
    order = [
        "mainnet",
        "arbitrum",
        "base",
        "avalanche",
        "gnosis",
        "optimism",
        "polygon",
        "hyperevm",
        "monad",
        "plasma",
        "xlayer",
        "zkevm",
        "fraxtal",
        "mode",
        "bsc",
    ]

    for chain in order:
        factories = enabled.get(chain) or []
        # Still emit V3-only grant payloads even if no factories left to disable
        result = build_payload(chain, factories)
        chain_sum: dict[str, Any] = {
            "safe": safe_for(chain),
            "authorizer": get_authorizer(chain),
            "enabled_factories": len(factories),
            "v2": sum(1 for f in factories if f["proto"] == "v2"),
            "v3": sum(1 for f in factories if f["proto"] == "v3"),
            "factories": [
                {
                    "task": f["task"],
                    "contract": f["contract"],
                    "address": f["address"],
                    "proto": f["proto"],
                    "source": f.get("source"),
                    "disableActionId": f.get("disableActionId"),
                    "adminHasDisable": f.get("adminHasDisable"),
                    "pauseActionId": (f.get("pause") or {}).get("actionId"),
                    "recoveryActionId": (f.get("recovery") or {}).get("actionId"),
                }
                for f in factories
            ],
        }
        if result is None:
            chain_sum["payload"] = None
            chain_sum["notes"] = ["no transactions needed"]
            print(f"{chain}: no txs")
        else:
            fname = f"BIP-936-{chain}.json"
            path = OUT_DIR / fname
            path.write_text(json.dumps(result["payload"], indent=2) + "\n")
            (OUT_DIR / f"BIP-936-{chain}.notes.txt").write_text(
                "\n".join(result["notes"]) + "\n"
            )
            chain_sum["payload"] = fname
            chain_sum["tx_count"] = result["tx_count"]
            chain_sum["notes_file"] = f"BIP-936-{chain}.notes.txt"
            print(f"{chain}: wrote {fname} ({result['tx_count']} txs)")
        summary["chains"][chain] = chain_sum

    (OUT_DIR / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (CACHE / "enabled_onchain.json").write_text(json.dumps(enabled, indent=2))
    print(f"\nWrote payloads under {OUT_DIR}")


if __name__ == "__main__":
    main()
