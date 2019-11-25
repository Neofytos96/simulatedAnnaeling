from matplotlib.pyplot import xlabel, ylabel, title, scatter, plot, show, xlim
from scipy import stats

from statistical_analysis import data

stopping_criterion = data['num_non_improve']

stopping_constant = data[stopping_criterion>10].groupby('num_non_improve').mean()

stopping_constant['kemeny_score']
kemeny_score_const = stopping_constant['kemeny_score']
stopping_constant = stopping_constant.index

xlabel('Number non improve')
ylabel('Kemeny score')
title('Number Non Improve Vs Kemeny Score')
scatter(stopping_constant, kemeny_score_const, s=40, c='b', marker='o', edgecolors=None)

line = stats.linregress(stopping_constant, kemeny_score_const)[0]*stopping_constant+stats.linregress(stopping_constant, kemeny_score_const)[1]
plot(stopping_constant, line,'r-', label='solid')

show()