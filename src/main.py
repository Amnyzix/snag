import os
import re

import questionary
import yt_dlp
from rich.console import Console
from rich.prompt import Prompt

from installation import BIN_DIR, ensure_dependencies
from options import get_ydl_opts

console = Console()


def download_media(url, ydl_opts):
    """Handles the download process with the provided options."""
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            console.print("\n[bold yellow]Snagging media...[/bold yellow]")
            ydl.download([url])
            console.print("\n[bold green]Download completed successfully.[/bold green]")
        except Exception as e:
            console.print("\n[bold red]Failed to retrieve media.[/bold red]")
            error_msg = str(e)
            clean_msg = re.sub(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])", "", error_msg)

            console.print(f"[red]{clean_msg}[/red]")


def main():
    try:
        ensure_dependencies()
        os.environ["PATH"] += os.pathsep + str(BIN_DIR)

        console.print("\n[bold cyan]=== Snag CLI ===[/bold cyan]")

        url = Prompt.ask("Paste the media URL here")

        if not url.strip():
            console.print("[red]No URL provided. Exiting.[/red]")
            return

        format_choice = questionary.select(
            "Select the format:", choices=["Video (MP4)", "Audio (MP3)"]
        ).ask()

        quality_choice = questionary.select(
            "Select the quality:", choices=["High", "Medium", "Low"]
        ).ask()

        opts = get_ydl_opts(format_choice, quality_choice)

        download_media(url.strip(), opts)
    except KeyboardInterrupt:
        console.print("\n[red]Operation cancelled by user.[/red]")
    except Exception as e:
        console.print("\n[bold red]An unexpected error occurred.[/bold red]")
        error_msg = str(e)
        clean_msg = re.sub(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])", "", error_msg)
        console.print(f"[red]{clean_msg}[/red]")
    finally:
        print("\n")
        print("Press enter to quit...")


if __name__ == "__main__":
    main()
