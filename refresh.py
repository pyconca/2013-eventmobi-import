#!/usr/bin/env python
"""Data-Munging for PyConCa 2013 Mobile Application Import."""

import os
import shutil
import sys

import components.schedule
import components.speakers
import util.spreadsheet


OUTPUT_DIR = os.path.join(os.getcwd(), "out")


def main(argv):
    """Refresh all the data associated with the conference."""
    shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
    os.makedirs(OUTPUT_DIR)

    speakers = components.speakers.get_speakers()
    schedule = components.schedule.speaker_names_to_ids(
        components.schedule.get_schedule(),
        speakers
    )

    util.spreadsheet.write_spreadsheet(
        schedule,
        "schedule",
        os.path.join(OUTPUT_DIR, "schedule.xls")
    )
    util.spreadsheet.write_spreadsheet(
        speakers,
        "speakers",
        os.path.join(OUTPUT_DIR, "speakers.xls")
    )


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
