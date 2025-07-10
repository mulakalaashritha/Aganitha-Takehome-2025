import requests
import pandas as pd
from typing import List, Dict

def fetch_pubmed_data(query: str, retmax: int = 10) -> List[str]:
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": retmax
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data["esearchresult"]["idlist"]

def fetch_paper_details(pmid: str) -> str:
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": pmid,
        "retmode": "xml"
    }
    response = requests.get(base_url, params=params)
    return response.text

def is_non_academic(text: str) -> bool:
    academic_keywords = [
        'university', 'institute', 'college', 'school', 'hospital',
        'centre', 'center', 'clinic', 'academy', 'research', 'irccs', 'department'
    ]
    text_lower = text.lower()
    return not any(word in text_lower for word in academic_keywords)



def parse_paper_xml(xml_data: str) -> Dict:
    import xml.etree.ElementTree as ET
    tree = ET.ElementTree(ET.fromstring(xml_data))
    root = tree.getroot()
    paper_data = {
        "PubmedID": "",
        "Title": "",
        "Publication Date": "",
        "Non-academic Author(s)": [],
        "Company Affiliation(s)": [],
        "Corresponding Author Email": ""
    }

    article = root.find(".//Article")
    if article is not None:
        paper_data["Title"] = article.findtext("ArticleTitle", default="")

    paper_data["Publication Date"] = root.findtext(".//PubDate/Year", default="")

    authors = root.findall(".//Author")
    for author in authors:
        affil = author.findtext("AffiliationInfo/Affiliation", default="")
        name = author.findtext("LastName", "") + " " + author.findtext("ForeName", "")
        if affil and is_non_academic(affil):
            paper_data["Non-academic Author(s)"].append(name)
            paper_data["Company Affiliation(s)"].append(affil)

    pmid_tag = root.find(".//PMID")
    if pmid_tag is not None:
        paper_data["PubmedID"] = pmid_tag.text

    email_tag = root.find(".//AffiliationInfo/Affiliation")
    if email_tag is not None and '@' in email_tag.text:
        paper_data["Corresponding Author Email"] = email_tag.text

    return paper_data