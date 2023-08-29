def peak_onset(event_trace, event_num, time, invert, file_handle):
	#Find peaks and valleys in signal
	
	#Input Arguments:
	#event_trace = list of signal to analyze
	#event_num = interger of event number for use in saving figure
	#time = list of timestamps for the event_trace
	#invert = boolean of whether to invert trace for analysis
	#file_handle = string of name for output figure labeling
	import numpy as np
	from scipy import signal
	import matplotlib.pyplot as plt
	
	if invert == True:
		event_trace = event_trace * -1
	
	peak_index = signal.argrelextrema(event_trace, np.greater)
	peak_index_x = peak_index[0]
	peak_index = peak_index_x.tolist()#These originally are np.array

	valley_index = signal.argrelextrema(event_trace, np.less)
	valley_index_x = valley_index[0]
	valley_index = valley_index_x.tolist()#These originally are np.array

	#Find value for peak with highest amplitude and valley with lowest amplitude
	peak_amp = 0
	peak_amp_list = []
	
	for index in peak_index:
		for point_num, point in enumerate(event_trace):
			if point_num == index:
				peak_amp_list.append(point)
				if point > peak_amp:
					peak_amp = point
					max_peak_index = index
					max_peak_time = time[index]
					
	if invert == True:
		flip = event_trace * -1
				
	valley_amp = []
	min_valley_amp = 999
	min_valley_time = 0
	min_valley_index = 0

	for index in valley_index:
		for point_num, point in enumerate(event_trace):
			if point_num == index:
				valley_amp.append(point)
				if point < min_valley_amp:
					min_valley_amp = point
					min_valley_time = time[index]
					min_valley_index = index
				

	#Find distances between peaks and valleys
	length_check = min([len(peak_index),len(valley_index)])
	peak_index = peak_index[0:length_check]
	valley_index = valley_index[0:length_check]
	valley_amp = valley_amp[0:length_check]
	
	pv_dist = []
	pv_diff = []
	
	for item_num, item in enumerate(valley_index):
		pv_dist.append(item - max_peak_index)
		pv_diff.append(peak_amp - valley_amp[item_num])


	prev_amp = 0
	prev_time = -9999
	
	for point_num, point in enumerate(valley_amp):
		tempx = valley_index[point_num]
		temp_time = time[tempx]
		if point <= prev_amp and temp_time > prev_time and valley_index[point_num] < max_peak_index:
			peak_onset_index = valley_index[point_num]
			peak_onset_time = time[peak_onset_index]
			peak_onset_amp = point
			prev_amp = point
	
	if 'peak_onset_index' in locals():
		
		if invert == True:
			peak_onset_amp = flip[peak_onset_index]
			event_trace = flip
			
		event_name = 'Event ' + str(event_num + 1)
	
		#Generate figure for individual signals and
		time_length_check = min([len(time),len(event_trace)])
		plot_time = time[0:time_length_check]
		plot_trace = event_trace[0:time_length_check]
		plt.plot(plot_time, plot_trace)
		plt.plot(plot_time[max_peak_index], plot_trace[max_peak_index], 'x')
		plt.plot(plot_time[peak_onset_index], plot_trace[peak_onset_index], 'o')
		plt.xlabel('Time (s)')
		plt.ylabel('DF/F0 Zscore')
		#plt.title(file_handle + '_Event_Trace_' + str(event_num+1))
		plt.savefig(file_handle + '_Event_Trace_' + str(event_num + 1) + '.png')
		plt.close()

		return [event_name, peak_onset_index, peak_onset_time, peak_onset_amp, max_peak_index, max_peak_time, peak_amp, min_valley_index, min_valley_time, min_valley_amp]
	
	if 'peak_onset_index' not in locals():
		
		peak_onset_index = 'nan'
		peak_onset_time = 'nan'
		peak_onset_amp = 'nan'
		
		if invert == True:
			event_trace = flip
			
		event_name = 'Event ' + str(event_num + 1)
		
		time_length_check = min([len(time),len(event_trace)])
		plot_time = time[0:time_length_check]
		plot_trace = event_trace[0:time_length_check]
		plt.plot(plot_time, plot_trace)
		plt.xlabel('Time (s)')
		plt.ylabel('DF/F0 Zscore')
		#plt.title(file_handle + '_Event_Trace_' + str(event_num+1) + ' NOT_DETECTED')
		plt.savefig(file_handle + '_Event_Trace_' + str(event_num + 1) + '_NOT_DETECTED' + '.png')
		plt.close()
		
		return [event_name, peak_onset_index, peak_onset_time, peak_onset_amp, max_peak_index, max_peak_time, peak_amp, min_valley_index, min_valley_time, min_valley_amp]
		
