import os

faces = r"D:\new- carts\faces"

images_in_folder = os.listdir(faces)

with open("extracted_faces_cleaned.txt", "w") as data:
	data.write("source_image|face_image\n")

with open("extracted_faces.txt") as data:
	faces = data.read().split("\n")

	for face in faces[1:-1]:
		source_image, face_image =face.split("|")
		if face_image in images_in_folder:
			with open("extracted_faces_cleaned.txt", "a") as data:
				data.write("{}|{}\n".format(source_image, face_image))
