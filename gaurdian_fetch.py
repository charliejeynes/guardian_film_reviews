import pandas as pd
import requests as req

url0 = 'http://content.guardianapis.com/search?order-by=newest&show-fields=bodyText&q=politics&api-key=test'

def requestContent(url):
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

def convert2df_totalResults(total_results):
      total_content = []
      for result in total_results:
            for item in result['response']['results']:
                  total_content.append(item)
      df = pd.DataFrame(total_content)
      fields = [x for x in df['fields']]
      df1 = pd.DataFrame(fields)
      df3 = pd.concat([df, df1], axis=1, join="inner")
      return df3

def getParams():
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

def pageIterate(pageNumber=1):
      url = 'https://content.guardianapis.com/search?q=peter%20bradshaw' \
            '&format=json&tag=film/film,tone/reviews&from-date=2000-01-01'\
      '&show-tags=peter%20bradshaw&show-fields=starRating,headline,thumbnail,short-url,bodyText' \
            '&show-refinements=all&order-by=relevance&api-key=55eae2e6-6f53-4545-8b01-6d618c991427'\
            '&page-size=200'\
      '&page={}'.format(pageNumber)
      data = requestContent(url)
      return data

def allReviews():
      url = 'https://content.guardianapis.com/search?' \
      '&section=film' \
      '&show-tags=contributor'\
            '&format=json&tag=film/film,tone/reviews&from-date=2000-01-01'\
      '&show-fields=starRating,headline,thumbnail,short-url,bodyText' \
            '&show-refinements=all&order-by=relevance&api-key=55eae2e6-6f53-4545-8b01-6d618c991427'\
            '&page-size=200'\
      '&page={}'.format(1)
      data = requestContent(url)
      return data

if __name__ == '__main__':

      ##### this gets all peter bradshaw's reviews
      data = pageIterate(pageNumber=1)
      total_results = []
      totalPages = data['response']['pages']
      for page in range(totalPages):
            page = page+1
            data = pageIterate(pageNumber=page)
            total_results.append(data)

      df = convert2df_totalResults(total_results)

      df.to_csv('./data/brads_test.csv')

      ##### this is to get all film reviews
      # data = allReviews()
      # content = data['response']['results']
      # df = pd.DataFrame(content)
      # df = convert2df(data)

