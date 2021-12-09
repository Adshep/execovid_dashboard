'''This module tests the functions which make up my covid application.'''
from covid_data_handler import covid_API_request, parse_csv_data, process_covid_csv_data
from covid_news_handling import news_API_request
from time_conversions import hhmm_to_seconds
import pytest
def test_parse_csv_data():
    data = parse_csv_data('../nation_2021-10-28.csv')
    assert len(data) == 639, 'There should be 639 entries of data.'

def test_process_covid_csv_data():
    last7days_cases, current_hospital_cases, total_deaths = process_covid_csv_data(parse_csv_data('../nation_2021-10-28.csv'))
    assert last7days_cases == 240299, 'last7days_cases should be 240299'
    assert current_hospital_cases == 7019, 'current_hospital_cases should be 7019'
    assert total_deaths == 141544, 'total_deaths should be 141544'

def test_covid_API_request():
    data = covid_API_request()['data']
    assert len(data) > 0, 'There should be 631 entries of data.'

def test_news_API_request():
    news = news_API_request()['articles']
    assert len(news[0]) == 8, 'Should contain 8 tags for each news article.'

def test_hhmm_to_seconds():
    seconds_after_midnight = hhmm_to_seconds('01:00')
    assert seconds_after_midnight == 3600, 'Should be 3600 seconds between 1 and 12am.'