def lowpass(data, cutoff, fs, order):
	#Filter signal with butterworth lowpass filter
	
	#Input Arguments:
	#data = list of signal to be filtered
	#cutoff = interger of desired Hz for filter cutoff
	#fs = interger of sampling rate
	#order = interger of ordering for filter (i.e., use 2 to indicate polynomial signal)
	
	from scipy.signal import butter, filtfilt

	norm_cutoff = cutoff/(0.5*fs)
	b, a = butter(order, norm_cutoff, btype='low', analog=False)
	y = filtfilt(b, a, data)
	return y


def plot_average_signals(time, signals, x_label, y_label, file_handle):
	#Average all event signals together and save plot with error bands.
	
	#Input Arguments:
	#time = list of timestamps
	#x_label = string of name for x axis
	#y_label = string of name for y axis
	#signals = nested list of signals for all events
	#file_handle = string of desired name/format for saved figure (e.g., 'figure')
	
	import pandas as pd
	import matplotlib.pyplot as plt
	
	#Convert nested list of signals to dataframe
	event_list = pd.DataFrame(signals)
	event_list = event_list.T

	#Calculate mean and sem of event signals and error bands
	event_list_avg = event_list.mean(axis = 1, numeric_only = True)
	event_list_sem = event_list.sem(axis = 1, numeric_only = True)
	event_list_avg = event_list_avg.tolist()
	event_list_sem = event_list_sem.tolist()
	
	#Create error bands for plotting
	pos_error = []
	neg_error = []
	
	for point_num, point in enumerate(event_list_avg):
		pos_error.append(point + event_list_sem[point_num])
		neg_error.append(point - event_list_sem[point_num])
		
	#Make all data the same dimensions for plotting.
	len_check = min(len(time),len(event_list_avg))
	time = time[0:len_check]
	event_list_avg = event_list_avg[0:len_check]
	pos_error = pos_error[0:len_check]
	neg_error = neg_error[0:len_check]
		
	#Create and save plot of averaged signal with shaded error bands
	plt.plot(time, event_list_avg)
	plt.fill_between(time, pos_error, neg_error, alpha = 0.2)
	plt.xlabel('Time (s)')
	plt.ylabel('DF/F0 Zscore')
	plt.savefig(file_handle + '.png')
	plt.close()
	
	#Write averaged signals to output.
	avg_output = open(file_handle + '.csv', 'w')
	title_line = ['Time (s)','Averaged Event','SEM']
	avg_output.write(','.join(title_line) + '\n')
	
	current_line = []
	for line_num, line in enumerate(time):
		current_line.append(str(line))
		current_line.append(str(event_list_avg[line_num]))
		current_line.append(str(pos_error[line_num]))
		avg_output.write(','.join(current_line) + '\n')
		current_line = []
		
def plot_all_signals(time, events, x_label, y_label, file_handle):
	#Returns plot and csv of individual signals
	
	import pandas as pd
	import matplotlib.pyplot as plt
	
	#Input Arguments:
	#time = nested list of timestamps
	#events = nested list of event signals
	#x_label = string of name for x axis.
	#y_label = string of name for y axis.
	#file_handle = string of desired name/format for saved figure (e.g., 'figure')
	
	#Create and save plot of signals
	for event_num, event in enumerate(events):
		plt.plot(time[event_num], event, label = 'Event' + str(event_num + 1))
	
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	plt.legend(bbox_to_anchor=(1.02,1), loc="upper left")
	plt.savefig(file_handle + '.png', bbox_inches = 'tight')
	plt.close()
	
	#Find longest time for saving data
	longest_time = []
	prev_len = 0

	for x in time:
		z = len(x)
		if z > prev_len:
			longest_time = x
			prev_len = z
	
	#Write all signals to output.
	events_df = pd.DataFrame(events)
	events_df = events_df.T
	time_df = pd.DataFrame(longest_time)
	output_df = pd.concat([time_df, events_df], axis = 1)
	event_list = ['Event ' + str(x + 1) for x in range(len(events))]
	col_names = [x_label]
	for name in event_list:
		col_names.append(name)
	output_df.columns = col_names
	output_df.to_csv(file_handle + '.csv')

		
def unpickle(pickles):
	#Return a list containing unpacked pickle files
	
	#Input Arguments:
	#pickles = list of pickle file names
	
	import pickle
	
	unpickle =[[] for file in range(len(pickles))]
	
	for file_num, file in enumerate(pickles):
		f = open(file,'rb')
		unpickle[file_num] = pickle.load(f)
		f.close()
	
	return unpickle

