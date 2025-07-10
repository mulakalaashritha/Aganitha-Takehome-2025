import sys
import pandas as pd
from pubmed_utils import fetch_pubmed_data, fetch_paper_details, parse_paper_xml

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <search query>")
        return

    query = sys.argv[1]
    pmids = fetch_pubmed_data(query)

    results = []
    for pmid in pmids:
        xml_data = fetch_paper_details(pmid)
        paper = parse_paper_xml(xml_data)
        if paper["Non-academic Author(s)"]:
            results.append(paper)

    df = pd.DataFrame(results)
    df.to_csv("results.csv", index=False)
    print(" Done! Results saved to results.csv")

# Just this line replaces _name_ block
main()