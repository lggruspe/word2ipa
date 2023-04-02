#!/usr/bin/env bash

# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html

# Download Kaikki dictionary.

url="https://kaikki.org/dictionary/All%20languages%20combined/kaikki.org-dictionary-all.json"

parse-last-modified() {
	rg 'Last-Modified: (.*)' -or '$1'
}

function last-modified() {
	date -I -d "$(wget -S --spider "$url" 2> >(parse-last-modified))"
}

outfile="data/kaikki/all-$(last-modified).jsonl"

if [ -f "$outfile" ]; then
	echo "$outfile already exists"
	exit 0
fi

echo "Downloading $outfile"

mkdir -p data/kaikki
wget --output-document "$outfile" "$url" --show-progress
