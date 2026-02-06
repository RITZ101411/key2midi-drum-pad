#!/bin/bash
cd "$(dirname "$0")/.."
cd src-view
npm run build
cd ..
uv run src/main.py
