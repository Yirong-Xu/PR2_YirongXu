import unittest
from unittest.mock import patch
from YIRONG_16S import read_fastq_files, replace_column_names, get_sample_names, trunc_sequences, trim_sequences,filter_sequences, dict_to_dataframe, save_dataframe_to_excel
import os
import pandas as pd
import subprocess
import glob
import re
from Bio import SeqIO
import gzip
import requests

# data
path = './data'

# Extracted samples names
name = get_sample_names(path)

# Read sequences in FASTQ files
RawSequences =  read_fastq_files(path)

# Truncate sequences
Trun_Sequences = trunc_sequences(RawSequences, trim_position = 150)

# Trim sequences
Trim_Sequences = trim_sequences(Trun_Sequences)

# Delete the short sequences
filtered_dict = filter_sequences(Trim_Sequences, min_length=100)

# Convert dictionary to DataFram with sequences counts
df = dict_to_dataframe(filtered_dict)

# Replace column names of DataFrame
df_new_name = replace_column_names(df,name)

# Save DataFrame to Excel file
save_dataframe_to_excel(df_new_name)
