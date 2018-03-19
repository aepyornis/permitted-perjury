build: html html/images html/index.html

html:
	mkdir -v -p html

html/images: images
	mkdir -v -p html/images
	rsync -a -v --delete images/ html/images/

html/%.html: src/%.md style.css.html
	pandoc -s --from=markdown -H style.css.html -o $@ $<

clean:
	rm -fr ./html

.PHONY: clean
