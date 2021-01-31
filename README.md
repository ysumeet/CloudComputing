# COVID-19 Symptom Checker and Test Centres Locator
COSC2626/2640 Cloud Computing | PGRD Summer Semester , 2021 | Assignment 2 | RMIT Unversity

### Designed & Developed By: Sumeet Yedula | Sainath Reddy Kodiganti
##### Application link: [https://s3797892-s3804879-covid.ts.r.appspot.com](s3797892-s3804879-covid.ts.r.appspot.com "Heading link")


## Introduction
Cloud Computing has drastically changed one’s approach towards the way of accessing data and processing power. It has brought a disruptive view for providing on demand information access and applications from anywhere at any time. Features of Cloud Computing include:  Scalability, Resource Pooling, Easy Network Access, Availability, Easy Maintenance, Automation and Security. It is because of these features both the hosts and clients who are responsible for operations and management of their applications are viewing Cloud Computing as their ultimate resource. It is also very easy to use which alone makes its reach to the end users much more domineering than the available technologies.

Due to the current pandemic situation, there has been many discrepancies and delays in the information about the COVID symptoms that is being relayed to the masses. It is still not clear to the people what are the symptoms that they should be worried about, the extent up to which it affects the person and spread in the surroundings and where should they go to treat their symptoms.

It is these high reach, availability, and scalability features and services of Cloud Computing that we are leveraging upon to build and host the current web application which helps the common people to assess their symptoms and get to know the test centres and its details that are available in their location to treat the affected.

There is no previous existing application providing the exact functionality intended by us. Nevertheless, we have drawn inspiration from sources such as the questionnaire from spectrum health and testing location data from public data set COVID-19 Testing Locations . We have also got idea for visualisation from various search engine results that are displayed for COVID-19 stats.

## High Level Architecture

