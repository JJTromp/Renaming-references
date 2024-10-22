# Renaming-references
This script renames PDF files based on the DOI information extracted from them. It utilises the CrossRef API to retrieve metadata such as the title, authors, year of publication, and journal name, allowing you to standardise your file naming conventions efficiently.

## Features
- Extracts DOI from PDF files.
- Fetches publication details (title, authors, year, journal) using the CrossRef API.
- Renames PDF files based on customizable order and format options.

## Prerequisites
- Python 3.x
- Required Python packages:
  - `requests`
  - `pdfplumber`

You can install the necessary packages using pip:
```bash
pip install requests pdfplumber
```

## Usage
You can run the script directly from the command line. Below are the available options:
```bash
usage: Rename_references.py [-h] [-d DIRECTORY] [-o ORDER [ORDER ...]] [-n NUM_WORDS] [--spaces {hyphen,space}]

Rename PDF files based on DOI information.

options:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        Directory containing PDF files (default: current directory).
  -o ORDER [ORDER ...], --order ORDER [ORDER ...]
                        Order of components in the filename (default: Last Year Journal Title). 
                        Options: Last, Year, Journal, Title, First, AllAuthors, ShortTitle. 
                        Example: "First Last Year Journal" will produce "John_Smith_2023_International_Journal.pdf".
  -n NUM_WORDS, --num_words NUM_WORDS
                        Number of words to include from journal and title (default: 2). 
                        Example: "-n 3" will include the first three words.
  --spaces {hyphen,space}
                        Choose how to handle spaces: "hyphen" for hyphens, "space" for spaces (default: hyphen). 
                        Example: "--spaces space" will produce "John Smith 2023 International Journal.pdf".
```

### Example Usage
1. **Running the script without arguments:**
   ```bash
   python Rename_references.py
   ```
   **Default behavior:**
   Renamed: `example_paper.pdf` -> `Doe_2023_International-Journal_A-Study.pdf`

2. **Running the script with arguments:**
   ```bash
   python Rename_references.py -d . -o First Last Year Journal -n 3 --spaces space
   ```
   **Expected output:**
   Renamed: `example_paper.pdf` -> `John_Doe_2023_International_Journal_of_Testing_A_Study.pdf`

## Contributing
If you find a bug or have a feature request, please open an issue. Contributions are welcome!

