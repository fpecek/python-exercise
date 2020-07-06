#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import subprocess
import zipfile

"""
Copy Special exercise
"""


# +++your code here+++
# Write functions and modify main() to call them
def get_special_paths(directory):
    """
    Returns a list of the absolute paths of the special files in the given directory.
    "special" file is one where the name contains the pattern __w__ somewhere,
    where the w is one or more word chars.
    """
    special_files = []
    filenames = os.listdir(directory)
    for filename in filenames:
        special_file_match = re.search(r'__\w+__', filename)
        if special_file_match:
            special_files.append(os.path.abspath(os.path.join(directory, filename)))

    return special_files


def copy_to(paths, directory):
    """
    Copy all paths to given directory
    """
    if not os.path.exists(directory):
        os.mkdir(directory)

    for path in paths:
        shutil.copy(path, directory)


def zip_to(paths, zip_path):
    """
    Add all files from given paths to zip file
    """
    # REVIEW: did you mean: zipfile.ZipFile(zip_path, 'w')
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for path in paths:
            zipf.write(path)


def zip_to_command(paths, zip_path):
    """
    Add all files from given paths to zip file
    """
    subprocess.run(['zip', '-j', zip_path] + paths)


def main():
    # This basic command line argument parsing code is provided.
    # Add code to call your functions below.

    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]
    if not args:
        print("usage: [--todir dir][--tozip zipfile] dir [dir ...]")
        sys.exit(1)

    # todir and tozip are either set from command line
    # or left as the empty string.
    # The args array is left just containing the dirs.
    to_dir = ''
    if args[0] == '--todir':
        to_dir = args[1]
        del args[0:2]

    to_zip = ''
    if args[0] == '--tozip':
        to_zip = args[1]
        del args[0:2]

    if len(args) == 0:
        print("error: must specify one or more dirs")
        sys.exit(1)

    # +++your code here+++
    # Call your functions
    for directory in args:
        paths = get_special_paths(directory)
        if to_dir:
            copy_to(paths, to_dir)
        elif to_zip:
            zip_to_command(paths, to_zip)
        else:
            print('\n'.join(paths))


if __name__ == "__main__":
    main()
