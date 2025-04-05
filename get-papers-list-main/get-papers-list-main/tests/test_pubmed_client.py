from get_papers_list.pubmed_client import PubMedClient

def test_search_papers():
    client = PubMedClient()
    paper_ids = client.search_papers("cancer treatment", max_results=5)
    assert isinstance(paper_ids, list)
    assert len(paper_ids) <= 5