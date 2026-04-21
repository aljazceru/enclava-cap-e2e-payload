# Enclava CAP E2E Payload

Minimal real application used for clean-machine CAP lifecycle tests.

Runtime contract:
- listens on `8080`
- exposes `/health`
- has `/usr/local/bin/app`
- has `/bin/sh` for CAP secure-PV bootstrap wrapping
- writes a small state file under `/data`

The GitHub Actions workflow publishes a digest-pinned image to GHCR and uploads an `image-ref.txt` artifact containing the deployable `ghcr.io/...@sha256:...` reference.

Current default image version: v3.
