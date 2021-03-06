# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import os.path
from inlineplz.parsers.base import ParserBase
from inlineplz.decorators import linter
from inlineplz.util.system import vendored_path, JAVA_SEP

GROOVY_PATH = vendored_path(os.path.join("groovy", "groovy-all-2.4.15.jar"))
SLF4J_PATH = vendored_path(os.path.join("groovy", "slf4j-api-1.7.25.jar"))


@linter(
    {
        "name": "codenarc",
        "install": [],
        "help": [
            "java",
            "-classpath",
            "{}{}{}{}{}{}{}{}{}".format(
                GROOVY_PATH,
                JAVA_SEP,
                vendored_path(os.path.join("codenarc", "CodeNarc-1.1.jar")),
                JAVA_SEP,
                SLF4J_PATH,
                JAVA_SEP,
                vendored_path("codenarc"),
                JAVA_SEP,
                ".",
            ),
            "org.codenarc.CodeNarc",
            "-help",
        ],
        "run": [
            "java",
            "-classpath",
            "{}{}{}{}{}{}{}{}{}".format(
                GROOVY_PATH,
                JAVA_SEP,
                vendored_path(os.path.join("codenarc", "CodeNarc-1.1.jar")),
                JAVA_SEP,
                SLF4J_PATH,
                JAVA_SEP,
                vendored_path("codenarc"),
                JAVA_SEP,
                ".",
            ),
            "org.codenarc.CodeNarc",
            "-includes=**/*.groovy,**/Jenkinsfile,**/jenkinsfile,**/...groovy",
            "-report=console",
            "-rulesetfiles={}".format(os.path.join(os.getcwd(), "codenarc.xml")),
        ],
        "rundefault": [
            "java",
            "-classpath",
            "{}{}{}{}{}{}{}{}{}".format(
                GROOVY_PATH,
                JAVA_SEP,
                vendored_path(os.path.join("codenarc", "CodeNarc-1.1.jar")),
                JAVA_SEP,
                SLF4J_PATH,
                JAVA_SEP,
                vendored_path("codenarc"),
                JAVA_SEP,
                ".",
            ),
            "org.codenarc.CodeNarc",
            "-includes=**/*.groovy,**/Jenkinsfile,**/jenkinsfile,**/...groovy",
            "-report=console",
            "-rulesetfiles=codenarc.xml",
        ],
        "dotfiles": ["codenarc.xml"],
        "language": "groovy",
        "autorun": True,
        "run_per_file": False,
    }
)
class CodenarcParser(ParserBase):
    """Parse Codenarc output."""

    def parse(self, lint_data):
        messages = set()
        path = ""
        msg = ""
        line_no = -1
        for line in lint_data.split("\n"):
            try:
                if line.strip().startswith("File:"):
                    path = line.split("File:")[-1].strip()
                    continue

                if line.strip().startswith("Violation:"):
                    parts = line.strip().split()
                    line_no = int(parts[3].split("=")[-1])
                    msg = line.strip()
                else:
                    msg += "\n" + line
                if "Src=" in line:
                    messages.add((path, line_no, msg))
                    msg = ""
            except (ValueError, IndexError, TypeError):
                print("Invalid message: {0}".format(line))
        return messages
