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
