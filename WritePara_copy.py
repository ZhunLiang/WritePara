from optparse import OptionParser
import re
import sys
import numpy as np

parser = OptionParser()
parser.add_option("-i",dest = "input_gro", default = "start.gro", help = "gro file")
parser.add_option("-p",dest = "input_top", default = "topol.top", help = "top file")
parser.add_option("-w",dest = "write_mol", default = "-1 1 1", help = "which type molecular in MSD file you want to write in para file")
parser.add_option("-l",dest = "z_low", default = 0,type="float", help = "z low accordinate")
parser.add_option("-u",dest = "z_hight", default = 20,type="float", help = "z up accordinate")
parser.add_option("-n",dest = "bin_num", default = 1000,type="int", help = "bin number")

(options, args) = parser.parse_args()

input_gro = options.input_gro
input_top = options.input_top
write_mol = options.write_mol
z_low = options.z_low
z_hight = options.z_hight
bin_num = options.bin_num

is_write = np.array([int(float(write_mol.split("_")[i])) for i in range(len(write_mol.split("_")))])
is_write = is_write>0

Mol_Num = len(is_write)
#-----------------Get MSD of each molecular------------------#
try:
    MSD_file = open("MSD_charge_para.dat",'r')
except:
    print("NOTE: Parameter file cannot be loaded, mission terminated.")
    sys.exit()
MSD_data = MSD_file.read()
match_type = r"^(\w+)\S*\s+(\d+)"
#match_atomM = r"\d+\s+\S*\.?\d+\s+(\S+\.?\d+)$"
match_atomN = r"(\d+)\s+\S*\.?\d+\s+\S+\.?\d+$"
re_match_type = re.compile(match_type, re.M)
re_match_atomN = re.compile(match_atomN, re.M)
#1re_match_atomM = re.compile(match_atomM, re.M)
nType = int(re_match_type.findall(MSD_data)[0][1])
MoleName = []
numAt = np.zeros([nType])
atNCM = np.zeros([nType,100])
atom_index = 0
for i in range(nType):
    numAt[i] = int(re_match_type.findall(MSD_data)[i+1][1])
    MoleName.append(re_match_type.findall(MSD_data)[i+1][0])
    for j in range(int(numAt[i])):
        atNCM[i][j] = float(re_match_atomN.findall(MSD_data)[atom_index])
        if atNCM[i][j] > 0:
            atNCM[i][j] = 1.0
        else:
            atNCM[i][j] = 0.0
        atom_index += 1
MSD_file.close()

#----------------Get each molecular number in topol file --------------#
top_file = open(input_top,'r')
top_line = top_file.read()
write_num = np.zeros(Mol_Num)

for i in range(Mol_Num):
    temp = r"^"+MoleName[i]+"\s+(\d+)"
    re_temp_match = re.compile(temp,re.M)
    write_num[i] = int(re_temp_match.findall(top_line)[0])

top_file.close()

#--------------Get box xyz---------------------#
gro_file = open(input_gro,'r')
gro_lines = gro_file.readlines()
Box = np.zeros([3])
for i in range(3):
    Box[i] = np.ceil(float(gro_lines[-1].split()[i]))
#--------------Write parameter file------------#
total_write = np.sum(is_write)

para_file = open("para_dens_vel.dat",'w')
para_file.write("binz:\t\t" + str(int(bin_num)) + "\n")
para_file.write("Z_1_2:\t\t" + str(int(z_low)) + "  " + str(int(z_hight)) + "\n")
para_file.write("Type_of_molecule:\t" + str(int(total_write)) + "\n")
start = 0
for i in range(Mol_Num):
    if i == 0:
        start = 0
    else:
        start += numAt[i-1]*write_num[i-1]
    if is_write[i] == 1:
        para_file.write("start#:\t\t" + str(int(start)) + "\n")
        para_file.write("#ofmolecule:\t" + str(int(write_num[i])) + "\n")
        para_file.write("#ofatoms_inonemolecule:  " + str(int(numAt[i])) + "\n")
        for j in range(int(numAt[i])):
            temp2 = (j+1)%10
            if temp2 == 1:
                para_file.write(str(int(atNCM[i][j])))
            elif temp2 == 0 and j != numAt[i]-1:
                para_file.write(" " + str(int(atNCM[i][j])) + "\n")
            else:
                para_file.write(" " + str(int(atNCM[i][j])))
        para_file.write("\n")
        para_file.write("out_of_area:    0\n")
        para_file.write("X_area:         -1       " + str(int(Box[0])) + "\n")
        para_file.write("Y_area:         -1       " + str(int(Box[1])) + "\n")

para_file.close()


