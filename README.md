# word2ipa

Word-to-IPA transcriptions extracted from Wiktionary.

Sample:

```csv
en,ablest,eɪ.bləst
en,abligation,ɑb.ləˈɡeɪ.ʃən
en,abligurition,əˌblɪɡjʊˈɹɪʃən
en,ablings,ˈeɪ.blɪnz
en,ablood,əˈblʌd
en,abloom,əˈbluːm
en,ablow,əˈbloʊ
en,ablude,əˈbluːd
en,abluent,ˈæb.lu.ənt
en,ablur,əˈblɜː
en,ablur,əˈblɜːɹ
en,ablush,əˈblʌʃ
en,ablute,əˈbluːt
en,ablute,əˈblut
en,ablutionary,əˈblu.ʃəˌnɛ.ɹi
```

Each row contains a Wiktionary language code, a word and its transcription.

## Extracting IPA transcriptions

```bash
# Clone the repo.
git clone https://github.com/lggruspe/word2ipa
cd word2ipa

# Install some requirements.
python -m venv env
. env/bin/activate
pip install orjson

# Download machine-readable Wiktionary data from kaikki.
wget https://kaikki.org/dictionary/All%20languages%20combined/kaikki.org-dictionary-all.json
# Or https://kaikki.org/dictionary/<Language name>/kaikki.org-dictionary-<Language name>.json

# Extract transcriptions.
python -m word2ipa <.json dictionary from kaikki>
```

## Licenses

Copyright 2023 Levi Gruspe

The scripts in this repository are licensed under [GPLv3 or later](./LICENSES/GNU_GPLv3.txt).

The published CSV files are released under a [Creative Commons Attribution-ShareAlike 3.0 Unported License](./LICENSES/CC_BY-SA_3.0.txt).
These are extracted from Wiktionary with the help of [wiktextract](https://github.com/tatuylonen/wiktextract) and [kaikki.org](https://kaikki.org/index.html).

Wiktionary is licensed under [CC BY-SA 3.0](https://en.wiktionary.org/wiki/Wiktionary:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License).
