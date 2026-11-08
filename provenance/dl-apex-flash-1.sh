#!/usr/bin/env bash
# cantina-security/apex-flash-1 (BF16, ~643 GB, GLM-5.3-Flash post-train) at a pinned revision into the library HF cache
# (<library>/GLM/hub). Source for a local EXL3 4bpw conversion.
set -uo pipefail
HF=$HOME/.local/bin/hf
echo "start $(date -Is)"
$HF download cantina-security/apex-flash-1 --revision 28c647a6bd0444973a7ef3d940c24c67e64f52fe --cache-dir <library>/GLM/hub >/dev/null || { echo "FAILED $(date -Is)"; exit 1; }
echo "ALL DONE $(date -Is)"
