import os
import subprocess
import sys

import questionary
from rich.console import Console
from rich.prompt import Prompt

from installation import BIN_DIR, EXE_EXT, ensure_dependencies, update_engines
from options import get_ydl_args

console = Console()


def download_media(url, args):
    """Execute yt-dlp binary with the selected arguments."""
    ytdlp_exe = BIN_DIR / f"yt-dlp{EXE_EXT}"
    cmd = [str(ytdlp_exe)] + args + [url]

    console.print("\n[bold yellow]Snagging media...[/bold yellow]")
    result = subprocess.run(cmd)

    if result.returncode == 0:
        console.print("\n[bold green]Download completed successfully![/bold green]")
    else:
        console.print(
            "\n[bold red]Failed to retrieve media."
            "Try running 'snag --update' if the issue persists.[/bold red]"
        )


def main():
    # Immediate interception of the update command
    if len(sys.argv) > 1 and sys.argv[1] in ["--update", "-u"]:
        try:
            update_engines()
        except Exception as e:
            console.print(f"\n[bold red]Update failed:[/bold red] {str(e)}")
        return

    try:
        console.print("\n[bold cyan]=== Snag CLI ===[/bold cyan]")

        # 1. Verification of engines and PATH injection
        ensure_dependencies()
        os.environ["PATH"] = str(BIN_DIR) + os.pathsep + os.environ.get("PATH", "")

        # 2. URL input
        url = Prompt.ask("Paste the media URL here")
        if not url.strip():
            console.print("[red]No URL provided. Aborting.[/red]")
            return

        # 3. Format and quality selection
        format_choice = questionary.select(
            "Select the format:", choices=["Video (MP4)", "Audio (MP3)"]
        ).ask()
        if not format_choice:
            return

        quality_choice = questionary.select(
            "Select the quality:", choices=["High", "Medium", "Low"]
        ).ask()
        if not quality_choice:
            return

        # 4. Launching the download
        args = get_ydl_args(format_choice, quality_choice)
        download_media(url.strip(), args)

    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
    except Exception as e:
        console.print("\n[bold red]An unexpected error occurred:[/bold red]")
        console.print(f"[red]{str(e)}[/red]")
    finally:
        print("\n")
        input("Press Enter to quit...")


if __name__ == "__main__":
    main()
