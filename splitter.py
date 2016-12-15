import csv
import os
import os.path
from itertools import groupby

def write_csv(name, headers, rows):
	with open(name + '.csv', 'a', newline='') as outfile:
		writer = csv.writer(outfile)
		if headers:
			writer.writerow(headers)
		writer.writerows(rows)


#SMS Value = False
def process_first_cond(tags, input_rows):
	for tag in tags:
		output_rows = []
		for row in input_rows:
			if row[3] in tag and row[2] == 'FALSE':
				output_rows.append([row[0]])
		write_csv(tag + '_SMS_FALSE', ['user_uuid'], output_rows)


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
def process_third_cond(tags, input_rows, links):
	#Hardcoded message
	message = 'Come try upwork for free this week. For information, visit: %s'
	rows = []
	for i, tag in enumerate(tags):
		output_rows = []
		for row in input_rows:
			if row[3] in tag and row[2] == 'TRUE':
				output_rows.append([row[0], message % links[i]])
		rows += output_rows
	write_csv('Messages', ['user_uuid', 'message'], rows)


def main():
	try:
		input_rows = []

		print('Enter path to input .csv file')

		csv_path = input()

		if not os.path.isfile(csv_path):
			print('File not exists')
			return

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

		print('Please, enter links for each group, using separator | . Example: link1|link2|link3')
		links = []

		while True:
			answer = input()
			links = answer.split('|')
			if len(links) == len(unique_tags):
				break
			print('Number of tags != number of links. Please, enter links one more time.')

		process_first_cond(unique_tags, input_rows)
		process_second_cond(unique_tags, input_rows)
		process_third_cond(unique_tags, input_rows, links)
	except EOFError:
		return


if __name__ == "__main__":
	main()