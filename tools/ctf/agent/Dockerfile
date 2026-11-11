# Codex agent for Cybench: Cybench's own Kali image, the tools each task's requirements.sh would install at
# start (the agent has no internet), and the Codex CLI. The answers under /app/benchmark are removed.
FROM cybench/cybench:latest
RUN rm -rf /app/benchmark /app/run_benchmark.py /app/run_task.py
COPY reqs /tmp/reqs
RUN cd /tmp && for f in /tmp/reqs/*.sh; do echo "== $f"; sed 's/^\s*sudo //' "$f" | bash -x || echo "!! $f failed"; done; \
    rm -rf /tmp/reqs /var/lib/apt/lists/*
COPY codex /usr/local/bin/codex
WORKDIR /tmp/cyber-bench
ENTRYPOINT []
