#!/usr/bin/env python
# coding: utf-8

import sys, os, git

current_path = os.getcwd()
git_repo = git.Repo(current_path, search_parent_directories=True)
git_path = git_repo.git.rev_parse("--show-toplevel")

from tutorialslist import tutorials

sys.path.append(git_path + "/sphinx-to-latex/functions/")

from ReadRST import ReadRST
from WriteTEX import WriteTex
from FixDocument import FixDocument

mode = ["light"]

folder = '/sphinx-to-latex'

for level in tutorials.keys():
    if os.path.exists(git_path+folder+'/converted-files/'+level) is False:
        os.mkdir(git_path+folder+'/converted-files/'+level)
    for tutorial in tutorials[level]:
        rst_path = git_path+folder+'/lammpstutorials.github.io/docs/sphinx/source/tutorials/'+level+'/'
        rst_file_name = rst_path+tutorial+'.rst'
        tex_file_name = git_path+folder+'/converted-files/'+level+'/'+tutorial+'.tex'   
        RST = ReadRST(rst_file_name, rst_path)
        RST.convert_file()
        assert len(RST.label_positions) == 1, """Careful, more than one label"""
        TEX = WriteTex(tex_file_name, RST, git_path, rst_path, mode)
        TEX.convert_file()
        FIX = FixDocument(tex_file_name)
        FIX.fix_document()

print("Compilation completed")