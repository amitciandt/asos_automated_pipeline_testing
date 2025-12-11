import pandas as pd
from pathlib import Path
import os
import json
import csv
import glob

search_pattern = os.path.join(os.getcwd(),'/powerbi/models','**/*.json')
all_json_files = glob.glob(search_pattern, recursive=True)
json_data_map = {}

for filename in all_json_files:
     print(filename)
     with open(filename, 'r', encoding='utf-8') as f:
         data = json.load(f)
         key = os.path.splitext(filename)[0]
         json_data_map[key] = data


def check_string_in_json(data, target_string):                                                                                              
     if isinstance(data, dict):                                                                                                              
         for key, value in data.items():
             if check_string_in_json(key, target_string) or check_string_in_json(value, target_string):
                 return True
     elif isinstance(data, list):
         for item in data:
             if check_string_in_json(item, target_string):
                 return True
     elif isinstance(data, str):
         if target_string in data:
             return True
     return False

filtered_dict = {key: value for key, value in json_data_map.items() if check_string_in_json(value,'SourceTable')}
modified_dict = {key.split('/')[8]+','+key.split('/')[-1]: value['extendedProperties'] for key, value in filtered_dict.items()}
updated_dict = {key: value[1]['value']+'.'+value[2]['value']+'.'+value[3]['value'] for key, value in modified_dict.items()}

mylist = []
for key, value in updated_dict.items():
	mylist.append(key + ',' + value)
mylist.insert(0, 'powerbi_semantic_model,semantic_model_table,ade_serve_table')
	
filename = "powerbi_model_map.csv"

newlist = []
for a in mylist:
     newlist.append(a.split(','))

with open(filename, mode='w', newline='', encoding='utf-8') as file:
     writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
     writer.writerow(newlist[0])
     writer.writerows(newlist[1:])