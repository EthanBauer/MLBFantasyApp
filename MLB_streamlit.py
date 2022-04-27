from tkinter.tix import ROW
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import html5lib

st.title('MLB Player Stats Explorer for Fantasy')

st.markdown("""
This app performs simple webscraping of MLB player stats data!
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [Baseball-reference.com](https://www.baseball-reference.com/).
""")

# st.header('Year')
# selected_year = st.selectbox('',list(reversed(range(1950,2023))))

# Web scraping of NBA player stats
# @st.cache
# def load_data():
    # html1 = pd.read_html("https://www.baseball-reference.com/leagues/majors/2022-standard-batting.shtml")
html = pd.read_html("https://www.fantasypros.com/mlb/stats/hitters.php")
    # html = pd.read_html("https://www.baseball-reference.com/leagues/majors/2022-standard-batting.shtml")
    # df = html[0]
df = html[0]
df = df.drop(columns=['VBR', 'Unnamed: 17', 'Unnamed: 18'])
    # df1 = df.drop(df.index[0])
    # playerstats = df
    # raw = df.drop(df['Pos Summary'])
    # raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
    # playerstats = raw
    # return playerstats
    # return df
# df = load_data()

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



# # Sidebar - Team selection
# sorted_unique_team = sorted(playerstats.Tm.unique())
# selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# df_selected_team = playerstats[(playerstats.Tm.isin(selected_team))]

# df_selected_team.to_csv('output.csv', index=False)
# df_selected_team = pd.read_csv('output.csv')

st.header('Display Player Stats of All Teams in MLB')
st.write('Data Dimensions: ', df.shape[0], ' rows and ', df.shape[1], ' columns.')
st.dataframe(df)
# st.write('Data Dimension: ', df_selected_team.shape[0], ' rows and ', df_selected_team.shape[1], ' columns.')
# st.dataframe(df_selected_team)

# # Download NBA player stats data
# # https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df), unsafe_allow_html=True)

# # Heatmap
# if st.button('Intercorrelation Heatmap'):
#     st.header('Intercorrelation Matrix Heatmap')
#     df_selected_team.to_csv('output.csv',index=False)
#     df = pd.read_csv('output.csv')

#     corr = df.corr()
#     mask = np.zeros_like(corr)
#     mask[np.triu_indices_from(mask)] = True
#     with sns.axes_style("white"):
#         f, ax = plt.subplots(figsize=(7, 5))
#         ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
#     st.pyplot(f)
