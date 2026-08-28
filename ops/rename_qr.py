import os
import re
import csv


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "data.csv")
QR_FOLDER = os.path.join(BASE_DIR, "../qr_codes")


def safe_filename(name: str) -> str:
    # Remove characters invalid for Windows filenames.
    return re.sub(r'[<>:"/\\|?*]', "_", name).strip()


def normalize_roll(value: str) -> str:
    # Normalize roll values for deterministic matching across CSV and filename stems.
    return re.sub(r"\s+", "", value).upper()


def read_roll_to_email_map(csv_path: str) -> dict[str, str]:
    with open(csv_path, mode="r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        required_columns = {"Roll Number", "Email ID"}
        if not reader.fieldnames or not required_columns.issubset(set(reader.fieldnames)):
            raise ValueError("Columns 'Roll Number' and 'Email ID' are required in data.csv")

        roll_to_email = {}
        for row in reader:
            roll = normalize_roll(str(row.get("Roll Number") or "").strip())
            email = safe_filename(str(row.get("Email ID") or "").strip())
            if roll and email:
                roll_to_email[roll] = email
        return roll_to_email


def file_sort_key(filename: str):
    stem, _ = os.path.splitext(filename)
    # Prefer numeric ordering for roll-number filenames like 2020129.png.
    if stem.isdigit():
        return (0, int(stem))
    return (1, stem.lower())


def main() -> None:
    roll_to_email = read_roll_to_email_map(CSV_PATH)

    files = [
        filename
        for filename in sorted(os.listdir(QR_FOLDER), key=file_sort_key)
        if os.path.isfile(os.path.join(QR_FOLDER, filename))
    ]

    skipped = 0
    for filename in files:
        old_path = os.path.join(QR_FOLDER, filename)
        stem, ext = os.path.splitext(filename)

        roll_key = normalize_roll(stem)
        if roll_key not in roll_to_email:
            skipped += 1
            print(f"Skipped (roll not found in CSV): {filename}")
            continue

        new_name = f"{roll_to_email[roll_key]}{ext}"
        new_path = os.path.join(QR_FOLDER, new_name)

        if old_path == new_path:
            continue

        if os.path.exists(new_path):
            raise FileExistsError(f"Target file already exists: {new_name}")

        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {new_name}")

    if skipped:
        print(f"Done with {skipped} skipped file(s).")


if __name__ == "__main__":
    main()