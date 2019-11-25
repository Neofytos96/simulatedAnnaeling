import pandas as pd
from celery.utils.sysinfo import df
from matplotlib.pyplot import figure, xlabel, ylabel, title, scatter, plot, xlim, ylim, show
from pandas import Series, DataFrame
from scipy import stats

data = pd.read_csv('statistic4.csv')
data = data.dropna()

initial_temp = data['initial_temp'] == 100
cooling_multiple = data['cooling_multiple']
temp_length = data['temp_length']
num_non_improve = data['num_non_improve']
time_taken = data['time_taken']
kemeny_score = data['kemeny_score']

# find the min kemeny score and the average time taken to filter the data based on that
# print("Minimum kemeny score from all the data:", data.kemeny_score.min())
# print("Mean time taken from all the data:", data.time_taken.mean())

filtering = (data.kemeny_score < 70) & (data.time_taken < 1.6)

filtered_data = data[filtering]
# shows that the num_non_improve could be as down as 2000
# print("Num_non_improve median:", filtered_data['num_non_improve'].median())
# print("Cooling multiple median:", filtered_data['cooling_multiple'].median())
# print("Temperature lenght median", filtered_data['temp_length'].median())

filtering = (data.kemeny_score<64)
filtered_data = data[filtering]
print(type(filtered_data))
from pandas import DataFrame
df = DataFrame(filtered_data, columns=['initial_temp', 'cooling_multiple', 'temp_length', 'num_non_improve'])
print(df)
df.to_csv(r'bestCases.csv')

with open("bestCases.csv", "r") as out_file:
    print()
