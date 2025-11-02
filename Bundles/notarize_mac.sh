#!/usr/bin/env bash
set -euo pipefail

APP_NAME="${APP_NAME:-glossa-ide}"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_PATH="${APP_PATH:-$ROOT_DIR/Bundles/dist/macOS/$APP_NAME.app}"
ZIP_PATH="${ZIP_PATH:-$ROOT_DIR/Bundles/dist/macOS/$APP_NAME.zip}"

if [ ! -d "$APP_PATH" ]; then
  echo "Error: app bundle not found at $APP_PATH" >&2
  exit 1
fi

echo "Creating notarization archive at $ZIP_PATH"
rm -f "$ZIP_PATH"
ditto -c -k --keepParent "$APP_PATH" "$ZIP_PATH"

if [ -n "${MAC_NOTARY_PROFILE:-}" ]; then
  echo "Submitting with notarytool profile '$MAC_NOTARY_PROFILE'"
  xcrun notarytool submit "$ZIP_PATH" --wait --keychain-profile "$MAC_NOTARY_PROFILE"
else
  : "${APPLE_ID:?Set APPLE_ID or MAC_NOTARY_PROFILE}"
  : "${TEAM_ID:?Set TEAM_ID or MAC_NOTARY_PROFILE}"
  : "${APP_PASSWORD:?Set APP_PASSWORD (app-specific password) or MAC_NOTARY_PROFILE}"
  echo "Submitting with Apple ID $APPLE_ID"
  xcrun notarytool submit "$ZIP_PATH" \
    --wait \
    --apple-id "$APPLE_ID" \
    --team-id "$TEAM_ID" \
    --password "$APP_PASSWORD"
fi

echo "Stapling ticket to $APP_PATH"
xcrun stapler staple "$APP_PATH"

echo "Notarization completed successfully."
