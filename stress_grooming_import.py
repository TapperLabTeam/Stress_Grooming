import sys
import pickle
import pandas as pd
sys.path.append(sys.argv[3])
from signal_udfs import plot_average_signals
from signal_udfs import plot_all_signals

input_handle = sys.argv[1]
output_handle = sys.argv[2]

#Create dict for imported raw data
names1 = ['Time','DF/F0','Start Groom','End Groom']
import_dict = {name:[] for name in names1}

#Import raw data from .csv file
for line_num, line in enumerate(open(input_handle)):
	if line_num != 0:
		line = line.strip().split(',')
		for num_num, num in enumerate(line):
			if num != '':
				if num_num == 0:
					import_dict['Time'].append(float(num))
				if num_num == 1:
					import_dict['DF/F0'].append(float(num))
				if num_num == 2:
					import_dict['Start Groom'].append(float(num))
				if num_num == 3:
					import_dict['End Groom'].append(float(num))
					
#Create blank lists for extracting events					
base_time = [[] for x in range(len(import_dict['Start Groom']))]
base_trace = [[] for x in range(len(import_dict['Start Groom']))]
event_time = [[] for x in range(len(import_dict['Start Groom']))]
event_trace = [[] for x in range(len(import_dict['Start Groom']))]
full_time = [[] for x in range(len(import_dict['Start Groom']))]
full_trace = [[] for x in range(len(import_dict['Start Groom']))]

#Extract evens from raw data dict
for stamp_num, stamp in enumerate(import_dict['Start Groom']):
	for num_num, num in enumerate(import_dict['Time']):
		if num >= stamp - 5 and num < stamp:
			base_time[stamp_num].append(num)
			base_trace[stamp_num].append(import_dict['DF/F0'][num_num])
			full_time[stamp_num].append(num)
			full_trace[stamp_num].append(import_dict['DF/F0'][num_num])
		if num >= stamp and num <= import_dict['End Groom'][stamp_num]:
			event_time[stamp_num].append(num)
			event_trace[stamp_num].append(import_dict['DF/F0'][num_num])
			full_time[stamp_num].append(num)
			full_trace[stamp_num].append(import_dict['DF/F0'][num_num])


#Create blank lists for normalizing times			
base_time_norm = [[] for x in range(len(import_dict['Start Groom']))]
event_time_norm = [[] for x in range(len(import_dict['Start Groom']))]
term_time_norm = [[] for x in range(len(import_dict['Start Groom']))]
full_time_norm = [[] for x in range(len(import_dict['Start Groom']))]
			
#Normalize times
for time_num, time in enumerate(event_time):
	zero_time = event_time[time_num][0]
	for times in base_time[time_num]:
		base_time_norm[time_num].append(times - zero_time)
		full_time_norm[time_num].append(times - zero_time)
	for times in event_time[time_num]:
		event_time_norm[time_num].append(times - zero_time)
		full_time_norm[time_num].append(times - zero_time)

	
#Calculate baseline mean and STD for calculating Zscores
df = pd.DataFrame(base_trace)
df = df.T
base_means = df.mean(axis = 0, skipna = True)
base_stds = df.std(axis = 0, skipna = True)

#Create blank lists for trace zscores
base_trace_z = [[] for x in range(len(import_dict['Start Groom']))]
event_trace_z = [[] for x in range(len(import_dict['Start Groom']))]
full_trace_z = [[] for x in range(len(import_dict['Start Groom']))]

#Calculate Zscores
for num_num, num in enumerate(base_means):
	for point in base_trace[num_num]:
		base_trace_z[num_num].append((point - base_means[num_num])/base_stds[num_num])
	for point in event_trace[num_num]:
		event_trace_z[num_num].append((point - base_means[num_num])/base_stds[num_num])
	for point in full_trace[num_num]:
		full_trace_z[num_num].append((point - base_means[num_num])/base_stds[num_num])
		
#Find longest time for plotting
longest_time = []
prev_len = 0

for x in full_time_norm:
	z = len(x)
	if z > prev_len:
		longest_time = x
	prev_len = z

#Plot signals	
plot_average_signals(longest_time, full_trace_z, 'Time (s)', 'DF/F0 Zscore', output_handle[:-4] + '_avg_signals_1')
plot_all_signals(full_time_norm, full_trace_z, 'Time (s)', 'DF/F0 Zscore', output_handle[:-4] + '_all_signals_1')

#Pickle dict of trace data
event_dict = {}
event_dict['Base Time'] = base_time_norm
event_dict['Base Trace'] = base_trace_z
event_dict['Event Time'] = event_time_norm
event_dict['Event Trace'] = event_trace_z
event_dict['Full Time'] = full_time_norm
event_dict['Full Trace'] = full_trace_z

pickle.dump(event_dict,open('event_dict.pkl','wb'))
