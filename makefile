PANDOCOPT=--highlight-style tango --latex-engine=lualatex -V documentclass=ltjarticle -V geometry:margin=1in 
MD=$(shell ls */*.md)
PDF=$(MD:%.md=%.pdf)


TARGET=$(PDF)
all: $(TARGET)

%.pdf: %.md
	pandoc $< -s -o $@ $(PANDOCOPT)

