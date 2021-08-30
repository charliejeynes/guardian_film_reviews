#import SessionState
import streamlit as st
import numpy as np
import pandas as pd
import requests
import io

st.title('Guardian Film Review Database')
st.write("This website enables you to browse all of the Guardian's film reviews since 2000-present")
st.write("You can use the sidebar to filter results")

@st.cache(ttl=60, max_entries=20)
def get_data(filter=None):
    url = "https://raw.githubusercontent.com/charliejeynes/guardian_film_reviews/main/data/all_reviews.csv" # Make sure the url is the raw version of the file on GitHub
    download = requests.get(url).content
    df1 = pd.read_csv(io.StringIO(download.decode('utf-8')))
    df1 = df1.replace(np.nan, 'N/A', regex=True)
    pd.set_option('display.max_colwidth', -1)
    def make_clickable(link):
        # target _blank to open new window
        # extract clickable text to display for your link
        text = link
        return f'<a target="_blank" href="{link}">{text}</a>'
    # link is the column with hyperlinks
    df1['link'] = df1['shortUrl'].apply(make_clickable)
    df1 = df1[['Film name & headline', 'link', 'starRating', 'critic', 'date']]
    df1 = df1.drop_duplicates(subset=['link'], keep='last')
    df1 = df1.sort_values(by='date', ascending=False)
    if filter==film_search:
        df1 = df1[df1['Film name & headline'].str.contains(film_search, case=False) == True]
        rows = len(df1)
        df1 = df1.to_html(escape=False)
        return df1, rows
    elif filter==critic_select:
        df1 = df1[df1['critic'].str.contains(critic_select, case=False) == True]
        rows = len(df1)
        df1 = df1.to_html(escape=False)
        return df1, rows
    elif filter==starRating:
        df1 = df1[df1['starRating'].astype(str) == starRating]
        rows = len(df1)
        df1 = df1.to_html(escape=False)
        return df1, rows
    elif filter==[starRating, critic_select]:
        df1 = df1[(df1['critic'].str.contains(critic_select, case=False) == True) & (df1['starRating'].astype(str) == starRating)]
        rows = len(df1)
        df1 = df1.to_html(escape=False)
        return df1, rows
    else:
        rows = len(df1)
        df_pd = df1
        df1 = df1.to_html(escape=False)
        return df1, rows, df_pd

# title for film
st.sidebar.title("Search for a film")
film_search = st.sidebar.text_input("Search for a film")
# critics
st.sidebar.title("Filter by critic")
options_critic = {'select all' : '', 'Peter Bradshaw': 'Peter Bradshaw', 'Wendy Ide': 'Wendy Ide'}
critic_select = st.sidebar.selectbox("Select Critic", ('', 'Peter Bradshaw', 'Wendy Ide'))
# by starRating
st.sidebar.title("Filter by starRating")
starRating = st.sidebar.selectbox("Select starRating", ('', '1.0', '2.0', '3.0', '4.0', '5.0', 'N/A'))
# create user inputs options
if film_search:
    df1, rows = get_data(filter=film_search)
    st.write("There are {} reviews in the table below".format(rows))
    st.write(df1, unsafe_allow_html=True)
elif critic_select and starRating == '':
    df1, rows = get_data(filter=critic_select)
    st.write("There are {} reviews in the table below".format(rows))
    st.write(df1, unsafe_allow_html=True)
elif starRating and critic_select=='':
    df1, rows = get_data(filter=starRating)
    st.write("There are {} reviews in the table below. I'm at starRating".format(rows))
    st.write(df1, unsafe_allow_html=True)
elif starRating and critic_select:
    df1, rows = get_data(filter=[starRating, critic_select])
    st.write("There are {} reviews in the table below. I'm at starRating+critic_select".format(rows))
    st.write(starRating, critic_select)
    st.write(df1, unsafe_allow_html=True)
else:
    df1, rows, df_pd = get_data()
    clicked = st.button('click here to show all Guardian Film Reviews (takes about 5 seconds to load)')
    if clicked:
        st.write("There are currently {} Guardian Film reviews. The below table shows all of these.".format(rows))
        st.write(df1, unsafe_allow_html=True)
    else:
        st.write("There are currently {} Guardian Film reviews. The below table shows a sample of these".format(rows))
        st.write(df_pd.head(100).to_html(escape=False), unsafe_allow_html=True)








# # def add_stream_url(track_ids):
# # 	return [f'https://open.spotify.com/track/{t}' for t in track_ids]
# def make_clickable(url, text):
#     return f'<a target="_blank" href="{url}">{text}</a>'
# # show data
# if st.checkbox('Include Preview URLs'):
# 	# df['preview'] = add_stream_url(df.track_id)
# 	df1['html_link'] = df1['shortUrl'].apply(make_clickable, args = ('Listen',))
# 	st.write(df1.to_html(escape = False), unsafe_allow_html = True)
# else:
# 	st.write(df1)

#title for critics
# st.sidebar.title("Filter by critic")
# critic_select = st.sidebar.selectbox("Select Critic", ('All', 'Peter Bradshaw', 'Wendy Ide'))
# if critic_select:
#     df1[df1['critic'].str.contains(critic_select, case=False) == True]
# else:
#     st.write(get_data())



#if __name__ == '__main__':
