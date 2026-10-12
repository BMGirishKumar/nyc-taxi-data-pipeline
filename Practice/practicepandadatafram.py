import pandas as pd

#DataFrame is a 2d array-like object that can hold many data types, including objects. It is similar to a spreadsheet or a SQL table, or a dict of Series objects.

data={"Name":["Spongebob","Patrick","Squidward"],
      "Age":[30,35,50]}

df=pd.DataFrame(data, index=["Employee1","Employee2","Employee3"])

print(df.loc["Employee1"])

print(df.iloc[0])


#Add a new column to the DataFrame
df["Job"]=["Cook","N/A","Cashier"]

print(df)

# Add a new row to the DataFrame
new_row=pd.DataFrame([{"Name":"Sandy","Age":28,"Job":"Engineer"},{"Name":"Eugene","Age":60,"Job":"Manager"}],index=["Employee4","Employee5"])

df=pd.concat([df,new_row],ignore_index=True)

print(df)