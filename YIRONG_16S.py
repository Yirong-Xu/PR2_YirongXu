import os
import pandas as pd
import subprocess
import glob
import re
from Bio import SeqIO
import gzip
import requests



### 1. Download the files
def download_file(url, local_path):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Open the local file in binary write mode and write the contents of the response to it
            with open(local_path, 'wb') as f:
                f.write(response.content)
            print(f"File downloaded successfully to: {local_path}")
            return True
        else:
            print(f"Failed to download file from {url}. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"An error occurred while downloading file from {url}: {str(e)}")
        return False



### 2. Extracted samples names
def get_sample_names(relative_path):
    # Convert relative path to absolute path based on the script's current working directory
    absolute_path = os.path.abspath(relative_path)
    fn_fs = sorted(glob.glob(os.path.join(absolute_path, "*R1_001.fastq.gz")))
    fn_rs = sorted(glob.glob(os.path.join(absolute_path, "*R2_001.fastq.gz")))
    # Compile a regex pattern for extracting sample names
    pattern = re.compile(r"(.+?)_R[12]_001\.fastq\.gz")
    sample_names = []
    for fn in fn_fs:
        basename = os.path.basename(fn)
        match = pattern.match(basename)
        if match:
            sample_names.append(match.group(1))
        else:
            print(f"Filename '{basename}' does not match the expected pattern.")
    return fn_fs, fn_rs, sample_names


### 3. Read sequences in FASTQ files
def read_fastq_files(folder_path):
    # Initialize an empty dictionary to store sequences
    sequences_dict = {}
    # List all files in the folder
    files = os.listdir(folder_path)
    # Iterate over each file in the folder
    for file_name in files:
        # Check if the file is a FASTQ file
        if file_name.endswith('.fastq.gz'):
            # Create an empty list to store sequences from this file
            sequences = []
            # Open the FASTQ file
            with gzip.open(os.path.join(folder_path, file_name), 'rt') as f:
                # Read the lines of the FASTQ file
                lines = f.readlines()
                # Iterate over every 4 lines (header, sequence, "+", quality)
                for i in range(0, len(lines), 4):
                    # Extract the sequence (second line)
                    sequence = lines[i + 1].strip()
                    # Append the sequence to the list of sequences
                    sequences.append(sequence)
            # Add the list of sequences to the dictionary
            sequences_dict[file_name] = sequences
    return sequences_dict


# 4. Truncate sequences 
def trunc_sequences(input_dict, trim_position=150):
    trimmed_sequences_dict = {}
    for key, sequences in input_dict.items():
        trimmed_sequences = [seq[:trim_position] for seq in sequences]
        trimmed_sequences_dict[key] = trimmed_sequences
    return trimmed_sequences_dict


# 5. Trim sequences 
def trim_sequences(input_dict):
    # Initialize an empty dictionary to store updated sequences
    updated_sequences_dict = {}  
    # loop over each base sequence in the sequences
    for seq_name, sequences in input_dict.items():
        updated_sequences = []
        # remove the first 20 and last 20 bases
        for seq in sequences:
            # remove the firat and the last 20 bases
            updated_seq = seq[20:-20]
            # append the updated sequence to the list
            updated_sequences.append(updated_seq)
        # store the list of updates sequences in the updated dictionary
        updated_sequences_dict[seq_name] = updated_sequences    
    return updated_sequences_dict


### 6. Delete the short sequences
def filter_sequences(seq_dict, min_length=100):
    filtered_dict = {}
    for key, sequences in seq_dict.items():
        filtered_sequences = [seq for seq in sequences if len(seq) >= min_length]
        filtered_dict[key] = filtered_sequences
    return filtered_dict
import pandas as pd


### 7. Convert dictionary to DataFram with sequences counts
def dict_to_dataframe(data_dict):
    # initialize an empty dataframe
    df = pd.DataFrame()
    # loop over the key-value pairs in the dictionary
    for sample, sequences in data_dict.items():
        # add sequences and counts for each sample to the dataframe
        df[sample] = pd.Series(sequences)
    # calculate the counts of each sequence for each sample using value_counts() function and convert to dataframe
    df = df.apply(pd.Series.value_counts) 
    # fill NaN values with 0
    df = df.fillna(0)
    return df


### 8. Replace column names of DataFrame
def replace_column_names(df, new_column_names):
    sample_names = new_column_names[2]
   # sample_names.insert(0, 'Sequence')
    df.columns = sample_names
    return df
    

### 9. Save DataFrame to Excel file
def save_dataframe_to_excel(df):
    df.to_excel('output.xlsx', index=True)





