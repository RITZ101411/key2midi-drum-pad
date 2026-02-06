#!/bin/bash
set -e

cd "$(dirname "$0")/.."

echo "Building frontend..."
cd src-view
npm run build
cd ..

echo "Installing PyInstaller..."
uv pip install pyinstaller

echo "Building app with PyInstaller..."
uv run pyinstaller build.spec --distpath build-output --workpath build-temp

echo "Signing app..."
codesign --force --deep --sign - build-output/fk2-hid-midi.app

echo "Build complete!"
echo "App location: build-output/fk2-hid-midi.app"
echo ""
echo "IMPORTANT: Grant accessibility permissions:"
echo "1. Open System Preferences > Privacy & Security > Accessibility"
echo "2. Add fk2-hid-midi.app and enable it"
echo "3. Also check Input Monitoring section"
