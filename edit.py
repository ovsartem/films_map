import pandas as pd
import numpy as np


file1 = open('locations.list', encoding="utf8", errors='ignore')
Lines = file1.readlines()
Lines_edited = Lines[14:]
Lines_edited1 = [i.split("(") for i in Lines_edited]
Lines_edited2 = [i for i in Lines_edited1 if len(i) > 1]
for i in range(len(Lines_edited2)):
    Lines_edited2[i][1] = Lines_edited2[i][1].split(")")
filtered_data = [[] for i in range((len(Lines_edited2)))]

# creating a new list
for i in range(len(Lines_edited2)):
    filtered_data[i].append(Lines_edited2[i][0].replace("\"", ""))
    filtered_data[i].append(Lines_edited2[i][1][0])
    to_edit = Lines_edited2[i][1]
    to_edit.pop(0)
    to_edit1 = ", ".join(to_edit).replace("\t", "").replace("\n", "")
    filtered_data[i].append(to_edit1)

df = pd.DataFrame(filtered_data, columns=["name", "year", "place"])


def clean_year(year):
    """
    Cleaning up year column
    """
    if len(year) > 3 and year[0].isnumeric() and year[3].isnumeric() and year[1].isnumeric() and year[2].isnumeric():
        return year[:4]
    else:
        return np.nan


df["year"] = df["year"].apply(lambda x: clean_year(x))


def clean_place(place):
    """
    Cleaning up place column
    """
    if "{" in place:
        return np.nan
    else:
        return place


df["place"] = df["place"].apply(lambda x: clean_place(x))

df = df.dropna(axis=0, how='any')


def united(place):
    """
    Changes shorted forms
    """
    if "USA" in place:
        return place[:-4] + " United States"
    if "UK" in place:
        return place[:-3] + " United Kingdom"
    else:
        return place


df["place"] = df["place"].apply(lambda x: united(x))

# local error
df = df[~df.place.str.contains("Federal", na=False)]

df.to_csv('filtered_data.csv', index=False)
