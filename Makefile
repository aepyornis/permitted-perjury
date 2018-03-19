build: docs docs/images docs/index.html

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
