import numpy as np

file_name = "dump.lammpstrj"
position_type = 1 # column where the atom type is printed
position_charge = 2 # column where charge is printed

charge_vs_frame_Si = []
charge_vs_frame_O = []
charge_vs_frame_H = []

cpt_frame = 0
with open(file_name) as f:
    for line in f:
        if "TIMESTEP" in line:
            cpt_frame += 1
        try:
            type = np.int32(line.split(" ")[position_type])
            charge = np.float32(line.split(" ")[position_charge])
            if type == 1:
                charge_vs_frame_Si.append([cpt_frame, charge])
            elif type == 2:
                charge_vs_frame_O.append([cpt_frame, charge])
            elif type == 3:
                charge_vs_frame_H.append([cpt_frame, charge])
        except:
            pass