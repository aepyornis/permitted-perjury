#######################
#  permitted perjury  #
#######################

PGDATABASE := nycdb
PGHOST := 127.0.0.1
PGUSER := nycdb
PGPASSWORD := nycdb

default:
	@echo 'permitted perjury'


jobs.csv: sql/jobs.sql
	psql -c \
	"COPY ( $(shell cat sql/jobs.sql) ) TO STDOUT WITH CSV HEADER DELIMITER ','" \
	> jobs.csv


# This downloads and parses LOTS of pdfs
# It takes a long time.
# By a long time, I mean WEEKS!
possible_liars.csv: find-all-liars.fish
	./find-all-liars.fish


liars.csv: possible_liars.csv
	csvsql --query "select * from possible_liars where liarStatus <> 'no'" possible_liars.csv > liars.csv


liars.zip: liars.csv
	./liars-zip.fish

##############
# Lead paint #
##############

lead_paint_bbls.csv: sql/lead_paint_violations.sql
	psql -c "COPY ( $(shell cat sql/lead_paint_violations.sql) ) TO STDOUT WITH CSV HEADER DELIMITER ','"  > lead_paint_bbls.csv

############
# notebook #
############

notebook-setup:
	python3 -m venv notebook/venv --without-pip --system-site-packages
	notebook/venv/bin/python3 -m pip install jupyter pandas matplotlib

notebook-serve:
	notebook/venv/bin/jupyter notebook --ip=127.0.0.1


##########
# report #
##########

report: docs docs/index.html

docs:
	mkdir -v -p docs

docs/%.html: report/%.md style.css.html
	pandoc -s --from=markdown -H style.css.html -o $@ $<

clean:
	rm -fr ./docs

.PHONY: clean notebook-setup notebook-serve
.EXPORT_ALL_VARIABLES:
