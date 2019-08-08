INDEX=$(shell ls */README.md | sed 's/README.md/index.html/')
INDEX+= index.html
PANDOC_HTMLOPT=--mathjax -t html --template=template
PANDOCOPT=--highlight-style tango --latex-engine=lualatex -V documentclass=ltjarticle -V geometry:margin=1in 
PDF=diffusion.pdf gray-scott.pdf logistic.pdf md.pdf newton.pdf

all: $(INDEX) 

index.md: README.md
	sed 's/README.md/index.html/' $< > $@

index.html: index.md
	pandoc -s $< -o $@ $(PANDOC_HTMLOPT)
	rm -f index.md 

%/index.md: %/README.md
	gsed '2a [[Up]](../index.html)' $< > $@
	gsed -i '3a [[Repository]](https://github.com/kaityo256/highschool2019)\n' $@

%/index.html: %/index.md
	pandoc -s $< -o $@ $(PANDOC_HTMLOPT)


diffusion.pdf: diffusion/README.md
	pandoc $< -s -o $@ $(PANDOCOPT)

gray-scott.pdf: gray-scott/README.md
	pandoc $< -s -o $@ $(PANDOCOPT)

logistic.pdf: logistic/README.md
	pandoc $< -s -o $@ $(PANDOCOPT)

md.pdf: md/README.md
	pandoc $< -s -o $@ $(PANDOCOPT)

newton.pdf: newton/README.md
	pandoc $< -s -o $@ $(PANDOCOPT)

clean:
	rm -f $(PDF)
	rm -f $(INDEX)
