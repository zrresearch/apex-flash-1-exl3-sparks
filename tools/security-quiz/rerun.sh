#!/usr/bin/env bash
# Re-ask each run's cut-off questions with a 32K token limit.
cd "$(dirname "$0")"
one() { # label url model conc
  python3 -I trunc-items.py $1.jsonl items.jsonl trunc-$1.items.jsonl
  python3 -I secquiz.py run trunc-$1.items.jsonl $2 $3 $1-32k.jsonl --conc $4 --max-tokens 32768 > $1-32k.log 2>&1
}
one apex-4x http://sw-head:8888 apex-flash-1-4x 8 &
one base-3x http://ring-head:8888 GLM-5.3-Flash-EXL3 6 &
( while pgrep -f "[s]ecquiz.py run items.jsonl http://pny-head" >/dev/null; do sleep 60; done
  one apex-2x http://pny-head:8888 apex-flash-1-2x 4 ) &
wait
echo RERUNS DONE; tail -qn1 apex-4x-32k.log base-3x-32k.log apex-2x-32k.log
