#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aaa
python3

Create dataset of files from 1993-1994 through present of results.
Source: http://www.football-data.co.uk/englandm.php
12th Man Analysis
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



# Import data
path = '<file path>'
files = [
    str(path+'9394E0.csv'),
    str(path+'9495E0.csv'),
    str(path+'9596E0.csv'),
    str(path+'9697E0.csv'),
    str(path+'9798E0.csv'),
    str(path+'9899E0.csv'),
    str(path+'9900E0.csv'),
    str(path+'0001E0.csv'),
    str(path+'0102E0.csv'),
    str(path+'0203E0.csv'),
    str(path+'0304E0.csv'),
    str(path+'0405E0.csv'),
    str(path+'0506E0.csv'),
    str(path+'0607E0.csv'),
    str(path+'0708E0.csv'),
    str(path+'0809E0.csv'),
    str(path+'0910E0.csv'),
    str(path+'1011E0.csv'),
    str(path+'1112E0.csv'),
    str(path+'1213E0.csv'),
    str(path+'1314E0.csv'),
    str(path+'1415E0.csv'),
    str(path+'1516E0.csv'),
    str(path+'1617E0.csv'),
    str(path+'1718E0.csv')
]
data = pd.DataFrame()
seasons = []
for file in files:
    season = str(file[40:42]+'/'+file[42:44])
    print(season)
    seasons.append(season)
    df0 = pd.read_csv(file)
    df1 = df0.dropna(axis = 0, how = 'all')
    df2 = df1.dropna(axis = 1, how = 'all')
    df2['Season'] = season
    data = pd.concat([data, df2])



# Color scheme
homeColor = '#319E7C'
awayColor = '#D4533E'
drawColor = '#F1B416'


# All obs
# Count of home wins, away wins, and draws across all obs.
resultAllData = data['FTR'].value_counts()
# Fig 1 Pie chart of results across all obs.
fig1, ax1 = plt.subplots()
colors = [homeColor, awayColor, drawColor]
# Fig Title
ax1.set_title('Premier League Match Results', fontweight = 'bold')
# Plot type - Pie chart
ax1.pie(resultAllData, labels = ['Home Win', 'Away Win', 'Draw'], autopct='%1.1f%%',
        shadow=True, startangle=90, colors = colors, explode = (0.075, 0.05, 0.05))
# Equalize scale of x & y axis
ax1.axis('equal')
plt.show()

# Mean points per game for home teams across all obs
avgHomePPG = (resultAllData['H'] * 3 + resultAllData['D']) / (resultAllData['H'] + resultAllData['D'] + resultAllData['A'])
# Mean PPG for away teams across all obs
avgAwayPPG = (resultAllData['A'] * 3 + resultAllData['D']) / (resultAllData['H'] + resultAllData['D'] + resultAllData['A'])



# By Season
# Aggregate Home wins, Away wins, and draws by season
resultBySeason = pd.crosstab(data.Season, data.FTR)
# Calculate home win % of games, home PPG, away PPG
resultBySeason['homeWin'] = resultBySeason['H'] / (resultBySeason['H']
                            + resultBySeason['A'] + resultBySeason['D'])
resultBySeason['hPtsPerGame'] = (resultBySeason['H'] * 3 + resultBySeason['D']) / (
                                resultBySeason['H'] + resultBySeason['A'] 
                                + resultBySeason['D'])
resultBySeason['aPtsPerGame'] = (resultBySeason['A'] * 3 + resultBySeason['D']) / (
                                resultBySeason['H'] + resultBySeason['A'] 
                                + resultBySeason['D'])
