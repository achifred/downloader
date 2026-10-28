# YouTube Downloader

A command-line tool for downloading YouTube videos and playlists, with support for high-quality audio extraction using FFmpeg.

## Features

- Download individual YouTube videos or entire playlists.
- Extract audio into formats such as MP3, M4A, Opus, and FLAC.
- Download videos and extract audio in a single operation.
- Display download progress, speed, and estimated time remaining.
- Skip previously downloaded videos using a download archive.
- Saves downloaded videos and audio into your default Downloads folder or the custom folder provided.


## Requirements

- Python 3.10+
- [FFmpeg](https://ffmpeg.org/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)

## Installation
Run setup.py to install dependencies
```bash
python setup.py
```

## Build the cli tool
Run build.py to build the project into a cli tool
```bash
python build.py

```

Ensure `ffmpeg` and `ffprobe` are available on your system's PATH.

## Usage

Download a video:

```bash
./dist/downloader "YOUTUBE_URL" --mode video
```

Extract audio:

```bash
./dist/downloader "YOUTUBE_URL" --mode audio
```

Download a playlist:

```bash
./dist/downloader "PLAYLIST_URL" --playlist --mode video
```

Download a playlist and extract audio:

```bash
./dist/downloader "PLAYLIST_URL" --playlist --mode both
```

Choose an audio format:

```bash
./dist/downloader "YOUTUBE_URL" --mode audio --audio-format flac
```

Run the following command to view all available options:

```bash
./dist/downloader --help
```

## Output

Downloaded files are saved in the `Downloads` default directory. The download archive tracks successfully downloaded videos to help avoid repeat downloads.

## Disclaimer

Use this tool only for content you own or are authorized to download, and comply with applicable laws and YouTube's terms of service.
