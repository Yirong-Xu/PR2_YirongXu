Function Descriptions

1. Download File (download_file)
Downloads a file from a given URL and saves it to a specified local path. Uses the requests library to make a GET request and save the response content to the local file.

2. Get Sample Names (get_sample_names)
Extracts sample names from FASTQ file names in a specified folder path. Uses regular expressions to parse the sample names from the file names.

3. Read FASTQ Files (read_fastq_files)
Reads sequences from FASTQ files in a specified folder path. Parses the FASTQ files, extracts the sequence lines, and stores them in a dictionary with file names as keys.

4. Truncate Sequences (trunc_sequences)
Truncates sequences in a dictionary of sequences to a specified length. Trims each sequence to the specified length from the beginning.

5. Trim Sequences (trim_sequences)
Trims sequences in a dictionary of sequences by removing a fixed number of bases from the beginning and end of each sequence.

6. Filter Sequences (filter_sequences)
Filters sequences in a dictionary of sequences based on a minimum length threshold. Removes sequences shorter than the specified minimum length.

7. Convert Dictionary to DataFrame (dict_to_dataframe)
Converts a dictionary of sequences into a DataFrame with sequence counts. Counts the occurrences of each sequence in each sample and creates a DataFrame with sequences as rows and sample names as columns.

8. Replace Column Names of DataFrame (replace_column_names)
Replaces the column names of a DataFrame with new names. Takes a list of new column names and assigns them to the DataFrame columns.

9. Save DataFrame to Excel File (save_dataframe_to_excel)
Saves a DataFrame to an Excel file with the specified file name. Uses Pandas' to_excel function to export the DataFrame to an Excel file.



Test Functions README

Test 1: Extracted Sample Names
Verifies the correctness of the function get_sample_names.
Checks if sample names are correctly extracted from FASTQ file names.

Test 2: Truncate Sequences
Verifies the correctness of the function trunc_sequences.
Checks if sequences are truncated to the specified length.

Test 3: Trim Sequences
Verifies the correctness of the function trim_sequences.
Checks if sequences are trimmed by removing bases from the beginning and end.

Test 4: Delete Short Sequences
Verifies the correctness of the function filter_sequences.
Checks if sequences shorter than a specified minimum length are filtered out.

Test 5: Convert Dictionary to DataFrame
Verifies the correctness of the function dict_to_dataframe.
Checks if a dictionary of sequences is correctly converted into a DataFrame with sequence counts.