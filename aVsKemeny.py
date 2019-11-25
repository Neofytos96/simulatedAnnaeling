from matplotlib.pyplot import xlabel, ylabel, title, scatter, plot, show, xlim
from scipy import stats

from statistical_analysis import data

cooling_a = data['cooling_multiple']

cooling_constant = data[cooling_a>0.199].groupby('cooling_multiple').mean()
cooling_constant['kemeny_score']
kemeny_score_const = cooling_constant['kemeny_score']
cooling_constant = cooling_constant.index

xlabel('Cooling multiple')
ylabel('Kemeny score')
title('Cooling multiple Vs Kemeny Score')
scatter(cooling_constant, kemeny_score_const, s=40, c='b', marker='o', edgecolors=None)
xlim([0.987,1.000])



line = stats.linregress(cooling_constant, kemeny_score_const)[0]*cooling_constant+stats.linregress(cooling_constant, kemeny_score_const)[1]
plot(cooling_constant, line,'r-', label='solid')

show()