#!/usr/bin/env python
"""Produce a spreadsheet-like structure describing the conference schedule."""

import collections
import time

import requests


SCHEDULE_URL = "https://2013.pycon.ca/en/schedule/conference.json"

FIELDS = collections.OrderedDict([
    ("conf_key", {
        "header": "ID*",
        "converter": unicode
    }),
    ("name", {
        "header": "Topic*",
        "converter": unicode
    }),
    ("description", {
        "header": "Description*",
        "converter": unicode
    }),
    ("kind", {
        "header": "Track",
        "converter": unicode
    }),
    ("date", {
        "header": "Date (yyyy-mm-dd)",
        "converter": lambda x: None  # HACK: Not in JSON, so we fix this later.
    }),
    ("start", {
        "header": "Start Time (hh:mm)*",
        "converter": lambda x: time.strftime(
            "%H:%M", time.strptime(x, "%Y-%m-%dT%H:%M:%S"))
    }),
    ("end", {
        "header": "End Time (hh:mm)*",
        "converter": lambda x: time.strftime(
            "%H:%M", time.strptime(x, "%Y-%m-%dT%H:%M:%S"))
    }),
    ("room", {
        "header": "Location",
        "converter": lambda x: x.split(u", ")[0]
    }),
    ("authors", {
        "header": "Speakers",
        "converter": u", ".join
    }),
    ("attendees", {"header": "Attendees", "converter": lambda x: None})
])


def speaker_names_to_ids(schedule, speakers):
    """Convert a schedule full of speaker names into one with speaker IDs."""
    schedule_speaker_idx = schedule[0].index("Speakers")
    speaker_id_idx = speakers[0].index("ID*")
    speaker_name_idx = speakers[0].index("Name*")

    for slot in schedule[1:]:
        if slot[schedule_speaker_idx] == "":
            continue

        speaker_names = slot[schedule_speaker_idx].split(u", ")
        speaker_ids = []
        for name in speaker_names:
            speaker_id = [row[speaker_id_idx] for row in speakers
                          if row[speaker_name_idx].upper() == name.upper()][0]
            speaker_ids.append(speaker_id)
        slot[schedule_speaker_idx] = u", ".join(speaker_ids)

    return schedule


def track_names_to_ids(schedule, tracks):
    """Convert a schedule with track names into one with track IDs."""
    schedule_track_idx = schedule[0].index("Track")
    track_id_idx = tracks[0].index("ID*")
    track_name_idx = tracks[0].index("Description*")

    for slot in schedule[1:]:
        slot[schedule_track_idx] = [
            track[track_id_idx] for track in tracks
            if track[track_name_idx].upper() == slot[schedule_track_idx].upper()
        ][0]

    return schedule


def get_schedule():
    """Generate a spreadsheet-like structure with the conference schedule."""
    schedule_req = requests.get(SCHEDULE_URL)
    schedule = schedule_req.json()["schedule"]
    spreadsheet = [[FIELDS[field]["header"] for field in FIELDS.keys()]]

    date_idx = spreadsheet[0].index("Date (yyyy-mm-dd)")  # HACK (see below).

    for slot in schedule:
        spreadsheet.append(
            [FIELDS[field]["converter"](slot.get(field))
             for field in FIELDS.keys()]
        )

        # HACK: The website JSON doesn't have this field, so we fake it.
        spreadsheet[-1][date_idx] = time.strftime(
            "%Y-%m-%d", time.strptime(slot["start"],  "%Y-%m-%dT%H:%M:%S"))

    return spreadsheet

def get_tracks():
    """Generate a spreadsheet-like structure with schedule tracks."""
    return [
        ["ID*", "Parent ID", "Description*",   "Color"],
        ["1",   "0",         "Keynote",        "red"],
        ["2",   "0",         "Tutorial",       "blue"],
        ["3",   "0",         "Talk",           "black"],
        ["4",   "0",         "Lightning Talk", "orange"]
    ]
