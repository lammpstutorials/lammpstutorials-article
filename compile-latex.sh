#!/bin/bash
set -e

# pull the last version
git pull

# update lammps tutorials in case changes were made
git submodule update --remote

rm -f *.aux
rm -f *.bbl
rm -f *.blg
rm -f *.out

pdflatex lammps-tutorials.tex
bibtex lammps-tutorials
pdflatex lammps-tutorials.tex
pdflatex lammps-tutorials.tex
