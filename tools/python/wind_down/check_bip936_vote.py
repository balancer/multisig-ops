#!/usr/bin/env python3
"""Check BIP-936 Snapshot state. Exit 0 only if closed and passed."""

from __future__ import annotations

import json
import ssl
import sys
import urllib.request

PROP = "0x47126e7bd8e02a63ee7022e32c01ec2884a4443c770b9533621391b001663563"
CTX = ssl.create_default_context()


def main() -> int:
    q = {
        "query": (
            "query { proposal(id: \"%s\") { id title state end scores "
            "scores_total votes quorum } }" % PROP
        )
    }
    req = urllib.request.Request(
        "https://hub.snapshot.org/graphql",
        data=json.dumps(q).encode(),
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 BalancerOps/1.0",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
        data = json.loads(r.read())["data"]["proposal"]
    print(json.dumps(data, indent=2))
    scores = data.get("scores") or []
    yes = float(scores[0]) if scores else 0.0
    total = float(data.get("scores_total") or 0)
    quorum = float(data.get("quorum") or 0)
    state = data.get("state")
    passed = state == "closed" and yes > total / 2 and total >= quorum
    print(
        f"state={state} yes={yes} total={total} quorum={quorum} passed={passed}",
        file=sys.stderr,
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
