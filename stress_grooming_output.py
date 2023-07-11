import sys
import pickle
sys.path.append(sys.argv[1])
from signal_udfs import unpickle
import pandas as pd

#IMPORT BLOCK
output_handle = sys.argv[2]

unpickle = unpickle(sys.argv[3:])
event_dict = unpickle[0]
calc_dict = unpickle[1]

#EXPORT TRACES

#Find longest times
base_longest = []
event_longest = []
full_longest = []

prev_len = 0

for event in event_dict['Base Time']:
	x = len(event)
	if x > prev_len:
		base_longest = event
		prev_len = x
		base_time_df = pd.DataFrame(base_longest)
		base_time_df.columns = ['Baseline Time (s)']
prev_len = 0		
for event in event_dict['Event Time']:
	x = len(event)
	if x > prev_len:
		base_longest = event
		prev_len = x
		event_time_df = pd.DataFrame(base_longest)
		event_time_df.columns = ['Event Time (s)']	
prev_len = 0
for event in event_dict['Full Time']:
	x = len(event)
	if x > prev_len:
		base_longest = event
		prev_len = x
		full_time_df = pd.DataFrame(base_longest)
		full_time_df.columns = ['Full Time (s)']

#Create names for event output columns		
base_names = ['Baseline ' + str(x + 1) for x in range(len(event_dict['Base Time']))]
event_names = ['Event ' + str(x + 1) for x in range(len(event_dict['Event Time']))]
full_names = ['Full Trace ' + str(x + 1) for x in range(len(event_dict['Full Time']))]

#Prepare dfs of traces
base_trace_df = pd.DataFrame(event_dict['Base Trace'])
base_trace_df = base_trace_df.T
base_trace_df.columns = base_names

event_trace_df = pd.DataFrame(event_dict['Event Trace'])
event_trace_df = event_trace_df.T
event_trace_df.columns = event_names

full_trace_df = pd.DataFrame(event_dict['Full Trace'])
full_trace_df = full_trace_df.T
full_trace_df.columns = full_names

event_output_df = pd.concat([base_time_df, base_trace_df, event_time_df, event_trace_df, full_time_df, full_trace_df], axis = 1)
event_output_df.to_csv(output_handle[:-4] + '_main_trace_output.csv', index = False)

#EXPORT CALCS
calc_output_df = pd.DataFrame.from_dict(calc_dict)
calc_output_df.to_csv(output_handle[:-4] + '_main_calc_output.csv', index = False)
