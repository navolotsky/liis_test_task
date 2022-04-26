#!/usr/bin/env python
"""console_scripts entrypoint"""

import os
import sys


def main():
    cwd = os.getcwd()

    try:
        os.chdir(os.path.dirname(os.path.dirname(__file__)))

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "liis_test_task.core.settings")

        from django.core.management import execute_from_command_line

        execute_from_command_line(sys.argv)

    finally:
        os.chdir(cwd)


if __name__ == "__main__":
    main()
