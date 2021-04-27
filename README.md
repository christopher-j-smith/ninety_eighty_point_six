# 98Point6 Homework Assignment
This repository contains the python (3.7) script and SQL File used to create the PostgreSQL database, tables, views and final result sets used to answer the homework questions 1-3.

## ninety_eight_point_six.sql
This is the sql file that has all the sql used to create the views along with the last three queries which are used to produce csv's for final analysis. This file is read into the python script and delimited on the semicolon (;). This hides all that messy sql from the python file and increases readibility of the file.

## game_run.py
Python file where all the magic happens. Basic workflow is:
  1. Create PostgreSQL Database - REQUIRES A POSTGRES SERVER TO BE SET UP. Connection string is modified by the tester on lines 10-12. 
  2. Loop through iterative calls to the Player API and parse result set into list until an empty array is returned. -Final list of lists is converted into a dataframe-
  3. Read Game Results csv directly into a dataframe. 
  4. Load both dataframes into their respective tables leveraging SQL Alchemies engine connector and Panda to_sql function
  5. Read SQL File and iterate through to create views and result set from views
  6. CSVs for analysis are in working directory

## requirements.txt
Output of pip freeze in case there are incompatability issues
