import csv
import os
from itertools import groupby

def write_csv(name, headers, rows):
	with open(name + '.csv', 'w', newline='') as outfile:
		writer = csv.writer(outfile)
		if headers:
			writer.writerow(headers)
		writer.writerows(rows)

def process_one_tag(csv_path, tag, output_name_1, output_name_2, output_name_3, headers1=['user_uuid'], headers2=[], headers3=['guest_uuid']):
	"""
	Main function
	param csv_path: path to input .csv file (without extension)
	param tag: tag
	param name: output .csv name
	headers: output headers
	"""
	#Result rows of 1,2,3 outputs

	rows1 = []
	rows2 = []
	rows3 = {}
	input_rows = []

	with open(csv_path, newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    	#Slice headers of input file
		input_rows = [row for row in reader][1:]

	#Filter first and second conditions
	for row in input_rows:
		if row[3] in tag and row[2] == 'TRUE':
			rows1.append([row[0]])
		if row[3] in tag and row[2] == 'FALSE':
			rows2.append(row)

	#Filter third condition
	#Grouping by level and then tag in each group
	for level, group in groupby(input_rows, lambda row: row[1]):
		for row in group:
			if row[3] in tag:
				if level not in rows3:
					rows3[level] = [[row[0]]]
				else:
					rows3[level].append([row[0]])

    #Output .csv files
	write_csv(output_name_1, headers1, rows1)
	write_csv(output_name_2, headers2, rows2)
	
	for level in rows3.keys():
		write_csv(output_name_3 + '_level_' + str(level), headers3, rows3[level])

#This is the enter function
def split_csv(csv_path, tags, output_names_1=[],
			output_names_2=[], output_names_3=[]):
	for i, tag in enumerate(tags):
		process_one_tag(csv_path, tag, output_names_1[i], output_names_2[i], output_names_3[i])

if __name__ == "__main__":
	split_csv('upwork_example.csv',tags=['2016_12_5_chicago','2016_12_5_london'],
	 output_names_1=['res1','res1_2'], output_names_2=['res2','res2_2'], output_names_3=['res3','res3_2'])