import os
import requests
import pdfplumber
import re
import argparse

def extract_doi_from_pdf(pdf_path):
    doi_pattern = r'10\.\d{4,9}/[-._;()/:A-Z0-9]+'
    doi_found = None
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                match = re.search(doi_pattern, text, re.IGNORECASE)
                if match:
                    doi_found = match.group(0)
                    break

    return doi_found

def get_publication_info(doi):
    url = f"https://api.crossref.org/v1/works/{doi}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        title = data['message'].get('title', ['Unknown Title'])[0]
        authors = [f"{author['given']} {author['family']}" for author in data['message'].get('author', [])]
        year = data['message'].get('published-print', {}).get('date-parts', [[None]])[0][0] or \
               data['message'].get('published-online', {}).get('date-parts', [[None]])[0][0] or "Unknown Year"
        journal = data['message'].get('container-title', ['Unknown Journal'])[0]
        
        return {
            'title': title,
            'authors': authors,
            'year': year,
            'journal': journal
        }
    else:
        print(f"Error fetching data for DOI {doi}: {response.status_code}")
        return None

def rename_pdfs_in_directory(folder_path, order, num_words, use_hyphens, include_spaces):
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            doi = extract_doi_from_pdf(pdf_path)
            if doi:
                publication_info = get_publication_info(doi)
                if publication_info:
                    first_author_last_name = publication_info['authors'][0].split()[-1]  # Get the last name of the first author
                    year = publication_info['year']
                    
                    # Get the first 'num_words' words of the journal and title
                    journal_words = publication_info['journal'].split()[:num_words]
                    title_words = publication_info['title'].split()[:num_words]
                    
                    # Create the new filename based on the specified order
                    new_filename_parts = []
                    for part in order:
                        if part == "Last":
                            new_filename_parts.append(first_author_last_name)
                        elif part == "Year":
                            new_filename_parts.append(year)
                        elif part == "Journal":
                            new_filename_parts.append('-'.join(journal_words) if use_hyphens else ' '.join(journal_words))
                        elif part == "Title":
                            new_filename_parts.append('-'.join(title_words) if use_hyphens else ' '.join(title_words))
                        elif part == "First":
                            new_filename_parts.append(publication_info['authors'][0].split()[0])  # First name of the first author
                        elif part == "AllAuthors":
                            new_filename_parts.append('_'.join(publication_info['authors']))  # All authors
                        elif part == "ShortTitle":
                            new_filename_parts.append(title_words[0])  # First word of the title
                    
                    new_filename = f"{'_'.join(new_filename_parts)}.pdf"
                    new_pdf_path = os.path.join(folder_path, new_filename)
                    os.rename(pdf_path, new_pdf_path)
                    print(f"Renamed: {filename} -> {new_filename}")
                else:
                    print(f"Could not retrieve publication info for DOI: {doi}")
            else:
                print(f"No DOI found in: {filename}")

def main():
    parser = argparse.ArgumentParser(description='Rename PDF files based on DOI information.')
    parser.add_argument('-d', '--directory', type=str, default='.', help='Directory containing PDF files (default: current directory).')
    parser.add_argument('-o', '--order', type=str, nargs='+', default=['Last', 'Year', 'Journal', 'Title'],
                        help='Order of components in the filename (default: Last Year Journal Title). Options: Last, Year, Journal, Title, First, AllAuthors, ShortTitle. '
                             'Example: "First Last Year Journal" will produce "John_Smith_2023_International_Journal.pdf"')
    parser.add_argument('-n', '--num_words', type=int, default=2, help='Number of words to include from journal and title (default: 2). Example: "-n 3" will include the first three words.')
    parser.add_argument('--spaces', choices=['hyphen', 'space'], default='hyphen',
                        help='Choose how to handle spaces: "hyphen" for hyphens, "space" for spaces (default: hyphen). '
                             'Example: "--spaces space" will produce "John Smith 2023 International Journal.pdf".')
    
    parser.epilog = """Example Usage:
1. Running the script without arguments:
   python Rename_references.py
   Default behavior:
   Renamed: example_paper.pdf -> Doe_2023_International-Journal_A-Study.pdf

2. Running the script with arguments:
   python Rename_references.py -d . -o First Last Year Journal -n 3 --spaces space
   Expected output:
   Renamed: example_paper.pdf -> John_Doe_2023_International_Journal_of_Testing_A_Study.pdf"""

    args = parser.parse_args()

    rename_pdfs_in_directory(args.directory, order=args.order, num_words=args.num_words, use_hyphens=(args.spaces == 'hyphen'))

if __name__ == "__main__":
    main()
