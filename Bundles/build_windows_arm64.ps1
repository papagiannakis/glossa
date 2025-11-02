#!/usr/bin/env pwsh
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$bundle = Join-Path $root 'Bundles'
$dist = Join-Path $bundle 'dist\windows-arm64'
$build = Join-Path $bundle 'build\windows-arm64'

New-Item -ItemType Directory -Force -Path $dist | Out-Null
New-Item -ItemType Directory -Force -Path $build | Out-Null

Set-Location $root

pyinstaller `
  --clean `
  --noconfirm `
  --onefile `
  --windowed `
  --name glossa-ide `
  --target-arch arm64 `
  --add-data "samples;samples" `
  run_ide.py

Move-Item -Force "dist\glossa-ide.exe" $dist
if (Test-Path "dist\glossa-ide") {
  Move-Item -Force "dist\glossa-ide" $dist
}

Remove-Item -Recurse -Force build, dist, glossa-ide.spec

Write-Host "Windows ARM64 bundle stored in $dist"
