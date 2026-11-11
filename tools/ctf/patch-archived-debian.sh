#!/usr/bin/env bash
# Point challenge images built on retired Debian releases (buster, bullseye) at archive.debian.org, so their
# `apt-get update` still works. Changes only where packages are downloaded from, not the challenge.
# Usage: patch-archived-debian.sh <Dockerfile>...
set -euo pipefail
FIX='RUN if [ -f /etc/apt/sources.list ] \&\& grep -qE "buster|bullseye" /etc/apt/sources.list /etc/os-release 2>/dev/null; then sed -i -e "s|deb.debian.org|archive.debian.org|g" -e "s|security.debian.org|archive.debian.org|g" -e "/-updates/d" /etc/apt/sources.list; fi; if [ -f /etc/apt/sources.list.d/debian.sources ] \&\& grep -qE "buster|bullseye" /etc/os-release; then sed -i -e "s|deb.debian.org|archive.debian.org|g" -e "s|security.debian.org|archive.debian.org|g" -e "s| [a-z]*-updates||" /etc/apt/sources.list.d/debian.sources; fi; true # ctf-harness: archived Debian'
for f in "$@"; do
  grep -q 'ctf-harness: archived Debian' "$f" && continue
  # after every FROM line (multi-stage builds get it in each stage)
  sed -i "/^FROM /a $FIX" "$f"
  echo "patched $f"
done
