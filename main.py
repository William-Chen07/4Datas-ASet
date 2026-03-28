import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import warnings

warnings.filterwarnings('ignore')

# ── LOAD DATA ──────────────────────────────────────────────────────────────────
dfLap = pd.read_csv("LapTimes.csv")
dfRace = pd.read_csv("RaceResults.csv")

# Qualifying time conversions
dfRace['Q1Seconds'] = pd.to_timedelta(dfRace['Q1']).dt.total_seconds()
dfRace['Q2Seconds'] = pd.to_timedelta(dfRace['Q2']).dt.total_seconds()
dfRace['Q3Seconds'] = pd.to_timedelta(dfRace['Q3']).dt.total_seconds()
dfRace['BestQual'] = dfRace[['Q1Seconds','Q2Seconds','Q3Seconds']].min(axis=1)
dfRace['IsTop10'] = (dfRace['Position'] <= 10).astype(int)
dfRace['PosChange'] = dfRace['GridPosition'] - dfRace['Position']

# Lap time conversions
dfLap['LapTimeSeconds'] = pd.to_timedelta(dfLap['LapTime']).dt.total_seconds()
dfLap['PitOutTimeSeconds'] = pd.to_timedelta(dfLap['PitOutTime']).dt.total_seconds()
dfLap['PitInTimeSeconds'] = pd.to_timedelta(dfLap['PitInTime']).dt.total_seconds()
dfLap['Sector1TimeSeconds'] = pd.to_timedelta(dfLap['Sector1Time']).dt.total_seconds()
dfLap['Sector2TimeSeconds'] = pd.to_timedelta(dfLap['Sector2Time']).dt.total_seconds()
dfLap['Sector3TimeSeconds'] = pd.to_timedelta(dfLap['Sector3Time']).dt.total_seconds()
dfLap['Sector1SessionTimeSeconds'] = pd.to_timedelta(dfLap['Sector1SessionTime']).dt.total_seconds()
dfLap['Sector2SessionTimeSeconds'] = pd.to_timedelta(dfLap['Sector2SessionTime']).dt.total_seconds()
dfLap['Sector3SessionTimeSeconds'] = pd.to_timedelta(dfLap['Sector3SessionTime']).dt.total_seconds()

# Top 10 summary
top_ten = dfRace[dfRace['Position'] <= 10].sort_values(by='TeamName')
#print(top_ten[['TeamName','Position','FullName','Location']].head(10))
#print(top_ten.groupby('TeamName').size().reset_index(name='Top 10 Count').to_string(index=False))
#print(top_ten[['Q1Seconds','Q2Seconds','Q3Seconds']])
#print(dfLap[['LapTimeSeconds','PitOutTimeSeconds','PitInTimeSeconds',
#             'Sector1TimeSeconds','Sector2TimeSeconds','Sector3TimeSeconds',
#            'Sector1SessionTimeSeconds','Sector2SessionTimeSeconds','Sector3SessionTimeSeconds']])

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

BG = '#0d1117'
PANEL = '#161b22'

# ── CHART 1: Driver Championship Standings ────────────────────────────────────
fig1, ax = plt.subplots(figsize=(16, 8))
fig1.patch.set_facecolor(BG)
ax.set_facecolor(BG)

cum = dfRace.sort_values(['FullName','Round'])
cum['CumPoints'] = cum.groupby('FullName')['Points'].cumsum()

