# -*- coding: utf-8 -*-
"""
@title: HW 1 - Late Submission
Created on Fri Nov  3 11:44:30 2017

@author: Connor Smith
"""

import csv
import pandas
import re
# import file
vcf_file = open("PTEN.vcf","r")

vcf_lines = vcf_file.readlines()
#strip lines
vcf_clean = [line.rstrip() for line in vcf_lines]

vcf_file.close()

#create dictionary for data dict

data_dict = {}

# check for ##INFO lines
for line in vcf_clean:
    match = re.search(r"##INFO",line)
    if match:
        attribs = re.search(r"<(.*)>",line).group(1).split(',')
        info_id = attribs[0][3:]
        info_def = attribs[3][12:].replace('"','')
        info_type = attribs[2][5:]
        # range to be added later
        info_range = ''
        data_dict[info_id] = [info_def,info_type,info_range]
print(data_dict)

# ignore the specific mutation columns
data_raw = [line.split('\t') for line in vcf_clean[252:]]
list_of_dict = []
for row in data_raw[1:]:
    # extract info variables
    info = row[7]
    info_dict = {}
    for item in info.split(';'):
        match = re.search(r"=",item)
        if match:
            info_dict[item.split("=")[0]] = item.split("=")[1]
        else:
            # deals with FLAG columns
            info_dict[item] = 1
    #info_split = {item.split('=')[0]: item.split('=')[1] for item in info.split(";") if item.split('=')[0] != 'EX_TARGET'}
    row_dict = {'#CHROM':row[0],
               'POS':row[1],
               'ID':row[2],
               'REF':row[3],
               'ALT':row[4],
               'QUAL':row[5],
               'FILTER':row[6],
               'INFO':row[7],
               'FORMAT':row[8]}
    row_dict.update(info_dict)
    list_of_dict.append(row_dict)
PTEN_data = pandas.DataFrame(list_of_dict)

print('Number of SNPs: '+str(len(PTEN_data.loc[PTEN_data['VT'].str.contains("SNP")])))

# Set range/unique values for each column
for key, item in data_dict.items():
    if key in PTEN_data.columns:
        item[2] = str(len(PTEN_data[key].unique()))+' unique values'
    else:
        item[2] = 'No Values Found'
        
# Print Dictionary
dict_file = open('data_dictionary_PTEN.txt','w')
dict_file.write('TERM\tDEFINITION\tTYPE\tRANGE\n')
for key,item in data_dict.items():
    dict_file.write(key+'\t'+item[0]+'\t'+item[1]+'\t'+item[2]+'\n')
dict_file.close()

# Subset the columns we care about
PTEN_summary = PTEN_data[['ID','POS','REF','ALT','DP','AA','VT','AC','AF','EAS_AF','EUR_AF','AFR_AF','AMR_AF','SAS_AF']]

# Print to file
PTEN_summary_snp = PTEN_summary[:][PTEN_data['VT'].str.contains("SNP")]
table_file = open('PTEN_informative.csv','w')
PTEN_summary_snp.to_csv(table_file)
table_file.close()