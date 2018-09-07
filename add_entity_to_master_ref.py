terms_to_clean = ["Photograph of ", "Carte de visite portrait of ", "Portraits of ", "Portrait of ",  "[", "]"]

with open("merged_ref_with_names.txt", "w") as data:
	data.write("tiaki_ref|detail|IE|atl_cms_ref|fname|entity\n")

with open("merged_ref.txt") as data:
	rows = data.read().split("\n")
	for row in rows[1:-1]:
		tiaki_ref, detail, IE, atl_cms_ref, fname = row.split("|")
		
		### tries to split out image maker from image subject based on observed patterns
		### defaults to whole item being the entity anyway. 
		if ":" in detail:
			__, entity = detail.split(':', 1)
		elif ";" in detail:
			__, entity = detail.split(';', 1)
		elif "- Photograph taken by " in detail:
			entity, __ = detail.split('- Photograph taken by ', 1)
		elif "- Photographed by " in detail:
			entity, __ = detail.split('- Photographed by ', 1)
		else:
			entity = detail[:]

		### tries to move off the contextual descriptors from the newly minted entity
		for term in terms_to_clean:
			entity = entity.replace(term, "")

		### removes leading and trailing whitespaces, and hiding newlines
		entity = entity.replace("\n", "").strip()

		with open("merged_ref_with_names.txt", "a") as data:
			data.write("{}|{}|{}|{}|{}|{}\n".format(tiaki_ref, detail, IE, atl_cms_ref, fname, entity))
