#!/usr/bin/env python

# Copyright © 2026 FriedrichFroebel
#
# This file is part of pdf2djvu.
#
# pdf2djvu is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation. If you like, you might use the
# `check_for_updates.py` script under the terms of the MIT license as well, id
# est this file can be considered "GPL-2.0-only OR MIT".
#
# pdf2djvu is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.

import sys
from pathlib import Path

import requests
import yaml
from bs4 import BeautifulSoup


URL = "https://gitlab.freedesktop.org/poppler/poppler/-/tags?format=atom"


def fetch_latest_poppler_release():
    soup = BeautifulSoup(requests.get(URL).content, features="xml")
    entry = soup.find("entry")
    version = entry.find("title").text

    assert version, version
    assert version.startswith("poppler-"), version
    version = version.split("poppler-")[1]
    assert version, version
    return version


def get_all_workflow_files():
    return Path(".github/workflows").glob("*.yml")


def check_workflow(workflow_path, latest_poppler_release):
    with open(workflow_path) as fd:
        content = yaml.safe_load(fd)
    env = content.get("env")
    if not env:
        return True
    current_version = env.get("POPPLER_VERSION")
    if not current_version:
        return True
    if current_version != latest_poppler_release:
        print(f"Poppler version {latest_poppler_release} is available for {workflow_path} (currently: {current_version}).")
        return False
    return True


def main():
    latest_poppler_release = fetch_latest_poppler_release()
    are_valid = True
    for workflow_path in get_all_workflow_files():
        are_valid &= check_workflow(
            workflow_path=workflow_path,
            latest_poppler_release=latest_poppler_release,
        )
    if not are_valid:
        sys.exit(5)


if __name__ == "__main__":
    main()
