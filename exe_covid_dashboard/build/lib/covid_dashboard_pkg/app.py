'''This module controls the UI of my dashboard'''
import sched
import logging
import time
from flask import Flask, render_template, request
from covid_data_handler import process_covid_json_data
from covid_news_handling import update_news
from time_conversions import hhmm_to_seconds, current_time
from config_handler import get_picture, get_location

#Create/open log file.
logging.basicConfig(
    filename = 'sys.log',
    level = logging.DEBUG,
    encoding = 'utf-8'
)

#Declaring Flask and scheduler
app = Flask(__name__)
scheduler = sched.scheduler(time.time, time.sleep)
scheduled_updates = []

def display_covid_update():
    '''refreshes the covid_data variable contained in render_template'''
    global covid_data
    covid_data = process_covid_json_data()
    logging.info('Covid data updated!')

def display_news_update():
    '''refreshes the news variable contained in render_template'''
    global news
    news = update_news()
    logging.info('Covid news updated!')

def schedule_news_updates(update_interval: int, update_name: str):
    '''Controls the interval at which the news on the dashboard is refreshed'''
    e1 = scheduler.enter(update_interval, 1, display_news_update)
    if update_name == 'repeat':
        scheduler.enter(24*60*60, 1, schedule_news_updates, argument=(0, 'repeat'))
    logging.info('News update succesfully scheduled.')
        
def schedule_covid_updates(update_interval: int, update_name: str):
    '''Schedules updates for the COV19 API.
    :param update_interval: interval between a process being scheduled and ran.
    :param update_name: Declares whether event is being repeated or not.
    '''
    e2 = scheduler.enter(update_interval, 1, display_covid_update)
    #Continually reschedules updates if argument update_name = repeat.
    if update_name == 'repeat':
        scheduler.enter(24*60*60, 1, schedule_covid_updates, argument=(0, 'repeat'))
    logging.info('Covid data update sucesfully scheduled.')

@app.route('/index')
def index():
    '''Controls the main page of my dashboard, updating info on it.'''
    #Fetches arguments from the URL.
    text_box = request.args.get('two')
    delete_news = request.args.get('notif')
    delete_sched = request.args.get('update_item')
    if text_box:
        #Avoids program crashing when a user creates a schedule without setting a time.
        try:
            update_time = request.args.get('update')
            current_time_hhmm = current_time()
            update_time_seconds = hhmm_to_seconds(update_time) - hhmm_to_seconds(current_time_hhmm)
            #Prevents negative times being scheduled.
            if update_time_seconds < 0:
                update_time_seconds = 86400 + update_time_seconds
            covid_checkbox = request.args.get('covid-data')
            news_checkbox = request.args.get('news')
            repeat_checkbox = request.args.get('repeat')
            if covid_checkbox:
                try:
                    if repeat_checkbox:
                        content = 'Update time: ' + update_time + ' Repeat: yes'
                        schedule_covid_updates(update_time_seconds, 'repeat')
                except UnboundLocalError:
                    logging.error('Could not schedule function as only repeat checkbox is chosen')
                else:
                    schedule_covid_updates(update_time_seconds, 'no_repeat')
                    content = 'Update time: ' + update_time + ' Repeat: no'
            if news_checkbox:
                if repeat_checkbox:
                    print('repeat checkbox')
                    schedule_news_updates(update_time_seconds, 'repeat')
                    content = 'Update time: ' + update_time + ' Repeat: yes'
                else:
                    try: 
                        content = 'Update time: ' + update_time + ' Repeat: no' 
                        schedule_news_updates(update_time_seconds, 'no_repeat')
                    except UnboundLocalError:
                        logging.error('Could not schedule function as only repeat checkbox is chosen')

            else:
                logging.error('Nothing scheduled as update type not selected.')
            try:
                scheduled_updates.append({'title': text_box, 'content': content})
            except UnboundLocalError:
                logging.error('Could not schedule function as only repeat checkbox is chosen.')
        except TypeError:
            logging.error('Schedule could not be created.')
    #Conditionals below check if the tickboxes have been ticked.
    if delete_news:
        count = 0
        for article in news:
            #Linear search finds and deletes the article the user selected to delete.
            if article['title'] == delete_news:
                news.pop(count)
                logging.info('News article deleted.')
            else:
                count = count + 1
    if delete_sched:
        count = 0
        try:
            for event in scheduled_updates:
                #Linear search finds and removes scheduled updates.
                if event['title'] == delete_sched:
                    scheduled_updates.pop(count)
                    scheduler.cancel(scheduler.queue[count])
                    logging.info('Event succesfully removed from scheduler')
                else:
                    count = count + 1
        except IndexError:
            #Deletes from the dictionary however doesnt remove the schedule as it does not exist.
            logging.warning('Event removed from UI but not from scheduler as it does not exist.')
    scheduler.run(blocking = False)
    #Updates the index.html template with live covid info.
    return render_template('index.html',
        title = 'Daily update',
        nation_location = get_location()[1], #Fetches location specified in the config file.
        location = get_location()[0],
        national_7day_infections = covid_data[1]['cases'],
        local_7day_infections = covid_data[0]['cases'],
        news_articles = news,
        deaths_total = 'Total deaths: ' + str(covid_data[1]['deaths']),
        hospital_cases = 'Hospitalisations: ' + str(covid_data[1]['hospitalisations']),
        updates = scheduled_updates,
        image = get_picture()
        )
#Load covid data when the program is launched.
display_news_update()
display_covid_update()
#Run the flask application
if __name__ == '__main__':
    app.run()
