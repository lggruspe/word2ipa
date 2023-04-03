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
	date -d "${BASH_REMATCH[1]}" '+%Y.%m.%d'
}

# Build CSV files.
dictionary="$(find-latest-dictionary)"
version="$(version "$dictionary")"
echo "Building version $version"

python -m word2ipa "$dictionary" -b data/broad.csv -n data/narrow.csv -u data/unknown.csv
echo "$version" > data/version.txt

echo "Done :)"
