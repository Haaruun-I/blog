build:
	- clear
	make generate
	- clear
	hugo --gc --minify

serve:
	- clear
	./hugo serve -p 8006

generate:
		- clear
		- make clear
		python ./scripts/generate.py

clear:
	- find . -wholename "./content/*/*.md" ! -name "_index.md" -exec rm {} \;
