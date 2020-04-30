#!/usr/bin/env python
# coding: utf-8

# In[89]:


import pandas as pd
import time
import numpy as np
import plotly.offline as pyo
import plotly.graph_objs as go
import plotly.express as px


# In[10]:


def get_nfl_pfr_fantasy(year):
    
    # courtesy sleep between calls
    time.sleep(5)
    print(year)
    # read html of the year
    df = pd.read_html(f'https://www.pro-football-reference.com/years/{year}/fantasy.htm',
                     header=[0,1])
    # returns a list of dataframes
    df1 = df[0]
    # Clean columns, columns are multi-indexed
    cols = [col[0]+ '_' + col[1] for col in df1.columns.tolist()]
    df1.columns = cols
    df1 = df1.rename(columns={
        'Unnamed: 0_level_0_Rk':'Rank',
        'Unnamed: 1_level_0_Player':'Player',
        'Unnamed: 2_level_0_Tm':'Team',
        'Unnamed: 3_level_0_FantPos': 'FantPos',
        'Unnamed: 4_level_0_Age':'Age'
    })
    # Filter out their column names that are used in rows to scroll down page
    df1 = df1[df1['Rank'] != 'Rk']
    # Adjust the datatypes
    for i in df1.columns:
        if i == 'Player' or i == 'Team' or i == 'FantPos':
            continue
        df1[i] = df1[i].astype(float)
    # Clean up player names
    df1.Player = df1.Player.str.replace("[*+]",'')
    df1.FantPos = df1.FantPos.str.upper()
    df1['Year'] = int(year)
    return df1


# In[13]:


dfs = [get_nfl_pfr_fantasy(year) for year in range(2010, 2020)]


# In[14]:


df = pd.concat(dfs)


# In[27]:


df['Fantasy_PPR'] = df['Fantasy_PPR'].fillna(0)
df = df[df['Fantasy_PPR'] > 25]


# In[193]:


df.sort_values(by='Fantasy_PPR', ascending=False)


# In[29]:


df.Team.unique()


# In[30]:


df[df['Team'] == '3TM']


# In[43]:


df[df['Player'] == 'Michael Thomas']


# In[195]:


df.columns


# In[22]:


import pandas as pd
import numpy as np


# In[3]:



df = pd.read_html(f'https://www.pro-football-reference.com/players/K/KirkCh01/gamelog/',
                 header=[0,1])
  


# In[7]:


df = df[0]


# In[8]:


df.head()


# In[184]:


df1 = df.copy()


# In[11]:


cols = [col[0]+ '_' + col[1] for col in df.columns.tolist()]
df.columns = cols
df = df.rename(columns={
    'Unnamed: 0_level_0_Rk':'Rank',
    'Unnamed: 1_level_0_Year':'Year',
    'Unnamed: 2_level_0_Date':'Date',
    'Unnamed: 3_level_0_G#': 'Game_Num',
    'Unnamed: 4_level_0_Week':'Week',
    'Unnamed: 5_level_0_Age':'Age',
    'Unnamed: 6_level_0_Tm':'Team',
    'Unnamed: 7_level_0_Unnamed: 7_level_1':'Home',
    'Unnamed: 8_level_0_Opp':'Opponent',
    'Unnamed: 9_level_0_Result':'Result',
    'Unnamed: 10_level_0_GS':'Started'
})


# In[12]:


df.columns


# In[13]:


df.iloc[0,:]


# In[25]:


df = df[df['Rank'] != 'Rk']
df = df.iloc[:-1,:]


# In[27]:


df['Rank'] = df['Rank'].astype(int)
df['Year'] = df['Year'].astype(int)
df['Game_Num'] = df['Game_Num'].astype(int)
df['Week'] = df['Week'].astype(int)
df['Age'] = df['Age'].astype(float)
df['Home'] = np.where(df['Home']=='@', 0, 1)
df['Started'] = np.where(df['Started']=='*', 1, 0)
df.Receiving_Tgt = df.Receiving_Tgt.astype(float)
df.Receiving_Rec = df.Receiving_Rec.astype(float)
df.Receiving_Yds = df.Receiving_Yds.astype(float)
df['Receiving_Y/R'] = df['Receiving_Y/R'].astype(float)
df.Receiving_TD = df.Receiving_TD.astype(int)
df['Punt Returns_Ret'] = df['Punt Returns_Ret'].astype(float)
df['Punt Returns_Yds'] =df['Punt Returns_Yds'].astype(float)
df['Punt Returns_Y/R'] =df['Punt Returns_Y/R'].astype(float)
df['Punt Returns_TD'] =df['Punt Returns_TD'].astype(float)
df['Scoring_2PM'] = df['Scoring_2PM'].astype(float)
df['Scoring_TD'] = df['Scoring_TD'].astype(float)
df['Off. Snaps_Num'] = df['Off. Snaps_Num'].astype(int)
df['Off. Snaps_Pct'] = df['Off. Snaps_Pct'].str.replace("%",'')
df['Off. Snaps_Pct'] = df['Off. Snaps_Pct'].astype(float)


# In[102]:


