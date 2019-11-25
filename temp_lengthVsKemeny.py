from matplotlib.pyplot import xlabel, ylabel, title, scatter, plot, show
from scipy import stats

from statistical_analysis import data

temp_length = data['temp_length']

temp_length_constant = data[temp_length>99].groupby('temp_length').mean()

temp_length_constant['kemeny_score']
kemeny_score_const = temp_length_constant['kemeny_score']
temp_length_constant = temp_length_constant.index

xlabel('Temperature Length')
ylabel('Kemeny score')
title('Temperature length Vs Kemeny Score')
scatter(temp_length_constant, kemeny_score_const, s=40, c='b', marker='o', edgecolors=None)

line = stats.linregress(temp_length_constant, kemeny_score_const)[0]*temp_length_constant+stats.linregress(temp_length_constant, kemeny_score_const)[1]
plot(temp_length_constant, line,'r-', label='solid')

show()