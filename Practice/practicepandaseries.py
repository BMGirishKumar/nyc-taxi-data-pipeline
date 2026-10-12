import pandas as pd

print(pd.__version__)

#Series is a 1d array-like object that can hold many data types, including objects. It is similar to a column in a spreadsheet or a database table.

data=[100,102,104,106,108,200,202]
series=pd.Series(data,index=['a','b','c','d','e','f','g'])

series.loc['c'] = 200

print (series.loc['a'])
print (series.loc['c'])
print(series.iloc[2])

print(series[series>=200])


calories={"Day1":1750, "Day2":2000, "Day3":2500}
calories_series=pd.Series(calories)
print(calories_series)

print(calories_series[calories_series>=2000])