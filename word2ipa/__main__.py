# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""Extract IPA data from kaikki dump."""

from argparse import ArgumentParser, Namespace
from csv import writer
from pathlib import Path
import sys

from . import extract_transcriptions


def parse_args() -> Namespace:
    """Parse command-line arguments."""
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "dictionary",
        type=Path,
        help="kaikki dictionary file (.jsonl file)",
    )
    parser.add_argument(
        "--include-narrow-transcriptions",
        dest="include_narrow_transcriptions",
        default=False,
        action="store_true",
    )
    return parser.parse_args()


def main(args: Namespace) -> None:
    """Script entrypoint."""
    csv_writer = writer(sys.stdout)
    for language, word, transcription in extract_transcriptions(
        args.dictionary,
        include_narrow_transcriptions=args.include_narrow_transcriptions,
    ):
        csv_writer.writerow((language, word, transcription))


if __name__ == "__main__":
    main(parse_args())
