import pandas as pd
import matplotlib.pyplot as plt

# Read CSV
dfLap = pd.read_csv("LapTimes.csv")
dfRace = pd.read_csv("RaceResults.csv")
top_ten = dfRace[dfRace["Position"] <= 10]
top_ten_sorted = top_ten.sort_values(by="TeamName")
print(top_ten_sorted[["TeamName","Position","FullName","Location"]].head(10))
print(top_ten_sorted.groupby("TeamName").size().reset_index(name="Top 10 Count").to_string(index=False))
top_ten_sorted["Q1Seconds"] = pd.to_timedelta(top_ten_sorted["Q1"]).dt.total_seconds()
top_ten_sorted["Q2Seconds"] = pd.to_timedelta(top_ten_sorted["Q2"]).dt.total_seconds()
top_ten_sorted["Q3Seconds"] = pd.to_timedelta(top_ten_sorted["Q3"]).dt.total_seconds()
print(top_ten_sorted[["Q1Seconds","Q2Seconds","Q3Seconds"]])