import csv
import os

### this step take the Tiaki collection listing, and a list of the files 
### in the corresponding rosetta export, and generates a master reference 
### list for the next step.


### this is output of Tiaki for a given set. 
### it expects 4 bits of data er row:
### tiaki_ref, detail, IE, atl_cms_ref
### as discussed below, its tolerant of more than one IE per line. 
atl = r"Cartes de visite set 2 Term.csv"

### this is the product of running the script over the exported IEs
### https://github.com/jayGattusoNLNZ/code_snippets/blob/master/basic_rosetta_export_member_lister.py 
rosetta = r"files_in_tar.txt"

IE_lookup = {}
with open(rosetta) as data:
	lines = data.read().split('\n')
	for line in lines:
		IE_path, f = line.split('|')
		root, collection, IE, rep, __ = IE_path.split("\\")
		if "/" in f:
			__, f = f.rsplit('/')
		if IE not in IE_lookup:
			IE_lookup[IE] = []
		IE_lookup[IE].append(f)

atl_lookup = {}
IEs = []
with open(atl) as data:
	atl_reader = csv.reader(data)
	next(atl_reader)
	for row in atl_reader:
		tiaki_ref, detail, IE, atl_cms_ref = row
		
		### this step deals with more than one IE in the ref line - might be an error in the export from tiaki, might not
		### does no harm anyway so leaving here.. 
		if "\n" in IE:
			if not IE.endswith("\n"):
				IE = IE+"\n"
			while '\n' in IE:
				IEa, IE = IE.split('\n', 1)
				atl_lookup[IEa] = [tiaki_ref, detail, IEa, atl_cms_ref]
		else:
			atl_lookup[IE] = [tiaki_ref, detail, IE, atl_cms_ref]

with open("merged_ref.txt", "w") as data:
	data.write("tiaki_ref|detail|IE|atl_cms_ref|filename\n")
for ie in atl_lookup:
	for f in  IE_lookup[ie]:
		tiaki_ref, detail, IE, atl_cms_ref = atl_lookup[ie]
		with open("merged_ref.txt", "a") as data:
			data.write("{}|{}|{}|{}|{}\n".format(tiaki_ref, detail, IE, atl_cms_ref, f))


