# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""kaikki.org dictionary word schema."""

import typing as t


class SoundSchema(t.TypedDict):
    """Schema for .sounds values."""
    ipa: t.NotRequired[str]


class Schema(t.TypedDict):
    """Schema for each line in a kaikki.org dictionary."""
    word: str
    lang_code: str
    sounds: t.NotRequired[list[SoundSchema]]


__all__ = ["Schema"]
