import streamlit as st
import pandas as pd
import base64

st.title('MLB Player Stats Explorer for Fantasy')

st.markdown("""
This app performs simple webscraping of MLB player stats data!
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [FantasyPros.com](https://www.fantasypros.com/mlb/stats/hitters.php).
""")
html = pd.read_html("https://www.fantasypros.com/mlb/stats/hitters.php")
df = html[0]
df = df.drop(columns=['VBR', 'Unnamed: 17', 'Unnamed: 18'])

def zScoreAdd(cat):
    zScore = []
    for player in df.index:
        zScore.append((df.iloc[player][cat]-df[cat].mean())/df[cat].std())
    df['z'+cat] = zScore
    df['z'+cat] = df['z'+cat].round(decimals=3)

categories = ['R', 'SB', 'RBI', 'AVG', 'HR']
for cat in categories:
    zScoreAdd(cat)

df['zTotal'] = (df.loc[0:df.shape[0], ['zR','zSB','zRBI','zAVG','zHR']].sum(axis=1))/5
df['zTotal'].round(decimals=3)
df.sort_values('zTotal', axis=0, ascending=False, inplace=True, na_position='first')
df = df.reset_index(drop=True)

st.header('Display Player Stats of All Teams in MLB')
st.text(f"This table calculates and adds the zScore for each fantasy baseball category:\n   Runs ['R'], Home Runs ['HR'], Runs Batted In ['RBI'], Stolen Bases ['SB']\n     and Batting Average ['AVG']")
st.text(f"There is an added z[category] column for each category.\nThis is the zScore of that specific category for that specific player.")
st.text(f"Example: {df.loc[0][0]} has {df.loc[0][2]} Runs and his zScore for runs is {df.loc[0][16]}.\nA score of zR = 0 would mean that Anthony Rizzo is exactly average.\n    However, a positive zR in this case means that\n        {df.loc[0][0]} is that much above average.\nThe zTotal is the average of all fantasy categories:\n          (zR + zHR + zRBI + zSB + zAVG)/5")
st.text(f"zScore for one category is calculated as:\n((specific players R)-(total R mean))/(total standard deviation of all players R)")
st.header(f"Batter Stats")
st.write('Data Dimensions: ', df.shape[0], ' rows and ', df.shape[1], ' columns.')
st.dataframe(df)
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df), unsafe_allow_html=True)


st.header("Starting Pitcher Stats")
st.text(f'*SV zScore is not taken into consideration*')
html = pd.read_html("https://www.fantasypros.com/mlb/stats/pitchers.php?range=2022")
df = html[0]
df = df.drop(columns=['VBR', 'Unnamed: 18', 'Unnamed: 19'])
df = df[df['Player'].str.contains('SP', regex=False, case=False, na=False)]
df.sort_values('K', axis=0, ascending=False, inplace=True, na_position='first')
df = df.reset_index(drop=True)


categories = ['K', 'W', 'SV']
for cat in categories:
    zScoreAdd(cat)

def zScorePitch(cat):
    zScore = []
    for player in df.index:
        value = (df.iloc[player][cat]-df[cat].mean())/df[cat].std()
        if value>0:
            value = -(abs(value))
        else:
            value = abs(value)
        zScore.append(value)
    df['z'+cat] = zScore
    df['z'+cat] = df['z'+cat].round(decimals=3)

categories = ['WHIP', 'ERA']
for cat in categories:
    zScorePitch(cat)
df['zTotal'] = (df.loc[0:df.shape[0], ['zK','zW','zERA','zWHIP']].sum(axis=1))/4
df['zTotal'].round(decimals=3)
df.sort_values('zTotal', axis=0, ascending=False, inplace=True, na_position='first')
df = df.reset_index(drop=True)
st.write('Data Dimensions: ', df.shape[0], ' rows and ', df.shape[1], ' columns.')
st.dataframe(df)
st.markdown(filedownload(df), unsafe_allow_html=True)






st.header("Relief Pitcher Stats")
st.text(f'*W zScore is not taken into consideration*')
html = pd.read_html("https://www.fantasypros.com/mlb/stats/pitchers.php?range=2022")
df = html[0]
df = df.drop(columns=['VBR', 'Unnamed: 18', 'Unnamed: 19'])
df = df[df['Player'].str.contains('RP', regex=False, case=False, na=False)]
df.sort_values('K', axis=0, ascending=False, inplace=True, na_position='first')
df = df.reset_index(drop=True)


categories = ['K', 'W', 'SV']
for cat in categories:
    zScoreAdd(cat)

def zScorePitch(cat):
    zScore = []
    for player in df.index:
        value = (df.iloc[player][cat]-df[cat].mean())/df[cat].std()
        if value>0:
            value = -(abs(value))
        else:
            value = abs(value)
        zScore.append(value)
    df['z'+cat] = zScore
    df['z'+cat] = df['z'+cat].round(decimals=3)

categories = ['WHIP', 'ERA']
for cat in categories:
    zScorePitch(cat)
df['zTotal'] = (df.loc[0:df.shape[0], ['zK','zSV','zERA','zWHIP']].sum(axis=1))/4
df['zTotal'].round(decimals=3)
df.sort_values('zTotal', axis=0, ascending=False, inplace=True, na_position='first')
df = df.reset_index(drop=True)
st.write('Data Dimensions: ', df.shape[0], ' rows and ', df.shape[1], ' columns.')
st.dataframe(df)


st.markdown(filedownload(df), unsafe_allow_html=True)