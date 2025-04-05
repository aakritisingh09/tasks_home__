import csv
from typing import List, Dict

class CSVWriter:
    def write_to_csv(self, papers: List[Dict], filename: str):
        """Write paper details to a CSV file."""
        headers = ["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"]
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            for paper in papers:
                writer.writerow({
                    "PubmedID": paper.get("id"),
                    "Title": paper.get("title"),
                    "Publication Date": paper.get("date"),
                    "Non-academic Author(s)": ", ".join(paper.get("authors", [])),
                    "Company Affiliation(s)": ", ".join(paper.get("affiliations", [])),
                    "Corresponding Author Email": paper.get("corresponding_email")
                })