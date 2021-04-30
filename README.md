# Automated Processing Data from Local Storage to GCP
Imagine that you have huge amount of data everyday on your local storage and need to procees that. 
So, how can we do that?
In this repository, I've made automation scheduling that aims to processed the data and load it to BigQuery.
This project using Cloud Dataproc, Cloud Storage, and BigQuery as the data warehouse

## Data
I used the flight schedule data. Where the data is sent one day after the day of the flight.
The process that I do here is to change the data type in the airline_code column and also create a function to create the actual flight data column (flight date & time + delay time).
![alt text](https://github.com/fdhanh/etl-from-local-to-cloud/blob/master/add_files/eda.JPG?raw=true)

## Flow
From local storage, data will be sent to cloud storage.
Then with a Spark Job, I process it and grab some required columns.
After the data has been processed, it will be stored in the BigQuery.
![alt text](https://github.com/fdhanh/etl-from-local-to-cloud/blob/master/add_files/bigquery-view.JPG?raw=true)

# Installation
Use git to clone this repository<br>
`git clone https://github.com/fdhanh/etl-from-local-to-cloud.git`

# Prerequisite
Make sure you have python 3.6 installed on your machine <br>
`python --version`

To run the script in this repository, you need to install the prerequisite library from requirements.txt <br>
`pip install -r requirements.txt`

# Usage
Make sure that you have enable Dataproc API and activate Cloud SDK on your local device. <br>

Before running the main program, run the command below <br>
`export PROJECT_ID='your-project-id'`

Run the main program: <br>
`bash main.sh`