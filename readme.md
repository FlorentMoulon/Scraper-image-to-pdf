# Scrapper Image to PDF

This project extracts images from a specified website, downloads them, and concatenates them into a single PDF file.

## Requirements

Make sure you have the following Python packages installed:
```makefile
requests
beautifulsoup4
pillow
reportlab
```

You can install all the required packages using the following command:
```bash
pip install -r requirements.txt
```

## Project Structure
```
main.py: The main script that runs the image extraction and PDF creation.
requirements.txt: The list of required Python packages.
temp/: Temporary folder for downloaded images.
out/: Output folder for the final PDF.
```

## Usage
- Clone the repository or download the script files
- Ensure all required packages are installed
- Update the links list `LINKS` with your own links :
  ```python
  LINKS = [
    "https://example.com/comics_name/",
    "https://example.com/comics_name/"
  ]
  ```
- Run the script


## How It Works
1. Initialization :
   - Creates the necessary directories (temp and out).
2. Extract Image Links :
   - Extracts image links from the specified web page(s).
3. Download Images :
    - Downloads the extracted images to the temp folder.
4. Convert Images to PDF :
    - Concatenates all downloaded images into a single PDF file.