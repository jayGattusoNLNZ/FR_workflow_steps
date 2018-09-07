import os
import shutil
import tarfile

####### #edit this line only ########
source = r"K:\cartes_de_visites"
#####################################

for item in os.listdir(source):
	item_path = os.path.join(source, item)
	try:
		os.remove(os.path.join(item_path, "ie.xml"))
	except FileNotFoundError:
		pass
	for rep in os.listdir(item_path):
		for my_file in os.listdir(os.path.join(item_path, rep)):
			my_file_path = os.path.join(item_path, rep, my_file)
			try:
				tar = tarfile.open(my_file_path, "r:")
				files = tar.getnames()
				for f in files:
					with open("files_in_tar.txt", "a") as data:
						print (my_file_path)
						print (f)
						data.write(("{}|{}\n").format(my_file_path, f))
			except tarfile.ReadError:
				with open("missed_tars_from_membership_count.txt", "a") as data:
					data.write("{}\n".format(my_file_path))
