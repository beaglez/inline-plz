# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import os.path

from inlineplz.parsers.base import ParserBase
from inlineplz.decorators import linter


@linter(
    {
        "name": "stylint",
        "install": [["npm", "install", "stylint"]],
        "help": [os.path.normpath("./node_modules/.bin/stylint"), "-h"],
        "run": [os.path.normpath("./node_modules/.bin/stylint")],
        "rundefault": [
            os.path.normpath("./node_modules/.bin/stylint"),
            "-c",
            "{config_dir}/.stylintrc",
        ],
        "dotfiles": [".stylintrc"],
        "language": "stylus",
        "autorun": True,
        "run_per_file": False,
    }
)
class StylintParser(ParserBase):
    """Parse stylint output."""

    def parse(self, lint_data):
        messages = set()
        current_path = None
        current_line = None
        current_message = None
        for line in lint_data.split("\n"):
            if line.startswith("File:"):
                current_path = line.split("File:")[-1].strip()
            elif line.startswith("Line:"):
                current_line = int(line.split(":")[1])
            elif line:
                current_message = line.strip()
            if all([current_line, current_path, current_message]):
                messages.add((current_path, current_line, current_message))
                current_path = None
                current_line = None
                current_message = None
        return messages
