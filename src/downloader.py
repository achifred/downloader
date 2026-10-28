
#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path
from typing import Any

import yt_dlp

from src.config.constant import AUDIO_FORMATS
from src.config.logger_config import get_logger
from src.utils import create_directories , postprocessor_hook , progress_hook , validate_dependencies , validate_url

logger = get_logger()


# --------------------------------------------------
# Download configuration
# --------------------------------------------------

def build_options(
    mode: str,
    audio_format: str,
    audio_quality: str,
    playlist: bool,
    out_dir: Path,
) -> dict[str, Any]:
    """Build yt-dlp options for the selected download mode."""

    output_template = (
        "%(playlist_title)s/%(playlist_index)03d - %(title)s.%(ext)s"
        if playlist
        else "%(title)s.%(ext)s"
    )

    common: dict[str, Any] = {
      "noplaylist": not playlist,
      "ignoreerrors": True,
      "continuedl": True,
      "retries": 3,
      "fragment_retries": 3,
      "outtmpl": str(out_dir / output_template),
      "windowsfilenames": True,
      "overwrites": False,
      "nooverwrites" : True ,
      "download_archive" : str( out_dir / "downloaded.txt" ) ,
      "logger": logger,
      "progress_hooks": [progress_hook],
      "postprocessor_hooks": [postprocessor_hook],
    }

    if mode == "video":
        common.update({
            "format": "bv*+ba/b",
            "merge_output_format": "mkv",
        })

    elif mode == "audio":
        common.update({
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": audio_format,
                    "preferredquality": audio_quality,
                }
            ],
        })

    return common


# --------------------------------------------------
# Main download function
# --------------------------------------------------

def download(
    url: str,
    mode: str = "audio",
    audio_format: str = "mp3",
    audio_quality: str = "320",
    playlist: bool = False,
    out_dir: str = None

) -> None:
    """
    Download a video or playlist.

    mode:
        video - video only
        audio - audio only
        both  - video and extracted audio
    """

    validate_url(url)
    validate_dependencies()
    output_dir = create_directories(out_path = out_dir)

    options = build_options(
        mode=mode,
        audio_format=audio_format,
        audio_quality=audio_quality,
        playlist=playlist,
      out_dir=output_dir
    )

    logger.info("Starting download")
    logger.info("Mode: %s", mode)
    logger.info("Playlist enabled: %s", playlist)

    try:
        with yt_dlp.YoutubeDL(options) as dl:
            result = dl.download([url])

        if result != 0:
            logger.warning(
                "Some downloads may have failed. "
                "Check the log output and resulting files."
            )
        else:
            logger.info("Download process completed.")

    except Exception as exc:
        logger.error("Download failed: %s", exc)
        raise


# --------------------------------------------------
# Command-line interface
# --------------------------------------------------

def downloader() -> None:
    parser = argparse.ArgumentParser(
        description="Download authorized YouTube videos/playlists "
                    "and extract audio."
    )

    parser.add_argument(
        "url",
        help="YouTube video URL or playlist URL",
    )

    parser.add_argument(
        "--mode",
        choices=("video", "audio", "both"),
        default="both",
        help="Download video, audio, or both (default: both)",
    )

    parser.add_argument(
        "--playlist",
        action="store_true",
        help="Download the full playlist",
    )

    parser.add_argument(
        "--audio_format",
        choices=AUDIO_FORMATS,
        default="mp3",
        help="Audio output format (default: mp3)",
    )

    parser.add_argument(
        "--audio_quality",
        default="320",
        help="Audio bitrate for MP3 conversion, e.g. 320",
    )
    parser.add_argument(
      "--outdir" ,
      default = None ,
      help = "Location to save your downloads. defaults to Downloads" ,
    )

    args = parser.parse_args()

    try:
        download(
            url=args.url,
            mode=args.mode,
            audio_format=args.audio_format,
            audio_quality=args.audio_quality,
            playlist=args.playlist,
        )
    except (ValueError, RuntimeError, yt_dlp.utils.DownloadError) as exc:
        logger.error("%s", exc)
        sys.exit(1)



if __name__ == "__main__":
  downloader()