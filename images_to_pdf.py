import os
from PIL import Image


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(BASE_DIR, "qr_codes")
SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".webp"}


def convert_image_to_pdf(image_path: str, pdf_path: str) -> None:
    with Image.open(image_path) as img:
        # PDF export needs RGB mode.
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(pdf_path, "PDF", resolution=100.0)


def main() -> None:
    if not os.path.isdir(IMAGE_FOLDER):
        raise FileNotFoundError(f"Image folder not found: {IMAGE_FOLDER}")

    image_files = [
        name
        for name in sorted(os.listdir(IMAGE_FOLDER))
        if os.path.isfile(os.path.join(IMAGE_FOLDER, name))
        and os.path.splitext(name)[1].lower() in SUPPORTED_EXTENSIONS
    ]

    if not image_files:
        print("No supported image files found.")
        return

    converted = 0
    skipped = 0

    for image_name in image_files:
        image_path = os.path.join(IMAGE_FOLDER, image_name)
        stem, _ = os.path.splitext(image_name)
        pdf_name = f"{stem}.pdf"
        pdf_path = os.path.join(IMAGE_FOLDER, pdf_name)

        if os.path.exists(pdf_path):
            skipped += 1
            print(f"Skipped (PDF already exists): {pdf_name}")
            continue

        convert_image_to_pdf(image_path, pdf_path)
        converted += 1
        print(f"Converted: {image_name} -> {pdf_name}")

    print(f"Done. Converted: {converted}, Skipped: {skipped}")


if __name__ == "__main__":
    main()