# Sort by seasons list to get chronological ordering
resultBySeason = resultBySeason.reindex([seasons])
# Create dataset of home PPG vs away PPG for chart
hVsAPtsPerGameBySeason = resultBySeason[['hPtsPerGame','aPtsPerGame']]
# Fig 2 Scatter plot of Home vs Away Points Per Game Over Time
fig2, ax2 = plt.subplots()
# Title
ax2.set_title('Points Per Game', fontweight = 'bold')
# X-axis length to match number of seasons - labels added later
x = np.arange(len(hVsAPtsPerGameBySeason.index))
# Scatter plot of home PPG vs away PPG by season
ax2.scatter(x, hVsAPtsPerGameBySeason['hPtsPerGame'], c=homeColor, label = 'Home')
ax2.scatter(x, hVsAPtsPerGameBySeason['aPtsPerGame'], c=awayColor, label = 'Away')
# Add ticks and X label of seasons list
ax2.set_xticks(x)
ax2.set_xticklabels(seasons, rotation = 90)
ax2.set_xlabel('Season', weight='bold')
# Add legend and Y label
ax2.legend()
ax2.set_ylabel('Points Per Game', weight='bold')
ax2.yaxis.grid()
# Linear trend line for home PPG
z = np.polyfit(x, hVsAPtsPerGameBySeason['hPtsPerGame'], 1)
p = np.poly1d(z)
ax2.plot(x, p(x), c = homeColor, linestyle = ":")
# Linear trend line for away PPG
z = np.polyfit(x, hVsAPtsPerGameBySeason['aPtsPerGame'], 1)
p = np.poly1d(z)
ax2.plot(x, p(x), c = awayColor, linestyle = ":")
plt.show()



# By Team
# Aggregate results by Team
df1 = pd.crosstab(data.HomeTeam, data.FTR)
# Calculate home win %, home PPG by team
df1['hWinPct'] = df1['H'] / (df1['H'] + df1['A'] + df1['D'])
df1['hPPG'] = (df1['H'] * 3 + df1['D'])/ (df1['H'] + df1['A'] + df1['D'])
df1 = df1.rename(columns={'H':'hW', 'A':'hL', 'D':'hD'})
df2 = pd.crosstab(data.AwayTeam, data.FTR)
# Calculate away win %, PPG by team
df2['aWinPct'] = df2['A'] / (df2['H'] + df2['A'] + df2['D'])
df2['aPPG'] = (df2['A'] * 3 + df2['D'])/ (df2['H'] + df2['A'] + df2['D'])
df2 = df2.rename(columns={'H':'aL', 'A':'aW', 'D':'aD'})
# Concatenate dataframes
resultsByTeam = pd.concat([df1, df2], axis = 1)
# Count number of games for each team
resultsByTeam['n'] = resultsByTeam['hW'] + resultsByTeam['hL'] + resultsByTeam['hD'] + resultsByTeam['aW'] + resultsByTeam['aL'] + resultsByTeam['aD']
# Generate list of unique teams in data
teams = list(data['HomeTeam'].unique())
# Add big-6 categorical
big6 = ['Arsenal', 'Chelsea', 'Liverpool', 'Man City', 'Man United', 'Tottenham']
resultsByTeam['big6'] = resultsByTeam.index.map(lambda x: x in big6)
# Calculate big6 vs non-big6 averages
df1 = pd.pivot_table(resultsByTeam, values=['hW', 'hL', 'hD', 'aW', 'aL', 'aD'], index=['big6'], aggfunc=np.sum)
df1['hWinPct'] = (df1['hW'])/ (df1['hW'] + df1['hL'] + df1['hD'])
df1['hPPG'] = (df1['hW'] * 3 + df1['hD'])/ (df1['hW'] + df1['hL'] + df1['hD'])
df1['aWinPct'] = (df1['aW'])/ (df1['aW'] + df1['aL'] + df1['aD'])
df1['aPPG'] = (df1['aW'] * 3 + df1['aD'])/ (df1['aW'] + df1['aL'] + df1['aD'])
df1['n'] = df1['hW'] + df1['hL'] + df1['hD'] + df1['aW'] + df1['aL'] + df1['aD']
# Rename indexes
df1 = df1.rename({0:'Non Big-6 Avg.', 1:'Big-6 Avg.'})
# Reorder columns to concatenate
df1.reindex_axis(['hW', 'hD', 'hL', 'hWinPct', 'hPPG', 'aW', 'aD', 'aL', 'aWinPct', 'aPPG', 'n'])
# Concatenate big-6 and non big-6 to dataset by teams
resultsByTeamWBig6Avg = pd.concat([resultsByTeam, df1])
# Calculate home PPG - away PPG
resultsByTeamWBig6Avg['hVsADiff'] = resultsByTeamWBig6Avg['hPPG'] - resultsByTeamWBig6Avg['aPPG']

