import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

from src.config.constant import ALLOWED_HOSTS , APP_NAME , SCRIPT_PATH


def get_root_path () :
  current_path = Path( __file__ ).resolve()

  for parent in current_path.parents :
    if (parent / ".gitignore").exists() :
      return parent

  return current_path.parents[ 2 ]


PROJECT_ROOT = get_root_path()


def get_path ( *path_name: str ) :
  target_path = PROJECT_ROOT.joinpath( *path_name )
  print(f"target path: {target_path}" )

  if not target_path.exists() :
    target_path.parent.mkdir( parents = True , exist_ok = True )

  return target_path


def get_default_download_path():
  if sys.platform in ["darwin", "linux", "linux2"] :
    out_dir = "~/Downloads"
  else:
    out_dir = "%USERPROFILE%\\Downloads"

  return out_dir



# --------------------------------------------------
# Validation
# --------------------------------------------------

def validate_dependencies() -> None:
    """Ensure FFmpeg and FFprobe are available."""
    missing = [
        name
        for name in ("ffmpeg", "ffprobe")
        if shutil.which(name) is None
    ]

    if missing:
      print("installing FFmpeg and FFprobe dependencies...")
      try:
        print("here")
        output = subprocess.run(["chmod","+x", SCRIPT_PATH], capture_output=True)
        print(f"there: {output.stdout}")

        result = subprocess.run(
          [SCRIPT_PATH],
          check=True,
          text=True,
          capture_output=True
        )
        print("scrip successful")
        print(f"output: ${result.stdout}")

      except subprocess.CalledProcessError as e:
        raise e


def validate_url(url: str) -> None:
    """Basic validation of a YouTube video or playlist URL."""

    parsed = urlparse(url.strip())
    host = (parsed.hostname or "").lower()

    if parsed.scheme not in ("http", "https") or host not in ALLOWED_HOSTS:
        raise ValueError("Please provide a valid YouTube URL.")


# --------------------------------------------------
# Output directories
# --------------------------------------------------

def create_directories(out_path:str):
    """Create output directories if they do not exist."""
    if out_path:
      out_dir = Path(out_path).expanduser().resolve()
    else:
      out_dir = Path(get_default_download_path()) / APP_NAME
    out_dir.mkdir(parents=True, exist_ok=True)

    return out_dir




def format_size(size: int | None) -> str:
    """Convert bytes into a human-readable size."""
    if size is None:
        return "Unknown"

    value = float(size)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if value < 1024 or unit == "TB":
            return f"{value:.2f} {unit}"
        value /= 1024

    return f"{value:.2f} TB"


def format_time(seconds: int | float | None) -> str:
    """Format seconds as HH:MM:SS."""
    if seconds is None:
        return "--:--"

    seconds = max(0, int(seconds))
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)

    if hours:
        return f"{hours:02}:{minutes:02}:{secs:02}"

    return f"{minutes:02}:{secs:02}"


def progress_hook(data: dict) -> None:
    """display download progress in the terminal."""

    status = data.get("status")

    if status == "downloading":
        downloaded = data.get("downloaded_bytes", 0)
        total = (
            data.get("total_bytes")
            or data.get("total_bytes_estimate")
        )

        speed = data.get("speed")
        eta = data.get("eta")

        if total and total > 0:
            percentage = min(100.0, downloaded / total * 100)
            bar_width = 30
            filled = int(bar_width * percentage / 100)

            bar = "#" * filled + "-" * (bar_width - filled)

            message = (
                f"\r[{bar}] {percentage:6.2f}% "
                f"| {format_size(downloaded)} / {format_size(total)}"
            )
        else:
            message = (
                f"\rDownloaded: {format_size(downloaded)} "
                "| Total size: unknown"
            )

        speed_text = (
            f"{format_size(int(speed))}/s"
            if speed is not None
            else "--"
        )

        message += (
            f" | Speed: {speed_text}"
            f" | ETA: {format_time(eta)}"
        )

        sys.stdout.write(message)
        sys.stdout.flush()

    elif status == "finished":
        sys.stdout.write(
            f"\nDownload finished: {data.get('filename', 'file')}\n"
        )
        sys.stdout.flush()


def postprocessor_hook(data: dict) -> None:

    status = data.get("status")
    name = data.get("postprocessor", "Postprocessor")

    if status == "started":
        print(f"\nProcessing with {name}...")

    elif status == "finished":
        print(f"Finished processing with {name}.")

