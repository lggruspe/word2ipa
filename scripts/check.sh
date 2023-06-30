#!/usr/bin/env bash

# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html

# Check code.

mypy --strict word2ipa
flake8 word2ipa
pylint word2ipa
