#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUNDLE_DIR="$ROOT_DIR/Bundles"
DIST_DIR="$BUNDLE_DIR/dist/macOS"
BUILD_DIR="$BUNDLE_DIR/build/macOS"
APP_NAME="glossa-ide"

mkdir -p "$DIST_DIR" "$BUILD_DIR"

cd "$ROOT_DIR"

pyinstaller \
  --clean \
  --noconfirm \
  --onefile \
  --windowed \
  --name "$APP_NAME" \
  --add-data "samples:samples" \
  run_ide.py

mkdir -p "$DIST_DIR"
mv "dist/$APP_NAME" "$DIST_DIR/" 2>/dev/null || true
if [ -d "dist/$APP_NAME.app" ]; then
  mv "dist/$APP_NAME.app" "$DIST_DIR/"
fi

rm -rf build dist glossa-ide.spec

CODE_SIGN_ID="${MAC_CODESIGN_ID:-}"
if [ -n "$CODE_SIGN_ID" ]; then
  echo "Signing binaries with identity: $CODE_SIGN_ID"
  if [ -f "$DIST_DIR/$APP_NAME" ]; then
    codesign --force --deep --options runtime --sign "$CODE_SIGN_ID" "$DIST_DIR/$APP_NAME"
  fi
  if [ -d "$DIST_DIR/$APP_NAME.app" ]; then
    codesign --force --deep --options runtime --sign "$CODE_SIGN_ID" "$DIST_DIR/$APP_NAME.app"
  fi
fi

echo "macOS bundle stored in $DIST_DIR"
