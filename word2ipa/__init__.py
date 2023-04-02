# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""Extract IPA data from kaikki dump."""

from pathlib import Path
import re
import typing as t

from orjson import loads    # pylint: disable=no-name-in-module


LanguageCode: t.TypeAlias = str
Word: t.TypeAlias = str
Transcription: t.TypeAlias = str


def extract_transcriptions(
    path: Path,
    include_narrow_transcriptions: bool = False,
) -> t.Iterator[tuple[LanguageCode, Word, Transcription]]:
    """Extract words and broad IPA transcriptions from kaikki dump file."""
    table = {
        ord(" "): "",
        ord("/"): "",
        ord("["): "",
        ord("]"): "",
    }
    with open(path, encoding="utf-8") as file:
        for line in file:
            data = loads(line)
            word = data["word"]
            lang_code = data["lang_code"]
            for sound in data.get("sounds", []):
                if "ipa" not in sound:
                    continue

                raw = sound.get("ipa", "")
                is_transcription = (
                    is_broad_transcription(raw)
                    or (
                        include_narrow_transcriptions
                        and is_narrow_transcription(raw)
                    )
                )
                if not is_transcription:
                    continue

                raw = raw.translate(table)
                for transcription in alternate_transcriptions(raw):
                    yield lang_code, word, transcription


def is_broad_transcription(transcription: str) -> bool:
    """Check if the transcription is a broad transcription."""
    return transcription.startswith("/") and transcription.startswith("/")


def is_narrow_transcription(transcription: str) -> bool:
    """Check if the transcription is a narrow transcription."""
    return transcription.startswith("[") and transcription.endswith("]")


# Regex for removing parentheses and everything in between.
parenthesis_pattern = re.compile(r"\(.*\)")

# Translation table for removing parentheses.
parenthesis_table = {
    ord("("): "",
    ord(")"): "",
}


def alternate_transcriptions(raw: str) -> list[str]:
    """Extract alternate transcriptions from kaikki IPA value.

    There may be multiple transcriptions, because some IPA values have:

    - ~ (alternate transcriptions)
    - parentheses (optional sounds)
    """
    assert not raw.startswith("/")
    assert not raw.startswith("[")
    assert not raw.endswith("/")
    assert not raw.endswith("]")

    transcriptions = []
    for before in raw.split("~"):
        after = parenthesis_pattern.sub("", before)
        transcriptions.append(after.translate(parenthesis_table))
        if before != after:
            transcriptions.append(before.translate(parenthesis_table))
    return transcriptions


__all__ = ["extract_transcriptions"]
