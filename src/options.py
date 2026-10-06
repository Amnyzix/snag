def get_ydl_opts(format_choice, quality_choice):
    """
    Returns the yt-dlp configuration dictionary based on user preferences.
    """
    # Base options shared across all downloads
    opts = {
        "outtmpl": "%(title)s.%(ext)s",
        "noplaylist": True,
        "js_runtimes": {"deno": {}},
        "remote_components": ["ejs:github"],
    }

    # Video configuration
    if format_choice == "Video (MP4)":
        if quality_choice == "High":
            opts["format"] = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
        elif quality_choice == "Medium":
            opts["format"] = (
                "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best"
            )
        else:
            opts["format"] = (
                "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]/best"
            )

    # Audio configuration
    else:
        opts["format"] = "bestaudio/best"

        if quality_choice == "High":
            bitrate = "320"
        elif quality_choice == "Medium":
            bitrate = "192"
        else:
            bitrate = "128"

        opts["postprocessors"] = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": bitrate,
            }
        ]

    return opts


def get_ydl_args(format_choice, quality_choice):
    """
    Returns the list of CLI arguments for the standalone yt-dlp binary.
    """
    args = [
        "--output",
        "%(title)s.%(ext)s",
        "--no-playlist",
        "--js-runtimes",
        "deno",
        "--no-color",
        "--remote-components",
        "ejs:github",
    ]

    if format_choice == "Video (MP4)":
        if quality_choice == "High":
            fmt = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
        elif quality_choice == "Medium":
            fmt = (
                "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]"
                "[ext=mp4]/best"
            )
        else:  # Low
            fmt = (
                "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480]"
                "[ext=mp4]/best"
            )

        args.extend(["-f", fmt, "--merge-output-format", "mp4"])

    else:  # Audio (MP3)
        quality_map = {"High": "0", "Medium": "5", "Low": "9"}
        args.extend(
            [
                "-f",
                "bestaudio/best",
                "--extract-audio",
                "--audio-format",
                "mp3",
                "--audio-quality",
                quality_map.get(quality_choice, "0"),
            ]
        )

    return args
