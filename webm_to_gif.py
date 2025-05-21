import subprocess
import sys
from pathlib import Path

def run(cmd):
    subprocess.run(cmd, check=True)

def webm_to_gif(input_path, output_path=None, fps=15, width=480):
    input_path = Path(input_path)
    if not input_path.exists() or input_path.suffix.lower() != ".webm":
        raise ValueError("Invalid input file.")

    output_path = Path(output_path) if output_path else input_path.with_suffix('.gif')
    palette_path = input_path.with_name("palette.png")

    scale_filter = f"fps={fps},scale={width}:-1:flags=lanczos"

    try:
        run(["ffmpeg", "-i", str(input_path), "-vf", f"{scale_filter},palettegen", "-y", str(palette_path)])
        run([
            "ffmpeg", "-i", str(input_path), "-i", str(palette_path),
            "-filter_complex", f"{scale_filter}[x];[x][1:v]paletteuse",
            "-y", str(output_path)
        ])
    finally:
        if palette_path.exists():
            palette_path.unlink()

    print(f"✔ Converted: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python webm_to_gif.py input.webm [output.gif]")
        sys.exit(1)

    webm_to_gif(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
