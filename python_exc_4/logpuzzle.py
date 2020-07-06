#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib.request

"""
Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""


def url_sort_key(url):
    match = re.search(r'-(\w+)-(\w+)\.jpg', url)
    return match.group(2) if match else url


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
    # +++your code here+++
    base_url = 'http://{}'.format(filename.split('_')[1])

    with open(filename, 'r') as logfile:
        text = logfile.read()

    url_matches = re.findall(r'GET\s([\w+/-]+\.jpg)', text)
    # REVIEW: use string formatting instead of concatenation
    urls = {f'{base_url}{img_url}' for img_url in url_matches if 'puzzle' in img_url}

    return sorted(urls, key=url_sort_key)


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
    # +++your code here+++
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    with open(os.path.join(dest_dir, 'index.html'), 'w') as outf:
        outf.write('<html><body>')
        print('Downloading images...')
        for idx, img_url in enumerate(img_urls):
            print(img_url)
            img_name = 'img{}'.format(idx)
            urllib.request.urlretrieve(img_url, os.path.join(dest_dir, img_name))
            outf.write('<img src="{}">'.format(img_name))
        outf.write('\n</body></html>')


def main():
    args = sys.argv[1:]

    if not args:
        print('usage: [--todir dir] logfile ')
        sys.exit(1)

    to_dir = ''
    if args[0] == '--todir':
        to_dir = args[1]
        del args[0:2]

    img_urls = read_urls(args[0])

    download_images(img_urls, to_dir) if to_dir else print('\n'.join(img_urls))


if __name__ == '__main__':
    main()
