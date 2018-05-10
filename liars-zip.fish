#!/usr/bin/env fish

set DIR liars

mkdir -p $DIR

function col -a line n
    echo $line | awk -F ',' "{ print \$$n } "
end


set HEADERS (head -n 1 liars.csv)


tail -n +2 liars.csv | while read -l line
    set -l bbl (col $line 1)
    set -l job (col $line 2)
    set -l address (echo (col $line 8) | tr ' ' '_' | tr -d '"')
    set -l folder "$DIR/$job-$address"

    echo $folder
    
    mkdir -p $folder
    mkdir -p $folder/dof
    mkdir -p $folder/dob

    # save csv row as json
    printf "$HEADERS\n$line" | csvjson | jq '.' > $folder/jobinfo.json

    # extract dates of rent stabilized tax bills
    set bbl_json_file ~/.nyc-data/bbl/$bbl/$bbl.json

    # copy rent stabilized tax files
    cat $bbl_json_file | jq '.dof.taxBills | map(select(.rentStabilized)) | .[] | .date' | tr -d '"' \
    | xargs -I DATE date --date='DATE' +'%B*%Y*.pdf' \
    | xargs -I QUERY find ~/.nyc-data/dof/$bbl -type f -name 'QUERY' \
    | xargs -I FILE cp FILE $folder/dof
    
    # copy department of buildings pdfs and other files
    find ~/.nyc-data/dob/$job -type f | xargs -I FILE cp FILE $folder/dob
end

# zip it all up
zip -r liars.zip liars/
