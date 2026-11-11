#!/bin/bash
# Pull (or, failing that, build) every NYU CTF Bench test challenge's images. Logs one line per task.
cd /root/ctf/nyu/test || exit 1
find . -name 'docker-compose.y*ml' -print0 | sort -z | while IFS= read -r -d '' f; do
  d=$(dirname "$f")
  if (cd "$d" && docker compose -f "$(basename "$f")" pull -q >/tmp/nyu-pull.$$ 2>&1); then
    echo "PULL ok $d"
  elif (cd "$d" && docker compose -f "$(basename "$f")" build -q >/tmp/nyu-build.$$ 2>&1); then
    echo "BUILD ok $d"
  else
    echo "FAIL $d"; tail -5 /tmp/nyu-pull.$$ /tmp/nyu-build.$$ | sed 's/^/    /'
  fi
done
rm -f /tmp/nyu-pull.$$ /tmp/nyu-build.$$
echo DONE
