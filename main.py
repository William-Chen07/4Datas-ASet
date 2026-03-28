import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings('ignore')

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
dfLap["LapTimeSeconds"] = pd.to_timedelta(dfLap["LapTime"]).dt.total_seconds()
dfLap["PitOutTimeSeconds"] = pd.to_timedelta(dfLap["PitOutTime"]).dt.total_seconds()
dfLap["PitInTimeSeconds"] = pd.to_timedelta(dfLap["PitInTime"]).dt.total_seconds()
dfLap["Sector1TimeSeconds"] = pd.to_timedelta(dfLap["Sector1Time"]).dt.total_seconds()
dfLap["Sector2TimeSeconds"] = pd.to_timedelta(dfLap["Sector2Time"]).dt.total_seconds()
dfLap["Sector3TimeSeconds"] = pd.to_timedelta(dfLap["Sector3Time"]).dt.total_seconds()
dfLap["Sector1SessionTimeSeconds"] = pd.to_timedelta(dfLap["Sector1SessionTime"]).dt.total_seconds()
dfLap["Sector2SessionTimeSeconds"] = pd.to_timedelta(dfLap["Sector2SessionTime"]).dt.total_seconds()
dfLap["Sector3SessionTimeSeconds"] = pd.to_timedelta(dfLap["Sector3SessionTime"]).dt.total_seconds()
print(top_ten_sorted[["Q1Seconds","Q2Seconds","Q3Seconds"]])
print(dfLap[["LapTimeSeconds","PitOutTimeSeconds","PitInTimeSeconds","Sector1TimeSeconds","Sector2TimeSeconds","Sector3TimeSeconds","Sector1SessionTimeSeconds","Sector2SessionTimeSeconds","Sector3SessionTimeSeconds"]])




# ── LOAD DATA ──────────────────────────────────────────────────────────────────
dfRace = pd.read_csv('RaceResults.csv')
dfRace['Q1Seconds'] = pd.to_timedelta(dfRace['Q1']).dt.total_seconds()
dfRace['Q2Seconds'] = pd.to_timedelta(dfRace['Q2']).dt.total_seconds()
dfRace['Q3Seconds'] = pd.to_timedelta(dfRace['Q3']).dt.total_seconds()
dfRace['BestQual'] = dfRace[['Q1Seconds','Q2Seconds','Q3Seconds']].min(axis=1)
dfRace['IsTop10'] = (dfRace['Position'] <= 10).astype(int)

TEAM_COLORS = {
    'McLaren': '#FF8000', 'Red Bull Racing': '#3671C6', 'Mercedes': '#27F4D2',
    'Ferrari': '#E8002D', 'Williams': '#64C4FF', 'Aston Martin': '#229971',
    'Alpine': '#FF87BC', 'Racing Bulls': '#6692FF', 'Haas F1 Team': '#B6BABD',
    'Kick Sauber': '#52E252'
}

top10_drivers = ['Lando Norris','Max Verstappen','Oscar Piastri','George Russell',
                 'Charles Leclerc','Lewis Hamilton','Carlos Sainz','Alexander Albon',
                 'Kimi Antonelli','Fernando Alonso']

driver_team = dfRace.groupby('FullName')['TeamName'].first().to_dict()

# ── CHART 1: Driver Championship Standings ────────────────────────────────────
fig1, ax = plt.subplots(figsize=(16, 8))
fig1.patch.set_facecolor('#1a1a2e')
ax.set_facecolor('#1a1a2e')

cum = dfRace.sort_values(['FullName','Round'])
cum['CumPoints'] = cum.groupby('FullName')['Points'].cumsum()

for driver in top10_drivers:
    d = cum[cum['FullName'] == driver].sort_values('Round')
    team = driver_team.get(driver, 'McLaren')
    color = TEAM_COLORS.get(team, '#ffffff')
    ax.plot(d['Round'], d['CumPoints'], marker='o', markersize=4, linewidth=2,
            color=color, label=driver.split()[-1])

