ethiopia-forecasts
==================

Agricultural forecasts for Ethiopia. 

Documentation for Ethiopian Profitability Analysis Tool (12/21/14):
*Disclaimer: All information contained in this document is accurate as of December 21, 2014. Subsequent changes to the application may render portions of this documentation obsolete or inaccurate. Please contact Professor Joshua Woodard (woodardjoshua@gmail.com) or Jeff Smith (jks257@cornell.edu) for assistance. This document is meant as a high level overview of the application and is not meant to explain lines of code. For fine-grained code explanations, please review the code files, as the code should be sufficiently commented. For questions regarding the codebase, please contact Alex Maass (am838@cornell.edu). 

Project Description:
  The Ethiopian Profitability Analysis Tool is used to show the expected profitability of using fertilizer when growing crops in Ethiopia. In its current state, the profitability forecast model is incomplete and therefore, the application functions only as a demo for a potential user interface. While the infrastructure can handle different profitability models, it is currently only capable of graphically displaying weather data from the AGMERRA dataset. The AGMERRA dataset contains woreda level information on solar radiation, maximum temperature, minimum temperature, rainfall, and wind speed from Jan 1, 1980 to Dec 31, 2010. There are two modes in which the data can be queried and viewed: map view and table view. Map view allows for the visualization of weather data as an overlay over a map of Ethiopia. Woredas with data available are drawn over a satellite map of Ethiopia, with each woreda colored to show data values in comparison to other woredas. Table view allows for the visualization of data in a simple table format. This allows for the viewing of numerical data in a standard table format where each value is associated with a specific woreda ID. 

Repository Location:
  The current codebase is stored using a public repository on GitHub, a popular version control and source code management service. The repository can be found at:
  https://github.com/am838/ethiopia-forecasts

General Architecture:
  The Ethiopian Profitability Analysis Tool is a web application that was built using the Python Flask framework. It uses Python Flask version 0.10.1, which, at the time of writing, is the most up to date version of Python Flask. It utilizes the traditional model-view-controller (MVC) design paradigm of modern web applications. The client portion of the application is written using HTML, CSS, and JavaScript. The server portion of the application is written in Python. PostgreSQL is used as a backend database to store pre-computed values that can be queried by the server code. 
  In regards to hosting, both the application server and the database server are hosted on Amazon Web Services (AWS). The application server is set up and administered through Amazon’s Elastic Beanstalk (EB) service. Using Elastic Beanstalk, it is easy to continuously deploy new versions of the code and see how code changes influence the application. The database is hosted and administered through Amazon’s Relational Data Store (RDS) service. Currently, both the application server and the database are running on the free service tier of EB and RDS. If the database exceeds 5 GB, it will become necessary to switch to the paid tier of RDS. 

For further reading on how to utilize these services, please read: 
  Elastic Beanstalk Documentation: 
http://aws.amazon.com/documentation/elastic-beanstalk/
  Relational Database Service Documentation:
      http://aws.amazon.com/documentation/rds/

Client:
The client portion of the code is split into three different parts: HTML, which defines the structure of the frontend, CSS, which defines the style of the frontend, and JavaScript, which provides the animations and other interactive components of the interface. 
HTML: The HTML code can be found in the “templates” folder of the project. Due to the usage of the Python Flask framework, all HTML code must be located within this folder. This folder contains map.html and table.html. These are the files that are returned by the web server and loaded within a client browser. 
CSS: The CSS code can be found in the static/css folder of the project. To properly style the web application, the Bootstrap framework was heavily used. The CSS code is split up into different plugins and components. Within the static/css/plugins folder is the bootstrap.min.css file, which defines the styling for the Bootstrap framework. Within the static/css/fonts folder are the icon files used within the Bootstrap framework. In the main static/css folder are map.css, table.css, and sidebar.css. These files dictate the style for the map view, the table view, and the sidebar component, which is shared between both views. 
JavaScript: The JavaScript code can be found in both the HTML files in the templates folder and the static/js folder. The JavaScript found in the HTML files are used to make various frontend components interactive. The map.js file contains the JavaScript necessary to render the background satellite map for the map view. In the static/js/plugins folder are bootstrap-datepicker.js, bootstrap.min.js, and jquery-1.11.1.min.js files which provide the JavaScript code necessary for the datepicker component to function, bootstrap framework to be interactive, and the jQuery library to allow for interactive data querying, respectively. 
Images: The /img folder contains various images that are used in the application frontend. The loading gif is found here along with the acacia tree logo of the application. 
Maps: The /maps folder contains the topoJson file that is used to render the woreda shapes on top of Google Maps. The topoJson format was selected because the file sizes of topoJson files are significantly smaller than standard GeoJson. By using the topoJson format, it was possible to reduce the file size of the woreda shapes from 40+MB to slightly over 1MB. Please note that the topoJson format is not directly supported by Google Maps and does require a postprocessor. This postprocessor is included in the map.html file as a JavaScript import. To create the final topoJson file, the woreda shapes were exported out of ArcGIS, post-processed using the mapparse.py script found in the /scripts folder to clean up the properties field, converted to GeoJson, and then finally to topoJson. 

