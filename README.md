# apex-flash-1 EXL3 on DGX Sparks

Research record for building a 4-bit EXL3 quantization of
[cantina-security/apex-flash-1](https://huggingface.co/cantina-security/apex-flash-1) (a 321B post-train of
GLM-5.3-Flash) on one DGX Spark, and serving it with Mia's AI Lab's TensorFold recipe across 2, 3 and 4 GB10 nodes.

The write-up is `paper/apex-paper.html`, a self-contained page (open it in a browser). This repository holds the
data and configuration behind it.

## Status

| Stage | State |
|---|---|
| Source download (BF16, 642.7 GB @ `28c647a6`) | done, checksums verified |
| Conversion (EXL3 4 bpw, mcg, routed experts only) | done, 16 h 45 min on one Spark |
| Layout check against Mia's TensorFold checkpoint | pass, 150,226 tensors, dtypes match |
| Serving, 2 nodes | live: TP=2, 4 streams, 1M window, vision off |
| Serving, 3 nodes | live: TP=3, 8 streams, 1M window, vision off |
| Serving, 4 nodes (switch, Mia `tp4` branch) | first start in progress |
| Speed and quality benchmarks | 2 and 3 nodes done; base GLM-5.3-Flash compared (no difference on the general suite) |

## Layout

| Path | Contents |
|---|---|
| `paper/apex-paper.html` | The working paper |
| `data/conversion-layers.csv` | Per-layer converter stats: bpw, rfn, cos, SQNR, seconds, host memory (46 rows) |
| `data/conversion-experts.csv` | Per-projection stats for every quantized expert: bpw, proxy error, g_sc, seconds (37,152 rows) |
| `logs/download.log` | Library download log |
| `logs/convert.log` | ExLlamaV3 converter output, all chunks |
| `logs/run.log` | The conversion driver's full output, including the post-processing steps and the manual fixes |
| `logs/serving-*.log` | First-start logs of the serving recipe per node count |
| `config/conversion/recipe.yaml` | Per-tensor bitrate recipe (4 bpw routed experts, 16 elsewhere) |
| `config/conversion/run.sh.site.diff` | The one local change to the conversion driver (source eviction disabled) |
| `config/conversion/output-config.json` | The built checkpoint's `config.json`, with its quantization scope declaration |
| `config/serving-2x/` | Settings, launcher wrapper and local `start.sh` patch for the two-node run |
| `provenance/` | Download script, checksum verification, library index records |
| `benchmarks/` | Benchmark exports, added as runs complete |

## Pinned inputs

- Source: `cantina-security/apex-flash-1` @ `28c647a6bd0444973a7ef3d940c24c67e64f52fe`
- Conversion recipe: `WamboDNS/apex-flash-1-EXL3-4bpw` `quantize/` @ `099b04b`
- Converter: ExLlamaV3 v1.5.3 (integer-K patch) in `nvcr.io/nvidia/pytorch:26.07-py3`, CUDA arch 12.1
- Calibration: ExLlamaV3 default, 250 rows x 2,048 tokens
- Layout reference: `Mia-AiLab/GLM-5.3-Flash-EXL3-4bpw-TensorFold` @ `078455ff`
- Serving: `MiaAI-Lab/GLM-5.3-Flash-EXL3-2x-DGX-Sparks-TensorFold` @ `7d42f90` (2-3 nodes), branch `tp4` @ `d220030` (4 nodes), TensorFold v0.6.0
- Drafter: `incoai/GLM-5.3-Flash-DFlash2` @ `bf582e4e` (CC BY-NC-ND 4.0)

The checkpoint itself (175.7 GB) is not in this repository.

## Licenses

apex-flash-1 and the converted weights are MIT (Z.AI and Cantina). The DFlash2 drafter is CC BY-NC-ND 4.0. Logs and
data here are the operator's own.
