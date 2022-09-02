# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

"""
Responsible for writing the built news fragments to a news file without
affecting existing content.
"""


import os


def append_to_newsfile(
    directory, filename, start_string, top_line, content, single_file
):
    """
    Write *content* to *directory*/*filename* behind *start_string*.

    Double-check *top_line* (i.e. the release header) is not already in the
    file.

    if *single_file* is True, add it to an existing file, otherwise create a
    fresh one.
    """
    news_file = os.path.join(directory, filename)

    header, prev_body = _figure_out_existing_content(
        news_file, start_string, single_file
    )

    if top_line and top_line in prev_body:
        raise ValueError("It seems you've already produced newsfiles for this version?")

    with open(news_file, "w", encoding="utf8") as f:
        if header:
            f.write(header)

        f.write(content)

        if prev_body:
            f.write(f"\n\n{prev_body}")


def _figure_out_existing_content(news_file, start_string, single_file):
    """
    Try to read *news_file* and split it into header (everything before
    *start_string*) and the old body (everything after *start_string*).

    If there's no *start_string*, return empty header.

    Empty file and per-release files have neither.
    """
    if not single_file or not os.path.exists(news_file):
        # Per-release news files always start empty.
        # Non-existent files have no existing content.
        return "", ""

    with open(news_file, encoding="utf8") as f:
        content = f.read()

    t = content.split(start_string, 1)
    if len(t) == 2:
        return f"{t[0].rstrip()}\n\n{start_string}\n", t[1].lstrip()

    return "", content.lstrip()
