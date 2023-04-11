#import SessionState
import streamlit as st
import numpy as np
import pandas as pd
import requests
import io

from st_aggrid import AgGrid
from st_aggrid import JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder


def welcome_page():
    st.title('Guardian Film Review Database')
    st.write("This website enables you to browse all of the Guardian's film reviews since 2000-present")
    st.write("You can use the sidebar to filter results")

@st.cache_data()
def get_data_into_df(filter=None):
    url = "https://raw.githubusercontent.com/charliejeynes/guardian_film_reviews/main/data/all_reviews.csv" # Make sure the url is the raw version of the file on GitHub
    download = requests.get(url).content
    df = pd.read_csv(io.StringIO(download.decode('utf-8')))
    return df

def process_df(df):
    df = df.replace(np.nan, 'N/A', regex=True)
    pd.set_option('display.max_colwidth', None)
    def make_clickable(link):
        # target _blank to open new window
        # extract clickable text to display for your link
        text = link
        return f'<a target="_blank" href="{link}">{text}</a>'
    # link is the column with hyperlinks
    df['link'] = df['shortUrl'].apply(make_clickable)
    df = df[['Film name & headline', 'link', 'starRating', 'critic', 'distributor', 'date']]
    # df['starRating'] = df['starRating'].astype(dtype = float, errors='ignore').round(1).astype(str)
    df['starRating'] = df['starRating'].astype(str)
    df = df.drop_duplicates(subset=['link'], keep='last')
    df = df.sort_values(by='date', ascending=False)
    # df = df.reset_index(drop=True)
    return df

# def process_render_df(df):
#     # df = df.replace(np.nan, 'N/A', regex=True)
#     # df = df[['Film name & headline', 'starRating', 'critic', 'date']]
#     # # df = df.drop_duplicates(subset=['link'], keep='last')
#     # df = df.sort_values(by='date', ascending=False)
#     # Display the DataFrame
#     gd=GridOptionsBuilder.from_dataframe(df)
#     gd.configure_column("id", headerName="id", cellRenderer=JsCode('''function(params) {return '<a href="https://drive.google.com/file/d/' + params.value + '/view" target="_blank">' + params.value + '</a>'}'''),
#                     width=300)
#     gridoptions=gd.build()
#     gd.configure_column("id", headerName="id", cellRenderer=JsCode(
#         '''function(params) {return '<a href="https://drive.google.com/file/d/' + params.value + '/view" target="_blank">' + params.value + '</a>'}'''),
#                         width=300)
#     AgGrid(df, gridOptions=gridoptions, allow_unsafe_jscode=True, height=500, theme='alpine')

def implement_search_display_results(df, search, column1, column2=None):
    st.write(f'You are filtering results using the following:')
    st.write(search)
    if isinstance(search, list):
        search = '|'.join(search)
    st.write(search)
    if column2:
        df = df[df[column1].str.contains(search, case=False, regex=True) & df[column2].str.contains(search, case=False, regex=True)]
    else:
        df = df[df[column1].str.contains(search, case=False, regex=True)]
    rows = len(df)
    df = df.to_html(escape=False)
    st.write(f"There are {rows} reviews in the table below")
    st.write(df, unsafe_allow_html=True)

def sidebar_filter_implementation(df):
    # title for film
    st.sidebar.title("Search for a film")
    film_search = st.sidebar.text_input("Search for a film")
    # critics
    st.sidebar.title("Filter by critic")
    unique_critics = list(df['critic'].unique())
    critic_select = st.sidebar.multiselect("Select Critic", unique_critics, key='critic')
    # by starRating
    st.sidebar.title("Filter by starRating")
    rating = list(df['starRating'].unique())
    rating_select = st.sidebar.multiselect("Select Rating", rating, key='rating')
    # user selections logic
    if rating_select and critic_select:
        both_box_selections = st.session_state.rating + st.session_state.critic
        implement_search_display_results(df, both_box_selections, 'starRating', column2='critic')
    elif film_search:
        implement_search_display_results(df, film_search, 'Film name & headline')
    elif critic_select:
        implement_search_display_results(df, st.session_state.critic, 'critic')
    elif rating_select:
        implement_search_display_results(df, st.session_state.rating, 'starRating')
    else:
        st.write(
            "There are currently {} Guardian Film reviews. The below table shows the 100 most recent".format(len(df)))
        clicked = st.button('click here to show all Guardian Film Reviews (takes about 5 seconds to load)')
        st.write(df.head(100).to_html(escape=False), unsafe_allow_html=True)
        # AgGrid(df.head(100))
        if clicked:
            st.write(df, unsafe_allow_html=True)


def main():
    welcome_page()
    df = get_data_into_df()
    df = process_df(df)
    sidebar_filter_implementation(df)

if __name__ == "__main__":
    main()






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
