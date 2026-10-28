#!/usr/bin/env bash

echo "installing ffmpeg"

OS="$(uname -s)"

case "${OS}" in
  Linux*)
    if command -v apt &> /dev/null; then
      echo "installing via apt"
      sudo apt intall -y ffmpeg
    elif command -v dnf &> /dev/null; then
      sudo dnf install -y ffmpeg
    elif  command -v pacman &> /dev/null; then
      sudo pacman -S --noconfirm ffmpeg
    else
      echo "unsupported linux package"
      exit 1
    fi
    ;;
  Darwin*)
    echo "installing ffmpeg on mac"
    if ! command -v brew &> /dev/null; then
      echo "homebrew is not installed"
      exit 1
    fi
    brew install ffmpeg
    ;;
  CYGWIN*|MINGW*|MSYS_NT*)
    echo "Windows environment detected"
    if command -v winget &> /dev/null; then
      winget install -e --id Gyan.FFmpeg
    else
      echo "winget is not installed; please install ffmpeg manually"
      exit 1
    fi
    ;;
  *)
    echo "unknown operating system: ${OS}"


esac