def clean_player_logs(player):
    df = pd.read_html(f'https://www.pro-football-reference.com/players/{player[0]}/{player}/gamelog/',
                     header=[0,1])
    df = df[0]

    cols = [col[0]+ '_' + col[1] for col in df.columns.tolist()]
    df.columns = cols
    df = df.rename(columns={
        'Unnamed: 0_level_0_Rk':'Rank',
        'Unnamed: 1_level_0_Year':'Year',
        'Unnamed: 2_level_0_Date':'Date',
        'Unnamed: 3_level_0_G#': 'Game_Num',
        'Unnamed: 4_level_0_Week':'Week',
        'Unnamed: 5_level_0_Age':'Age',
        'Unnamed: 6_level_0_Tm':'Team',
        'Unnamed: 7_level_0_Unnamed: 7_level_1':'Home',
        'Unnamed: 8_level_0_Opp':'Opponent',
        'Unnamed: 9_level_0_Result':'Result',
        'Unnamed: 10_level_0_GS':'Started'
    })

    df = df[df['Rank'] != 'Rk']
    df = df.iloc[:-1,:]
    '''
    df['Rank'] = df['Rank'].astype(float)
    df['Year'] = df['Year'].astype(float)
    df['Game_Num'] = df['Game_Num'].astype(float)
    df['Week'] = df['Week'].astype(float)
    df['Age'] = df['Age'].astype(float)
    df['Home'] = np.where(df['Home']=='@', 0, 1)
    df['Started'] = np.where(df['Started']=='*', 1, 0)
    df.Receiving_Tgt = df.Receiving_Tgt.astype(float)
    df.Receiving_Rec = df.Receiving_Rec.astype(float)
    df.Receiving_Yds = df.Receiving_Yds.astype(float)
    df['Receiving_Y/R'] = df['Receiving_Y/R'].astype(float)
    df.Receiving_TD = df.Receiving_TD.astype(float)
    df['Off. Snaps_Num'] = df['Off. Snaps_Num'].astype(float)
    df['Off. Snaps_Pct'] = df['Off. Snaps_Pct'].str.replace("%",'')
    df['Off. Snaps_Pct'] = df['Off. Snaps_Pct'].astype(float)
    '''
    return df


# In[90]:


df1 = clean_player_logs('FitzLa00')


# In[91]:


df1


# In[92]:


import os


# In[44]:


os.chdir('C:/Users/e143426/FF')


# In[103]:


players = pd.read_csv('players.csv')


# In[104]:


players
players['Unnamed: 3'] = players['Unnamed: 3'].str.upper()
players = players[(players['Unnamed: 3'] == 'WR') | (players['Unnamed: 3'] == 'RB') | (players['Unnamed: 3'] == 'TE') ]


# In[105]:


player_list = players['Unnamed: 1'].values.tolist()


# In[96]:


player_list


# In[106]:


clean_players = []


# In[107]:


for i in player_list:
    var = i.split('\\')
    if len(var) > 1:
        clean_players.append(var)
                               


# In[99]:


clean_players


# In[108]:


player_list_for_df = []


# In[109]:


for i in clean_players:
    print(i)
    time.sleep(5)
    x = clean_player_logs(i[1])
    x['Player'] = i[0]
    player_list_for_df.append(x)


# In[110]:


len(player_list_for_df)


# In[111]:


df_player = pd.concat(player_list_for_df)


# In[112]:


df_player.shape


# In[113]:


df_player.columns


# In[126]:


keep = ['Rank', 'Year', 'Date', 'Game_Num', 'Week', 'Age', 'Team',
        'Home', 'Opponent', 'Result', 'Started', 'Rushing_Att',
        'Rushing_Yds',
       'Rushing_Y/A', 'Rushing_TD', 'Receiving_Tgt', 'Receiving_Rec',
       'Receiving_Yds', 'Receiving_Y/R', 'Receiving_TD', 'Receiving_Ctch%',
       'Receiving_Y/Tgt', 'Passing_Cmp', 'Passing_Att', 'Passing_Cmp%', 
        'Passing_Yds','Passing_TD','Passing_Int','Passing_Rate','Passing_Sk',
        'Passing_Yds.1', 'Passing_Y/A', 'Passing_AY/A', 'Off. Snaps_Num', 'Off. Snaps_Pct']


# In[127]:


df_player1 = df_player.copy()
df_player1 = df_player1[keep]


# In[117]:


df_player1.iloc[0,:]


# In[128]:


df_player1['Home'] = np.where(df_player1['Home'] == '@', 0, 1)
df_player1['Started'] = np.where(df_player1['Started'] == '*', 1, 0)
df_player1['Receiving_Ctch%'] = df_player1['Receiving_Ctch%'].str.replace("%","")
df_player1['Passing_Cmp%'] = df_player1['Passing_Cmp%'].str.replace("%","")


# In[129]:


df_player1['Off. Snaps_Pct'] = df_player1['Off. Snaps_Pct'].str.replace("%","")


# In[130]:


for i in df_player1.columns:
    try:
        df_player1[i] = df_player1[i].astype(float)
    except:
        print(i)


# In[131]:


df_player1['Receiving_Ctch%'] = df_player1['Receiving_Ctch%']/100
df_player1['Passing_Cmp%'] = df_player1['Passing_Cmp%']/100
df_player1['Off. Snaps_Pct'] = df_player1['Off. Snaps_Pct']/100


# In[133]:


df_player1['Player'] = df_player['Player'].str.replace("[*+]",'')


# In[134]:


df_player1.to_csv('player_game_logs_pfr.csv')


# In[ ]:




