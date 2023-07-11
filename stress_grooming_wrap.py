import os
import subprocess

#Extracts traces from photometry data based on event timestamps where baseline is -5s to event onset.
#Calculates zscores based on baselines.
#Imports from .csv file: Col 1 = photometry data timestamps, Col 2 = DF/F0, Col 3 = start times for behavior, Col 4 = end times for behavior

#Set input and output folder pahts
input_folder = 'C:/Users/Tim/Documents/Python/Stress_Grooming/input_folder/'
output_folder = 'C:/Users/Tim/Documents/Python/Stress_Grooming/output_folder/'
udf_path = 'C:/Users/Tim/Documents/Python/UDFs'

#Collect list of file names for processing
input_files = []
for file_name in os.listdir(input_folder):
	input_files.append(file_name)
	
#Main processing loop
for file_name in input_files:
	input_handle = input_folder + file_name
	output_handle = output_folder + file_name
	print('Processing: ' + file_name + '...')
	subprocess.call(['python', 'stress_grooming_import.py', input_handle, output_handle, udf_path])
	subprocess.call(['python', 'stress_grooming_calc.py', udf_path, 'event_dict.pkl'])
	subprocess.call(['python', 'stress_grooming_output.py', udf_path, output_handle, 'event_dict.pkl', 'calc_dict.pkl'])

print('Done')
