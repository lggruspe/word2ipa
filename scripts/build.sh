#!/usr/bin/env bash

# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html

# Build word lists.

find-latest-dictionary() {
	find data/kaikki | sort --reverse | head -n 1
}

version() {
	pattern="all-(.*).jsonl"
	[[ "$1" =~ $pattern ]]
	echo "${BASH_REMATCH[1]}"
}

path="$(find-latest-dictionary)"
broad="data/word2ipa-broad-$(version "$path")"
narrow="data/word2ipa-broad+narrow-$(version "$path")"

found=0
if [ -d "$broad" ]; then
	echo "$broad already exists"
	found="$((found + 1))"
fi

if [ -d "$narrow" ]; then
	echo "$narrow already exists"
	found="$((found + 1))"
fi

if [ "$found" = "2" ]; then
	echo ":)"
	exit 0
fi

# Build CSV files.
mkdir -p "$broad" "$narrow"
python -m word2ipa "$path" | sort | uniq > "$broad/word2ipa.csv"
python -m word2ipa "$path" --include-narrow-transcriptions | sort | uniq > "$narrow/word2ipa.csv"
echo ":)"
