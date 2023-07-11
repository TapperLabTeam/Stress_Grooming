# Stress_Grooming
Extracts traces from photometry data and calculates zscores based on timestamps from time locked behavior videos.

Instructions:
1. Create the folders "input_folder" and "output_folder."
2. Change the input and output folder directories in "stress_grooming_wrap.py" to match your directories.
3. Copy .csv files of photometry and behavior data to the input_folder.
4. .csv files should be organized thusly: column 1 = photometry data timestamps (seconds), column 2 = photometry DF/F0 trace, column 3 = behavior start times (seconds), column 4 = behavior end times (seconds).
5. Run "stress_grooming_wrap.py" to execute program.