ax.set_xlabel('Round', color='white', fontsize=12)
ax.set_ylabel('Cumulative Points', color='white', fontsize=12)
ax.set_title('Driver Championship — Points Across The Season', color='white', fontsize=15, fontweight='bold', pad=15)
ax.tick_params(colors='white')
ax.spines['bottom'].set_color('#444')
ax.spines['left'].set_color('#444')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(alpha=0.15, color='white')
ax.legend(loc='upper left', ncol=2, fontsize=9, facecolor='#2a2a3e', edgecolor='#444', labelcolor='white')
plt.tight_layout()
plt.savefig('chart1_standings.png', dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
plt.close()
print('Chart 1 saved: chart1_standings.png')

# ── CHART 2: Top 10 Consistency ───────────────────────────────────────────────
fig2, axes = plt.subplots(1, 2, figsize=(16, 7))
fig2.patch.set_facecolor('#1a1a2e')

consistency = dfRace.groupby('FullName').agg(
    Races=('Round','count'), Top10s=('IsTop10','sum'),
    AvgPos=('Position','mean'), TotalPoints=('Points','sum')
).reset_index()
consistency['Top10Rate'] = consistency['Top10s'] / consistency['Races']
top_c = consistency[consistency['Races'] >= 10].sort_values('Top10Rate', ascending=False).head(12)

colors_bar = [TEAM_COLORS.get(driver_team.get(d,'McLaren'), '#aaa') for d in top_c['FullName']]
bars = axes[0].barh(top_c['FullName'], top_c['Top10Rate']*100, color=colors_bar, edgecolor='none', height=0.6)
axes[0].set_xlabel('Top 10 Finish Rate (%)', color='white')
axes[0].set_title('Top 10 Consistency Rate', color='white', fontweight='bold', fontsize=13)
axes[0].set_facecolor('#1a1a2e')
axes[0].tick_params(colors='white')
axes[0].spines['bottom'].set_color('#444')
axes[0].spines['left'].set_color('#444')
axes[0].spines['top'].set_visible(False)
axes[0].spines['right'].set_visible(False)
axes[0].grid(axis='x', alpha=0.15, color='white')
for bar, val in zip(bars, top_c['Top10Rate']*100):
    axes[0].text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                 f'{val:.0f}%', va='center', color='white', fontsize=9)

for _, row in consistency[consistency['Races'] >= 10].iterrows():
    team = driver_team.get(row['FullName'],'McLaren')
    color = TEAM_COLORS.get(team,'#aaa')
    axes[1].scatter(row['AvgPos'], row['TotalPoints'], color=color, s=100, zorder=5)
    axes[1].annotate(row['FullName'].split()[-1], (row['AvgPos'], row['TotalPoints']),
                     fontsize=8, color='white', ha='left', xytext=(4,2), textcoords='offset points')
