import unittest
from unittest.mock import patch
from YIRONG_16S import get_sample_names, trunc_sequences, trim_sequences,filter_sequences, dict_to_dataframe
import pandas as pd
import os
import pytest


### test_1 (2. Extracted samples names)
@pytest.mark.parametrize("input_filenames,expected_sample_names", [
    ([
        "a_09-27-1_01_00_R1_001.fastq.gz",
        "a_09-27-1_01_00_R2_001.fastq.gz",
        "a_09-27-1_02_00_R1_001.fastq.gz",
        "a_09-27-1_02_00_R2_001.fastq.gz"
    ],
    [
        "a_09-27-1_01_00",
        "a_09-27-1_02_00"
    ])
])
def test_get_sample_names(tmpdir, input_filenames, expected_sample_names):
    # Create mock files in a temporary directory
    for filename in input_filenames:
        tmpdir.join(filename).write('')
    # Run the function with the temporary directory as the input
    _, _, sample_names = get_sample_names(str(tmpdir))
    # Check if the returned sample names match the expected list
    assert sorted(sample_names) == sorted(expected_sample_names), "Sample names did not match expected values."



### test_2 (4. truncate sequences)
def test_trunc_sequences():
    # generate example sequences
    seq1 = "ATCG" * 40  # length 160 sequence
    seq2 = "GCTA" * 30  # length 120 sequence
    seq3 = "TTAA" * 50  # length 200 sequence
    # build the input dictionary
    input_dict = {"Seq1": [seq1], "Seq2": [seq2], "Seq3": [seq3]}
    # expected truncated sequences
    expected_seq1 = "ATCG" * 30  # expected length 120 sequence
    expected_seq2 = "GCTA" * 30  # expected length 120 sequence
    expected_seq3 = "TTAA" * 30  # expected length 120 sequence
    # call the function
    trimmed_sequences_dict = trunc_sequences(input_dict, trim_position=120)
    # assert to check if the results match the expected values
    assert trimmed_sequences_dict["Seq1"][0] == expected_seq1
    assert trimmed_sequences_dict["Seq2"][0] == expected_seq2
    assert trimmed_sequences_dict["Seq3"][0] == expected_seq3
    print("Test passed!")



### test_3 (5. Trim sequences)
def test_trim_sequences():
    # define test data
    test_input_dict = {
        'seq1': ['CATTTGCTCCCCTAGCTTTCGTCTCTCAGTGTCAGTTTCGGCCCAGTAAAGTGCTTTCGCCATCGGTGTTCTTTCCAATATCTACGCATTTCACCGCTCCACTGGAAATT'],
        'seq2': ['CAGTTTGCTACCCTAGCTTTCGTCTCTGAGTGTTAGTAATAGCCCAGTAAAGTGCTTTCGCCATCGGTGTTCTTTCCAATATCTACGCATTTCACCGCTCCACTGGAAAT'],
    }
    expected_output_dict = {
        'seq1': ['GTCTCTCAGTGTCAGTTTCGGCCCAGTAAAGTGCTTTCGCCATCGGTGTTCTTTCCAATATCTACGCATT'],
        'seq2': ['CGTCTCTGAGTGTTAGTAATAGCCCAGTAAAGTGCTTTCGCCATCGGTGTTCTTTCCAATATCTACGCAT'],
    }
    # call the function to get the actual output
    actual_output_dict = trim_sequences(test_input_dict)
    # print the actual and expected output
    print("Actual Output:")
    print(actual_output_dict)
    print("Expected Output:")
    print(expected_output_dict)
    # assert to check if the actual output matches the expected output
    assert actual_output_dict == expected_output_dict, "Output dictionary does not match expected dictionary"


### test_4 (6. Delete the short sequences)
def test_filter_sequences():
    # generate a dictionary containing 3 sequences
    seq_dict = {
        'seq1': ['ATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCG',
                 'ATCGTGACTAGCCAATTTACGGAC'],
        'seq2': ['ATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCG',
                 'ATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCG'],
        'seq3': ['ATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCG']
    }
    # run the function for testing
    filtered_dict = filter_sequences(seq_dict, min_length=100)
    # check if the resulting match the expected values
    assert len(filtered_dict['seq1']) == 1
    assert len(filtered_dict['seq2']) == 2
    assert len(filtered_dict['seq3']) == 1



### test_5 (7. Convert dictionary to DataFram with sequences counts)
def test_dict_to_dataframe():
    # test data
    data_dict = {
        'Sample1': ['ATCG', 'ATCG', 'GCTA', 'GCTA', 'ATCG'],
        'Sample2': ['ATCG', 'ATCG', 'GCTA', 'GCTA', 'GCTA']
    }
    # expected output
    expected_df = {
        'Sample1': {'ATCG': 3, 'GCTA': 2},
        'Sample2': {'ATCG': 2, 'GCTA': 3}
    }
    # call the function
    df = dict_to_dataframe(data_dict)
    # check i fit matches the expeted output
    for sample, counts in expected_df.items():
        assert df[sample].to_dict() == counts
