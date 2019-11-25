from matplotlib.pyplot import xlabel, ylabel, title, scatter, plot, show
from scipy import stats

from statistical_analysis import data

initial_temp = data['initial_temp']

temp_initial_constant = data[initial_temp>99].groupby('initial_temp').mean()

temp_initial_constant['kemeny_score']
kemeny_score_const = temp_initial_constant['kemeny_score']
inital_temp_constant = temp_initial_constant.index

xlabel('Initial Temp')
ylabel('Kemeny score')
title('Initial Temperature Vs Kemeny Score')
scatter(inital_temp_constant, kemeny_score_const, s=40, c='b', marker='o', edgecolors=None)

line = stats.linregress(inital_temp_constant, kemeny_score_const)[0]*inital_temp_constant+stats.linregress(inital_temp_constant, kemeny_score_const)[1]
plot(inital_temp_constant, line,'r-', label='solid')



print ('slope=', round(stats.linregress(inital_temp_constant, kemeny_score_const)[0],2))
show()

