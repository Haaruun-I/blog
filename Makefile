build:
	- clear
	- pipenv install
	make generate
	- clear
	hugo --gc --minify
	- make clear

serve:
	- clear
	./hugo serve -p 8000

generate:
	- clear
	- pipenv shell
	mkdir './page_gen'
	- rm $$(find . -wholename "./content/projects/*" ! -name "_index.md")
	python ./scripts/generate.py
	cp ./page_gen/* ./content/projects/
	- rm $$(find . -wholename "./page_gen/*")
	rmdir ./page_gen

clear:
	- clear
	rm $$(find . -wholename "./content/projects/*" ! -name "_index.md")
