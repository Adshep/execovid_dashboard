'''This module gathers COVID news articles and formats it to be used by the Flask Dashboard.'''
import datetime
import json
import requests
from config_handler import get_API_key
import logging
def news_API_request(covid_terms: str = 'Covid&COVID-19&coronavirus&') -> json:
    '''Returns a JSON containing articles with topics specified in covid_terms
    :param covid_terms: string containing article topics in the format <topic>&<topic>&...
    '''
    #Calculates todays date and puts it in the format YYMMDD for the news API.
    today = datetime.datetime.now()
    date_url = today.strftime('%Y-%m-%d') + '&'
    #Formats the array with the current date and the topics in covid_terms
    url = ('https://newsapi.org/v2/everything?'
       'q=' + covid_terms +
       'from=' + date_url +
       'sortBy=popularity&'
       'apiKey=' + get_API_key())
    response = requests.get(url).json()
    return response

def update_news() -> dict:
    '''Formats the JSON produced by news_API_request to be used by the dashboard '''
    try:
        unparsed_news = news_API_request()['articles']
        parsed_news = []
        for item in unparsed_news:
            #Iterates through the array and creates a dictionary containing only headlines and content
            title = item['title']
            content = item['content']
            parsed_news.append({'title': title, 'content': content})
        return parsed_news
    except KeyError:
        logging.error('API key not in config file, so no news could be fetched')
