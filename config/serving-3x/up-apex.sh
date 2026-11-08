#!/usr/bin/env bash
# apex-flash-1 EXL3 4bpw (built locally 2026-11-08 from cantina-security/apex-flash-1 @28c647a6) on Mia's GLM-5.3-Flash
# TensorFold recipe, TP=3 over all three Sparks. Same recipe and flags as up-glm53tf.sh, for a like-for-like comparison.
# Checkpoint: local/apex-flash-1-EXL3-4bpw-mcg @local-20261108 in root's HF cache (library GLM/local/...).
# VISION=0: apex ships its own chat template, whose media markers TensorFold cannot extend.
# Stop with down-glm53tf.sh (same recipe, same container).
set -uo pipefail
cd /home/user/glm53/tensorfold || exit 1
exec env FOREGROUND=1 MODEL_ID=local/apex-flash-1-EXL3-4bpw-mcg MODEL_REVISION=local-20261108 SERVED_NAME=apex-flash-1-3x VISION=0 TF_GLM_LOOP_GUARD=1 ./start-tp3.sh --thinking-budget 16384
