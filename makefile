PANDOCOPT=--highlight-style tango --latex-engine=lualatex -V documentclass=ltjarticle -V geometry:margin=1in 
PDF=diffusion.pdf gray-scott.pdf logistic.pdf md.pdf newton.pdf

TARGET=$(PDF)
all: $(TARGET)

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
