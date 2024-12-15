# Makefile for building lammps-tutorials.pdf
all: build

# Target to build the PDF
build:
	latexmk -pdf lammps-tutorials.tex

# Target to clean up generated files
clean:
	rm -f lammps-tutorials.pdf \
	lammps-tutorials.aux \
	lammps-tutorials.log \
	lammps-tutorials.out \
	lammps-tutorials.bbl \
	lammps-tutorials.blg