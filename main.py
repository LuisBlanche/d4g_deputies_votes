import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import mechanicalsoup
from bs4 import BeautifulSoup
from unidecode import unidecode
import re


def get_names_from_group(group_name):
    ''' Get the names of the deputies from a group. 
    Uses the file deputes-historique.csv to get the names of the deputies. Please look 
    at the README.md file to know how to get this file.

    Args:
        group_name (str): Name of the group.
    Returns:
        names (list): List of names of the deputies.'''
    df_deputies_hist = pd.read_csv("deputes-historique.csv")
    df_last_legi = df_deputies_hist[df_deputies_hist["datePriseFonction"] == "2022-06-22"].copy()
    names = []
    for idx, fullname in df_last_legi[df_last_legi["groupe"] == group_name][["prenom", "nom"]].iterrows():
        names.append(unidecode(fullname[0].lower()).replace(" ", "").replace("-", "")
                     + " " +
                     unidecode(fullname[1].lower()).replace(" ", "").replace("-", ""))
    return names

def get_deputy_votes_page(politic_name):
    ''' Fetches the webpage containing the voting records of a specified deputy.

    Args:
        politic_name (str): Name of the deputy.
    Returns:
        politic_dict (dict): Dictionary containing the html page, the url and the
        name of the deputy.'''
    politic_name = unidecode(politic_name.lower()).replace(" ", "-")

    browser = mechanicalsoup.StatefulBrowser()
    url = "https://datan.fr/deputes"
    research_page = browser.open(url)
    research_html = research_page.soup

    politic_card = research_html.select(f'a[href*="{politic_name}"]')
    if politic_card:
        url_politic = politic_card[0]["href"]
        politic_page = browser.open(url_politic+"/votes")
        politic_html = politic_page.soup
        politic_dict = {"html_page": politic_html, "url": url_politic, "name": politic_name}
        return politic_dict
    else:
        raise ValueError(f"Politic {politic_name} not found")

def get_votes_from_politic_page(politic_dict):
    ''' Extracts the voting records from the html page of a deputy.

    Args:
        politic_dict (dict): Dictionary containing the html page, the url and the
        name of the deputy.
    Returns:
        df (pd.DataFrame): DataFrame containing the voting records of the deputy.'''
    #<div class="col-md-6 sorting-item institutions" style="position: absolute; left: 0px; top: 0px;">
    politic_html = politic_dict["html_page"]
    politic_name = politic_dict["name"]
    vote_elements = politic_html.find_all("div", class_="card card-vote")
    vote_categories = politic_html.find_all(class_=re.compile("col-md-6 sorting-item*"))
    votes = []
    for i, vote_element in enumerate(vote_elements):
        for_or_against = vote_element.find("div", class_="d-flex align-items-center").text.replace("\n", "").strip()
        vote_topic = vote_element.find("a", class_="stretched-link underline no-decoration").text.replace("\n", "").strip()
        vote_id = vote_element.find("a", class_="stretched-link underline no-decoration")["href"].split("/")[-1].replace("\n", "").strip()
        vote_date = vote_element.find("span", class_="date").text.replace("\n", "").strip()
        vote_category = vote_categories[i]["class"][-1]
        # color = "green" if for_or_against == "Pour" else "red"
        votes.append([vote_id, for_or_against, vote_topic, vote_date, politic_name, vote_category])
    df = pd.DataFrame(votes, columns=["vote_id", "for_or_against", "vote_topic", "vote_date", "politic_name", "vote_category"])
    return df

def get_politic_votes(politic_name):
    ''' Fetches the voting records of a deputy.

    Args:
        politic_name (str): Name of the deputy.
    Returns:
        df (pd.DataFrame): DataFrame containing the voting records of the deputy.'''
    politic_html = get_deputy_votes_page(politic_name)
    df = get_votes_from_politic_page(politic_html)
    return df

def write_politic_votes(politic_name):
    ''' Writes the voting records of a deputy to a csv file.

    Args:
        politic_name (str): Name of the deputy.'''

    df = get_politic_votes(politic_name)
    df.to_csv(f"{politic_name}.csv", index=False)

def write_group_votes(group_name):
    ''' Writes the voting records of a group to a csv file.

    Args:
        group_name (str): Name of the group.'''
    names = get_names_from_group(group_name)
    # Concatenate all votes from all deputies of the group
    df = pd.DataFrame()
    for name in names:
        try:
            df_politic = get_politic_votes(name)
            df = pd.concat([df, df_politic])

        except ValueError:
            print(f"Politic {name} not found")
            continue
    df.to_csv(f'{group_name.replace(" ", "_").lower()}.csv', index=False)

if __name__ == "__main__":
    # Working example
    name_of_politic = "Sandra Regol"
    write_politic_votes(name_of_politic)

    # Working example
    group_name = "Rassemblement National"
    write_group_votes(group_name)

    # TODO:
    #   - [] Add a column with the social vote to emphasize the antisocial votes of the deputies.
    #   - [X] Add a categories of the votes such as "social", "environmental", "economic", "security", etc.
    #   - [] Add a way to build a nice one page visualization of the dangerous votes of the deputies.


