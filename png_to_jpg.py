import argparse
from pathlib import Path
from PIL import Image


def convert_png_to_jpg(quality: int) -> None:
    base_dir = Path(__file__).resolve().parent
    input_dir = base_dir / "input"
    output_dir = base_dir / "output"

    if not input_dir.exists():
        print(f"Input folder not found: {input_dir}")
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    png_files = list(input_dir.glob("*.png")) + list(input_dir.glob("*.PNG"))

    if not png_files:
        print("No .png files found in the 'input' folder.")
        return

    for png_path in png_files:
        jpg_path = output_dir / f"{png_path.stem}.jpg"
        with Image.open(png_path) as img:
            # Handle transparency (RGBA / LA / P) by placing on a white background
            if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                alpha = img.convert("RGBA")
                background = Image.new("RGB", alpha.size, (255, 255, 255))
                background.paste(alpha, mask=alpha.split()[3])
                rgb_img = background
            else:
                rgb_img = img.convert("RGB")

            rgb_img.save(jpg_path, "JPEG", quality=quality, subsampling=0)
            print(f"Converted: {png_path.name} -> {jpg_path.name} (quality={quality})")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert .png images from 'input' folder to .jpg in 'output' folder."
    )
    parser.add_argument(
        "-q",
        "--quality",
        type=int,
        default=100,
        choices=range(1, 101),
        metavar="[1-100]",
        help="JPEG output quality from 1 to 100 (default: 100)",
    )
    args = parser.parse_args()
    convert_png_to_jpg(args.quality)


if __name__ == "__main__":
    main()

