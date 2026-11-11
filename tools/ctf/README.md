# Cybench with Codex and Pi

`ctfrun.py` runs Cybench tasks through an agent harness, one isolated Docker network per attempt (see its docstring).

Setup used:
- Cybench `andyzorigin/cybench` @ `ca483c64`, with `cybench-repairs.diff` applied (Debian archive sources, a removed Java image).
- GlacierCTF tasks: `LosFuzzys/GlacierCTF2023_writeups` @ `af41b3b` cloned into `benchmark/LosFuzzys/`, with
  `glacierctf-cybench-issue789.patch` (posted in Cybench issue 789) applied inside it.
- Agent image: `agent/Dockerfile`, built on `cybench/cybench:latest`, with every task's `metadata/requirements.sh`
  copied into `agent/reqs/` and the Codex CLI binary as `agent/codex`.

Pi agent image: `agent-pi/Dockerfile` (Node 22.20.0, Pi 1.4.0), built on the Codex agent image. Add `--harness pi`.

Run one model:

    python3 ctfrun.py batch cybench/task_list.txt <served-model-name> <host:port> <outdir> --tries 3 --conc 4 --minutes 45

`probe` mode sets up an attempt and runs a fixed shell command instead of the agent, to check isolation.
