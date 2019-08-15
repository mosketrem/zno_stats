import pandas as pd
import json

from consts import SUBJECTS


regions = set()
for f in  pd.read_csv('/vagrant/ZNO/OpenData2018.csv', chunksize=1000, sep=';'):
    regions.update(f.REGNAME.unique())

results = {}
for region in regions:
    temp_df = pd.DataFrame()
    for f in  pd.read_csv('/vagrant/ZNO/OpenData2018.csv', chunksize=1000, sep=';'):
        temp = f[f.REGNAME == region]
        temp_df = pd.concat([temp_df, temp])
    results[region] = {s:temp_df[s].mean() for s in SUBJECTS}
    areas = set(temp_df.AREANAME.unique())
    for area in areas:
        temp = temp_df[temp_df.AREANAME == area]
        results[region][area] = {s:temp[s].mean() for s in SUBJECTS}
        cities = set(temp.TERNAME.unique())
        for city in cities:
            city_df = temp[temp.TERNAME == city]
            results[region][area][city] = {s:city_df[s].mean() for s in SUBJECTS}

with open('/vagrant/ZNO/results.json', 'w') as f:
    json.dump(results, f, ensure_ascii=False)