# Fig 3 list/scatter of home and away PPG by team - ordered by home PPG
# Sort dataframe by home PPG
resultsByTeamWBig6Avg = resultsByTeamWBig6Avg.sort_values(['hPPG'], ascending=False)
# Generate position var to order data in scatter plot
resultsByTeamWBig6Avg['pos'] = np.arange(len(resultsByTeamWBig6Avg.index)-1, -1, -1)
# Generate team var to label ticks
resultsByTeamWBig6Avg['team'] = resultsByTeamWBig6Avg.index
# Fig size
fig3, ax3 = plt.subplots(figsize=(6, 12))
# X axis points of home PPG and away PPG
x1 = resultsByTeamWBig6Avg['hPPG']
x2 = resultsByTeamWBig6Avg['aPPG']
# Y axis order by position var
y = resultsByTeamWBig6Avg['pos']
# Title
ax3.set_title('Points Per Game - Home vs Away', fontweight = 'bold')
# Scatter plot of home and away PPG
ax3.scatter(x1, y, c=homeColor, label = 'Home', alpha=0.6)
ax3.scatter(x2, y, c=awayColor, label = 'Away', alpha=0.6)
# Add y ticks
ax3.set_yticks(y, minor=True)
# Remove default tick label format
ax3.yaxis.set_major_formatter(plt.NullFormatter())
# Add y tick labels
ylabels = list(resultsByTeamWBig6Avg['team'])
ax3.set_yticklabels(ylabels, minor=True)
# Add legend
ax3.legend()
# Add gridlines
ax3.grid(which='minor', linestyle=':')
plt.show()


# Fig 4 Scatter plot of home PPG versus away PPG by team
fig4, ax4 = plt.subplots(figsize=(7.5, 5))
# X axis = home PPG by team
x = resultsByTeam['hPPG']
# Y axis = away PPG by team
y = resultsByTeam['aPPG']
# Size points by number of obs
size = resultsByTeam['n']
# Title
ax4.set_title('Points Per Game by Team', fontweight = 'bold')
# Scatter plot
ax4.scatter(x, y, s=size, c=drawColor, alpha=0.6)
# X and Y Labels
ax4.set_xlabel('Home', weight='bold')
ax4.set_ylabel('Away', weight='bold')
# Add away PPG line
y_mean = [avgAwayPPG]*len(x)
ax4.plot(x, y_mean, linestyle='-', c=awayColor, alpha=0.5)
# Add home PPG line
x_mean = [avgHomePPG]*len(y)
ax4.plot(x_mean, y, linestyle='-', c=homeColor, alpha=0.5)
ax4.text(1.68, 0.4, 'Above Avg. Home, Below Avg. Away')
# Create labels for average PPG lines
ax4.text(2.1, 1.0, 'Avg. Away PPG', style='italic')
ax4.text(1.5, 1.87, 'Avg. Home PPG', style='italic')
# Create labels for quadrants
ax4.text(.87, 1.75, 'Below Avg. Home, Above Avg. Away')
ax4.text(1.8, 1.75, 'Above Avg. Home & Away')
ax4.text(1.0, 0.4, 'Below Avg. Home & Away')





# by ELO
# ELO Calculation
# Set all ELOs to start at 1500, home field advantage to 0, number of games to 0
eloDict = {}
for team in teams:
    eloDict[team] = {'hUnscaled':1500, 'hScaled':1500, 'hfaScaled':0, 
                     'hfaUnscaled':0, 'nUnscaled': 0, 'nScaled': 0, 
                     'aUnscaled':1500, 'aScaled':1500}
hfaHistory = {}
for team in teams:
    hfaHistory[team] = {}

