#!/usr/bin/env bash

# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html

# Package TSV files.

if [ ! -f data/version.txt ]; then
	echo "Version file not found"
	exit 1
fi

if [ ! -f data/broad.tsv ]; then
	echo "Broad transcriptions not found"
	exit 1
fi

if [ ! -f data/narrow.tsv ]; then
	echo "Narrow transcriptions not found"
	exit 1
fi

if [ ! -f data/unknown.tsv ]; then
	echo "Error transcriptions not found"
	exit 1
fi


version="$(cat data/version.txt)"
name="word2ipa-$version"
dest="dist/$name"

echo "Packaging $name"

mkdir -p "$dest"
cp data/broad.tsv data/narrow.tsv data/unknown.tsv README.md "$dest"
cp data/version.txt "$dest"
cp LICENSES/CC_BY-SA_3.0.txt "$dest/LICENSE"
cd dist || exit 1
tar -czf "$name.tar.gz" "$name"

echo "Done :)"
