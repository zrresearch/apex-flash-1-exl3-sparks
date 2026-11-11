#!/usr/bin/env python3
"""Security knowledge quiz: CyberMetric-2000, CTIBench CTI-MCQ, SecQA v1+v2 test.

One prompt for every set, temperature 0, thinking on. Results are appended to a JSONL
file one line per item, so a run can stop and resume.

  secquiz.py items <datadir> <items.jsonl>
  secquiz.py run <items.jsonl> <base_url> <model> <out.jsonl> [--conc N] [--limit N] [--max-tokens N]
"""
import csv, json, re, sys, time, threading, urllib.request, concurrent.futures as cf

PROMPT = ("Answer the following multiple-choice question about cybersecurity. "
          "Think it through, then finish with a final line of the form \"Answer: X\", "
          "where X is one of the letters {letters}.\n\nQuestion: {q}\n\n{opts}")


def build_items(d, out):
    items = []
    cm = json.load(open(f"{d}/cybermetric-2000.json"))["questions"]
    for i, q in enumerate(cm):
        items.append(dict(id=f"cybermetric-{i:04d}", set="cybermetric-2000", question=q["question"],
                          options=q["answers"], answer=q["solution"].strip()))
    with open(f"{d}/cti-mcq.tsv", newline="") as f:
        for i, r in enumerate(csv.DictReader(f, delimiter="\t")):
            items.append(dict(id=f"cti-mcq-{i:04d}", set="cti-mcq", question=r["Question"],
                              options={k: r[f"Option {k}"] for k in "ABCD"}, answer=r["GT"].strip().upper()))
    for v in ("v1", "v2"):
        with open(f"{d}/secqa_{v}_test.csv", newline="") as f:
            for i, r in enumerate(csv.DictReader(f)):
                items.append(dict(id=f"secqa-{v}-{i:03d}", set=f"secqa-{v}", question=r["Question"],
                                  options={k: r[k] for k in "ABCD"}, answer=r["Answer"].strip()))
    bad = [it["id"] for it in items if it["answer"] not in it["options"]]
    assert not bad, f"answer key not among options: {bad[:5]}"
    with open(out, "w") as f:
        for it in items:
            f.write(json.dumps(it) + "\n")
    from collections import Counter
    print(len(items), dict(Counter(it["set"] for it in items)))


ANS = re.compile(r"answer\s*[:：]?\s*\**\s*\(?([A-D])\b", re.I)


def parse(text):
    m = ANS.findall(text or "")
    if m:
        return m[-1].upper()
    t = (text or "").strip()
    m = re.fullmatch(r"\(?([A-D])\)?[.)]?", t)
    return m.group(1) if m else None


def ask(base, model, it, max_tokens):
    letters = sorted(it["options"])
    opts = "\n".join(f"{k}. {it['options'][k]}" for k in letters)
    body = dict(model=model, temperature=0, max_tokens=max_tokens,
                messages=[{"role": "user", "content": PROMPT.format(letters=", ".join(letters), q=it["question"], opts=opts)}])
    req = urllib.request.Request(base.rstrip("/") + "/v1/chat/completions", json.dumps(body).encode(),
                                 {"content-type": "application/json"})
    t0 = time.time()
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=1800) as r:
                d = json.load(r)
            break
        except Exception as e:  # retry transient errors
            err = repr(e)
            time.sleep(10 * (attempt + 1))
    else:
        return dict(id=it["id"], set=it["set"], error=err)
    ch = d["choices"][0]
    msg = ch["message"]
    content = msg.get("content") or ""
    pred = parse(content)
    return dict(id=it["id"], set=it["set"], answer=it["answer"], pred=pred, correct=pred == it["answer"],
                finish=ch.get("finish_reason"), completion_tokens=d.get("usage", {}).get("completion_tokens"),
                seconds=round(time.time() - t0, 1), content=content[-400:],
                reasoning_chars=len(msg.get("reasoning_content") or msg.get("reasoning") or ""))


def run(items_path, base, model, out, conc=4, limit=None, max_tokens=8192):
    items = [json.loads(l) for l in open(items_path)]
    done = set()
    try:
        for l in open(out):
            r = json.loads(l)
            if "error" not in r:
                done.add(r["id"])
    except FileNotFoundError:
        pass
    todo = [it for it in items if it["id"] not in done]
    if limit:
        todo = todo[:limit]
    lock = threading.Lock()
    n = ok = 0
    t0 = time.time()
    with cf.ThreadPoolExecutor(conc) as ex, open(out, "a") as f:
        for r in ex.map(lambda it: ask(base, model, it, max_tokens), todo):
            with lock:
                f.write(json.dumps(r) + "\n"); f.flush()
                n += 1; ok += bool(r.get("correct"))
                if n % 50 == 0 or n == len(todo):
                    print(f"{time.strftime('%H:%M:%S')} {model}: {n}/{len(todo)} done, {ok/n:.3f} right, "
                          f"{(time.time()-t0)/n:.1f} s/item wall", flush=True)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "items":
        build_items(a[1], a[2])
    else:
        kw = {}
        for flag, key in (("--conc", "conc"), ("--limit", "limit"), ("--max-tokens", "max_tokens")):
            if flag in a:
                i = a.index(flag); kw[key] = int(a[i + 1]); del a[i:i + 2]
        run(a[1], a[2], a[3], a[4], **kw)