def eloInputs(marginForHomeTeam):
    # Inputs: name of home team, away team, and what the goal margin was for 
    # home team (home goals scored - away goals scored)
    # Outputs: outcome for home, outcome for away, k factor, and scaling factor
    # outcome range 1 win, 0.5 draw, 0 loss 
    if marginForHomeTeam >= 1:
        outcomeH = 1
        outcomeA = 0
    elif marginForHomeTeam  == 0:
        outcomeH = 0.5
        outcomeA = 0.5
    else:
        outcomeH = 0
        outcomeA = 1
    # k factor = 15 - via http://pena.lt/y/2013/02/07/applying-elo-ratings-to-football/
    k = 15
    # scaled by goal margin for game played
    scaling = 1
    goalDiff = abs(marginForHomeTeam)
    if goalDiff <= 1: scaling = 1
    elif goalDiff == 2: scaling = 1.51
    elif goalDiff== 3: scaling = 1.85
    elif goalDiff== 4: scaling = 2.11
    elif goalDiff == 5: scaling = 2.32
    elif goalDiff == 6: scaling = 2.49
    elif goalDiff == 7: scaling = 2.64
    elif goalDiff == 8: scaling = 2.77
    elif goalDiff == 9: scaling = 2.88
    elif goalDiff >= 10: scaling = 2.99
    
    return outcomeH, outcomeA, k, scaling

def eloCalc(homeTeam, awayTeam, marginForHomeTeam):
        # Inputs: home team, away team, and margin for team
        # Calls: eloInputs to get equation input values
        # Calculates change in ELO
        # Updates: ELO dictionaries
        # Output: no meaningful return value
        
        # Call eloInputs
        outcomeH, outcomeA, k, scaling = eloInputs(marginForHomeTeam)
        # ELO calculation
        def _calc(hELO, hAwayELO, hfa, n, aELO, outcomeH, outcomeA, k, scaling):
            # Inputs: home ELO (home team), away ELO (away team),
            #        running total of delta between hELO(hTeam) - aELO(hTeam)
            #        n games played
            #        away ELO
            #        outcome h and a, k, scaling
            # Calculates: expected outcome (h & a), new delta between hELO(hTeam) - aELO(hTeam)
            #             new ELO (h & a), adds +1 to n
            # Returns: new ELO (h & a), new hfa delta, and new n
            # home and away expected outcome
            hExpectedOutcome = 1 / (1 + 10 **  ((aELO - hELO) / 400))
            aExpectedOutcome = 1 / (1 + 10 **  ((hELO - aELO) / 400))
            # home change in ELO calc
            hELO = hELO + k * scaling * (outcomeH - hExpectedOutcome)
            # add difference in home ELO (home team) - away ELO (home team) to running total
            hfa += hELO - hAwayELO
            # add 1 to games played
            n += 1
            # calculate away ELO
            aELO = aELO + k * scaling * (outcomeA - aExpectedOutcome)
            return hELO, hfa, n, aELO
        # Unscaled - call _calc with inputs for unscaled ELO
        eloDict[homeTeam]['hUnscaled'], eloDict[homeTeam]['hfaUnscaled'], eloDict[homeTeam]['nUnscaled'], eloDict[awayTeam]['aUnscaled'] = _calc(
                eloDict[homeTeam]['hUnscaled'], eloDict[homeTeam]['aUnscaled'], 
                eloDict[homeTeam]['hfaUnscaled'], eloDict[homeTeam]['nUnscaled'], 
                eloDict[awayTeam]['aUnscaled'], outcomeH, outcomeA, k, 1) 
        
        # Scaled - call _calc with inputs for scaled ELO
        eloDict[homeTeam]['hScaled'],  eloDict[homeTeam]['hfaScaled'], eloDict[homeTeam]['nScaled'], eloDict[awayTeam]['aScaled'] = _calc(eloDict[homeTeam]['hScaled'], eloDict[homeTeam]['aScaled'], 
                eloDict[homeTeam]['hfaScaled'], eloDict[homeTeam]['nScaled'], 
               eloDict[awayTeam]['aScaled'],
              outcomeH, outcomeA, k, scaling) 
