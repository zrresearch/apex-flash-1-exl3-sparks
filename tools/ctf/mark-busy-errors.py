#!/usr/bin/env python3
"""Mark OpenCode attempts that died on 'all serving lanes are busy' (HTTP 429) as errors, so batch reruns them.
Usage: mark-busy-errors.py <outdir>   (run only while no batch writes to <outdir>)"""
import json, os, sys
d = sys.argv[1]; p = os.path.join(d, "results.jsonl")
rows = [json.loads(l) for l in open(p)]
n = 0
for r in rows:
    if "error" in r or r.get("answer"):
        continue
    ev = os.path.join(d, "runs", r["rid"], "events.jsonl")
    if os.path.exists(ev) and "lanes are busy" in open(ev).read():
        r["error"] = "model server busy (429); OpenCode stopped"; n += 1
open(p + ".tmp", "w").write("".join(json.dumps(r) + "\n" for r in rows)); os.replace(p + ".tmp", p)
print(f"marked {n} of {len(rows)}")