for driver in top10_drivers:
    d = cum[cum['FullName'] == driver].sort_values('Round')
    color = TEAM_COLORS.get(driver_team.get(driver, 'McLaren'), '#ffffff')
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
plt.savefig('chart1_standings.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
#print('Chart 1 saved: chart1_standings.png')

# ── CHART 2: Top 10 Consistency ───────────────────────────────────────────────
fig2, axes = plt.subplots(1, 2, figsize=(16, 7))
fig2.patch.set_facecolor(BG)

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
axes[0].set_facecolor(BG)
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
    color = TEAM_COLORS.get(driver_team.get(row['FullName'],'McLaren'),'#aaa')
    axes[1].scatter(row['AvgPos'], row['TotalPoints'], color=color, s=100, zorder=5)
    axes[1].annotate(row['FullName'].split()[-1], (row['AvgPos'], row['TotalPoints']),
                     fontsize=8, color='white', ha='left', xytext=(4,2), textcoords='offset points')
axes[1].set_xlabel('Average Finish Position', color='white')
axes[1].set_ylabel('Total Points', color='white')
axes[1].set_title('Avg Position vs Total Points', color='white', fontweight='bold', fontsize=13)
axes[1].set_facecolor(BG)
axes[1].tick_params(colors='white')
axes[1].invert_xaxis()
for spine in ['top','right']: axes[1].spines[spine].set_visible(False)
for spine in ['bottom','left']: axes[1].spines[spine].set_color('#444')
axes[1].grid(alpha=0.15, color='white')
fig2.patch.set_facecolor(BG)
plt.tight_layout()
plt.savefig('chart2_consistency.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
#print('Chart 2 saved: chart2_consistency.png')

# ── CHART 3: Qualifying vs Race Performance ───────────────────────────────────
fig3, axes = plt.subplots(1, 2, figsize=(16, 7))
fig3.patch.set_facecolor(BG)

qual_race = dfRace[['FullName','TeamName','BestQual','Q1Seconds','Q2Seconds','Q3Seconds',
                     'GridPosition','Position','PosChange','Points','Round']].dropna(subset=['GridPosition','Position'])

colors_qr = [TEAM_COLORS.get(t,'#aaa') for t in qual_race['TeamName']]
axes[0].scatter(qual_race['GridPosition'], qual_race['Position'], c=colors_qr, alpha=0.6, s=60)
axes[0].plot([1,20],[1,20], color='white', linestyle='--', alpha=0.4)
axes[0].fill_between([1,20],[1,20],[0,0], alpha=0.04, color='#27F4D2')
axes[0].fill_between([1,20],[1,20],[21,21], alpha=0.04, color='#E8002D')
axes[0].text(16, 3, '← Gained positions', color='#27F4D2', fontsize=8, alpha=0.8)
axes[0].text(2, 17, 'Lost positions →', color='#E8002D', fontsize=8, alpha=0.8)
axes[0].set_xlabel('Grid Position (Qualifying)', color='white')
axes[0].set_ylabel('Race Finish Position', color='white')
axes[0].set_title('Grid Position vs Race Finish', color='white', fontweight='bold', fontsize=13)
axes[0].set_facecolor(BG)
axes[0].tick_params(colors='white')
axes[0].invert_xaxis()
axes[0].invert_yaxis()
for spine in ['top','right']: axes[0].spines[spine].set_visible(False)
for spine in ['bottom','left']: axes[0].spines[spine].set_color('#444')
axes[0].grid(alpha=0.15, color='white')
axes[0].legend(handles=[mpatches.Patch(color=TEAM_COLORS[t], label=t) for t in TEAM_COLORS],
               fontsize=7, facecolor='#2a2a3e', edgecolor='#444', labelcolor='white', ncol=2)

avg_change = qual_race.groupby('FullName')['PosChange'].mean().sort_values(ascending=False).head(15)
colors_ch = [TEAM_COLORS.get(driver_team.get(d,'McLaren'),'#aaa') for d in avg_change.index]
axes[1].barh(avg_change.index, avg_change.values, color=colors_ch, height=0.6)
axes[1].axvline(0, color='white', linewidth=0.8, alpha=0.5)
axes[1].set_xlabel('Avg Positions Gained (+) / Lost (−)', color='white')
axes[1].set_title('Qualifying → Race: Avg Position Change', color='white', fontweight='bold', fontsize=13)
axes[1].set_facecolor(BG)
axes[1].tick_params(colors='white')
for spine in ['top','right']: axes[1].spines[spine].set_visible(False)
for spine in ['bottom','left']: axes[1].spines[spine].set_color('#444')
axes[1].grid(axis='x', alpha=0.15, color='white')
fig3.patch.set_facecolor(BG)
plt.tight_layout()
plt.savefig('chart3_qual_vs_race.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
#print('Chart 3 saved: chart3_qual_vs_race.png')

# ── CHART 4: Team Performance ─────────────────────────────────────────────────
fig4, axes = plt.subplots(1, 2, figsize=(16, 7))
fig4.patch.set_facecolor(BG)

team_cum = dfRace.groupby(['TeamName','Round'])['Points'].sum().reset_index()
team_cum = team_cum.sort_values(['TeamName','Round'])
team_cum['CumPoints'] = team_cum.groupby('TeamName')['Points'].cumsum()
top_teams = dfRace.groupby('TeamName')['Points'].sum().nlargest(8).index.tolist()

for team in top_teams:
    d = team_cum[team_cum['TeamName'] == team]
    axes[0].plot(d['Round'], d['CumPoints'], marker='o', markersize=4, linewidth=2.5,
                 color=TEAM_COLORS.get(team,'#aaa'), label=team)
axes[0].set_xlabel('Round', color='white')
axes[0].set_ylabel('Cumulative Points', color='white')
axes[0].set_title('Constructor Championship Standings', color='white', fontweight='bold', fontsize=13)
axes[0].set_facecolor(BG)
axes[0].tick_params(colors='white')
for spine in ['top','right']: axes[0].spines[spine].set_visible(False)
for spine in ['bottom','left']: axes[0].spines[spine].set_color('#444')
axes[0].grid(alpha=0.15, color='white')
axes[0].legend(fontsize=9, facecolor='#2a2a3e', edgecolor='#444', labelcolor='white')

driver_pts = dfRace.groupby(['TeamName','FullName'])['Points'].sum().reset_index()
driver_pts = driver_pts[driver_pts['TeamName'].isin(top_teams)]
driver_pts['LastName'] = driver_pts['FullName'].apply(lambda x: x.split()[-1])
all_drivers = driver_pts['LastName'].unique()
driver_color_map = dict(zip(all_drivers, plt.cm.Set2(np.linspace(0, 1, len(all_drivers)))))

bottom_vals = {t: 0 for t in top_teams}
for _, row in driver_pts.iterrows():
    idx = top_teams.index(row['TeamName'])
    axes[1].bar(idx, row['Points'], bottom=bottom_vals[row['TeamName']],
                color=driver_color_map[row['LastName']], edgecolor=BG, linewidth=0.5)
    if row['Points'] > 10:
        axes[1].text(idx, bottom_vals[row['TeamName']] + row['Points']/2,
                     row['LastName'], ha='center', va='center', fontsize=8, color='white', fontweight='bold')
    bottom_vals[row['TeamName']] += row['Points']

axes[1].set_xticks(range(len(top_teams)))
axes[1].set_xticklabels([t.replace(' Racing','').replace(' F1 Team','') for t in top_teams],
                         rotation=30, ha='right', color='white', fontsize=9)
axes[1].set_ylabel('Total Points', color='white')
axes[1].set_title('Driver Contributions by Team', color='white', fontweight='bold', fontsize=13)
axes[1].set_facecolor(BG)
axes[1].tick_params(colors='white')
for spine in ['top','right']: axes[1].spines[spine].set_visible(False)
for spine in ['bottom','left']: axes[1].spines[spine].set_color('#444')
axes[1].grid(axis='y', alpha=0.15, color='white')
fig4.patch.set_facecolor(BG)
plt.tight_layout()
plt.savefig('chart4_teams.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
#print('Chart 4 saved: chart4_teams.png')

# ── CHART 5: Qualifying vs Race — Detailed ────────────────────────────────────
driver_summary = qual_race.groupby('FullName').agg(
    AvgGrid=('GridPosition','mean'),
    AvgFinish=('Position','mean'),
    AvgPosChange=('PosChange','mean'),
    AvgBestQual=('BestQual','mean'),
    Races=('Round','count'),
    TotalPoints=('Points','sum')
).reset_index()
driver_summary['TeamName'] = driver_summary['FullName'].map(driver_team)
driver_summary['LastName'] = driver_summary['FullName'].apply(lambda x: x.split()[-1])
driver_summary = driver_summary[driver_summary['Races'] >= 8]

fig = plt.figure(figsize=(22, 18))
fig.patch.set_facecolor(BG)
gs = GridSpec(3, 3, figure=fig, hspace=0.48, wspace=0.38)

ax1 = fig.add_subplot(gs[0, :2])
ax1.set_facecolor(PANEL)
for team in dfRace['TeamName'].unique():
    td = qual_race[qual_race['TeamName']==team].dropna(subset=['GridPosition','Position'])
    ax1.scatter(td['GridPosition'], td['Position'],
                color=TEAM_COLORS.get(team,'#aaa'), alpha=0.55, s=55, label=team)
ax1.plot([1,20],[1,20], color='white', linestyle='--', alpha=0.35, linewidth=1.5)
ax1.fill_between([1,20],[1,20],[0,0], alpha=0.04, color='#27F4D2')
ax1.fill_between([1,20],[1,20],[21,21], alpha=0.04, color='#E8002D')
ax1.text(16, 3, '← Gained positions', color='#27F4D2', fontsize=8, alpha=0.8)
ax1.text(2, 17, 'Lost positions →', color='#E8002D', fontsize=8, alpha=0.8)
ax1.set_xlabel('Grid Position (Qualifying)', color='white', fontsize=11)
ax1.set_ylabel('Race Finish Position', color='white', fontsize=11)
ax1.set_title('Grid Position vs Race Finish — Every Race', color='white', fontsize=13, fontweight='bold')
ax1.invert_xaxis(); ax1.invert_yaxis()
ax1.tick_params(colors='white')
for sp in ['top','right']: ax1.spines[sp].set_visible(False)
for sp in ['bottom','left']: ax1.spines[sp].set_color('#333')
ax1.grid(alpha=0.08, color='white', linestyle='--')
ax1.legend(fontsize=7.5, facecolor=BG, edgecolor='#333', labelcolor='white', ncol=2, loc='upper right')

ax2 = fig.add_subplot(gs[0, 2])
ax2.set_facecolor(PANEL)
ds_sorted = driver_summary.sort_values('AvgPosChange', ascending=False)
bars = ax2.barh(ds_sorted['LastName'], ds_sorted['AvgPosChange'],
                color=[TEAM_COLORS.get(t,'#aaa') for t in ds_sorted['TeamName']],
                edgecolor='none', height=0.65)
ax2.axvline(0, color='white', linewidth=0.8, alpha=0.5)
for bar, val in zip(bars, ds_sorted['AvgPosChange']):
    ax2.text(val + 0.1 if val >= 0 else val - 0.1,
             bar.get_y()+bar.get_height()/2, f'{val:+.1f}', va='center', color='white', fontsize=8)
ax2.set_xlabel('Avg Positions Gained (+) / Lost (−)', color='white', fontsize=10)
ax2.set_title('Race vs Qualifying\nPosition Change', color='white', fontsize=12, fontweight='bold')
ax2.tick_params(colors='white')
for sp in ['top','right']: ax2.spines[sp].set_visible(False)
for sp in ['bottom','left']: ax2.spines[sp].set_color('#333')
ax2.grid(axis='x', alpha=0.1, color='white', linestyle='--')

ax3 = fig.add_subplot(gs[1, 0])
ax3.set_facecolor(PANEL)
for _, row in driver_summary.iterrows():
    color = TEAM_COLORS.get(row['TeamName'],'#aaa')
    ax3.scatter(row['AvgBestQual'], row['TotalPoints'], color=color, s=110, zorder=5)
    ax3.annotate(row['LastName'], (row['AvgBestQual'], row['TotalPoints']),
                 fontsize=7.5, color='white', xytext=(4,2), textcoords='offset points')
ax3.set_xlabel('Avg Best Qualifying Time (s)', color='white', fontsize=10)
ax3.set_ylabel('Total Season Points', color='white', fontsize=10)
ax3.set_title('Qualifying Pace vs Points Scored', color='white', fontsize=12, fontweight='bold')
ax3.tick_params(colors='white')
for sp in ['top','right']: ax3.spines[sp].set_visible(False)
for sp in ['bottom','left']: ax3.spines[sp].set_color('#333')
ax3.grid(alpha=0.1, color='white', linestyle='--')

ax4 = fig.add_subplot(gs[1, 1])
ax4.set_facecolor(PANEL)
for _, row in driver_summary.iterrows():
    color = TEAM_COLORS.get(row['TeamName'],'#aaa')
    ax4.scatter(row['AvgGrid'], row['AvgFinish'], color=color, s=110, zorder=5)
    ax4.annotate(row['LastName'], (row['AvgGrid'], row['AvgFinish']),
                 fontsize=7.5, color='white', xytext=(4,2), textcoords='offset points')
ax4.plot([1,20],[1,20], color='white', linestyle='--', alpha=0.3, linewidth=1)
ax4.set_xlabel('Avg Grid Position', color='white', fontsize=10)
ax4.set_ylabel('Avg Finish Position', color='white', fontsize=10)
ax4.set_title('Avg Qualifying vs Avg Finish\n(below diagonal = gains places)', color='white', fontsize=12, fontweight='bold')
ax4.tick_params(colors='white')
for sp in ['top','right']: ax4.spines[sp].set_visible(False)
for sp in ['bottom','left']: ax4.spines[sp].set_color('#333')
ax4.grid(alpha=0.1, color='white', linestyle='--')

ax5 = fig.add_subplot(gs[1, 2])
ax5.set_facecolor(PANEL)
teams_ordered = dfRace.groupby('TeamName')['Points'].sum().nlargest(10).index.tolist()
pos_data = [qual_race[qual_race['TeamName']==t]['PosChange'].dropna().values for t in teams_ordered]
bp = ax5.boxplot(pos_data, vert=True, patch_artist=True, widths=0.6,
                 medianprops=dict(color='white', linewidth=2),
                 whiskerprops=dict(color='#666'), capprops=dict(color='#666'),
                 flierprops=dict(marker='o', markerfacecolor='#666', markersize=3, alpha=0.5))
for patch, team in zip(bp['boxes'], teams_ordered):
    patch.set_facecolor(TEAM_COLORS.get(team,'#aaa'))
    patch.set_alpha(0.8)
ax5.axhline(0, color='white', linewidth=0.8, alpha=0.4, linestyle='--')
ax5.set_xticklabels([t.replace(' Racing','').replace(' F1 Team','') for t in teams_ordered],
                     rotation=40, ha='right', color='white', fontsize=8)
ax5.set_ylabel('Positions Gained/Lost', color='white', fontsize=10)
ax5.set_title('Positions Gained per Team\n(median + spread)', color='white', fontsize=12, fontweight='bold')
ax5.tick_params(colors='white')
for sp in ['top','right']: ax5.spines[sp].set_visible(False)
for sp in ['bottom','left']: ax5.spines[sp].set_color('#333')
ax5.grid(axis='y', alpha=0.1, color='white', linestyle='--')

ax6 = fig.add_subplot(gs[2, :])
ax6.set_facecolor(PANEL)
top12 = driver_summary.sort_values('TotalPoints', ascending=False).head(12)['FullName'].tolist()
rounds = sorted(dfRace['Round'].unique())
locations = dfRace.groupby('Round')['Location'].first().to_dict()
heatmap = []
for driver in top12:
    row_vals = []
    for r in rounds:
        val = dfRace[(dfRace['FullName']==driver) & (dfRace['Round']==r)]['PosChange']
        row_vals.append(val.values[0] if len(val) > 0 else np.nan)
    heatmap.append(row_vals)
heatmap_arr = np.array(heatmap, dtype=float)

im = ax6.imshow(heatmap_arr, aspect='auto', cmap='RdYlGn', vmin=-8, vmax=8, interpolation='nearest')
ax6.set_xticks(range(len(rounds)))
ax6.set_xticklabels([locations[r] for r in rounds], rotation=45, ha='right', color='#aaa', fontsize=8)
ax6.set_yticks(range(len(top12)))
ax6.set_yticklabels([d.split()[-1] for d in top12], color='white', fontsize=9)
for i in range(len(top12)):
    for j in range(len(rounds)):
        val = heatmap_arr[i,j]
        if not np.isnan(val):
            ax6.text(j, i, f'{int(val):+d}', ha='center', va='center',
                     color='white' if abs(val) > 3 else '#333', fontsize=7, fontweight='bold')
plt.colorbar(im, ax=ax6, orientation='vertical', label='Positions Gained/Lost', shrink=0.8)
ax6.set_title('Positions Gained/Lost per Race — Green = Gained, Red = Lost', color='white', fontsize=12, fontweight='bold')
ax6.tick_params(colors='white')

plt.suptitle('Qualifying vs Race Performance Analysis', color='white', fontsize=18, fontweight='bold', y=1.01)
plt.savefig('qual_vs_race.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
#print('Chart 5 saved: qual_vs_race.png')

#print('\nAll charts saved!')
