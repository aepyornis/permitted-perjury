#!/usr/bin/env fish

if test -e $BBLER_PATH/lib/functions.fish
    source $BBLER_PATH/lib/functions.fish
else
    echo "Failed to source BBLER functions. Is BBLER installed?" 1>&2
    exit 1
end


function __files_downloaded -a bbl job
    set -l num_of_tax_bills (find ~/.nyc-data/dof/$bbl -type f -name '*.pdf' | wc -l)
    
    if test $num_of_tax_bills -lt 2
	return 1
    else if not test -e ~/.nyc-data/dob/$job/$job.html
	return 1
    else
	return 0
    end
end

set out_file 'possible_liars.csv'
set headers (string join "," (head -n 1 jobs.csv) 'rentStabAnswer' 'liarStatus' 'liar' 'z_unit_count_15' 'z_unit_count_16' 'z_unit_count_17' )

echo $headers > $out_file

tail -n +2 jobs.csv | while read -l line
    # Set variables for BBl and JOB
    set -l bbl (echo $line | awk -F ',' '{print $1}')
    set -l job (echo $line | awk -F ',' '{print $2}')
    echo "Job #$job for BBL: $bbl"

    
    # This skips lines for jobs or bbls that are missing downloaded tax or dob information
    # if we commented them out, they wll get downloaded, but it greatly slows down the process
    # if not __files_downloaded $bbl $job
    # 	print_blue 'skipping...'
    # 	continue
    # end

    # run bbler to get lot'o'info about the tax lot for this job
    # bbler stores data in ~/.nyc-data and won't re-downloaded
    # it it already exists 
    bbler $bbl

    # bbler will usually download and parse the data we need.
    # But it probably only succeeds about 80% of the time
    # (such is life with parsing pdfs from slow city websites)
    # We will attempt to re download and parse them here
    if not __files_downloaded $bbl $job
	download_and_parse_job $job
    end
    
    set -l liar_json (python3 ./find-liar.py $job)

    # If the python program above fails, 
    # we'll just skip this line of jobs.csv alltogether
    if test $status -eq 0
	set -l liar_csv (echo $liar_json | jq '[.rentStabAnswer, .liarStatus, .liar] | @csv')
	
	if test -e ~/.nyc-data/bbl/$bbl/$bbl.json
	    set unit_counts (string unescape (unit_counts_as_csv_for $bbl))
	else
	    set unit_counts ',,'
	end

	echo (string join '' $line ',' (string unescape $liar_csv) ',' $unit_counts) >> $out_file
    end
end
