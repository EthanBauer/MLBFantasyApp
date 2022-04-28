import streamlit as st
import pandas as pd
import base64

st.title('MLB Player Stats Explorer for Fantasy')

st.markdown("""
This app performs simple webscraping of MLB player stats data!
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [Baseball-reference.com](https://www.baseball-reference.com/).
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

df['zTotal'] = df.loc[0:df.shape[0], ['zR','zSB','zRBI','zAVG','zHR']].sum(axis=1)
df['zTotal'].round(decimals=3)
df.sort_values('zTotal', axis=0, ascending=False, inplace=True, na_position='first')
df = df.reset_index(drop=True)

st.header('Display Player Stats of All Teams in MLB')
st.write('Data Dimensions: ', df.shape[0], ' rows and ', df.shape[1], ' columns.')
st.dataframe(df)
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df), unsafe_allow_html=True)
