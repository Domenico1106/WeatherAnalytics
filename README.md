# Weather Analytics
Weather Analytics is a project that was implemented for the Big Data course during the master's degree in Computer Engineering at the University of Calabria.
The goal is to provide a tool for analyzing weather data collected over the territory of the United States of America in the year 2013.
The technologies that have been used in development are:
1. **APACHE STORM**: Real-time distributed computing system for processing large volumes of data at high speed.
2. **DASH**: an open source Python framework, used to create data analysis web applications.
3. **PLOTLY**: A high-level declarative graph library. It is used to import and analyze data, creating interactive browser-based graphs.

As the dataset we were provided with is very large, a data cleaning was done, keeping only the rainfall and temperature data used to make daily and monthly analysis. 
In addition to the dataset provided, the *wban_stato_capitale* file was also created to restrict the analysis to the capital cities of the fifty US states.
A regression algorithm was implemented by which, using data from the years 2010 to 2013, a prediction of the monthly data for the year 2014 was made. For the forecast of annual temperatures, on the other hand, the TemperatureUSA file was used, which contains annual data from 1875 to 2013.
Finally, the dataset of effective values for 2014 was used to check the accuracy of the forecasts, obtaining very good results.

## Backend
The previously mentioned Apache Storm was used to implement the application logic of the tool.
The structure of the backend is shown in the following image where the Spouts are the sources that perform the data filtering operations by extracting the rainfall and temperatures of the 50 capitals respectively. The Bolts receive the data from the Spouts perform the various operations and output the results in the form of CSV data (the CSV output format was chosen for convenience, it is not a standard)

![Struttura Backend](./imgs/Screenshot%202024-09-07%20215822.png)

As can be seen from the image Città Bolt does not have a Spout as it uses as input the data emitted by Pioggia Bolt and Temperatura Bolt.
A Spout and a Bolt were also created for regression analysis.

The Topology class defines the Storm topology, creating the various Spouts and Bolts that describe its behaviour, setting the degree of parallelism and the timeout that causes execution to terminate if no more Spouts are emitting tuples. Since there is no cluster on which to execute it, the topology consists of a single node that is simultaneously **Nimbus**, **Zookeeper** and **Supervisor**.

A Utilities class was then created to write standard functionalities used in the various classes.

> **+++ Note**: Initially the dataset provided text files, before passing the data to the spouts these files were converted to CSV through the described program converter.py custom written in python.

## Frontend
The frontend was implemented in Python using the Dash library for implementing the web dashboard and the Plotly library for creating the charts based on the analysis results produced by the backend. The home page looks as shown in the following image

![homepage](./imgs/homepage.png)

The *Pioggia* nav-item shows by default a histogram that for each month represents the average daily rainfall amount expressed in mm throughout the year under analysis in the US capitals. Below the graph are checklists each labelled with the name of a month. Initially, these checklists are all enabled, but the user is allowed to disable one or more months by ticking the corresponding checklists to view the trend over a subset of months (e.g. leave only the June, July and August checklists active to see the average rainfall trend over the summer season...). At the top there are two radio buttons. By default, the one that is ticked is labelled ‘Resoconto Annuale’, and if clicked, it shows the page just described. The second radio button labelled ‘Analisi Mensile’ takes us to another page showing a map of the United States with coloured dots on the US capitals. The month to which this chart refers is shown in a DropDownMenu which by default is placed on the month of January but when clicked opens a list of DropDownItems in which the user is allowed to view a specific month.
The characteristic feature of the dots depicted on the map is that their size is directly proportional to the average daily rainfall in the capital represented: the higher the average daily rainfall value in that city, the larger the dot. Below the graph are two tables showing respectively the wettest and the least rainy day in that month and the city where these data were recorded.

Similar to Pioggia, the *Temperatura* nav-item also has two radio buttons and by default the 'Resoconto Annuale' is shown divided into tables:
The first table shows for each month of the year the average of the maximum temperatures, the average of the minimum temperatures, and the average of the mean temperatures. the higher the temperature value, the more the cell takes on a warm colour (tending towards red), the lower the temperature value, the more the cell takes on a cooler colour (tending towards blue).
Three more tables are given on this page, two of which show the maximum and minimum temperatures recorded during the year, respectively, with the month and place where they were recorded.
The third table shows the temperature range, calculated as the difference between the maximum and minimum temperature, and the month to which this value refers.
Clicking on the Monthly Analysis radio button takes you to a page containing a DropDownMenu in the top right-hand corner, which defaults to January. The main part of the page consists of a histogram where the abscissas describe each day of the month while the ordinates describe, for each day, the average maximum temperature expressed by a red bar, the average minimum temperature expressed in blue and the average temperature expressed by an orange bar.
Immediately below the graph, four tables are shown, three of which describe, respectively, the maximum and minimum values of average temperature, minimum temperature and maximum temperature recorded in the reference month, also showing the cities where these values were recorded. The fourth table shows the monthly temperature range data.

The *Capitali* nav-item shows the temperature or rainfall values of all US capital cities based on the value of a checklist located in the top right-hand corner. 
Specifically, a graph expressing the map of the United States is shown where each state is coloured according to the temperature value (or rain value respectively, depending on the graph being observed) of its capital city. In particular, a colour scale was chosen for the temperature graph, ranging from cooler colours for low temperature values to warmer colours for higher temperatures. For rainfall, on the other hand, a colour chart based on a blue scale was taken and a lighter colour is assumed for a low rainfall value, a darker colour is used for more intense rainfall values. Next to the map of the USA are two tables showing the ten hottest (or rainiest respectively) and ten coldest (or least rainy respectively) cities, based on an average analysis of values throughout the year.
At the top there are two radio buttons: ‘All Cities’ shows the page just described, while ‘Single City’ takes you to another page where the data for individual capital cities are displayed. 
By default this page shows the data for the city of Albany, capital of the state of New York, however, the user can change the reference city by means of a Select in the top right-hand corner. The content of this page is made up of two graphs, the first shows the map of the USA highlighting the state of the capital you are viewing, the second graph shows the temperature trend, expressed by a red broken line, and the rainfall trend, expressed by a blue broken line.
At the bottom we have four charts: the first two show the wettest and the least rainy day during the year, the next two show the hottest and the coldest day.

Finally, the *Regressione* nav-item shows two graphs, the first is a histogram showing for each month of 2014 the comparison between the prediction made by the regression algorithm, represented by a pink bar, and the actual value taken from that year's actual dataset, represented by a purple bar. The second graph is a scatter plot showing the linear regression between year and temperature from 1875 to 2013.
Below the graphs, a table shows the comparison between the average temperature value predicted by the regression algorithm for the year 2014 and the actual value.

## Other Files
- **converter.py**: this file was created to conver the dataset .txt original file into .csv file for the sake of convenience.
- **Links Dataset.txt**: this file contains links from which to download the datasets that were used in the realisation of this project. In particular, after conversion via the converter.py file, it is recommended to put the result in the dataset folder.
- **Relazione Progetto BigData.pdf**: contains the project report in Italian written by the team members.
- **dataset**: this folder contains the file wban_state_capital.csv created by the team to extract the data of the capitals only and the datasets used for the linear regression as not all datasets were used for this analysis but only the monthly files.
- **Info Dataset**: contains information on how to read data from datasets.
## Team Members
- [Domenico Carreri](https://github.com/Domenico1106)
- [Giuseppe Cavallo](https://github.com/Giugiugit)
- [Francesco Mandarino](https://github.com/FrancescoMandarino)
