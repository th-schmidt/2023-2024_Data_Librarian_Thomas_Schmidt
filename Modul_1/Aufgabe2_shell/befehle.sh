#!/bin/bash

# Grep all ISSN from all columns, remove trailing whitespaces and save them to tsv
cut -f 4,5,7,12,14 2023-11-20-Article_list_dirty.tsv | grep -Eo "\w{4}-\w{4}\s|\s\w{4}-\w{4}\s" | sed -E 's/\t| //g' > col_issn.tsv

# Grep all corresponding dates from all columns, remove trailing whitespaces and save them to a seperate tsv
cut -f 4,5,7,12,14 2023-11-20-Article_list_dirty.tsv | grep -Eo "\s19[0-9]{2}" | sed -E 's/\t| //g' > col_date.tsv

# Combine both tsvs using paste
paste col_issn.tsv col_date.tsv > issn_date.tsv

# Sort tsv, remove duplicates and save final version
sort -n issn_date.tsv | uniq > 2023-11-30-Dates_and_ISSNs.tsv
