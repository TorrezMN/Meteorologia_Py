#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Torrez, Milton N.

import requests
from bs4 import BeautifulSoup
import datetime

base_url = "https://www.meteorologia.gov.py/pronostico/"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
}


def get_data():
    """Gets page content."""
    response = requests.get(base_url, headers=headers)
    return response.text


def get_current_date():
    """Returns the current date in the format dd/mm/yy."""
    today = datetime.date.today()
    return f"{today.day}/{today.month}/{today.year % 100}"


def get_current_time():
    """Returns the current time in the format HH:MM:SS."""
    now = datetime.datetime.now()
    return f"{now.hour:02d}:{now.minute:02d}:{now.second:02d}"


def make_row(row):
    title = row.find("h4", {"class": "pronostico--title"}).text.split("\n")
    r = {
        "running_date": get_current_date(),
        "running_time": get_current_time(),
        "origin": title[1],
        "updated": title[2],
    }
    print(r)


def parse_results():
    """Parse the page content."""
    soup = BeautifulSoup(get_data(), "html.parser")
    pronosticos = soup.find("div", {"class": "pronostico--content"})
    pron = pronosticos.findAll("section")
    data = [i for i in pron[1] if len(i) == 9]
    for i in data:
        make_row(i)
        break


if __name__ == "__main__":
    parse_results()