![alt text](https://github.com/ysumeet/CloudComputing/blob/main/doc_images/Picture1.png)

## Implementation
The user is presented with a rich client-side web application through which he can assess his symptoms and access its contents. When the user enters the credentials and form data for assessing his symptoms through the front end, they are fetched and saved in the google cloud data store using a request handler. The web application as a proxy to the user makes a post request call to the API gateway which in turn acts as a proxy between the Lambda function that handles the backend services and the client. Then the function fetches the location data from the S3 bucket and provides it to the API gateway which returns the data as a response json object to the client-side application where it will be visually presented to the end user. The data here is nothing but the location data which is sent to the Google maps API where it will be parsed, and the data is presented.

Here in this project, we are also using some public data sets provided by google to represent some statistical information visually to the user with the help of google big query tool and google data studio. The big query tool parses the huge volumes of data in the public data set and filters out the information needed to present it to the user and sends it to the google data studio where it is converted into the visual format and then later embedded into the client- side application. Cloud watch here plays the role of maintaining logs and records of the API calls made to the lambda function for the location data and filter out the exceptions and errors if any.

This entire application is then made available globally to all the end users by hosting it online with the help of Google app engine. The google app engine maintains and controls the application by providing it its rightful responses from other applications and services from time to time and keeps it running. Hence in this way the following high-level architecture is designed and developed to make the client-side web application working and presentable to the end users.

## Developer Guide
This guide is to replicate the setup of the Environment. It also outlines the procedures that are followed for the development and hosting of the various cloud services used in the COVID-Detector. The application is a web based responsive site and primarily uses Google App Engine to serve the application and draws support from various cloud service to enable the versatility and elasticity that is offered as an advantage by cloud.

### Google App engine configuration:
  - To begin with proceed to https://console.cloud.google.com/ and click on create new project.
  - Download and Install Google Cloud SDK https://cloud.google.com/sdk
  - Download Install Git https://git-scm.com/downloads 
  - Install App engine extension for python using the command from command line/terminal:
  ```
  $ gcloud components install app-engine-python
  ```
  - Install additional python libraries using the command
  ```
  $ gcloud components install app-engine-python-extras
  ```
  - Run the following command to update all the installed Google Cloud SDK components, including the App Engine extension for Python
  ```
  $ gcloud components update
  ```
  - Install python 2.7 on the local OS and ensure the PATH variable is set correctly by executing
  ```
  $ python -version
  ```
  - Open the google cloud SDK shell and navigate to the Covid-Detector directory in the terminal
  ```
  $ dev_appserver.py app.yaml
  ```
  - Visit http://localhost:8080/ in your web browser to view the app
  - To deploy your app to App Engine, run the following command from within the root directory of your application where the app.yaml file is located:
  ```
  $ gcloud app deploy
  ```
  - To launch your browser and view the app at http://[YOUR_PROJECT_ID].appspot.com, run the following command
  ```
  $ gcloud app browse
  ```

## S3 Storage configuration:
The Locations.json containing the data related to testing centres is stored in the amazon s3 bucket as an object for easier access and to be used by lambda further down.
  - To being with navigate to https://s3.console.aws.amazon.com/s3 and select create a bucket
  - Name the bucket locations-covid, enter any desired tags to help with better identification and select create bucket
  - Select the locations-covid and select upload the "locations.json"
  
## Lambda configuration:
The locations from the json are served on REST call using the AWS Lambda service due to the benefits provided and deploy the code as a serverless function which be used by any service with simple REST call.
  - Navigate to https://console.aws.amazon.com/lambda/home?region=us-east-1#/discover
  - Select create a function and select Author from scratch enter the function name as "lambda_request_handler" and Runtime as Python 3.6 and select create a function
  - Create a lambda_function.py and paste the code in the editor and use Test button to test the code

## API Gateway
The AWS API Gateway sits in between the lambda function that webservices to expose the service as an access door for the functionality.
  - Navigate to https://console.aws.amazon.com/apigateway/main/apis?region=us-east-1
  - Select create API
  - Select REST API and click build
  - Select New API and enter the API name and create API
  - Select Action dropdown and choose Create Method and then select ANY
  - Configure the method and choose appropriate lambda function from the dropdown
  - Use the Test button to test the API
  - Select Stages from left navigation rail and select create, provide stage name and deployment type, and click on create
  - Navigate to Logs and Enable cloud watch logs and select save changes
  - There will be a Invoke URL that will be displayed which can be used to invoke the designated Lambda function. Place this URL in locations.html at url: "[Your invoke URL]".
  - Expand the navigation menu on the left to view the individual URL’s for specific REST URLs

## CloudWatch configuration:
CloudWatch can be used to trace the logs from the lambda function that was crated earlier. This can help in troubleshooting the function when required.
  - To view the logs, select monitoring from the lambda function dashboard that was created earlier
  - Select the view logs in CloudWatch to redirect to the CloudWatch console
  - The logs are displayed as per the timeline in log streams section.
  - Select an item from the list to see the details with its timestamp.

## BigQuery Configuration:
BigQuery from Google is serverless technology that is highly scalable service to manage any massive dataset and extract meaningful insights from the data. Besides, it also provides a large collection of public datasets with live data to explore.
  - To configure the BigQuery navigate to https://console.cloud.google.com/bigquery?_ga=2.188234792.1472939372.1611970822- 1702988852.1609721798&project=s3797892-s3804879-covid
  - Create a dataset named Covid_Final_Dataset
  - Select add data and then explore public datasets
  - There will be a new project appearing in the workspace with name bigquery-public-data and select the covid19_open_data
  - Select create a query and paste the following query
  ```
  Select subregion1_name as State, max(cumulative_confirmed) as Confirmed_Cases from
  bigquery-public-data.covid19_open_data.covid19_open_data where country_code = 'US' and subregion1_name != ''
  group by subregion1_name;
  ```
  - Save the query and select schedule and create new schedule query
  - Enter the name for schedule and repeats daily->‘start now’->‘End never’->Select destination table as Covid-Detector and Covid_Final_Dataset.
  - Enter a valid table name->choose ‘append to table’->click on ‘schedule’ button. This will create scheduled job to pull this specific data from public dataset to project’s table.
  
## Data studio Configuration:
Data studio offers a powerful cloud platform to visualise data as charts and tables with various connectors available out of the box and ability to create custom connectors.
  - To create a report on Data studio, select Blank report from add data to report section. Select BigQuery connect to data.
  - Select My projects->COVID- Detector->Covid_Final_Dataset->Now select the table that was created earlier to store the scheduled query data.
  - Select Add chart and insert table. Select state as Dimensions (Column) and Total_Tested, Confirmed_cases and Confirmed_Deaths as Metrics (Row)
  - Now select dropdown from share and select Embed report
  - Copy the Embed code from text field and place it in stats.html of the project as
  ```
  <iframe class="studio" src="[EMBED CODE]
  frameborder="0" style="border:0" allowfullscreen></iframe>
  ```

## Google Maps Configuration:
Google provides developers access to is Maps as a cloud product which can be used in project to display the testing centre locations to users.
 - To utilise the google maps in the project the developer API keys needs to be created which be used to invoke the service via any of the available SDK. JS client in this case
 - Navigate to https://console.cloud.google.com/google/maps- apis/overview?folder=&organizationId=&project=s3797892-maps-api
 - Select pick API’s and select enable Geocoding API and Maps JavaScript API
 - Select Credentials and create a new API key and ensure to copy the key as it is required to access the service
 - Place the key at
 ```
  <script async defer
  src="https://maps.googleapis.com/maps/api/js?key=[KEY]&callback=myMap"></script>
 ```
  
## Sample Screenshots
![alt text](https://github.com/ysumeet/CloudComputing/blob/main/doc_images/Picture18.png)
![alt text](https://github.com/ysumeet/CloudComputing/blob/main/doc_images/Picture17.png)
![alt text](https://github.com/ysumeet/CloudComputing/blob/main/doc_images/Picture19.png)
![alt text](https://github.com/ysumeet/CloudComputing/blob/main/doc_images/Picture20.png)
![alt text](https://github.com/ysumeet/CloudComputing/blob/main/doc_images/Picture21.png)
![alt text](https://github.com/ysumeet/CloudComputing/blob/main/doc_images/Picture22.png)
![alt text](https://github.com/ysumeet/CloudComputing/blob/main/doc_images/Picture23.png)
![alt text](https://github.com/ysumeet/CloudComputing/blob/main/doc_images/Picture24.png)
