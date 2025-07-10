# Aganitha Python Takehome Exercise - 2025

##  Problem
Build a command-line tool in Python to fetch research papers from PubMed using a user-specified query and return papers with **at least one non-academic author** (e.g., pharmaceutical or biotech affiliation).

## Input
Search keyword passed via command-line (example: `"cancer"`)

## Output
A CSV file with:
- PubmedID
- Title
- Publication Date
- Non-academic Author(s)
- Company Affiliation(s)
- Corresponding Author Email

## How to Run

```bash
python main.py cancer
