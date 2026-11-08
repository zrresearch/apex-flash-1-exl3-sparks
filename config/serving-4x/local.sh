# site switch-dell: head sw-head (rank 0, API :8888) + the three Dells on the CRS804 QSFP switch (lossless, PFC prio 0),
# reached over the CX-7 fabric. Every CX-7 half sits in one of two shared subnets (100.x / 101.x), so every pair of ranks
# shares a RoCE subnet, as start-tp4.sh requires on a switch.
WORKER=user@<addr>     # sw-2
WORKER2=user@<addr>    # sw-3
WORKER3=user@<addr>    # sw-4
MASTER_ADDR=<addr>     # keep rendezvous on the fabric
# apex-flash-1 EXL3 4bpw (mcg, routed experts only), converted locally 2026-11-08. Not on the Hub: the prepare step's
# download fails and it falls back to this pinned local snapshot.
MODEL_ID=local/apex-flash-1-EXL3-4bpw-mcg
MODEL_REVISION=local-20261108
SERVED_NAME=apex-flash-1-4x
# Vision off: apex ships its own chat template, whose media markers TensorFold cannot extend.
VISION=0
