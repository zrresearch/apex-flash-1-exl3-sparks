# Security knowledge quiz

4,710 multiple-choice questions, one prompt, temperature 0, thinking on (`tools/security-quiz/secquiz.py`).

| Set | Source | Revision | Items |
|---|---|---|---|
| CyberMetric-2000 | huggingface.co/datasets/tihanyin/CyberMetric (Apache-2.0) | 32759c2f | 2,000 |
| CTIBench CTI-MCQ | huggingface.co/datasets/AI4Sec/cti-bench (CC BY-NC-SA 4.0) | 9237e163 | 2,500 |
| SecQA v1 + v2 test | huggingface.co/datasets/zefang-liu/secqa (CC BY-NC-SA 4.0) | d00a0748 | 210 |

Question text is not redistributed here; item ids are `<set>-<row index>` in the source files.

Files, one line per item (`id, set, answer, pred, correct, finish, completion_tokens, seconds`):

- `apex-4x`, `base-3x`, `apex-2x`: main runs, 8,192-token limit. apex on 4 Sparks, base GLM-5.3-Flash on 3, apex on 2.
- `*-32k`: items cut off (`finish == length`) in the main run, re-asked with a 32,768-token limit under the server's 16,384-token thinking budget.
- `apex-2x-32k-nocap`: first 2-Spark re-ask attempt, on a server without the thinking budget; discarded (81 of 95 still cut off).

`merge.py` replaces each main-run item with its re-ask and prints per-set scores and exact McNemar tests.
