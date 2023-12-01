#!/bin/bash

# Clean rows starting with IMPORTANT string to get correct column series
sed -E 's/IMPORTANT\t*//g' 2023-11-20-Article_list_dirty.tsv > clean_issn.tsv

# Grep ISSN and Date column but preserve column layout
cut -f 5,12 clean_issn.tsv | grep -E "[0-9]{4}[-0-9A-Z]*" > issn_dates.tsv

# Remove ISSN strings from iss_dates.tsv and sort it uniquly; ignore non-printable chars
sed -E 's/issn[:[:space:]]*//gI' issn_dates.tsv | sort -ui > 2023-11-30-ISSN_DATES_ths.tsv

# Remove temp tsvs
rm clean_issn.tsv issn_dates.tsv
