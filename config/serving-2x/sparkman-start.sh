#!/usr/bin/env bash
# SparkMan launcher entry: a non-interactive SSH session lacks ~/.local/bin (hf).
export PATH=$HOME/.local/bin:$PATH
cd "$(dirname "$(readlink -f "$0")")" || exit 1
exec ./start.sh "$@"
