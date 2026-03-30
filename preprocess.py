import pandas as pd

# Creating crop data frame
df = pd.read_csv("raw_crop_data.csv")
print(df.head())
print(df.columns)
