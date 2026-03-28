import pandas as pd
import matplotlib.pyplot as plt

# Read CSV
dfLap = pd.read_csv("LapTimes.csv")
dfRace = pd.read_csv("RaceResults.csv")
top_ten = dfRace[dfRace["Position"] <= 10]
top_ten_sorted = top_ten.sort_values(by="TeamName")
print(top_ten_sorted[["TeamName","Position","FullName","Location"]].head(10))
print(top_ten_sorted.groupby("TeamName").size().reset_index(name="Top 10 Count"))
