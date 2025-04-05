from typing import List, Dict

class PaperFilter:
    def __init__(self):
        self.non_academic_keywords = ["pharma", "biotech", "inc", "ltd"]
        self.academic_keywords = ["university", "college", "lab"]

    def is_non_academic(self, affiliation: str) -> bool:
        """Check if an affiliation is non-academic."""
        affiliation_lower = affiliation.lower()
        return any(keyword in affiliation_lower for keyword in self.non_academic_keywords) and \
               not any(keyword in affiliation_lower for keyword in self.academic_keywords)

    def filter_papers(self, papers: List[Dict]) -> List[Dict]:
        """Filter papers with at least one non-academic author."""
        filtered_papers = []
        for paper in papers:
            # Parse authors and affiliations from paper details
            # Example: Check each author's affiliation
            if any(self.is_non_academic(affiliation) for affiliation in paper.get("affiliations", [])):
                filtered_papers.append(paper)
        return filtered_papers