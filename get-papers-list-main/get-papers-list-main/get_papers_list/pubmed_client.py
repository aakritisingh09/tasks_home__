# get_pharma_papers/pubmed_fetcher.py
import csv
from typing import List, Dict, Optional
from Bio import Entrez
import requests
import re
from datetime import datetime

Entrez.email = "your.email@example.com"  # Replace with your actual email

def is_non_academic(affiliation: str) -> bool:
    """Heuristic to determine if an affiliation is likely non-academic."""
    if not affiliation:
        return False
    affiliation_lower = affiliation.lower()
    non_academic_keywords = ["inc", "ltd", "corp", "gmbh", "sa", "pty", "biotech", "pharmaceuticals", "research and development"]
    academic_keywords = ["university", "college", "institute", "school", "department", "center", "laboratory", "hospital"]
    if any(keyword in affiliation_lower for keyword in non_academic_keywords) and not any(keyword in affiliation_lower for keyword in academic_keywords):
        return True
    # Additional heuristic based on email domain (less reliable but can help)
    if "@" in affiliation and not any(domain in affiliation.lower() for domain in [".edu", ".ac.", ".gov", ".mil"]):
        return True
    return False

def fetch_pubmed_papers(query: str, debug: bool = False) -> List[Dict]:
    """
    Fetches research papers from PubMed based on a query.

    Args:
        query: The search query to use for PubMed.
        debug: If True, prints debug information.

    Returns:
        A list of dictionaries, where each dictionary represents a paper.
    """
    try:
        handle = Entrez.esearch(db="pubmed", term=query, retmax="500")  # Adjust retmax as needed
        record = Entrez.read(handle)
        handle.close()
        if debug:
            print(f"Found {len(record['IdList'])} papers for the query.")
        if not record['IdList']:
            return []
        handle = Entrez.efetch(db="pubmed", id=record['IdList'], rettype="medline", retmode="text")
        medline_records = handle.read()
        handle.close()
        papers_data: List[Dict] = []
        for record in medline_records.strip().split("\n\n"):
            paper_info: Dict = {}
            authors = []
            non_academic_authors = []
            company_affiliations = set()
            corresponding_author_email = None
            pmid = None
            title = None
            pub_date = None

            for line in record.splitlines():
                if line.startswith("PMID- "):
                    pmid = line.split("- ")[1].strip()
                    paper_info['PubmedID'] = pmid
                elif line.startswith("TI  - "):
                    title = line.split("- ")[1].strip()
                    paper_info['Title'] = title
                elif line.startswith("DP  - "):
                    try:
                        date_str = line.split("- ")[1].strip()
                        pub_date_obj = datetime.strptime(date_str, "%Y/%m/%d %H:%M")
                        pub_date = pub_date_obj.strftime("%Y-%m-%d")
                        paper_info['Publication Date'] = pub_date
                    except ValueError:
                        try:
                            pub_date_obj = datetime.strptime(date_str, "%Y %b %d")
                            pub_date = pub_date_obj.strftime("%Y-%m-%d")
                            paper_info['Publication Date'] = pub_date
                        except ValueError:
                            paper_info['Publication Date'] = date_str # Keep as string if parsing fails
                elif line.startswith("AU  - "):
                    authors.append(line.split("- ")[1].strip())
                elif line.startswith("AD  - "):
                    affiliation = line.split("- ")[1].strip()
                    if is_non_academic(affiliation):
                        non_academic_authors.append(authors[-1]) # Assume last listed author has this affiliation
                        # Further attempt to extract company name (can be improved with more sophisticated regex/NLP)
                        company_match = re.search(r"(?:^|,\s*)([A-Za-z0-9\s&'-.]+?(?:Inc|Ltd|Corp|GmbH|SA|Pty|Biotech|Pharmaceuticals))\b", affiliation)
                        if company_match:
                            company_affiliations.add(company_match.group(1).strip())
                elif line.startswith("FAU - "):
                    pass # Full author name - can be used for more robust affiliation matching if needed
                elif line.startswith("ADR - "):
                    pass # Author address - might contain more detailed affiliation info
                elif line.startswith("CON - "):
                    if "Corresponding author" in line:
                        match = re.search(r"Email: (\S+)", line)
                        if match:
                            corresponding_author_email = match.group(1)
                            paper_info['Corresponding Author Email'] = corresponding_author_email

            if company_affiliations:
                paper_info['Non-academicAuthor(s)'] = ", ".join(non_academic_authors)
                paper_info['CompanyAffiliation(s)'] = ", ".join(sorted(list(company_affiliations)))
                papers_data.append(paper_info)

        return papers_data
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def save_as_csv(data: List[Dict], filename: str):
    """
    Saves the fetched paper data to a CSV file.

    Args:
        data: A list of dictionaries representing the paper data.
        filename: The name of the CSV file to save to.
    """
    if not data:
        print("No relevant papers found to save.")
        return
    fieldnames = ['PubmedID', 'Title', 'Publication Date', 'Non-academicAuthor(s)', 'CompanyAffiliation(s)', 'Corresponding Author Email']
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"Results saved to {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

if __name__ == "__main__":
    # Example usage (for testing the module directly)
    query = "cancer therapy"
    papers = fetch_pubmed_papers(query, debug=True)
    if papers:
        print("\nSample of fetched papers:")
        for paper in papers[:2]:
            print(paper)
        save_as_csv(papers, "sample_pharma_papers.csv")