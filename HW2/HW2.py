
# coding: utf-8

# HW 2 - Connor Smith - Late

# First, we need to cleanup the input file. I am using the current build of the csv package to simplify import/export

# In[30]:

import csv
print("CSV Version: "+csv.__version__)
import sys
print("Python/Anaconda Info: "+sys.version)


# In[25]:

# Set up corrected file

# import file
with open("var_list.txt") as in_file:
    file_data = csv.reader(in_file,delimiter='\t')
    # remove empty lists
    file_cleaned = [line for line in file_data if line != []]
    # save to new file with modifications
    with open("var_list_annovar.avinput","w", newline = '') as out_file:
        out_writer = csv.writer(out_file,delimiter="\t")
        for line in file_cleaned:
            # only return chromosome number
            chrom = line[0][3:]
            # start location
            start = line[1]
            # reference allele
            ref = line[2]
            # alternate allele
            alt = line[3]
            # start location + length of reference to get end, required by wANNOVAR
            end = int(start) + len(ref) - 1
            out_writer.writerow([chrom,start,end,ref,alt])
        print("File conversion complete")


# Next, I ran this file through the wANNOVAR program because I have not used PERL an am not sure how. My online submission number was 131582. I downloaded the results, not I want to import them with the annovar format.

# In[33]:

import pandas
print("Pandas Verion: "+pandas.__version__)

# import results file
with open("query.output.genome_summary.txt") as in_results:
    results_data = pandas.read_csv(in_results,delimiter="\t")
    results_filtered = results_data[['Chr',
                                    'Start',
                                    'End',
                                    'Ref',
                                    'Alt',
                                    'Func.refgene',
                                    'Gene.refgene',
                                    'ExonicFunc.refgene',
                                    '1000G_ALL',
                                    '1000G_AFR',
                                    '1000G_AMR',
                                    '1000G_EAS',
                                    '1000G_EUR',
                                    '1000G_SAS',
                                    'ExAC_Freq',
                                    'ExAC_AFR',
                                    'ExAC_AMR',
                                    'ExAC_EAS',
                                    'ExAC_FIN',
                                    'ExAC_NFE',
                                    'ExAC_OTH',
                                    'ExAC_SAS',
                                    'ESP6500si_ALL',
                                    'ESP6500si_AA',
                                    'ESP6500si_EA',
                                    'CG46',
                                    'NCI60',
                                    'dbSNP',
                                    'COSMIC_DIS']]
    with open("results_annotated_hw2.txt","w") as result_out:
        results_filtered.to_csv(result_out,sep="\t")
        print("Annotated results saved as results_annotated_hw2.txt")

# The column ExonicFunc.refgene contains the functional effect of this variant