import os
import shutil
import tarfile
import pickle

##### edit these two lines only #####
source = r"K:\cartes_de_visites"
destination = r"K:\cartes_de_visites_unpacked"
#####################################

if not os.path.exists(destination):
	os.makedirs(destination)


if not os.path.exists('files_list.pickle'):
	files_list = os.listdir(source)
	pickle.dump(files_list, open('files_list.pickle','wb'))
else:
	files_list = pickle.load(open('files_list.pickle', 'b'))


for item in os.listdir(source):
	item_path = os.path.join(source, item)
	try:
		os.remove(os.path.join(item_path, "ie.xml"))
	except FileNotFoundError:
		pass
	for rep in os.listdir(item_path):
		for my_file in os.listdir(os.path.join(item_path, rep)):
			my_file_path = os.path.join(item_path, rep, my_file)
			new_file_destination = my_file_path.replace(os.path.join(item_path, rep), destination)
			shutil.copy2(my_file_path, new_file_destination)
			tar = tarfile.open(new_file_destination, "r:")
			tar.extractall(destination)
			tar.close()
			os.remove(new_file_destination)
