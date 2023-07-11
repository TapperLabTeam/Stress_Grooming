import sys
import pickle
sys.path.append(sys.argv[1])
from signal_udfs import unpickle
import pandas as pd

#IMPORT BLOCK
unpickle = unpickle(sys.argv[2:])
event_dict = unpickle[0]

base_df = pd.DataFrame(event_dict['Base Trace'])
event_df = pd.DataFrame(event_dict['Event Trace'])

event_names = ['Event ' + str(x + 1) for x in range(len(event_dict['Base Trace']))]

base_mean_zs = []
event_mean_zs = []

base_mean_zs = base_df.mean(axis = 1, skipna = True)
event_mean_zs = event_df.mean(axis = 1, skipna = True)

calc_dict = {}

calc_dict['Event Number'] = event_names
calc_dict['Base Mean Zscore'] = base_mean_zs
calc_dict['Event Mean Zscore'] = event_mean_zs

pickle.dump(calc_dict, open('calc_dict.pkl','wb'))
