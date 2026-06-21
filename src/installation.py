import os
import platform
import shutil
import tarfile
import urllib.request
import zipfile
from pathlib import Path

from rich.console import Console

console = Console()

USER_HOME = Path.home()
BIN_DIR = USER_HOME / ".snag" / "bin"

SYSTEM = platform.system().lower()
IS_WINDOWS = SYSTEM == "windows"
IS_LINUX = SYSTEM == "linux"

EXE_EXT = ".exe" if IS_WINDOWS else ""

if IS_WINDOWS:
    DENO_URL = "https://github.com/denoland/deno/releases/latest/download/deno-x86_64-pc-windows-msvc.zip"
    FFMPEG_URL = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
elif IS_LINUX:
    DENO_URL = "https://github.com/denoland/deno/releases/latest/download/deno-x86_64-unknown-linux-gnu.zip"
    FFMPEG_URL = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz"


def download_and_extract(url, dest_folder, target_name):
    """Donwload archive, extract only executable wanted and clean up."""
    filename = url.split("/")[-1]
    archive_path = dest_folder / filename

    try:
        urllib.request.urlretrieve(url, archive_path)

        target_file = f"{target_name}{EXE_EXT}"

        if filename.endswith(".zip"):
            with zipfile.ZipFile(archive_path, "r") as zip_ref:
                for file in zip_ref.namelist():
                    if file.endswith(target_file):
                        source = zip_ref.open(file)
                        target_path = dest_folder / target_file
                        with open(target_path, "wb") as target:
                            target.write(source.read())
                        break

        elif filename.endswith(".tar.xz"):
            with tarfile.open(archive_path, "r:xz") as tar_ref:
                for member in tar_ref.getmembers():
                    if member.name.endswith(target_file):
                        source = tar_ref.extractfile(member)
                        target_path = dest_folder / target_file
                        if source:
                            with open(target_path, "wb") as target:
                                target.write(source.read())
                        break

        os.remove(archive_path)

        if IS_LINUX:
            os.chmod(dest_folder / target_file, 0o755)
    except Exception as e:
        console.print(f"[red]Error downloading or extracting {target_name}: {e}[/red]")
        if archive_path.exists():
            os.remove(archive_path)


def ensure_dependencies():
    """Check dependencies and install them if missing."""
    if not (IS_WINDOWS or IS_LINUX):
        console.print(
            "[yellow]Unsupported OS for auto-install. Please install Deno and FFmpeg manually.[/yellow]"
        )
        return

    BIN_DIR.mkdir(parents=True, exist_ok=True)

    # Checking for Deno
    if not shutil.which("deno"):
        deno_exe = BIN_DIR / f"deno{EXE_EXT}"
        if not deno_exe.exists():
            console.print("[yellow]Downloading anti-blocking engine (Deno)...[/yellow]")
            download_and_extract(DENO_URL, BIN_DIR, "deno")

    # Checking for FFmpeg
    if not shutil.which("ffmpeg"):
        ffmpeg_exe = BIN_DIR / f"ffmpeg{EXE_EXT}"
        if not ffmpeg_exe.exists():
            console.print("[yellow]Downloading audio/video engine (FFmpeg)...[/yellow]")
            download_and_extract(FFMPEG_URL, BIN_DIR, "ffmpeg")
