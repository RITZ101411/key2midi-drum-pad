#!/bin/bash
set -e

cd "$(dirname "$0")/.."

if [ ! -d "build-output/key2midi-pad.app" ]; then
    echo "Error: build-output/key2midi-pad.app not found"
    echo "Run ./scripts/build.sh first"
    exit 1
fi

OUTPUT_DIR="release"
VERSION="0.1.0"
APP_NAME="key2midi-pad"
DMG_NAME="${APP_NAME}-${VERSION}.dmg"

echo "Creating release package..."
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

echo "Creating DMG..."
hdiutil create -volname "$APP_NAME" \
    -srcfolder "build-output/${APP_NAME}.app" \
    -ov -format UDZO \
    "$OUTPUT_DIR/$DMG_NAME"

echo "Creating ZIP..."
cd build-output
zip -r "../$OUTPUT_DIR/${APP_NAME}-${VERSION}.zip" "${APP_NAME}.app"
cd ..

echo ""
echo "Release packages created:"
echo "  - $OUTPUT_DIR/$DMG_NAME"
echo "  - $OUTPUT_DIR/${APP_NAME}-${VERSION}.zip"
echo ""
echo "Upload these files to GitHub Releases"
