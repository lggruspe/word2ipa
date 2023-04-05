# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""Transcription type definition."""

from enum import auto, Enum
import re
import typing as t

from word2ipa.schema import Schema


class TranscriptionKind(Enum):
    """Transcriptions can be /broad/ or [narrow].

    Some transcriptions from Wiktionary aren't marked as broad or narrow.
    """
    BROAD = auto()
    NARROW = auto()
    UNKNOWN = auto()


class Transcription(t.NamedTuple):
    """IPA transcription and kind (/broad/, [narrow] or unknown)."""
    transcription: str
    kind: TranscriptionKind


def transcription_kind(ipa: str) -> TranscriptionKind:
    """Get transcription kind."""
    if ipa.startswith("/") and ipa.endswith("/"):
        return TranscriptionKind.BROAD
    if ipa.startswith("[") and ipa.endswith("]"):
        return TranscriptionKind.NARROW
    return TranscriptionKind.UNKNOWN


# Translation table for removing brackets from IPA transcriptions.
bracket_table = {
    ord("/"): "",
    ord("["): "",
    ord("]"): "",
}


def extract_transcriptions(data: Schema) -> t.Iterator[Transcription]:
    """Extract transcriptions for a given word from the kaikki data."""
    for sound in data.get("sounds", []):
        if "ipa" not in sound:
            continue

        raw = sound["ipa"]
        kind = transcription_kind(raw)
        raw = raw.translate(bracket_table)

        for transcription in expand(raw):
            yield Transcription(
                transcription=transcription,
                kind=kind,
            )


# Regex for removing parentheses and everything in between.
parenthesis_pattern = re.compile(r"\(.+?\)|⁽[¹²³⁴⁵⁻ʰʲᵏˡᵖˢᵗʷᵝ]*⁾")

# Translation table for removing parentheses.
parenthesis_table = {
    ord("("): "",
    ord(")"): "",
    ord("⁽"): "",
    ord("⁾"): "",
}


def expand(raw: str) -> t.Iterator[str]:
    """Expand transcription.

    Alternate transcriptions separated by `~` are expanded into multiple
    transcriptions. E.g. `a~o` becomes `[a, o]`.

    If the raw transcription has parentheses, the transcription is expanded
    into two: (1) with the optional parts, and (2) without the optional parts.
    E.g. `pa(ra)` becomes `[pa, para]`.
    """
    assert not raw.startswith("/")
    assert not raw.endswith("/")

    assert not raw.startswith("[")
    assert not raw.endswith("]")

    for before in raw.split("~"):
        after = parenthesis_pattern.sub("", before)
        yield after.translate(parenthesis_table)

        if before != after:
            yield before.translate(parenthesis_table)


__all__ = ["extract_transcriptions", "Transcription", "TranscriptionKind"]
