#!/usr/bin/env python
"""Produce a spreadsheet-like structure describing conference sponsors."""

import collections
import os
import shutil
import StringIO

import PIL.Image
import requests

import util.zip


SPONSORS_URL = "https://2013.pycon.ca/en/sponsors/sponsors.json"

FIELDS = collections.OrderedDict([
    ("id", {
        "header": "ID*",
        "converter": unicode
    }),
    ("name", {
        "header": "Exhibitor Name*",
        "converter": unicode
    }),
    ("description", {
        "header": "Description",
        "converter": unicode
    }),
    ("email", { "header": "Email", "converter": lambda x: None}),
    ("booth", { "header": "Booth", "converter": lambda x: None}),
    ("phone", { "header": "Phone Number", "converter": lambda x: None}),
    ("website", {
        "header": "Website",
        "converter": unicode
    }),
    ("twitter", { "header": "Twitter Username", "converter": lambda x: None}),
    ("facebook", { "header": "Facebook", "converter": lambda x: None}),
    ("linkedin", { "header": "LinkedIn", "converter": lambda x: None}),
    ("ad", { "header": "Banner Ad Message", "converter": lambda x: None}),
    ("logo", {
        "header": "Picture",
        "converter": lambda x: _generate_sponsor_logo(x) if x else None
    }),
    ("level", {
        "header": "Categories",
        "converter": unicode
    }),
    ("edit-link", {"header": "Self Edit Link", "converter": lambda x: None})
])

OUTPUT_DIR = os.path.join(os.getcwd(), "out")
LOGOS_TMP_DIR = os.path.join(OUTPUT_DIR, "sponsor-logos-tmp")


def _generate_sponsor_logo(logo_url):
    """Download, crop, and save the logo of a particular sponsor."""
    img_filename = logo_url.split("/")[-1]
    img = PIL.Image.open(StringIO.StringIO(requests.get(logo_url).content))
    img.save(os.path.join(LOGOS_TMP_DIR, img_filename))
    return img_filename


def level_names_to_ids(sponsors, levels):
    """Convert a sponsor roster with level names to one with level IDs."""
    sponsor_level_idx = sponsors[0].index("Categories")
    level_id_idx = levels[0].index("ID*")
    level_name_idx = levels[0].index("Description*")

    for sponsor in sponsors[1:]:
        sponsor[sponsor_level_idx] = [
            level[level_id_idx] for level in levels
            if level[level_name_idx].upper() == sponsor[sponsor_level_idx].upper()
        ][0]

    return sponsors


def get_sponsors():
    """
    Generate a spreadsheet-like structure with sponsor info.

    Note that, as a side-effect, this also produces a zipped file containing
    all the sponsors' logos.
    """
    shutil.rmtree(LOGOS_TMP_DIR, ignore_errors=True)
    os.makedirs(LOGOS_TMP_DIR)

    sponsors_req = requests.get(SPONSORS_URL)
    sponsors = sponsors_req.json()["sponsors"]
    spreadsheet = [[field["header"] for field in FIELDS.values()]]
    for sponsor in sponsors:
        spreadsheet.append(
            [FIELDS[field]["converter"](sponsor.get(field))
             for field in FIELDS.keys()]
        )

    util.zip.zip_dir(
        LOGOS_TMP_DIR,
        os.path.join(OUTPUT_DIR, "sponsor-logos.zip")
    )
    shutil.rmtree(LOGOS_TMP_DIR)

    return spreadsheet


def get_sponsor_levels():
    """Produce a spreadsheet of sponsor levels."""
    return [
        ["ID*", "Parent ID", "Description*",           "Color"],
        ["15",  "0",         "Diamond",                "lightblue"],
        ["1",   "0",         "Gold",                   "orange"],
        ["2",   "0",         "Silver",                 "black"],
        ["3",   "0",         "Bronze",                 "brown"],
        ["4",   "0",         "Education Outreach",     "red"],
        ["5",   "0",         "Party",                  "plum"],
        ["6",   "0",         "Community",              "green"],
        ["7",   "0",         "Diversity",              "blue"],
        ["8",   "0",         "Mobile Tech",            "purple"],
        ["9",   "0",         "Sprints"    ,            "lime"],
        ["10",  "0",         "Venue",                  "gold"],
        ["11",  "0",         "Volunteer Appreciation", "darkpurple"],
        ["12",  "0",         "Internet",               "pink"],
        ["13",  "0",         "Hosting",                "yellow"],
        ["14",  "0",         "Contributor",            "lightblue"],
    ]
