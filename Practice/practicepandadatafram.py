import pandas as pd
'''
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

print(df)#*

'''
#Group by:

data = {
    'Zone': ['A', 'A', 'B', 'B', 'A', 'B'],
    'Item': ['Widget', 'Gadget', 'Widget', 'Gadget', 'Widget', 'Gadget'],
    'Quantity': [10, 5, 10, 5, 10, 5],
    'Weight': [1.2, 0.5, 1.2, 0.5, 1.1, 0.6]
      }

df=pd.DataFrame(data)
print(df)
'''
#Single agg

total_qty=df.groupby('Zone')['Quantity'].sum().reset_index()
print(total_qty)

#Multiple agg

zone_mentrix=df.groupby('Zone').agg({'Quantity':'sum','Weight':'mean'}).reset_index()
print(zone_mentrix)




# Create a pivot table showing total quantity by Zone (Rows) and Item (Columns)
pivot_df = df.pivot_table(
    values='Quantity', 
    index='Zone', 
    columns='Item', 
    aggfunc='sum', 
    fill_value=0
)

print("\nPivot Table (Zone vs Item Quantity):")
print(pivot_df)



#Merge datasets

df_orders=pd.DataFrame({
    'OrderID': [1, 2, 3, 4],
    'Sku': ['A123', 'B456', 'C789', 'D012'],
})

df_products=pd.DataFrame({
    'Sku': ['A123', 'B456', 'C789', 'E345'],
    'Description': ['Widget', 'Gadget', 'Thingamajig', 'Doohickey'],
})

#Inner join: Only rows with matching SKU in bith DataFrames will be included in the result.
merged_inner=pd.merge(df_orders,df_products,on='Sku',how='inner')

left_merge=pd.merge(df_orders,df_products,on='Sku',how='left')

print("Inner Merge Result:")
print(merged_inner)
print("\nLeft Merge Result:")
print(left_merge)

'''

