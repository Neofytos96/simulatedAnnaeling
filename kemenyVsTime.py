from matplotlib.pyplot import figure, xlabel, ylabel, title, scatter, plot, xlim, ylim, show
from scipy import stats

import statistical_analysis

figure(figsize=(16, 8))
xlabel('Time Taken', fontsize=30)
ylabel('Kemeny score', fontsize=30)
title('Time taken Vs Kemeny Score', fontsize=30)
scatter(statistical_analysis.time_taken, statistical_analysis.kemeny_score, s=40, c='b', marker='o', edgecolors=None)

line = stats.linregress(statistical_analysis.time_taken, statistical_analysis.kemeny_score)[0] * statistical_analysis.time_taken + stats.linregress(
    statistical_analysis.time_taken, statistical_analysis.kemeny_score)[1]
plot(statistical_analysis.time_taken, line, 'r-', label='solid')
xlim([0, 5])
ylim([0, 300])
print ('slope=', round(stats.linregress(statistical_analysis.time_taken, statistical_analysis.kemeny_score)[0], 2))

show()