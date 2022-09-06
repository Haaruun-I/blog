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

generate-pipenv:
	- clear
	mkdir './page_gen'
	- rm $$(find . -wholename "./content/projects/*" ! -name "_index.md")
	pipenv run python ./scripts/generate.py
	cp ./page_gen/* ./content/projects/
	- make clear-temp


generate:
		- clear
		mkdir './page_gen'
		- make clear
		python ./scripts/generate.py
		cp ./page_gen/* ./content/projects/
		- make clear-temp

clear-temp:
	- rm $$(find . -wholename "./page_gen/*")
	- rmdir ./page_gen

clear:
	- rm $$(find . -wholename "./content/projects/*" ! -name "_index.md")
