# README for main.py

## Overview
The script `main.py` is designed to scrape and process data about French deputies' votes from the website "datan.fr". It provides functionalities to extract votes for individual politicians as well as for groups of politicians based on their political affiliation.

## Dependencies
- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `requests`
- `mechanicalsoup`
- `BeautifulSoup`
- `unidecode`

## Functions
- `get_names_from_group(group_name)`: Extracts the names of deputies belonging to a specified group from a historical dataset. The [historical dataset](https://www.data.gouv.fr/fr/datasets/historique-des-deputes-de-lassemblee-nationale-depuis-2002-informations-et-statistiques/) curated by the website [datan.fr](https://datan.fr/) contains information about the political affiliation of deputies.
- `get_deputy_votes_page(politic_name)`: Fetches the webpage containing the voting records of a specified deputy.
- `get_votes_from_politic_page(politic_dict)`: Extracts voting data from the HTML content of a deputy's voting record page.
- `get_politic_votes(politic_name)`: Combines the functionalities of fetching a deputy's voting page and extracting the voting data.
- `write_politic_votes(politic_name)`: Writes the voting data of a specified deputy to a CSV file.
- `write_group_votes(group_name)`: Writes the voting data of all deputies in a specified group to a CSV file.

## Usage
To use the script, ensure that all dependencies are installed and run the script. The script will execute the functions for the examples provided in the `__main__` block:
This will generate CSV files with the voting records for the specified politician and group.