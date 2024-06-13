import rstparse, os, shutil
import numpy as np
from PIL import Image

from utilities import replace_special_character, fix_math, fix_link, fix_italic, \
                      clean_block, filter_block, identify_subblock_id, read_sublock, \
                      count_line, fix_citation

class WriteTex:
    """Write Tex file."""
    def __init__(self, file_name, RST, git_path, rst_path, mode, nonumber = False, *args, **kwargs,):
        """Initialize"""
        super().__init__(*args, **kwargs)
        self.file_name = file_name
        self.RST = RST
        self.rst_path = rst_path
        self.git_path = git_path
        self.nonumber = nonumber
        self.mode = mode

    def convert_file(self):
        # Main convert function.
        self.open_f()
        self.write_main_title()
        self.write_main_label()
        self.loop_on_block()
        self.close_f()

    def open_f(self):
        self.f = open(self.file_name, "w") 

    def close_f(self):
        self.f.close()

    def loop_on_block(self):
        for block_id in np.unique(self.RST.main_block):
            raw_block, block_type, block_lines = clean_block(self.RST.file_content,
                                                             self.RST.main_block_type,
                                                             self.RST.main_block, block_id)
            filtered_block, n_subblock = filter_block(raw_block, block_type)

            # Look for title
            if block_lines[0] in self.RST.title_positions:
                title = self.RST.file_content[block_lines[0]]
                filtered_block = title
                block_type = np.array(self.RST.title_types)[np.array(self.RST.title_positions) == block_lines[0]]
            ids_subblock, types_subblock = identify_subblock_id(n_subblock, block_lines, self.RST)
            filtered_subblock, sub_block_number = read_sublock(n_subblock, filtered_block,
                                                               ids_subblock, self.RST)
            self.write_paragraph(filtered_block, block_type, filtered_subblock,
                                 ids_subblock, types_subblock, sub_block_number)
            self.write_equation(filtered_block, block_type)
            self.write_title(filtered_block, block_type)
        
    def write_main_title(self):
        title_position = self.RST.title_positions[np.where(np.array(self.RST.title_types) == "main")[0][0]]
        if self.nonumber is False:
            self.f.write('\chapter{'+self.RST.file_content[title_position]+'}')
        else:
            if self.RST.file_content[title_position] == "Before you start":
                self.f.write('\chapter*{Preface}')
            else:
                self.f.write('\chapter*{'+self.RST.file_content[title_position]+'}')
        self.f.write('\n')

    def write_main_label(self):
        label_position = self.RST.label_positions[np.where(np.array(self.RST.label_types) == "main")[0][0]]
        label = self.RST.file_content[label_position].split("_")[1][:-1]
        self.f.write('\label{'+label+'}')
        self.f.write('\n')

    def write_paragraph(self, filtered_block, block_type, filtered_subblock, ids_subblock, types_subblock, sub_block_number):
        
        if ("text" in block_type):
            for line in filtered_block:
                line = replace_special_character(line, '* 1', r'$\star 1$')
                line = replace_special_character(line, '#', r'$\#$')
                line = replace_special_character(line, 'Å', r'$\text{\AA{}}$')
                line = replace_special_character(line, '*->*', r'$\rightarrow$')
                line = fix_link(self.RST, line)
                line = fix_math(line)
                line = fix_citation(line)
                line = fix_italic(line, replace_underscore=True)
                self.f.write(line)
                self.f.write('\n')
        elif ("admonition" in block_type) & ("You can support" not in block_type):
            #if block_type
            cpt = 0
            caption = block_type[11:]
            self.f.write(r'\begin{tcolorbox}[colback=mylightblue!5!white,colframe=mylightblue!75!black,title='+caption+']'+'\n')
            #self.f.write(r'\noindent \textbf{' + caption + '} -- ')
            for line in filtered_block:
                line = fix_math(line)
                line = fix_link(self.RST, line)
                line = fix_italic(line, replace_underscore=True)
                if line == '[insert-sub-block]': 
                    filtered_subblock_0 = []
                    for line, n in zip(filtered_subblock, sub_block_number):
                        if n == cpt:
                            filtered_subblock_0.append(line)    
                    if ('figure' not in types_subblock[cpt]) & ('math' in types_subblock[cpt]):
                        self.write_equation(filtered_subblock_0, types_subblock[cpt])
                    elif ('figure' not in types_subblock[cpt]) & ('lammps-equation' in types_subblock[cpt]):
                        self.write_equation(filtered_subblock_0, types_subblock[cpt])
                    cpt += 1
                else:

                    if cpt == 0:
                        self.f.write(line)
                        self.f.write('\n')
                    else:
                        if ('math' not in types_subblock[cpt-1]) & ('lammps-equation' not in types_subblock[cpt-1]):
                            n = count_line(line)
                            line = line[n:]
                            self.f.write(line)
                            self.f.write('\n')
            self.f.write(r'\end{tcolorbox}')
        elif "hatnote" in block_type:
            for line in filtered_block:
                line = fix_math(line)
                self.f.write(r'\vspace{-1cm} '
                + r'\noindent \textcolor{graytitle}{\textit{{\Large '+line+
                '}}'
                + r'\vspace{0.5cm} }')
                self.f.write('\n')
        elif ("figure::" in block_type) & (self.mode == "light") & ("light" in block_type):
            align = None
            for line in filtered_block:
                if "height" in line:
                    height = line[9:]
                elif "align" in line:
                    align = line[8:]
            figure_path_and_name = block_type.split('::')[1].strip()
            figure_name = figure_path_and_name.split('/')[-1]
            relative_path = figure_path_and_name[:-len(figure_name)]
            absolute_path = (self.rst_path + relative_path).strip()
            figure_format = figure_name.split('.')[-1]

            if figure_format == "webp":
                # replace webp animation by png image
                figure_format = ".png"
                figure_name = figure_name.split('.')[0]+figure_format

            if os.path.exists(absolute_path + figure_name) is False:
                print("Warning, figure not found", absolute_path + figure_name)

            if align is None:
                self.f.write(r'\begin{figure}[h!]'+'\n')
                self.f.write(r'\includegraphics[width=\linewidth]{' + absolute_path + figure_name + '}'+'\n')
                self.f.write(r'\end{figure}'+'\n')  
            elif 'right' in align:
                self.f.write(r'\hspace{-0.45cm}')
                self.f.write(r'\begin{wrapfigure}{r}{4cm}'+'\n')
                self.f.write(r'\includegraphics[width=4cm]{' + absolute_path + figure_name + '}'+'\n')
                self.f.write(r'\end{wrapfigure}'+'\n')
        elif ("figure::" in block_type) & (self.mode == "dark") & ("dark" in block_type):
            align = None
            for line in filtered_block:
                if "height" in line:
                    height = line[9:]
                elif "align" in line:
                    align = line[8:]
            figure_path_and_name = block_type.split('::')[1].strip()
            figure_name = figure_path_and_name.split('/')[-1]
            relative_path = figure_path_and_name[:-len(figure_name)]
            absolute_path = (self.rst_path + relative_path).strip()
            figure_format = figure_name.split('.')[-1]
            if figure_format == "webp":
                # replace webp animation by png image
                figure_format = ".png"
                figure_name = figure_name.split('.')[0]+figure_format
            if os.path.exists(absolute_path + figure_name) is False:
                print("Warning, figure not found", absolute_path + figure_name)
            if align is None:
                self.f.write(r'\begin{figure}[h!]'+'\n')
                self.f.write(r'\includegraphics[width=\linewidth]{' + absolute_path + figure_name + '}'+'\n')
                self.f.write(r'\end{figure}'+'\n')  
            elif 'right' in align:
                self.f.write(r'\hspace{-0.45cm}')
                self.f.write(r'\begin{wrapfigure}{r}{4cm}'+'\n')
                self.f.write(r'\includegraphics[width=4cm]{' + absolute_path + figure_name + '}'+'\n')
                self.f.write(r'\end{wrapfigure}'+'\n')

        elif "figurelegend" in block_type:
            for line in filtered_block:
                line = replace_special_character(line, '#', r'$\#$')
                line = replace_special_character(line, '*->*', r'$\rightarrow$')
                line = fix_link(self.RST, line)
                line = fix_math(line)
                line = fix_italic(line, replace_underscore=True)    
                self.f.write('[legend-to-add]' + line)
                self.f.write('\n')
        self.f.write('\n')

    def write_title(self, filtered_block, block_type):
        if ("subtitle" in block_type):
            if self.nonumber is False:
                self.f.write('\section{' + filtered_block + '}')
            else:
                self.f.write('\section*{' + filtered_block + '}')
            self.f.write('\n')
        elif ("subsubtitle" in block_type):
            if self.nonumber is False:
                self.f.write('\subsection{' + filtered_block + '}')
            else:
                self.f.write('\subsection*{' + filtered_block + '}')
            self.f.write('\n')

    def write_equation(self, filtered_block, block_type):

        if ("lammps" in block_type):
            self.f.write(r'\begin{lcverbatim}'+'\n')
            for line in filtered_block:
                if ':caption:' not in line:
                    if len(line) >= 76:
                        print(line)
                    assert len(line) < 76, """WARNING: line too long"""
                    self.f.write(line)
                    self.f.write('\n')
            self.f.write(r'\end{lcverbatim}'+'\n')
        elif ("bw" in block_type) | ("bash" in block_type) | ("python" in block_type):
            self.f.write(r'\begin{lcverbatim}'+'\n')
            for line in filtered_block:
                if ':caption:' not in line:
                    self.f.write(line)
                    self.f.write('\n')
            self.f.write(r'\end{lcverbatim}'+'\n')
        elif ("math" in block_type):
            for line in filtered_block:
                line = replace_special_character(line, 'Å', r'$\text{\AA{}}$')
                if len(line) > 0:
                    self.f.write('$$' + line + '$$')
        self.f.write('\n')