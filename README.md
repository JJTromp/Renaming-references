# Renaming-references
Rename journal article pdfs based on the information available from the pdf DOI. File name will then be renamed based on the DOI information such as the first author's last name, year published, journal name, title etc. 

usage: Rename_references.py [-h] [-d DIRECTORY] [-o ORDER [ORDER ...]] [-n NUM_WORDS] [--spaces {hyphen,space}]

Rename PDF files based on DOI information.

options:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        Directory containing PDF files (default: current directory).
  -o ORDER [ORDER ...], --order ORDER [ORDER ...]
                        Order of components in the filename (default: Last Year Journal Title). Options: Last, Year, Journal, Title, First, AllAuthors, ShortTitle. Example: "First Last Year Journal" will
                        produce "John_Smith_2023_International_Journal.pdf"
  -n NUM_WORDS, --num_words NUM_WORDS
                        Number of words to include from journal and title (default: 2). Example: "-n 3" will include the first three words.
  --spaces {hyphen,space}
                        Choose how to handle spaces: "hyphen" for hyphens, "space" for spaces (default: hyphen). Example: "--spaces space" will produce "John Smith 2023 International Journal.pdf".

Example Usage:
1. Running the script without arguments:
   python Rename_references.py
   Default behavior:
   Renamed: example_paper.pdf -> Doe_2023_International-Journal_A-Study.pdf

2. Running the script with arguments:
   python Rename_references.py -d . -o First Last Year Journal -n 3 --spaces space
   Expected output:
   Renamed: example_paper.pdf -> John_Doe_2023_International_Journal_of_Testing_A_Study.pdf

