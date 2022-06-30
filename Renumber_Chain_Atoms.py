import os
import re


def get_lines(file_name):
    file = open(file_name, "r")
    raw_lines = file.readlines()
    lines = []
    for i in raw_lines:
        i = i.rstrip("\n")
        lines.append(i)
    return lines


def renumber():
	pdb_name = "npt_2.pdb"
	pdb_lines = get_lines(pdb_name)

	new_file_name = pdb_name[:-4] + "_Chains_Renumbered.pdb"
	new_file = open(new_file_name, "w")

	res_flag = False
	chain_res_nums = []
	chain_res_combs = []
	pattern_res_info = re.compile(r'^ATOM\s+\S+\s+\S+\s+\S+\s+(\S+)\s+(\S+)') 
	# ATOM   200   NE2 GLN A 153      31.290  46.090  55.550  1.00  0.00           N
	# ATOM   201   HE2 GLN A 153      31.330  46.190  55.250  1.00  0.00           H
	# ATOM   4383  NE2 GLN B 153      31.290  46.090  55.550  1.00  0.00           N
	# When it encouters the first atom of residue A_153 it appends 153 to the list of numbers and A_153 to the list of combinations.
	# This first encounter is identified by not having A_153 in the list of combinations already.
	# When it encouters the second atom of the same amino acid then the A_153 is already present in the combinations list.
	# Therefore, no change to the residue number should be made.
	# When it encounters the same amino acid for the B chain, the number is already present in the list of numbers but the combination is not present in the list
	# of combinations.
	# In this case the number should be changed to one above the maximum number (which is the last one appended in the list of numbers).
	# Now this change must be made for every atom of the new residue. So, a flag is reaised to True until a new amino acid is found, because the new number
	# will be appended to hte list of numbers thus it would not allow otherwise the change to be made for the rest atoms of the residue.
	for line in pdb_lines:
		result_res_info = pattern_res_info.search(line)
		if result_res_info:
			chain_id = result_res_info.group(1)
			res_num = result_res_info.group(2)
			res_comb = chain_id + "_" + res_num
			res_num = int(res_num)
			if res_comb not in chain_res_combs:
				chain_res_combs.append(res_comb)
				res_flag = False
				if res_num in chain_res_nums:
					new_num = chain_res_nums[-1] + 1
					line_splited = re.split(r'(\s+)', line)
					line_splited[10] = str(new_num)
					# The number of whitespaces before the new residue number is determined by the number of whitespaces of the maximum residue number by the previous num.
					whitespace_str = wh_counter * " "
					line_splited[9] = whitespace_str
					# Join the splited line
					line = "".join(line_splited)
					chain_res_nums.append(new_num)
					res_flag = True
				else:
					# Determine the number of whitespaces to be used by the new res numbers.
					line_splited = re.split(r'(\s+)', line)
					wh_counter = len(line_splited[9])
					chain_res_nums.append(res_num)
			elif res_flag:
				new_num = chain_res_nums[-1]
				line_splited = re.split(r'(\s+)', line)
				line_splited[10] = str(new_num)
				# The number of whitespaces before the new residue number is determined by the number of whitespaces of the maximum residue number by the previous chain.
				whitespace_str = wh_counter * " "
				line_splited[9] = whitespace_str
				# Join the splited line
				line = "".join(line_splited)
		new_file.write(line + "\n")
	new_file.close()


if __name__ == "__main__":
	renumber()
