# Optional: email QRs to students

These helpers are optional. The GitHub Pages scanner works without them. Use
them only after completing the main QR-generation flow in the repository
[README](../README.md): create a local `students.csv`, run
`python generate_qr.py students.csv`, and confirm that `qr_codes/` contains one
QR image per student.

> **Safety warning:** Never commit `qr_codes/`, generated PDFs, `data.csv`, or
> any roster containing real student information. Keep `TEST_MODE = true` until
> a dry run succeeds for every intended recipient.

## 1. Create a local email mapping

Copy `data.example.csv` to `data.csv` in this directory and replace the sample
values with the actual roll-number-to-email mapping. Keep the header names
exactly as shown:

```csv
Roll Number,Email ID
CS21-014,student1@iiitd.ac.in
CS21-015,student2@iiitd.ac.in
```

`data.csv` is gitignored. It must remain local.

## 2. Rename the QR images

From the `ops` directory, run:

```bash
python rename_qr.py
```

The script renames each matching QR in `../qr_codes/` from its roll number to
the email address, for example `CS21-014.png` becomes
`student1@iiitd.ac.in.png`. It skips QR files with no matching roll number and
stops rather than overwrite an existing target filename. Make a backup first
if you want to preserve the roll-number filenames.

## 3. Convert the images to PDFs

Run:

```bash
python images_to_pdf.py
```

This writes a PDF beside each QR image, for example
`student1@iiitd.ac.in.pdf`. It requires Pillow, which is included in the main
project dependencies:

```bash
pip install -r requirements.txt
```

Run that command from the repository root, or install `pillow` directly if you
use a separate environment for these helpers.

## 4. Configure `Code.gs`

1. Upload the generated PDFs to a private Google Drive folder.
2. Open the folder URL and copy its ID: the text after `/folders/`.
   
   For Example:

      https://drive.google.com/drive/u/1/folders/2UWM7zvOWghExfunP6zHa9VYlW4Lm83_k

      Above URL points to folder with uploaded QR PDFs having folder ID - 2UWM7zvOWghExfunP6zHa9VYlW4Lm83_k
3. Create a Google Sheet with the following headers. `Name` is optional.

   ```csv
   Email,Name,Status
   student1@iiitd.ac.in,Student1,
   student2@iiitd.ac.in,Student2,
   ```

4. In the sheet, choose **Extensions → Apps Script**, then paste the contents
   of `Code.gs` into the editor.
5. Set `FOLDER_ID`, `SUBJECT`, `SENDER_NAME`, and `EMAIL_BODY` for the course.
   Use `{{name}}` in `EMAIL_BODY` to insert the optional `Name` value.

`Code.gs` looks for a Drive file named exactly `<email>.pdf`. Its
`sendBulkEmails` function uses the active sheet, skips blank email rows and
rows already marked `Sent`, and writes results to the `Status` column.

## 5. Dry run, then send

1. Leave `const TEST_MODE = true`.
2. Run `sendBulkEmails` from Apps Script and authorize it when Google asks.
3. Confirm every intended row says `TEST OK`. `ERROR: PDF not found` means the
   matching `<email>.pdf` file is missing from the selected Drive folder.
4. Only after all rows pass, set `TEST_MODE` to `false` and run
   `sendBulkEmails` again.

When email is actually sent, the row becomes `Sent`. Other Apps Script errors
are written as `ERROR: ...`; correct the issue and run the script again. Rows
already marked `Sent` are not sent a second time.
