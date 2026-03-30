import pandas as pd

# Creating crop data frame
df = pd.read_csv("raw_crop_data.csv")
# Used to test df
# print(df.head())
# print(df.columns)

# Droping useless column
df = df.drop(columns=["Unnamed: 0"])

# Creating IDs
crop_map = {name: i+1 for i, name in enumerate(df['Item'].unique())}

location_map = {name: i+1 for i, name in enumerate(df['Area'].unique())}

# Creating crops.cvs
crops = pd.DataFrame({
    'crop_id': list(crop_map.values()),
    'crop_name': list(crop_map.keys()),
})

crops.to_csv("data/crops.csv", index=False)

# Creating locations.cvs
locations = pd.DataFrame({
    'location_id': list(location_map.values()),
    'country': list(location_map.keys()),
    'region': None
})

locations.to_csv("data/locations.csv", index=False)

# Creating yearly_conditions.csv
conditions = df.copy()

conditions['location_id'] = conditions['Area'].map(location_map)

conditions_table = conditions[[
    'location_id',
    'Year',
    'average_rain_fall_mm_per_year',
    'avg_temp',
    'pesticides_tonnes'
]].drop_duplicates()

conditions_table.insert(0, 'condition_id', range(1, len(conditions_table)+1))

conditions_table.columns = [
    'condition_id',
    'location_id',
    'year',
    'avg_rainfall',
    'avg_temp',
    'tonnes_pesticide'
]

conditions_table.to_csv("data/yearly_conditions.csv", index=False)

# Creating yield_records.csv
yield_df = df.copy()

yield_df['crop_id'] = yield_df['Item'].map(crop_map)
yield_df['location_id'] = yield_df['Area'].map(location_map)

yield_table = yield_df[[
    'crop_id',
    'location_id',
    'Year',
    'hg/ha_yield'
]]

yield_table.insert(0, 'yield_id', range(1, len(yield_table)+1))

yield_table.columns = [
    'yield_id',
    'crop_id',
    'location_id',
    'year',
    'hg_per_ha_yield'
]

yield_table.to_csv("data/yield_records.csv", index=False)