Server:
The server-side code of the application can be found in the application.py file found in the root folder. In application.py, there are two routes, signified by the “@application.route” annotation. These routes are the handlers to return the map and table views of the application. In addition to the map handler, there is also a request handler to do data querying. The “/lookup” route handler handles POST requests coming from the client. These requests can be found in the JavaScript code and are AJAX requests. The “/lookup” route handler parses out the data type and date range from the POST request, interprets the request, and sends a request to the Postgres database. Once the requested data is fetched from the Postgres database, the handler does some post processing to calculate the average value for the given date range for each woreda. The final woreda-value mapping is then stored in a JSON object, converted to a JSON string, and sent back to the client, where it will be rendered on screen. 

Database:
  A Postgres database instance is used by the application to store pre-computed values for future rendering. As mentioned previously, there is a Postgres database instance hosted on AWS that contains the AGMERRA data that is currently being used by the web application. The database code is split up between the application.py file and the various Python scripts found in the scripts folder. To store and request data from the Postgres database, the web application utilizes the SQLAlchemy database connector that comes built in with Flask. The database connection is established by defining a  'SQLALCHEMY_DATABASE_URI' property in the application configuration and then calling the SQLAlchemy initializer on the application. The 'SQLALCHEMY_DATABASE_URI' needs to be set for different values when connecting to a local or remote database instance. In the code, the different URIs are commented. 
  In the application.py file, the Weather database model is defined. In the current version of the application, this Weather model is a wrapper around each individual data point contained within the AGMERRA data set. Each row in the Postgres database is defined as having 8 fields: a unique row ID, the date of measurement, the woreda the measurement was taken in, the solar radiation measured, the maximum temperature measured, the minimum temperature measured, the rainfall measured, and the wind speed measured.  
  In the “/scripts” there are numerous Python scripts to preprocess data prior to uploading to the database. These scripts are not run during normal usage of the application, but instead are used to populate the database prior to any usage of the application. In the scripts folder, the following files can be found:
- AgMERRA_db.csv: The final preprocessed CSV version of the AGMERRA dataset. This dataset has all of the data formatted in the form of database rows and simply needs to be imported to a Postgres database instance. 
- Mapparser.py: This script reads in the given KML file that originally defined the woredas and parses out specific portions of the properties field. In the original KML file, all of the properties are formatted using HTML as a single string instead of being properly separated into variable-value format. This script takes care of that and was used to create the KML file that was eventually converted into the topoJSON file that is being used in the final application. 
- Models.py: A standalone implementation of the Weather model currently defined in application.py. Eventually, as more and more models are added to the database, it will make sense to transition to a separate models file such as this. This file currently is unused. 
- Views.py: A standalone implementation containing the route handlers currently defined in application.py. Eventually, as more and more routes are added, it will make sense to transition them to a separate views file such as this. This file currently is unused. 
- Testdb.py: This was an old Python script that I used to test the database when I first set it up. This script utilizes the psycopg2 plugin, which is not used in the final version of the web application and is actually unsupported by AWS (hence the transition away). 
- uploadWeather.py: A test script to upload data to a Postgres database instance. This should not be used, as it is much faster to simply upload a csv file directly to the database. 
- WTHparser.py: This python script combines data from the AgMerra_WeightMatrix.csv file and the AGMERRA data points to map specific AGMERRA data points to a specific woreda. This script generates the AgMERRA_db.csv file. This file should be run in the same directory as the WTH files of the AGMERRA dataset. The Weights Matrix file should also be located in the same directory. 

Running a Local Instance:
  The application server has only been tested to run on *NIX machines (e.g any Linux distribution and MacOSX). Running the application server on Windows is untested and not recommended due to the different file directory separators used in Windows. To run a local instance of the application, clone the repository from Git using the following command:
  git clone https://github.com/am838/ethiopia-forecasts.git
Once the repository has been cloned, download Pip:
  https://pip.pypa.io/en/latest/installing.html
Pip is a Python package manager and is used to download the dependencies necessary for the application to run. Once pip has been installed, enter the directory and begin installing the necessary dependencies:
  pip install requirements.txt
Once all the dependencies have finished installing, it is now possible to start the application server. To start the application server, enter the directory and run:
  python application.py
This should start an application server on your local computer waiting for requests on port 5000. To connect to this application server, open up Google Chrome or Mozilla Firefox (Internet Explorer is currently untested as development was performed on a Mac OSX). In the address bar, go to:
  http://localhost:5000
You should now be connected to a local instance of the application. 

Setting Up a Developer’s Environment:
To set up a developer’s environment, please ensure that a version of Python 2.7 or 2.8 is installed. 
- Install Git from: 
http://git-scm.com/downloads
- Clone the repository using the command: 
git clone https://github.com/am838/ethiopia-forecasts
- Install Pip from:
  https://pip.pypa.io/en/latest/installing.html
- Install dependencies using the command: 
  pip install requirements.txt
