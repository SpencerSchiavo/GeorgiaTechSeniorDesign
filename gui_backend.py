#inputs : demand, no of associates, ~SD of demand~, min time to sort, max time to sort, mean time to sort, ~number of simulated days~
#outputs : number hours w/current, number of hours with optimal, optimal number of associates
#gamma stuff : Gamma( alpha, beta) -> mean = alpha * beta -> variance = mean * beta
import numpy as np
import math
import pandas as pd

daily_demand = 1200
no_of_associates = 4
min_time_to_sort = 10
mean_time_to_sort = 26
max_time_to_sort = 60
distribution = "triangularb"
buffer_num = 1.4

data = pd.read_csv('WSI_dimensional_data.csv')
Volume = data['Volume']

#sorting times
sort_list = []
if distribution == "triangular":
    for carton in range(daily_demand):
        sort_list.append(np.random.triangular(min_time_to_sort,mean_time_to_sort,max_time_to_sort))

elif distribution == "uniform":
    for carton in range(daily_demand):
        sort_list.append(np.random.uniform(min_time_to_sort, max_time_to_sort))

elif distribution == "constant":
    for carton in range(daily_demand):
        sort_list.append(mean_time_to_sort)


#dimensional data
pallets=0
Vol=0
dims = np.random.choice(Volume, daily_demand)
for i in range(len(dims)):
    if Vol+dims[i] > 115000:
        pallets += 1
        Vol=dims[i]
    else:
        Vol += dims[i]
    if dims[i] > 23000:
        sort_list[i] = sort_list[i] * 2

loading_time = np.random.uniform(1200, 1800)

if pallets > 12:
    loading_time = loading_time * 2

 #sum of all sorting times + sum of all loading times + constant value for wrapping times the buffer which accounts for staging
manhours = ((sum(sort_list)+loading_time+pallets*90)*buffer_num)/3600

no_hours_current = manhours/no_of_associates

if manhours < 18:
    optimal_associates = 2
    no_hours_optimal = manhours/2
else:
    optimal_associates = math.ceil(manhours/9)
    no_hours_optimal = manhours/optimal_associates

print("With the current number of associates the hours needed are:", no_hours_current)
print("With the optimal number of associates the hours needed are:", no_hours_optimal)
print("The optimal number of associates for today is:", optimal_associates)






#insert code to check if time to sort fields are empty or not




