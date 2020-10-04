# ETL using Airflow
This project is related to the [Udacity Data Engineer Nanodegree](https://www.udacity.com/course/data-engineer-nanodegree--nd027) program, submitted in October 2020. The goal of the project is to build an ELT process using S3 and Redshift, orchestated by an Airflow DAG.

## Motivation
The ETL process follows a ficticious company called Sparkify (hence the name of the DAG), which wants to create a relational database in Redshift based on a database of songs it holds in `json` format (the [Million Song Dataset](https://labrosa.ee.columbia.edu/millionsong/)), and combine it with logs of user activity data (i.e. users listening to specific songs). Ultimately, we want to build a star-schema database, which contains the following tables:

FACT: songplays
DIM: artists
     songs
     time
     users

In this project, we are using specifically Airflow to schedule the execution of this ETL pipeline, broken down into specific `tasks` in an Airflow DAG. This provides the following advantages over simply running a Python script at a specified interval:
1. Increased visibility into each step of the ETL process through Airflow UI
2. Speed up of processes via parallelization
3. Fault tolerance for specific tasks failing -- they can rerun, without affecting the whole pipeline
4. Increased accountability to stakeholders via clearly defined steps, definitions, schedules and SLAs
5. Ability to create reusable and easily maintable code base via custom Operators and SubDAGs
6. Easy parametrization of each run with context data (e.g. the time/date it was run)
7. Simplified backfilling of past runs

## How to run
### Prerequisites
In order to be able to run this project, you need the following:

1. AWS credentials (IAM user credentials for a role that has full access to Redshift and Read access to S3)
2. Python 3.7 (and an environment with `airflow` installed)
3. A Redshift cluster running, which allows incoming traffic.

### Running the Aiflow DAG
You will need to configure Airflow to run on your device. I suggest following the steps outlined in the documentation ([Quick Start](http://airflow.apache.org/docs/stable/start.html)).
Once you have accessed the Airflow browser UI, you will need to enter your `aws_credentials` and `redshift` Connections under the Admin section. You need these environment variables to be available in order to run the DAG.

Finally, once your scheduler is running and has picked up the DAG, you should be able to see the DAG in the web UI. All you need to do is to turn it on via the toggle. From the on, it will try to first backfill all the past data, and once it reaches current time, it will then run once every hour.