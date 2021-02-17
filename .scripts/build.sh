#!/usr/bin/env bash
apt-get update \
  && apt-get install -y \
      python3-venv \
      libgstreamer-plugins-base1.0-dev
      python3-dev

python3 -m venv .dockervenv
.dockervenv/bin/pip install --upgrade pip
.dockervenv/bin/pip wheel .
