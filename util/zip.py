#!/usr/bin/env python
"""Helpers to work with zip files."""

import os.path
import zipfile


def zip_dir(in_dir, out_file):
    """Zip up a whole directory into one zipfile."""
    zipped_file = zipfile.ZipFile(out_file, "w", zipfile.ZIP_DEFLATED)
    for root, _, files in os.walk(in_dir):
        for cur_file in files:
            file_path = os.path.join(root, cur_file)
            zipped_file.write(file_path, os.path.relpath(file_path, in_dir))
    zipped_file.close()
