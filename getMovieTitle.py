
import csv
import re
from datetime import datetime
import pprint


file_name = 'raw_data_UCpoPaQt8v-_72nDqUbtVO1g.csv'
#file_name = 'raw_data_UCHBqTYEwBSR1h6zGmHdue7g.csv'
#file_name = 'raw_data_UCHuEAf_vytSUkliGEyLlQPg.csv'

m = re.search("raw_data_",file_name)
end_index = m.end()
prefix = file_name[end_index:-4]

data = []

with open(file_name, encoding='utf8', newline='') as f:
    csvreader = csv.reader(f)
    for row in csvreader:
        data.append(row)

def getTitleByManualRule(q,id):
    movie_list = []
    res_iter = re.finditer(':',q)
    for res in res_iter:       
       start_index = res.start()
       # URLの除外
       if q[start_index+1:res.start()+3] != "//":
            end_index = q[res.start():].find('""') + start_index
            if end_index-start_index > 0:
                movie_title = q[start_index+3:end_index]
                movie_title = movie_title.replace('『','')
                movie_title = movie_title.replace('』','')
                movie_title = movie_title.replace(' ','')
                movie_list.append(movie_title)
                movie_list.append(id)
    return movie_list

def getTitleByManualRuleFromTitle(q,id,key):
    movie_list = []
    
    if key == "『":
        start_key = "『"
        end_key = "』"
    elif key == "「":
        start_key = "「"
        end_key = "」"        
    else:
        print("Key is not defined")

    res_iter = re.finditer(start_key,q)
    for res in res_iter:       
        start_index = res.start()
        end_index = q[res.start():].find(end_key) + start_index
        if end_index-start_index > 0:
            movie_title = q[start_index+1:end_index]
            movie_list.append(movie_title)
            movie_list.append(id)
    return movie_list


data_size = len(data)
movie_list = []

print("Data size : " + str(data_size))

for i in range(data_size):
    
    tmp_videoId = data[i][6]

    if prefix == 'UCpoPaQt8v-_72nDqUbtVO1g':
        tmp_str = data[i][2]
        movie_list.extend(getTitleByManualRule(tmp_str,tmp_videoId))    
    elif prefix == 'UCHBqTYEwBSR1h6zGmHdue7g':
        tmp_str = data[i][1]
        movie_list.extend(getTitleByManualRuleFromTitle(tmp_str,tmp_videoId,"『"))
    elif prefix == 'UCHuEAf_vytSUkliGEyLlQPg':
        tmp_str = data[i][1]
        movie_list.extend(getTitleByManualRuleFromTitle(tmp_str,tmp_videoId,"「"))


    '''
    res_iter = re.finditer(':',tmp_str)
    for res in res_iter:       
       start_index = res.start()
       # URLの除外
       if tmp_str[start_index+1:res.start()+3] != "//":
            end_index = tmp_str[res.start():].find('""') + start_index
            if end_index-start_index > 0:
                movie_list.append(tmp_str[start_index+3:end_index])
                movie_list.append(tmp_videoId)
    '''

#print('n'.join(movie_list))
pprint.pprint(movie_list)


output_file_name = "movie_list_" + prefix + ".csv"

with open(output_file_name, 'w', newline='',encoding='utf_8_sig') as f:
    writer = csv.writer(f)
    writer.writerow(["title", "id"])
    #print(len(movie_list))
    for i in range(int(len(movie_list)/2)):
        #print(movie_list[i*2])
        print(movie_list[i*2+1])
        writer.writerow([movie_list[i*2], movie_list[i*2+1]])