import numpy as np
import pandas as pd
import requests as req
from ast import literal_eval

eg_url = 'http://content.guardianapis.com/search?order-by=newest&show-fields=bodyText&q=politics&api-key=test'

def request_content(url:str) -> dict:
      """
      :param url: str call specified in api_call_film_reviews_page_iterate()
      :return: json dictionary which is very nested
      """
      resp = req.get(url)
      data = resp.json()
      return data

def convert_to_df_total_results(total_results: list[dict]) -> pd.DataFrame:
      """
      :param data: nested dictionary from api call
      :return: unpacked dict into a dataframe
      """
      total_content = []
      for result in total_results:
            for item in result['response']['results']:
                  total_content.append(item)
      df = pd.DataFrame(total_content)
      fields = [x for x in df['fields']]
      df1 = pd.DataFrame(fields)
      df2 = pd.concat([df, df1], axis=1, join="inner")
      return df2

# TODO: swap up the api call str for params in get instead as it's easier to read
def get_api_params():
      """not implemented"""
      MY_API_KEY = '55eae2e6-6f53-4545-8b01-6d618c991427'
      API_ENDPOINT = 'http://content.guardianapis.com/search'
      my_params = {
            'from-date': "",
            'to-date': "",
            'order-by': "newest",
            'show-fields': 'all',
            'page-size': 200,
            'api-key': MY_API_KEY
      }
      return my_params

def api_call_film_reviews_page_iterate(page_number:int = 1) -> dict:
      """
      Provides the REST api call
      :param page_number: default is 1 and can be iterated over to get all the pages
      :return: data from the website
      """
      url = \
      'https://content.guardianapis.com/search?' \
      '&section=film' \
      '&show-tags=contributor'\
      '&format=json'\
      '&tag=film/film,tone/reviews'\
      '&from-date=2000-01-01'\
      '&show-fields=starRating,headline,thumbnail,short-url,bodyText' \
      '&show-refinements=all&order-by=relevance'\
      '&api-key=55eae2e6-6f53-4545-8b01-6d618c991427' \
      '&page-size=200'\
      '&page={}'.format(page_number)
      data = request_content(url)
      return data


def unpack_all_reviews(df: pd.DataFrame) -> pd.DataFrame:
      """
      Cleans up the df and adds critics column
      :param df:
      :return: processed df
      """
      def get_critic(row):
            try:
                  return row[0]['webTitle']
            except:
                  pass

      fields = [x for x in df['fields']]
      df_fields = pd.DataFrame(fields)
      df_fields = df_fields.drop(columns='thumbnail')
      df_fields['date'] = df['webPublicationDate']
      df_fields['critic'] = df['tags'].apply(get_critic)
      df_fields = df_fields.rename(columns={'headline': 'Film name & headline'})
      return df_fields

def add_distributors_col(df:pd.DataFrame) -> pd.DataFrame:
      """
      add distributor column
      :param df:
      :return: df with extra column
      """
      distributor = [
            'Netflix',
            'Prime',
            'Now TV',
            'Disney',
            'True Story',
            'theatres',
            'cinemas',
            'digital platforms',
            'Mubi'
      ]

      distributor = '|'.join(distributor)
      df['distributor'] = df['bodyText'].str.extract(f'({distributor})')
      df['distributor'][df['distributor'].astype(str) == 'nan'] = 'presumed cinemas'
      return df

def main() -> pd.DataFrame:
      """
      iterates through the pages of the api call and gets all the data into a df
      :return: df with reviews
      """
      data = api_call_film_reviews_page_iterate(page_number=1) # intialise to get how many pages
      total_results = []
      total_pages = data['response']['pages'] # intialise to get how many pages
      for page in range(total_pages):
            page = page+1
            data = api_call_film_reviews_page_iterate(page_number=page)
            total_results.append(data)
      df = convert_to_df_total_results(total_results)
      df = unpack_all_reviews(df)
      df = add_distributors_col(df)
      df.to_csv('./data/all_reviews.csv')
      return df

if __name__ == '__main__':
      df = main()




