import json, sys
res, items, out = sys.argv[1:4]
ids = {json.loads(l)["id"] for l in open(res) if json.loads(l).get("finish") == "length"}
n = 0
with open(out, "w") as f:
    for l in open(items):
        if json.loads(l)["id"] in ids: f.write(l); n += 1
print(out, n)
