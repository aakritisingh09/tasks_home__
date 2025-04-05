# Get Pharma Papers

This Python program fetches research papers from PubMed based on a user-provided query and identifies papers with at least one author affiliated with a pharmaceutical or biotech company. The results are outputted as a CSV file.

## Code Organization

The codebase is organized into two main parts:

- `get_pharma_papers/pubmed_fetcher.py`: This module contains the core logic for fetching data from the PubMed API, parsing the results, and identifying non-academic affiliations.
- `get_pharma_papers/cli.py`: This script provides the command-line interface for the program, using the functionality from the `pubmed_fetcher` module.

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd get_pharma_papers