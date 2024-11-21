import pandas as pd

cities = pd.read_csv("../data/cities.csv", sep=";")
regions = pd.read_csv("../data/regions.csv", sep=";")

locations = pd.concat([cities, regions], axis="columns")

locations = locations.reindex(columns=['Name', 'Region', 'Coordinates'])

locations.to_csv("../data/locations.csv", sep=";", index=False)