from PIL import Image, ImageEnhance, ImageFilter
from pathlib import Path

def improve_image(input_path: Path, output_path: Path, scale_factor: int = 16):
    print(f"Processing: {input_path.name}")

    try:
        # 1. Open and convert to RGBA
        img = Image.open(input_path).convert("RGBA")
        original_size = img.size

        # --- SUPER-SAMPLING STAGE ---
        high_res_size = (original_size[0] * scale_factor, original_size[1] * scale_factor)
        print(f"  • Upscaling x{scale_factor} ({original_size} → {high_res_size})...")
        img_hr = img.resize(high_res_size, Image.Resampling.BICUBIC)

        r, g, b, a = img_hr.split()

        # Aggressive sharpening on high-res alpha (makes letters crisp)
        print("  • Sharpening edges on high-res alpha...")
        a = ImageEnhance.Sharpness(a).enhance(3.5)   # 2.5–4.0 works great

        # Apply Gaussian blur to alpha for subpixel anti-aliasing
        a = a.filter(ImageFilter.GaussianBlur(radius=0.8))

        # Optional: extra contrast before sharpening (uncomment if font is very noisy/old)
        a = ImageEnhance.Contrast(a).enhance(1.3)
        a = ImageEnhance.Sharpness(a).enhance(3.5)

        # Merge back and downscale with Lanczos (best anti-aliased result)
        img_hr = Image.merge("RGBA", (r, g, b, a))
        print("  • Downscaling with Lanczos (smooth & sharp edges)...")
        img_downscaled = img_hr.resize(original_size, Image.Resampling.LANCZOS)

        # --- FINAL ALPHA TOUCH-UP ---
        r, g, b, a = img_downscaled.split()
        a = ImageEnhance.Sharpness(a).enhance(1.5)   # Final edge crispness
        a = ImageEnhance.Contrast(a).enhance(1.1)    # Remove faint halo / fog around letters
        final_img = Image.merge("RGBA", (r, g, b, a))

        # Save with correct format
        if input_path.suffix.lower() == ".ico":
            final_img.save(output_path, format="ICO")
        else:
            final_img.save(output_path.with_suffix(".png"), "PNG", optimize=True)

        print(f"  Saved → output/{output_path.name}\n")

    except Exception as e:
        print(f"  Error {input_path.name}: {e}\n")


if __name__ == "__main__":
    supported = {".png", ".jpg", ".jpeg", ".ico"}
    files = [p for p in Path(".").iterdir() if p.is_file() and p.suffix.lower() in supported and p.name != "improve_all.py"]

    if not files:
        print("No PNG/JPG/JPEG/ICO files found in project root.")
    else:
        Path("output").mkdir(exist_ok=True)
        for f in files:
            out_name = f.stem + "_improved" + (f.suffix if f.suffix.lower() == ".ico" else ".png")
            improve_image(f, Path("output") / out_name)

        print(f"Done! Processed {len(files)} file(s). Check 'output' folder.")