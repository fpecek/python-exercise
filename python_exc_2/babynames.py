#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re

"""Baby Names exercise

Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 -Extract the year and print it
 -Extract the names and rank numbers and just print them
 -Get the names data into a dict and print it
 -Build the [year, 'name rank', ... ] list and print it
 -Fix main() to use the extract_names list
"""


def extract_names(filename):
    """
    Given a file name for baby.html, returns a list starting with the year string
    followed by the name-rank strings in alphabetical order.
    ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
    """
    name_ranks = []

    # REVIEW
    # You should release file handle as soon as posible.
    # If you have read the entire file in memory,there is no reason to keep the file handle opened.
    with open(filename, 'r') as f:
        file_content = f.read()

    year_match = re.search(r'\w+\s\w+\s(\d\d\d\d)', file_content)
    if year_match:
        name_ranks.append(year_match.group(1))

    # REVIEW
    # This regex is complex and correct, kudos :)
    # But it's a bit hard to read. Maybe break the problem into two parts.
    # First find the <tr> inner HTML using r'<tr align=\"right\">(.+)'
    # In the second part for every matched element perform another
    # regex r'<td>(.+?)<\/td>' to extract the values between <td> tags
    # return tuples (rank, male, female)
    name_rank_matches = re.findall(r'<td>(\d+)</td><td>(\w+)</td><td>(\w+)</td>', file_content)

    # d = {tuple[1] : idx + 1  for idx, tuple in enumerate(name_rank_matches)}
    # di = dict((male, rank) for rank, male, female in name_rank_matches)

    # This one is also correct, but maybe a bit over-complicated
    # try a simpler approach by creating a list of strings with
    # format 'name rank' by iterating through the list of tuples
    # and then sort the list
    # name_rank_dict = {}
    for rank_tuple in name_rank_matches:
        (rank, male, female) = rank_tuple
        name_ranks.append(f'{male} {rank}')
        name_ranks.append(f'{female} {rank}')

    return sorted(name_ranks)


def main():
    # This command-line parsing code is provided.
    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]

    if not args:
        print('usage: [--summaryfile] file [file ...]')
        sys.exit(1)

    # Notice the summary flag and remove it from args if it is present.
    summary = False
    if args[0] == '--summaryfile':
        summary = True
        del args[0]

    # +++your code here+++
    # For each filename, get the names, then either print the text output
    # or write it to a summary file
    for filename in args:
        result = '\n'.join(extract_names(filename))
        if summary:
            filename_summary = filename.split('.')[0] + "-summary.txt"
            with open(filename_summary, 'w') as outf:
                outf.write(result + '\n')
        else:
            print(result)


if __name__ == '__main__':
    main()
