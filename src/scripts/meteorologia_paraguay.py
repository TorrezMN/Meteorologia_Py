#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Torrez, Milton N.

import json
import requests
from bs4 import BeautifulSoup
import datetime

base_url = "https://www.meteorologia.gov.py/pronostico/"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
}


def pprint_data(d):
    """Prints nicely a dict."""
    data = json.dumps(d, indent=4, ensure_ascii=False)
    print(data)


def get_current_month_and_year():
    """Returns the current month and year in the format year-month."""
    now = datetime.datetime.now()
    month = now.month
    year = now.year
    return f"{year}-{month:02d}"


def get_data():
    """Gets page content."""
    response = requests.get(base_url, headers=headers)
    return response.content


def get_current_date():
    """Returns the current date in the format dd/mm/yy."""
    today = datetime.date.today()
    return f"{today.day}/{today.month}/{today.year % 100}"


def get_current_time():
    """Returns the current time in the format HH:MM:SS."""
    now = datetime.datetime.now()
    return f"{now.hour:02d}:{now.minute:02d}:{now.second:02d}"


def make_row(row):
    """Function that builds the row."""
    r = {}
    orig = row.find("h4", {"class": "pronostico--title"}).text.split("\n")
    temps = row.findAll("div", class_="col-sm-3 col-xs-4")
    pron_boxes = row.findAll("div", class_="col-md-4")

    #  DEBUG INFO
    r["debug_info"] = {}
    r["debug_info"]["running_date"] = get_current_date()
    r["debug_info"]["running_time"] = get_current_time()

    #  DATA
    r["data"] = {}
    r["data"]["origen"] = orig[1]
    r["data"]["last_update"] = orig[2]

    b = []
    for i in pron_boxes:
        r["data"]["pron_data"] = []
        box_base = i.find("div", {"class": "col-md-9 col-sm-10"})
        pron_temps = i.findAll("div", {"class": "col-sm-3 col-xs-4"})
        pron_box = {}

        #  Pronostic box.
        pron_box["text_date"] = box_base.find("h5").text
        pron_box["pron_content"] = box_base.find(
            "div", {"class": "pronostico--content"}
        ).text
        pron_box["temperatures"] = {}

        for i in pron_temps:
            temps = i.text.split()
            pron_box["temperatures"][temps[0]] = temps[1]

        b.append(pron_box)

    r["data"]["pron_data"].append(b)
    #  Append data to file.
    append_data_to_json_file(r, get_current_month_and_year())


def parse_results():
    """Parse the page content."""
    soup = BeautifulSoup(get_data(), "html.parser")
    pronosticos = soup.find("div", {"class": "pronostico--content"})
    pron = pronosticos.findAll("section")
    data = [i for i in pron[1] if len(i) == 9]
    for i in data:
        make_row(i)


def append_data_to_json_file(new_data, filename):
    """Appends data to a JSON file, creating the file if it does not exist.

    Args:
    new_data: The data to append to the file.
    filename: The path to the JSON file.
    """

    try:
        # Open the file in reading and writing mode.
        with open(f"data/{filename}.json", "r+") as f:
            # Load the existing data from the file.
            existing_data = json.load(f)

            # Append the new data to the existing data.
            existing_data.append(new_data)

            # Seek to the beginning of the file.
            f.seek(0)

            # Write the updated data to the file.
            json.dump(existing_data, f)
    except FileNotFoundError:
        # Create the file if it does not exist.
        with open(f"data/{filename}.json", "w") as f:
            json.dump([new_data], f)


def meteorlogia_py_main():
    parse_results()
