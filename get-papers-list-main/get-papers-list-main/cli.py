# get_pharma_papers/cli.py
import click
from typing import Optional
from .pubmed_fetcher import fetch_pubmed_papers, save_as_csv

@click.command()
@click.argument('query')
@click.option('-f', '--file', type=click.Path(), help='Specify the filename to save the results.')
@click.option('-d', '--debug', is_flag=True, help='Print debug information during execution.')
@click.option('-h', '--help', is_flag=True, help='Display usage instructions (this message).')
def main(query: str, file: Optional[str], debug: bool, help: bool):
    """
    Fetches research papers from PubMed with pharmaceutical/biotech affiliations.
    """
    if help:
        print(main.get_help(click.get_current_context()))
        return

    if debug:
        click.echo(f"Query: {query}")
        click.echo(f"Output File: {file}")
        click.echo(f"Debug Mode: {'on' if debug else 'off'}")

    papers = fetch_pubmed_papers(query, debug=debug)

    if file:
        save_as_csv(papers, file)
    else:
        if papers:
            click.echo("\nFound the following relevant papers:")
            for paper in papers:
                click.echo(f"  PubmedID: {paper.get('PubmedID')}")
                click.echo(f"  Title: {paper.get('Title')}")
                click.echo(f"  Publication Date: {paper.get('Publication Date')}")
                click.echo(f"  Non-academic Author(s): {paper.get('Non-academicAuthor(s)')}")
                click.echo(f"  Company Affiliation(s): {paper.get('CompanyAffiliation(s)')}")
                click.echo(f"  Corresponding Author Email: {paper.get('Corresponding Author Email')}")
                click.echo("-" * 20)
        else:
            click.echo("No papers with pharmaceutical/biotech affiliations found for the given query.")

if __name__ == "__main__":
    main()