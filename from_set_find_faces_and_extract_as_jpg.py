import face_recognition
import cv2
import os

### uses a rezizing step becuase of a limit on the fr side to handle larger images.
### I've not thought about optimal here -this needs some work
### #todo
### these are changeable here:
max_height = 10000
max_width = 10000
##############################

source_images_folder = r"D:\new- carts\images"
destination_folder_for_face_extracts = r"D:\new- carts\faces"

if not os.path.exists(destination_folder_for_face_extracts):
	os.makedirs(destination_folder_for_face_extracts)

def resize_image(img, max_width, max_height):
	height, width = img.shape[:2]
	# only shrink if img is bigger than required
	if max_height < height or max_width < width:
		# get scaling factor
		scaling_factor = max_height / float(height)
		if max_width/float(width) < scaling_factor:
			scaling_factor = max_width / float(width)
		# resize image
		img = cv2.resize(img, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
	return img

def find_face(my_file_path, max_width, max_height):
	### using the face locator, returns the coords of found faces in an image
	### because if memory issues, this needs to work down to a size it work with... not really ideal needs a check for sanity outside this machine
	### todo
	success = False
	while not success:
		try:	
			my_image = face_recognition.load_image_file(my_file_path)
			my_image = resize_image(my_image, max_width, max_height)
			face_locations = face_recognition.face_locations(my_image)
			success = True

		except:
			max_height = max_height - 1000
			max_width = max_width - 1000

	return my_image, face_locations

def make_sub_image(image, face_location, my_image, face_fname_path):
	### takes gthe image coords and makes a extracted image
	### faces are labelled i as they emerge - these need manually linking to an identity if >1 face in image
	### todo
	height, width, channels = image.shape	
	padding = 0
	top, right, bottom, left = face_location
	crop_img = image[top:bottom, left:right]
	cv2.imwrite(str(face_fname_path), crop_img)

with open("extracted_faces.txt", "w") as data:
	data.write("source_image|face_image\n")
	
for my_image in os.listdir(source_images_folder):
	my_image_path = os.path.join(source_images_folder, my_image)
	print ("Working on {}".format(my_image_path))
	img, faces_in_image = find_face(my_image_path, max_width, max_height)

	for i, face_location in enumerate(faces_in_image):
		my_face_fname = '{}__{}.jpg'.format(my_image, i+1)
		face_fname_path = os.path.join(destination_folder_for_face_extracts, my_face_fname)
		make_sub_image(img, face_location, my_image, face_fname_path )
		with open("extracted_faces.txt", "a") as data:
			data.write("{}|{}\n".format(my_image, my_face_fname))
