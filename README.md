# execovid_dashboard
Execovid_dashboard is a Python package used to display live covid data and news on a web dashboard. These updates can be scheduled using the UI to occur whenever you want.
## Prerequeisites
### Modules
This package requires both Flask and the uk_covid19 modules to be able to load the web based UI and update live covid data. Detailed information for these 2 external modules is provided below:\
\
https://publichealthengland.github.io/coronavirus-dashboard-api-python-sdk/ \
https://flask.palletsprojects.com/en/2.0.x/ 

### Other requirements
I've been running the application on Python 3.10, however versions as early as 3.6 should still work.\
The program requires a stable internet connection in order to work effectively. The dashboards response time is very dependent on your internet speed, so those with slower connections may find that it takes them longer to access live covid statistics and news.
## Installation 
Running the 2 pip install commands below in command prompt will set you up with all the modules necessary to run execovid_dashboard.\
pip install flask
pip install uk_covid19
## Configuration
Execovid_dashboard contains a configuration file which can be altered to fit the program to your needs, it contains various settings such as.
### Location
Both national_location and local_location can be altered in the config file under the 2 highlighted sections.
![image](https://user-images.githubusercontent.com/29089292/145421551-2cbaaccd-bd62-4d13-adec-20a153ac224c.png)
### Picture
The picture at the top of the dashboard can be changed to any 72x72 file saved in static/images, just make sure to add the name of the file in the config.json file.\
![image](https://user-images.githubusercontent.com/29089292/145422342-b352b91d-301c-4bad-81f5-f6f53a667cb9.png)
### API key
In order for the news to be fetched by the newsAPI.org service, and use my program an API key needs to be provided here. If you don't have an API key, visit https://newsapi.org/ \
![image](https://user-images.githubusercontent.com/29089292/145423645-f99a5908-3901-4b78-945d-396423a64abf.png)
## Getting Started
Firstly add your API key in the config.json folder in order for my program to load the dashboard correctly.
Once you've extracted my Python package, to start using the program you need to run the app.py module.\
\
Second, in your web browser type the following address: http://127.0.0.1:5000/index to be greeted with the interface for my application.
In the dashboard you can view the latest covid news articles on the right hand pane, and view scheduled updates on the left.
![image](https://user-images.githubusercontent.com/29089292/145430673-98fbd442-4909-469e-a1d9-87f32b5b0073.png)
\
In order to schedule updates, use the drop down menu to choose a time, name your update using the textbox, and click a checkbox depending on what type of update you want.\
\
If you would like to delete news articles or updates click the 'X' button on the top of the update/article.
![image](https://user-images.githubusercontent.com/29089292/145431002-b8890f39-de54-49f5-9f01-9038007d3ff6.png)
## Testing
Follows the unittest testing framework. My python file test_covid_app contains a series of tests which fit this.
## Developer documentation
The uk_covid19 module is responsible for providing my dashboard with up to date covid statistics locally and nationally by passing the location paramaters into my Covid_API_request function contained within the covid_data_handler module. These locations can be altered in the config file. The flask module is responsible for providing the User Interface side of my program, allowing users to see covid news and statistics in a presentable way, and schedule these updates by using the user friendly GUI widgets.
In addition to this my program also uses many built in python modules such as json, which handles the parsing of json files into several python data structures such as dictionaries, and sched which allows the user to schedule API updates whenever they wish.
## Details
Name: Adam Sheppard \
License: MIT \
Acknowledgements: Matt Collinson created the Flask UI.
