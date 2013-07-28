#!/usr/bin/env python
"""Produce a spreadsheet-like structure describing the conference speakers."""

import collections
import os
import random
import shutil
import StringIO

import easy_thumbnails.processors
import PIL.Image
import requests

import util.zip


SPEAKERS_URL = "https://2013.pycon.ca/en/speaker/speakers.json"

FIELDS = collections.OrderedDict([
    ("id", {
        "header": "ID*",
        "converter": unicode
    }),
    ("name", {
        "header": "Name*",
        "converter": unicode
    }),
    ("title", {"header": "Title", "converter": lambda x: None}),
    ("company", {"header": "Company Name", "converter": lambda x: None}),
    ("bio", {
        "header": "Description",
        "converter": unicode
    }),
    ("email", {"header": "Email", "converter": lambda x: None}),
    ("phone", {"header": "Phone", "converter": lambda x: None}),
    ("web", {"header": "Website", "converter": lambda x: None}),
    ("facebook", {"header": "Facebook", "converter": lambda x: None}),
    ("twitter", {"header": "Twitter", "converter": lambda x: None}),
    ("linkedin", {"header": "LinkedIn", "converter": lambda x: None}),
    ("photo", {
        "header": "Picture",
        "converter": lambda x: _generate_speaker_photo(x) if x else None
    }),
    ("edit-link", {"header": "Self Edit Link", "converter": lambda x: None})
])

OUTPUT_DIR = os.path.join(os.getcwd(), "out")
PHOTOS_TMP_DIR = os.path.join(OUTPUT_DIR, "speaker-photos-tmp")


def _generate_speaker_photo(photo_url):
    """Download, crop, and save the photograph of a particular speaker."""
    img_filename = str(random.randint(10000, 99999)) + photo_url.split("/")[-1]
    img = PIL.Image.open(StringIO.StringIO(requests.get(photo_url).content))
    cropped_img = easy_thumbnails.processors.scale_and_crop(
        img,
        (min(img.size), min(img.size)),
        crop="smart"
    )
    cropped_img.save(os.path.join(PHOTOS_TMP_DIR, img_filename))
    return img_filename


def get_speakers():
    """
    Generate a spreadsheet-like structure with conference speaker info.

    Note that, as a side-effect, this also produces a zipped file containing
    all the speaker photographs.
    """
    shutil.rmtree(PHOTOS_TMP_DIR, ignore_errors=True)
    os.makedirs(PHOTOS_TMP_DIR)

    speakers_req = requests.get(SPEAKERS_URL)
    speakers = speakers_req.json()["speakers"]
    spreadsheet = [[field["header"] for field in FIELDS.values()]]
    for speaker in speakers:
        spreadsheet.append(
            [FIELDS[field]["converter"](speaker.get(field))
             for field in FIELDS.keys()]
        )

    util.zip.zip_dir(
        PHOTOS_TMP_DIR,
        os.path.join(OUTPUT_DIR, "speaker-photos.zip")
    )
    shutil.rmtree(PHOTOS_TMP_DIR)

    return spreadsheet
