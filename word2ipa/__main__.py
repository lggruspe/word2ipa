# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""Extract IPA data from kaikki dump."""

from argparse import ArgumentParser, Namespace
from csv import writer
from pathlib import Path
import typing as t

from orjson import loads    # pylint: disable=no-name-in-module

from word2ipa.transcription import extract_transcriptions, TranscriptionKind


LanguageCode: t.TypeAlias = str
Word: t.TypeAlias = str
Pronunciation: t.TypeAlias = str
Record: t.TypeAlias = tuple[LanguageCode, Word, Pronunciation]


def parse_args() -> Namespace:
    """Parse command-line arguments."""
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "dictionary",
        type=Path,
        help="kaikki dictionary file (.jsonl file)",
    )
    parser.add_argument(
        "-b",
        "--broad",
        dest="broad",
        default=None,
        type=Path,
        help="output file for broad transcriptions",
    )
    parser.add_argument(
        "-n",
        "--narrow",
        dest="narrow",
        default=None,
        type=Path,
        help="output file for narrow transcriptions",
    )
    parser.add_argument(
        "-u",
        "--unknown",
        dest="unknown",
        default=None,
        type=Path,
        help="output file for unknown/invalid transcriptions",
    )
    return parser.parse_args()


def main(args: Namespace) -> None:
    """Script entrypoint."""
    if not any((args.broad, args.narrow, args.unknown)):
        return

    broad = set()
    narrow = set()
    unknown = set()

    with open(args.dictionary, encoding="utf-8") as file:
        for line in file:
            data = loads(line)
            word = data["word"]
            lang_code = data["lang_code"]

            for transcription in extract_transcriptions(data):
                record = (lang_code, word, transcription.transcription)
                match transcription.kind:
                    case TranscriptionKind.BROAD if args.broad is not None:
                        broad.add(record)
                    case TranscriptionKind.NARROW if args.narrow is not None:
                        narrow.add(record)
                    case TranscriptionKind.UNKNOWN if args.unknown is not None:
                        unknown.add(record)

    write_records(args.broad, broad)
    write_records(args.narrow, narrow)
    write_records(args.unknown, unknown)


def write_records(path: Path | None, records: set[Record]) -> None:
    """Write records into a CSV in sorted order."""
    if path is None:
        return

    with open(path, "w", encoding="utf-8") as file:
        csv_file = writer(file)
        for record in sorted(records):
            csv_file.writerow(record)


if __name__ == "__main__":
    main(parse_args())
