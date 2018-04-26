#!/usr/bin/env fish

set DIR liars

mkdir -p $DIR

function col -a line n
    echo $line | awk -F ',' "{ print \$$n } "
end


tail -n +2 liars.csv | head -n 25 | while read -l line
    set -l job (col $line 2)
    set -l address (echo (col $line 8) | tr ' ' '_' | tr -d '"')
    set -l folder "$DIR/$job-$address"
end
