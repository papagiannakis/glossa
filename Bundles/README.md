# Bundled Executables & Build Scripts

This directory contains helper scripts and notes for producing standalone binaries of the Glossa IDE.

> **Important:** The executables themselves are not included because PyInstaller is unavailable in this offline environment and cross-compilation to Windows must be performed on Windows hosts. Follow the instructions below on each target platform to build the bundles locally.

---

## macOS (Universal or Native)

Requirements:
- Python 3.9+ with Tk support.
- `pip install pyinstaller`
- (Recommended for zero warnings) Apple Developer ID Application certificate for code signing.

Steps:
```bash
cd "$(dirname "$0")/.."
python -m pip install --upgrade pyinstaller
# export MAC_CODESIGN_ID="Developer ID Application: Your Name (TEAMID)"
bash Bundles/build_mac.sh
```

The script produces:
- `Bundles/dist/macOS/glossa-ide` (one-file binary)
- `Bundles/dist/macOS/glossa-ide.app` (application bundle)

Optional signing/notarization:

1. Export `MAC_CODESIGN_ID` with your Developer ID certificate common name before running the build script to sign the app automatically.
2. To notarize and staple the ticket, set either:
   - `MAC_NOTARY_PROFILE` (created via `xcrun notarytool store-credentials`), **or**
   - `APPLE_ID`, `TEAM_ID`, and `APP_PASSWORD` (app-specific password),
   then run:
   ```bash
   bash Bundles/notarize_mac.sh
   ```
   This generates `glossa-ide.zip`, submits it, and staples the notarization ticket so end users won’t see Gatekeeper warnings.

## Windows 64-bit (x86)

Requirements:
- Windows 10/11 64-bit.
- Python 3.9+ (x86-64) with Tkinter.
- `pyinstaller` installed in that environment.

Steps (run in PowerShell):
```powershell
Set-Location (Join-Path $PSScriptRoot '..')
python -m pip install --upgrade pyinstaller
Bundles\\build_windows_x64.ps1
```

Output:
- `Bundles\\dist\\windows-x64\\glossa-ide.exe`

## Windows 64-bit (ARM)

Requirements:
- Windows on ARM device with Python 3.11+ for ARM64.
- PyInstaller 5.11+ (ARM64 support).

Steps:
```powershell
Set-Location (Join-Path $PSScriptRoot '..')
python -m pip install --upgrade pyinstaller
Bundles\\build_windows_arm64.ps1
```

Output:
- `Bundles\\dist\\windows-arm64\\glossa-ide.exe`

---

## Notes
- Each script removes old build artifacts inside `Bundles/build` and `Bundles/dist` before packaging.
- The PyInstaller invocations include the `samples/` folder so sample programs ship with the executable.
- `run_ide.py` is used as the entry point.

If you need to customise assets or icons, edit the respective script or the shared `glossa.spec`.
