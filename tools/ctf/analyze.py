#!/usr/bin/env python3
"""Cybench / NYU CTF results: apex vs base, per harness.

  analyze.py <results root> [--harness codex,pi,...] [--boot 10000] [--ratio R]

Reads <root>/<harness>-apex/results.jsonl and <root>/<harness>-base/results.jsonl. Reports
  - solve rates by attempt;
  - per-task scores (tries solved, 0..n) and an exact sign test over tasks where the models differ;
  - a 95% bootstrap interval for the solve-rate difference, resampling whole tasks;
  - the same after an equal-work correction: apex decodes faster, so an apex solve counts only if it finished
    within 45 min x (base tokens per 45 min / apex tokens per 45 min), measured on attempts that hit the cap.
"""
import json, math, random, statistics as st, sys
from collections import defaultdict


def load(path):
    rows = [json.loads(l) for l in open(path)]
    return [r for r in rows if "error" not in r]


def out_tokens(u):
    # generated tokens. Pi and Codex count reasoning inside output; OpenCode reports it apart
    # (its total = input + output + reasoning + cache reads/writes)
    u = u or {}
    for k in ("output", "output_tokens"):
        if k in u:
            apart = "total" in u and u["total"] == sum(u.get(x, 0) for x in ("input", "output", "reasoning", "cache_read", "cache_write"))
            return u[k] + (u.get("reasoning", 0) if apart else 0)
    return None


def sign_test(a, b):
    n, k = a + b, min(a, b)
    return min(1.0, 2 * sum(math.comb(n, j) for j in range(k + 1)) / 2 ** n) if n else 1.0


def analyse(root, harness, boot, cutoff_ratio=None, minutes=45):
    A, B = load(f"{root}/{harness}-apex/results.jsonl"), load(f"{root}/{harness}-base/results.jsonl")
    # tokens generated in a full 45-min attempt, per model (capped attempts that recorded usage)
    rate = {}
    for name, rows in (("apex", A), ("base", B)):
        t = [out_tokens(r["usage"]) for r in rows if r.get("timed_out") and out_tokens(r.get("usage"))]
        rate[name] = st.median(t) if t else None
    ratio = cutoff_ratio or (rate["base"] / rate["apex"] if rate["apex"] and rate["base"] else None)

    def score(rows, limit=None):
        s = defaultdict(dict)
        for r in rows:
            ok = bool(r.get("solved")) and (limit is None or r["seconds"] <= limit)
            s[r["task"]][r["attempt"]] = ok
        return s

    out = {"harness": harness, "tokens_per_45min": rate, "work_ratio": ratio}
    for label, limit in (("as run", None), ("equal work", minutes * 60 * ratio if ratio else None)):
        if label == "equal work" and limit is None:
            continue
        sa, sb = score(A, limit), score(B)
        tasks = sorted(set(sa) & set(sb))
        pairs = [(t, k) for t in tasks for k in sa[t] if k in sb[t]]
        ta = {t: sum(sa[t][k] for k in sb[t] if k in sa[t]) for t in tasks}
        tb = {t: sum(sb[t][k] for k in sa[t] if k in sb[t]) for t in tasks}
        n_try = {t: len([k for k in sa[t] if k in sb[t]]) for t in tasks}
        better_a = sum(ta[t] > tb[t] for t in tasks)
        better_b = sum(tb[t] > ta[t] for t in tasks)
        rate_a = sum(ta.values()) / len(pairs)
        rate_b = sum(tb.values()) / len(pairs)
        rnd = random.Random(0)
        diffs = []
        for _ in range(boot):
            pick = [rnd.choice(tasks) for _ in tasks]
            na = sum(n_try[t] for t in pick)
            diffs.append((sum(ta[t] for t in pick) - sum(tb[t] for t in pick)) / na)
        diffs.sort()
        att_a = sum(sa[t][k] and not sb[t][k] for t, k in pairs)
        att_b = sum(sb[t][k] and not sa[t][k] for t, k in pairs)
        out[label] = dict(
            tasks=len(tasks), attempts=len(pairs),
            apex=f"{sum(ta.values())}/{len(pairs)} = {100 * rate_a:.1f}%",
            base=f"{sum(tb.values())}/{len(pairs)} = {100 * rate_b:.1f}%",
            diff_pts=round(100 * (rate_a - rate_b), 1),
            ci95_pts=[round(100 * diffs[int(0.025 * boot)], 1), round(100 * diffs[int(0.975 * boot)], 1)],
            tasks_apex_better=better_a, tasks_base_better=better_b, task_sign_p=round(sign_test(better_a, better_b), 3),
            tasks_ever_solved_apex=sum(ta[t] > 0 for t in tasks), tasks_ever_solved_base=sum(tb[t] > 0 for t in tasks),
            attempts_apex_only=att_a, attempts_base_only=att_b,
            attempt_mcnemar_p_naive=round(sign_test(att_a, att_b), 3))
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    root = a[0]
    hs = a[a.index("--harness") + 1].split(",") if "--harness" in a else ["codex", "pi"]
    boot = int(a[a.index("--boot") + 1]) if "--boot" in a else 10000
    res = [analyse(root, h, boot) for h in hs]
    # Codex logs no usage for attempts killed at the cap; borrow Pi's ratio, stated in the output
    # (--ratio R: a ratio measured elsewhere, e.g. Pi's on Cybench for NYU, which ran Codex only)
    given = float(a[a.index("--ratio") + 1]) if "--ratio" in a else None
    pi = given or next((r["work_ratio"] for r in res if r["harness"] == "pi" and r["work_ratio"]), None)
    for i, r in enumerate(res):
        if r["work_ratio"] is None and pi:
            res[i] = analyse(root, r["harness"], boot, cutoff_ratio=pi)
            res[i]["work_ratio_from"] = "given (--ratio)" if given else "pi"
    print(json.dumps(res, indent=1))
