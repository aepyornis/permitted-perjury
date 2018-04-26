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

##########
# report #
##########

report: docs docs/images docs/index.html

docs:
	mkdir -v -p docs

docs/images: images
	mkdir -v -p docs/images
	rsync -a -v --delete images/ docs/images/

docs/%.html: src/%.md style.css.html
	pandoc -s --from=markdown -H style.css.html -o $@ $<

clean:
	rm -fr ./docs

.PHONY: clean
.EXPORT_ALL_VARIABLES:
