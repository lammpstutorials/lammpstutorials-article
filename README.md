<!--
WARNING: DO NOT MODIFY DIRECTLY THE README.md!
This README.md file was assembled using the sed command from the files listed in
"files.txt". See the script in "generateREADME.sh". To modify the content of 
the  README.md, modify the files listed in "files.txt", or add a new file to the
list in "files.txt".
-->


# A Set of Tutorials for the LAMMPS Simulation Package

This article introduces a suite of tutorials designed to make learning LAMMPS
more accessible to new users.

## Tutorials

- Tutorial 1: Lennard-Jones fluid
- Tutorial 2: Pulling on a carbon nanotube
- Tutorial 3: Polymer in water
- Tutorial 4: Nanosheared electrolyte
- Tutorial 5: Reactive silicon dioxide
- Tutorial 6: Water adsorption in silica
- Tutorial 7: Free energy calculation
- Tutorial 8: Reactive Molecular Dynamics

## Input files

All the input files from the tutorials can be found in the 
[**files/**](files/) folder. The Python scripts used to generate the plots 
are also provided.

For each tutorial, a `.manifest` file lists all the files required to 
follow the tutorial. These files can be downloaded from the LAMMPS-GUI by 
selecting `Start Tutorial X`. The solutions to the tutorials are provided 
within the solution repository located in each tutorial folder.

## PDF

Access the last version of the `.pdf` from
[the Actions tab](https://github.com/lammpstutorials/lammpstutorials-article/actions/runs/12458522247/artifacts/2354075042) here on GitHub,
or clone this repository and compile the `.tex` file yourself by typing in a terminal:

```
make
```
This will generate the `.pdf` version of the tutorial. Ensure you have LaTeX and the necessary dependencies installed on your system before attempting to compile.

## Contributing

We welcome contributions to improve the tutorials. If you encounter any issues, have suggestions, or want to ask questions, please open an issue in this repository. You can also contribute by submitting a pull request to improve the tutorials or fix any bugs.
Your feedback and contributions help make the tutorials more useful for everyone.

## License

This project is licensed under the Creative Commons Attribution 4.0 International License. This license covers all the input [**files/**](files/) and tutorial content. For more details, see the [LICENSE](LICENSE) file.

## Authors

- [Simon Gravelle](https://github.com/simongravelle) (corresponding author),
  Univ. Grenoble Alpes, CNRS, LIPhy, 38000 Grenoble, France
- [Jacob R. Gissinger](https://www.stevens.edu/profile/jgissing),
  Stevens Institute of Technology, Hoboken, NJ 07030, USA
- [Axel Kohlmeyer](https://sites.google.com/site/akohlmey),
  Institute for Computational Molecular Science, Temple University, Philadelphia,
  PA 19122, USA



## Acknowledgements

- Simon Gravelle acknowledges funding from the European Union's Horizon 2020
  research and innovation programme under the Marie Skłodowska-Curie grant
  agreement No 101065060.
- Axel Kohlmeyer acknowledges financial support by Sandia National Laboratories
  under POs 2149742 and 2407526.


