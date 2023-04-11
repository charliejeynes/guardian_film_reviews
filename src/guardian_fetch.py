import pandas as pd
import requests as req
from ast import literal_eval

url0 = 'http://content.guardianapis.com/search?order-by=newest&show-fields=bodyText&q=politics&api-key=test'

def request_content(url):
      resp = req.get(url)
      data = resp.json()
      return data

def convert2df(data):
      content = data['response']['results']
      df = pd.DataFrame(content)
      fields = [x for x in df['fields']]
      df1 = pd.DataFrame(fields)
      df3 = pd.concat([df, df1], axis=1, join="inner")
      return df3

def convert_to_df_total_results(total_results):
      total_content = []
      for result in total_results:
            for item in result['response']['results']:
                  total_content.append(item)
      df = pd.DataFrame(total_content)
      fields = [x for x in df['fields']]
      df1 = pd.DataFrame(fields)
      df3 = pd.concat([df, df1], axis=1, join="inner")
      return df3

def get_params():
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

def all_reviews_page_iterate(page_number=1):
      """
      Provides the REST apio call to get film reviews.
      :param page_number: default is
      :return: data from the website
      """
      url = \
      'https://content.guardianapis.com/search?' \
      '&section=film' \
      '&show-tags=contributor'\
      '&format=json'\
      '&tag=film/film,tone/reviews'\
      '&from-date=2023-01-01'\
      '&show-fields=starRating,headline,thumbnail,short-url,bodyText' \
      '&show-refinements=all&order-by=relevance'\
      '&api-key=55eae2e6-6f53-4545-8b01-6d618c991427'\
      '&page-size=200'\
      '&page={}'.format(page_number)
      data = request_content(url)
      return data

def get_critic(row):
      # lst = []
      # lst.append(row)
      try:
            return row[0]['webTitle']
      except:
            pass

def unpack_all_reviews(df):
      fields = [x for x in df['fields']]
      df_fields = pd.DataFrame(fields)
      df_fields = df_fields.drop(columns='thumbnail')
      df_fields['date'] = df['webPublicationDate']
      df_fields['critic'] = df['tags'].apply(get_critic)
      df_fields = df_fields.rename(columns={'headline': 'Film name & headline'})
      return df_fields


def add_distributors_col(df):
      distributor = [
            'Netflix',
            'Prime',
            'Now TV',
            'Disney',
            'True Story',
      ]

      distributor = '|'.join(distributor)
      test = f'({distributor})'

      df['distributor'] = df['bodyText'].str.extract(f'({distributor})')


def main():
      ##### this is to get all film reviews and page iterate
      data = all_reviews_page_iterate(page_number=1)
      total_results = []
      total_pages = data['response']['pages']
      for page in range(total_pages):
            page = page+1
            data = all_reviews_page_iterate(page_number=page)
            total_results.append(data)
      df = convert_to_df_total_results(total_results)
      df = unpack_all_reviews(df)
      df = add_distributors_col(df)
      return df

if __name__ == '__main__':

      df = main()
      text = df.loc[0:0, 'bodyText'].reset_index()
      text = df.at[108, 'bodyText']

      ##### this gets all peter bradshaw's reviews
      # data = pageIterate(pageNumber=1)
      # total_results = []
      # totalPages = data['response']['pages']
      # for page in range(totalPages):
      #       page = page+1
      #       data = pageIterate(pageNumber=page)
      #       total_results.append(data)
      # df = convert2df_totalResults(total_results)
      # df.to_csv('./data/brads_test.csv')

      ##### this is to get all film reviews
      # data = allReviews()
      # content = data['response']['results']
      # df = pd.DataFrame(content)
      # df = convert2df(data)
      # df = unpack_allReviews(df)
      # df['critic'] = df['tags'].apply(getCritic)
      # df = df.drop(columns=['tags'])

      # df['just_date'] = df['date'].dt.date


