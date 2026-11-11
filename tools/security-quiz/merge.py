import json, math, sys
def load(f):
    try: return {r["id"]: r for r in map(json.loads, open(f)) if "error" not in r}
    except FileNotFoundError: return {}
def merged(lbl):
    m = load(f"{lbl}.jsonl"); m.update(load(f"{lbl}-32k.jsonl")); return m
SETS = ["cybermetric-2000", "cti-mcq", "secqa-v1", "secqa-v2"]
runs = {l: merged(l) for l in ["apex-4x", "base-3x", "apex-2x"]}
for l, m in runs.items():
    cut = sum(r["finish"] == "length" for r in m.values())
    row = []
    for s in SETS + [None]:
        v = [r for r in m.values() if s is None or r["set"] == s]
        row.append(f"{(s or 'all')}: {sum(r['correct'] for r in v)}/{len(v)} = {100*sum(r['correct'] for r in v)/len(v):.1f}%")
    print(l, f"cut={cut}", " | ".join(row))
def mc(x, y, name):
    ids = [i for i in x if i in y]
    a = sum(x[i]["correct"] and not y[i]["correct"] for i in ids); b = sum(y[i]["correct"] and not x[i]["correct"] for i in ids)
    n = a + b; k = min(a, b)
    p = min(1, 2 * sum(math.comb(n, j) for j in range(k + 1)) / 2 ** n) if n else 1
    print(f"{name}: {len(ids)} paired, first-only {a}, second-only {b}, p={p:.3g}")
for s in SETS + [None]:
    f = lambda m: {i: r for i, r in m.items() if s is None or r["set"] == s}
    mc(f(runs["apex-4x"]), f(runs["base-3x"]), f"apex4 vs base [{s or 'all'}]")
mc(runs["apex-4x"], runs["apex-2x"], "apex4 vs apex2 [all]")
mc(runs["apex-2x"], runs["base-3x"], "apex2 vs base [all]")
