PANDOCOPT=--highlight-style tango --latex-engine=lualatex -V documentclass=ltjarticle -V geometry:margin=1in 

TARGET=diffusion.pdf
all: $(TARGET)

%.pdf: %.md
	pandoc $< -s -o $@ $(PANDOCOPT)

