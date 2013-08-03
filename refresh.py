#!/usr/bin/env python
"""Data-Munging for PyConCa 2013 Mobile Application Import."""

import os
import shutil
import sys

import components.schedule
import components.speakers
import components.sponsors
import util.spreadsheet


OUTPUT_DIR = os.path.join(os.getcwd(), "out")


def main():
    """Refresh all the data associated with the conference."""
    shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
    os.makedirs(OUTPUT_DIR)

    sponsor_levels = components.sponsors.get_sponsor_levels()
    sponsors = components.sponsors.get_sponsors()
    sponsors = components.sponsors.level_names_to_ids(sponsors, sponsor_levels)
    speakers = components.speakers.get_speakers()
    tracks = components.schedule.get_tracks()
    schedule = components.schedule.get_schedule()
    schedule = components.schedule.speaker_names_to_ids(schedule, speakers)
    schedule = components.schedule.track_names_to_ids(schedule, tracks)

    util.spreadsheet.write_spreadsheet(
        speakers,
        "speakers",
        os.path.join(OUTPUT_DIR, "speakers.xls")
    )
    util.spreadsheet.write_spreadsheet(
        tracks,
        "tracks",
        os.path.join(OUTPUT_DIR, "tracks.xls")
    )
    util.spreadsheet.write_spreadsheet(
        schedule,
        "schedule",
        os.path.join(OUTPUT_DIR, "schedule.xls")
    )
    util.spreadsheet.write_spreadsheet(
        sponsor_levels,
        "sponsor_levels",
        os.path.join(OUTPUT_DIR, "sponsor_levels.xls")
    )
    util.spreadsheet.write_spreadsheet(
        sponsors,
        "sponsors",
        os.path.join(OUTPUT_DIR, "sponsors.xls")
    )


if __name__ == "__main__":
    sys.exit(main())
