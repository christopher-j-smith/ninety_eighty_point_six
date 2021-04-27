# 98Point6 Homework Assignment
This repository contains the python (3.7) script and SQL File used to create the PostgreSQL database, tables, views and final result sets used to answer the homework questions 1-3.

## Instructions
  1. Download py file and sql file into a directory. Output csv files used to answer the analytics questions will be created in this directory. I recommend creating a new directory just for this process.
  2. Edit the python script user_name, password and host variables to match an already installed and running Postgres server. A new database by the name of ninety_eight_point_six will be created on that server which will be the destination for all data transformations.
  3. Execute the py file via command prompt/terminal.
  4. Three CSV files will be created which are used to answer the corresponding questions in the homework assignment.

## ninety_eight_point_six.sql
This is the sql file that has all the sql used to create the views along with the last three queries which are used to produce csv's for final analysis. This file is read into the python script and delimited on the semicolon (;). This hides all that messy sql from the python file and increases readibility of the file.

## game_run.py
Python file where all the magic happens. Basic workflow is:
  1. Create PostgreSQL Database __REQUIRES A POSTGRES SERVER TO BE SET UP__. Connection string is modified by the tester on lines 10-12. 
  2. Loop through iterative calls to the Player API and parse result set into list until an empty array is returned. __Final list of lists is converted into a dataframe__
  3. Read Game Results csv directly into a dataframe. 
  4. Load both dataframes into their respective tables leveraging SQL Alchemies engine connector and Panda to_sql function
  5. Read SQL File and iterate through to create views and result set from views
  6. CSVs for analysis are in working directory

## requirements.txt
Output of pip freeze in case there are incompatability issues
