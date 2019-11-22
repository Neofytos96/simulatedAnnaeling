import pandas as pd
from matplotlib.pyplot import figure, xlabel, ylabel, title, scatter, plot, xlim, ylim, show
from pandas import Series, DataFrame
from scipy import stats

data=pd.read_csv('statistic2.csv')
data=data.dropna()
# print(data)

initial_temp = data['initial_temp']==100
cooling_multiple = data['cooling_multiple']
temp_length = data['temp_length']
num_non_improve = data['num_non_improve']
time_taken = data['time_taken']
kemeny_score = data['kemeny_score']

# figure(figsize=(16, 8))
# xlabel('Initial Temperature', fontsize=30)
# ylabel('Kemeny score', fontsize=30)
# title('Initial Temperature Vs Kemeny Score', fontsize=30)
# scatter(initial_temp, kemeny_score, s=40, c='b', marker='o', edgecolors=None)
#
# line = stats.linregress(initial_temp, kemeny_score)[0]*initial_temp+stats.linregress(initial_temp, kemeny_score)[1]
# plot(initial_temp, line,'r-', label='solid')
# # xlim([0, 5])
# # ylim([0, 300])
# print ('slope=', round(stats.linregress(initial_temp, kemeny_score)[0],2))
# print ('intercept=', round(stats.linregress(initial_temp, kemeny_score)[1], 2))
# show()


print(data.kemeny_score.min())
print(data.time_taken.mean())
data_initialTemp_kemeny = data[['initial_temp', 'kemeny_score']]
# data_initialTemp_kemeny.set_index['kemeny_score']
filtering = (data.kemeny_score<70) & (data.time_taken<1.6)

# all_filters = kemeny_close_to_min
filtered_data = data[filtering]
print(filtered_data)
# data_initialTemp_kemeny