import pandas as pd

df=pd.read_csv(r"c:\Users\girishkumar.bm\Downloads\pp\Practice\data.csv")

# Selection by column
#print(df["Name"].to_string())
#print(df["Weight"].to_string())

#print(df[["Name","Weight"]].to_string())

#pokemon=input("Enter the name of the pokemon: ")

#try:
    #print(df.loc[pokemon].to_string())
#except KeyError:
    #print(f"{pokemon} not found.")

#Selection by rows
#print(df.loc["Pikachu"].to_string())



###################################################################################################
#Filtering the DataFrame based on a condition

#tall_pokemon=df[df["Height"]>2.0]

#print(tall_pokemon.to_string())

#legendary_pokemon=df[df["Legendary"]==1]
#print(legendary_pokemon.to_string())



## data cleaning and preprocessing

#df= df.drop(columns=["Legendary","No"])

#df=df.dropna(subset=["Type2"])

#df=df.fillna({"Type2":"None"})
#print(df.to_string())


df=df.drop(columns=["No"])
#3.Fix inconsistent data types

df["Type1"]=df["Type1"].replace({"Grass":"GRASS"
                                 ,"Fire":"FIRE",
                                 "Water":"WATER"})

#4.Standardize text data

df["Name"]=df["Name"].str.lower()

#5. Fix data entry errors

df["Legendary"]=df["Legendary"].astype(bool)

#6. Remove duplicates


df=df.drop_duplicates()
print(df.to_string())