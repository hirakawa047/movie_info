import glob
import csv
import pprint

file_list = glob.glob('./movie_list_*')

print(file_list)

data = []

for file_name in file_list:
    with open(file_name, encoding='utf8', newline='') as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            data.append(row)

#pprint.pprint(data)
data = (sorted(data))


output_file_name = "all_movie_list.csv"

with open(output_file_name, 'w', newline='',encoding='utf_8_sig') as f:
    writer = csv.writer(f)
    writer.writerow(["title", "id"])
    #print(len(movie_list))
    for row in data:
        row[1] = 'http://www.youtube.com/watch?v=' + row[1]
        #print(row)
        writer.writerow(row)