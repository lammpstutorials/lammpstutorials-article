#!/bin/bash
set -e

# pull the last version
git pull

# update lammps tutorials in case changes were made
git submodule update --remote

