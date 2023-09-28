#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Torrez, Milton N.

import requests
from bs4 import BeautifulSoup


base_url = "https://www.meteorologia.gov.py/pronostico/"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
}


def get_data():
    """Gets page content."""
    response = requests.get(base_url, headers=headers)
    return response.text


def parse_results():
    """Parse the page content."""
    soup = BeautifulSoup(get_data(), "html.parser")
    pronosticos = soup.find("div", {"class": "pronostico--content"})
    pron = pronosticos.findAll("section")
    data = [i for i in pron[1] if len(i) == 9]


if __name__ == "__main__":
    parse_results()
