#######################
#  permitted perjury  #
#######################

PGDATABASE := nycdb
PGHOST := 127.0.0.1
PGUSER := nycdb
PGPASSWORD := 

default:
	@echo 'permitted perjury'


jobs.csv: sql/jobs.sql
	psql -c \
	"COPY ( $(shell cat sql/buildings_with_jobs.sql) ) TO STDOUT WITH CSV HEADER DELIMITER ','" \
	> jobs.csv


build: docs docs/images docs/index.html


##########
# report #
##########

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