axes[1].set_xlabel('Average Finish Position', color='white')
axes[1].set_ylabel('Total Points', color='white')
axes[1].set_title('Avg Position vs Total Points', color='white', fontweight='bold', fontsize=13)
axes[1].set_facecolor('#1a1a2e')
axes[1].tick_params(colors='white')
axes[1].invert_xaxis()
for spine in ['top','right']: axes[1].spines[spine].set_visible(False)
for spine in ['bottom','left']: axes[1].spines[spine].set_color('#444')
axes[1].grid(alpha=0.15, color='white')
fig2.patch.set_facecolor('#1a1a2e')
plt.tight_layout()
plt.savefig('chart2_consistency.png', dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
plt.close()
print('Chart 2 saved: chart2_consistency.png')

# ── CHART 3: Qualifying vs Race Performance ───────────────────────────────────
fig3, axes = plt.subplots(1, 2, figsize=(16, 7))
fig3.patch.set_facecolor('#1a1a2e')

qual_race = dfRace[['FullName','TeamName','BestQual','GridPosition','Position']].dropna()
colors_qr = [TEAM_COLORS.get(t,'#aaa') for t in qual_race['TeamName']]

axes[0].scatter(qual_race['GridPosition'], qual_race['Position'], c=colors_qr, alpha=0.6, s=60)
axes[0].plot([1,20],[1,20], color='white', linestyle='--', alpha=0.4, label='Grid = Finish')
axes[0].set_xlabel('Grid Position (Qualifying)', color='white')
axes[0].set_ylabel('Race Finish Position', color='white')
axes[0].set_title('Grid Position vs Race Finish', color='white', fontweight='bold', fontsize=13)
axes[0].set_facecolor('#1a1a2e')
axes[0].tick_params(colors='white')
axes[0].invert_xaxis()
axes[0].invert_yaxis()
for spine in ['top','right']: axes[0].spines[spine].set_visible(False)
for spine in ['bottom','left']: axes[0].spines[spine].set_color('#444')
axes[0].grid(alpha=0.15, color='white')
patches = [mpatches.Patch(color=TEAM_COLORS[t], label=t) for t in TEAM_COLORS]
axes[0].legend(handles=patches, fontsize=7, facecolor='#2a2a3e', edgecolor='#444', labelcolor='white', ncol=2)

qual_race2 = qual_race.copy()
qual_race2['PosChange'] = qual_race2['GridPosition'] - qual_race2['Position']
avg_change = qual_race2.groupby('FullName')['PosChange'].mean().sort_values(ascending=False).head(15)
colors_ch = [TEAM_COLORS.get(driver_team.get(d,'McLaren'),'#aaa') for d in avg_change.index]
axes[1].barh(avg_change.index, avg_change.values, color=colors_ch, height=0.6)
axes[1].axvline(0, color='white', linewidth=0.8, alpha=0.5)
axes[1].set_xlabel('Avg Positions Gained (+) / Lost (−)', color='white')
axes[1].set_title('Qualifying → Race: Avg Position Change', color='white', fontweight='bold', fontsize=13)
axes[1].set_facecolor('#1a1a2e')
axes[1].tick_params(colors='white')
for spine in ['top','right']: axes[1].spines[spine].set_visible(False)
for spine in ['bottom','left']: axes[1].spines[spine].set_color('#444')
axes[1].grid(axis='x', alpha=0.15, color='white')
fig3.patch.set_facecolor('#1a1a2e')
plt.tight_layout()
plt.savefig('chart3_qual_vs_race.png', dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
plt.close()
print('Chart 3 saved: chart3_qual_vs_race.png')

# ── CHART 4: Team Performance ─────────────────────────────────────────────────
fig4, axes = plt.subplots(1, 2, figsize=(16, 7))
fig4.patch.set_facecolor('#1a1a2e')

team_cum = dfRace.groupby(['TeamName','Round'])['Points'].sum().reset_index()
team_cum = team_cum.sort_values(['TeamName','Round'])
team_cum['CumPoints'] = team_cum.groupby('TeamName')['Points'].cumsum()
top_teams = dfRace.groupby('TeamName')['Points'].sum().nlargest(8).index

for team in top_teams:
    d = team_cum[team_cum['TeamName'] == team]
    axes[0].plot(d['Round'], d['CumPoints'], marker='o', markersize=4, linewidth=2.5,
                 color=TEAM_COLORS.get(team,'#aaa'), label=team)
axes[0].set_xlabel('Round', color='white')
axes[0].set_ylabel('Cumulative Points', color='white')
axes[0].set_title('Constructor Championship Standings', color='white', fontweight='bold', fontsize=13)
axes[0].set_facecolor('#1a1a2e')
axes[0].tick_params(colors='white')
for spine in ['top','right']: axes[0].spines[spine].set_visible(False)
for spine in ['bottom','left']: axes[0].spines[spine].set_color('#444')
axes[0].grid(alpha=0.15, color='white')
axes[0].legend(fontsize=9, facecolor='#2a2a3e', edgecolor='#444', labelcolor='white')

driver_pts = dfRace.groupby(['TeamName','FullName'])['Points'].sum().reset_index()
driver_pts = driver_pts[driver_pts['TeamName'].isin(top_teams)]
driver_pts['LastName'] = driver_pts['FullName'].apply(lambda x: x.split()[-1])
teams_order = dfRace.groupby('TeamName')['Points'].sum().nlargest(8).index.tolist()

bottom_vals = {t: 0 for t in teams_order}
all_drivers = driver_pts['LastName'].unique()
driver_colors = plt.cm.Set2(np.linspace(0, 1, len(all_drivers)))
driver_color_map = dict(zip(all_drivers, driver_colors))

for _, row in driver_pts.iterrows():
    if row['TeamName'] in teams_order:
        idx = teams_order.index(row['TeamName'])
        axes[1].bar(idx, row['Points'], bottom=bottom_vals[row['TeamName']],
                    color=driver_color_map[row['LastName']], edgecolor='#1a1a2e', linewidth=0.5)
        if row['Points'] > 10:
            axes[1].text(idx, bottom_vals[row['TeamName']] + row['Points']/2,
                         row['LastName'], ha='center', va='center', fontsize=8, color='white', fontweight='bold')
        bottom_vals[row['TeamName']] += row['Points']

axes[1].set_xticks(range(len(teams_order)))
axes[1].set_xticklabels([t.replace(' Racing','').replace(' F1 Team','') for t in teams_order],
                         rotation=30, ha='right', color='white', fontsize=9)
axes[1].set_ylabel('Total Points', color='white')
axes[1].set_title('Driver Contributions by Team', color='white', fontweight='bold', fontsize=13)
axes[1].set_facecolor('#1a1a2e')
axes[1].tick_params(colors='white')
for spine in ['top','right']: axes[1].spines[spine].set_visible(False)
for spine in ['bottom','left']: axes[1].spines[spine].set_color('#444')
axes[1].grid(axis='y', alpha=0.15, color='white')
fig4.patch.set_facecolor('#1a1a2e')
plt.tight_layout()
plt.savefig('chart4_teams.png', dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
plt.close()
print('Chart 4 saved: chart4_teams.png')

print('\nAll charts saved!')