import pandas as pd
from celery.utils.sysinfo import df
from matplotlib.pyplot import figure, xlabel, ylabel, title, scatter, plot, xlim, ylim, show
from pandas import Series, DataFrame
from scipy import stats, std, sqrt

data=pd.read_csv('statistic4.csv')
data=data.dropna()


initial_temp = data['initial_temp']
cooling_multiple = data['cooling_multiple']
temp_length = data['temp_length']
num_non_improve = data['num_non_improve']
time_taken = data['time_taken'].round(2)
kemeny_score = data['kemeny_score']

#find the min kemeny score and the average time taken to filter the data based on that
#graphs to find the relationship with every variable compared to the kemeny ranking
kemeny_filtered = data['kemeny_score']

#find mean
kemeny_filtered_mean = round(kemeny_filtered.mean(),2)
#find min
kemeny_filtered_min = round(kemeny_filtered.min(),2)
#find max
kemeny_filtered_max = round(kemeny_filtered.max(),2)

#find standard deviation
kemeny_std = round(kemeny_filtered.std(),2)
#calculate the error
kemeny_err = 1.96*std(kemeny_filtered)/sqrt(len(kemeny_filtered))
#find the lower value for confidence interval
mean_min_err = round(kemeny_filtered_mean-kemeny_err)
#find the higher value for confidence interval
mean_plus_err = round(kemeny_filtered_mean+kemeny_err)

print('Mean of Kemeny score:', kemeny_filtered_mean)
print('Minimum of Kemeny score:', kemeny_filtered_min)
print('Maximum of kemeny score,', kemeny_filtered_max)
print('Standard deviation of Kemeny score:', kemeny_std)
print('95% confidence interval of Kemeny Score:', [mean_min_err, mean_plus_err])
print("Mean kemeny score:", round(data.kemeny_score.mean(),2))


def generate_csv_best_cases():
    global df
    filtering = (data.kemeny_score < 64)
    filtered_data = data[filtering]
    filtered_data.reset_index()
    filtered_data.index = pd.np.arange(1, len(filtered_data) + 1)

    print(type(filtered_data))
    from pandas import DataFrame
    df = DataFrame(filtered_data, columns=['initial_temp', 'cooling_multiple', 'temp_length', 'num_non_improve'])
    df.to_csv(r'bestCases.csv')


generate_csv_best_cases()


