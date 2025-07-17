# Python Script
# Licensed under CC BY 4.0
# By Simon Gravelle, Jacob R. Gissinger, and Axel Kohlmeyer
# Please cite doi.org/10.48550/arXiv.2503.14020
# Find more on GitHub: https://github.com/lammpstutorials

import os

FILE_TYPES = {
    ".lmp":     "LAMMPS Input File",
    ".py":      "Python Script",
    ".inc":     "LAMMPS Include File",
    ".mol":     "LAMMPS Molecule File",
    ".rxnmap":  "LAMMPS Reaction Map File",
}

HEADER_BODY = [
    "# Licensed under CC BY 4.0\n",
    "# By Simon Gravelle, Jacob R. Gissinger, and Axel Kohlmeyer\n",
    "# Please cite doi.org/10.48550/arXiv.2503.14020\n",
    "# Find more on GitHub: https://github.com/lammpstutorials\n",
]

def build_headers():
    headers = {}
    for ext, title in FILE_TYPES.items():
        headers[ext] = [f"# {title}\n"] + HEADER_BODY
    return headers

HEADERS = build_headers()

def find_files(root, extensions):
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            for ext in extensions:
                if filename.endswith(ext):
                    yield os.path.join(dirpath, filename), ext

def process_file(filepath, ext):
    desired_header = HEADERS[ext]
    with open(filepath, 'r') as f:
        lines = f.readlines()

    # Detect existing header as a line with "#" at the top
    header_end = 0
    for line in lines:
        if line.startswith("#"):
            header_end += 1
        else:
            break
    current_header = lines[:header_end]

    # If already correct, do nothing
    if current_header == desired_header:
        return

    # Otherwise, replace the detected header
    with open(filepath, 'w') as f:
        f.writelines(desired_header + lines[header_end:])
    print(f"[FIXED HEADER] {filepath}")

if __name__ == "__main__":
    root_dir = os.getcwd()  # All file within this folder
    for filepath, ext in find_files(root_dir, HEADERS.keys()):
        process_file(filepath, ext)
