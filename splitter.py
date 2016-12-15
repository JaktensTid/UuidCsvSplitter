import csv
import os
from itertools import groupby

def write_csv(name, headers, rows):
	with open(name + '.csv', 'w', newline='') as outfile:
		writer = csv.writer(outfile)
		if headers:
			writer.writerow(headers)
		writer.writerows(rows)

#SMS Value = False
def process_first_cond(tags, input_rows):
	for tag in tags:
		output_rows = []
		for row in input_rows:
			if row[3] in tag and row[2] == 'TRUE':
				output_rows.append([row[0]])
		write_csv(tag + '_SMS', ['user_uuid'], output_rows)

#Level grouping
def process_second_cond(tags, input_rows):
	for tag in tags:
		output_rows = {}
		for level, group in groupby(input_rows, lambda row: row[1]):
			for row in group:
				if row[3] in tag:
					if level not in output_rows:
						output_rows[level] = [[row[0]]]
					else:
						output_rows[level].append([row[0]])
		for level in output_rows.keys():
			write_csv(tag + '--l' + str(level), [], output_rows[level])

#SMS Value = True
def process_third_cond(tags, input_rows):



def process_one_tag(csv_path, input_rows, tag, output_name_1, output_name_2, output_name_3, headers1=['user_uuid'], headers2=['tools_uuid'], headers3=[]):
	"""
	Main function
	param csv_path: path to input .csv file (without extension)
	param tag: tag
	param name: output .csv name
	headers: output headers
	"""
	#Result rows of 1,2,3 outputs

	
	rows2 = []
	rows3 = {}
	
	
		if row[3] in tag and row[2] == 'FALSE':
			rows2.append([row[0]])

	

	
	write_csv(output_name_2, headers2, rows2)
	
	

#This is the enter function
def split_csv(csv_path, tags, output_names_1=[],
			output_names_2=[], output_names_3=[]):
	for i, tag in enumerate(tags):
		process_one_tag(csv_path, tag, output_names_1[i], output_names_2[i], output_names_3[i])

def main():
	input_rows = []

	with open(csv_path, newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    	#Slice headers of input file
		input_rows = [row for row in reader][1:]

	#Detect all unique tags
	unique_tags = list(set([row[3] for row in input_rows]))

	print('Detected unique tags:')

	for tag in unique_tags:
		print(tag)

	print('Here are the unique tags I have found from your sheet, is this correct? (y/n)')
	
	while True:
		answer = input()
		if answer.lower() == 'n':
			return
		if answer.lower() == 'y':
			break
		print('Please, enter y or n')






if __name__ == "__main__":
	split_csv('2016_12_12.csv',tags=['2016-12-12_nonweekender_nonweekday_AM'],
	 output_names_1=['2016_12_12_wewd_SMS','res1_2'], output_names_2=['2016_12_12_wewd_DE','res2_2'], output_names_3=['2016_12_12-wewd','res3_2'])