# Create copy of originat dataset
eloData = data.copy()
# Convert date to pandas date type
eloData['Date'] = pd.to_datetime(eloData['Date'], dayfirst = True)
# Order by date chronologically
eloData = eloData.sort_values(by = 'Date')
# Loop through data chronologically to get ELO
for match in eloData.itertuples():
    #print('\n')
    #print('H:', match.HomeTeam)
    #print('A:', match.AwayTeam)
    #print('H - Old hELO:', eloDict[match.HomeTeam]['hUnscaled'])
    #print('A - Old aELO:', eloDict[match.AwayTeam]['aUnscaled'])
    eloCalc(match.HomeTeam, match.AwayTeam, match.FTHG - match.FTAG)
    hfaHistory[match.HomeTeam][match.Date] = (eloDict[match.HomeTeam]['hScaled']-eloDict[match.HomeTeam]['aScaled'])
    #print('H - New hELO:', eloDict[match.HomeTeam]['hUnscaled'])
    #print('A - New aELO:', eloDict[match.AwayTeam]['aUnscaled'])

# Create dataframe of ELO values at present
eloResults = pd.DataFrame(eloDict)
eloResults = pd.DataFrame.transpose(eloResults)
# Calculate mean delta between home ELO - away ELO for each team
eloResults['avgHfaUnscaled'] = eloResults['hfaUnscaled'] / eloResults['nUnscaled']
eloResults['avgHfaScaled'] = eloResults['hfaScaled'] / eloResults['nScaled']

# Calculate average home field advantage across all obs
avgELOAdvScaled = eloResults.hfaScaled.sum() / eloResults.nScaled.sum()

# Fig 5 scatter plot of elo HFA by team
# Sort teams by mean HFA scaled
eloResults = eloResults.sort_values(['avgHfaScaled'], ascending=False)
# Create ordering variable
eloResults['pos'] = np.arange(len(eloResults.index)-1, -1, -1)
# Create team variable for labels
eloResults['team'] = eloResults.index
# Size of figure
fig5, ax5 = plt.subplots(figsize=(8, 12))
# X axis = home field advantage values
x = eloResults['avgHfaScaled']
# Y axis  = order from pos
y = eloResults['pos']
# NOT USED - Size by number of obs -
size = eloResults['nScaled']
# Title
ax5.set_title('ELO Home Field Advantage', fontweight = 'bold')
# Plot
ax5.scatter(x, y, s=120, c=homeColor, alpha=0.6)
# X label
ax5.set_xlabel('Average ELO Outperformance at Home', weight='bold')
# Add Y ticks
ax5.set_yticks(y, minor=True)
# Remove default Y tick label
ax5.yaxis.set_major_formatter(plt.NullFormatter())
# Add team names as labels
ylabels = list(eloResults['team'])
ax5.set_yticklabels(ylabels, minor=True)
# Add Grid
ax5.grid(which='minor', linestyle=':')
# Add average elo hfa line
x_mean = [avgELOAdvScaled]*len(y)
ax5.plot(x_mean, y, linestyle='--', c=awayColor, alpha=0.5)
# Add label for average elo  hfa line
ax5.text(68, 49.75, 'Avg: +77', style='italic')


# Chart hfa by team over time
hfaTimeSeries = pd.DataFrame(hfaHistory)

fig6, axes = plt.subplots(nrows=9, ncols = 1, figsize=(5, 15), sharey=True, sharex=True)
highlight = ['Newcastle', 'Stoke', 'Southampton', 'Fulham', 'Liverpool', 
             'Man United', 'Man City', 'Arsenal', 'Tottenham']
colors = ['#000000', '#D0122D', '#D41E29', '#121212', '#E0202C', 
          '#DC1F29', '#99C5E7', '#EC0C1C', '#11214B']
i = 0
for ax in axes:
    x = hfaTimeSeries.index
    y = hfaTimeSeries[highlight[i]]
    ax.scatter(x, y, s=5, c=colors[i], alpha=0.6)
    ax.set_title(highlight[i])
    i += 1
fig6.tight_layout()
