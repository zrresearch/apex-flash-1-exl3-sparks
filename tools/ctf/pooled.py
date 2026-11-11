#!/usr/bin/env python3
"""Codex on Cybench and NYU CTF together: one score per task (share of its attempts solved), apex minus base.

  pooled.py <cybench codex-apex.jsonl> <cybench codex-base.jsonl> <nyu apex results.jsonl> <nyu base results.jsonl>
"""
import json, math, random, statistics as st, sys
from collections import defaultdict


def per_task(path, tag):
    s = defaultdict(list)
    for l in open(path):
        r = json.loads(l)
        if "error" not in r:
            s[tag + r["task"]].append(1.0 if r.get("solved") else 0.0)
    return {k: st.mean(v) for k, v in s.items()}


ca, cb, na, nb = sys.argv[1:5]
A = {**per_task(ca, "cy:"), **per_task(na, "nyu:")}
B = {**per_task(cb, "cy:"), **per_task(nb, "nyu:")}
ids = sorted(set(A) & set(B))
d = [A[i] - B[i] for i in ids]
rng = random.Random(2026)
m = sorted(st.mean(rng.choices(d, k=len(d))) for _ in range(10000))
wa, wb = sum(x > 0 for x in d), sum(x < 0 for x in d)
n, k = wa + wb, min(wa, wb)
p = min(1.0, 2 * sum(math.comb(n, j) for j in range(k + 1)) / 2 ** n) if n else 1.0
print(json.dumps({"tasks": len(ids), "apex": round(100 * st.mean(A[i] for i in ids), 1), "base": round(100 * st.mean(B[i] for i in ids), 1),
                  "diff_pts": round(100 * st.mean(d), 1), "ci95_pts": [round(100 * m[250], 1), round(100 * m[9750], 1)],
                  "tasks_apex_better": wa, "tasks_base_better": wb, "task_sign_p": round(p, 3)}, indent=1))
