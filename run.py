from dag_analyzer import catalog_info, determine_path

prompt = "Type a number I guess: "

while(True):

	response = int(raw_input(prompt))

	determine_path(catalog_info[response])