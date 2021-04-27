
#import list
import requests
import pandas as pd
from sqlalchemy import create_engine


#normally these would go in a configuration table or file but in the name of succinctness we are going to name a lot of variables here
##set up API headers and url, CURL was provided which makes life easy
headers = {'Accept':'application/json'}
api_url = 'https://x37sv76kth.execute-api.us-west-1.amazonaws.com/prod/users?page='

#game history file
game_url= 'https://s3-us-west-2.amazonaws.com/98point6-homework-assets/game_data.csv'

#These variables need to be updated by the NinetyEightPointSix Tester, Database needs to be PostgreSQL
user_name = 'postgres'
password = 'root'
host = 'localhost'

#engine string is used by sqlalchemy to connect to the Postgres database that is on our local machine
def create_engine_string(user_name, password, host):
    engine_string = 'postgresql://' + user_name + ':' + password + '@' + host
    return engine_string

#column list is used to create a data frame out of the result list that is created via our API calls
column_list = ['id'
                ,'gender'
                ,'title'
                ,'first_name'
                ,'last_name'
                ,'street_address'
                ,'city'
                ,'state'
                ,'postcode'
                ,'email'
                ,'username'
                ,'password'
                ,'salt'
                ,'md5'
                ,'shal'
                ,'sha256'
                ,'date_of_birth'
                ,'registered_date'
                ,'phone_number'
                ,'cell_number'
                ,'id_name'
                ,'id_value'
                ,'large_picture_url'
                ,'medium_picture_url'
                ,'thumbnail_picture_url'
                ,'nationality']

#drop these columns as they don't belong in our database, should reach out and tell the API team that the password is being passed!!!
drop_columns = ['password'
                ,'salt'
                ,'md5'
                ,'shal'
                ,'sha256'
                ,'id_name'
                ,'id_value'
                ,'large_picture_url'
                ,'medium_picture_url'
                ,'thumbnail_picture_url']


def get_player_info(headers, url, iteration = 0):
    """utilizes 98point6 player api to grab all player information and assemble it into a list of lists
     headers = headers to be used for api, url= the url used for the get argument, iteration is an optional argument that can be used in the future to start the API call at a different page
     """
    results_list = []
    #creating an empty list, we are going to append lists to the list... it will make more sense later
    while True:
        get_url = url + str(iteration)
        response = requests.get(get_url,headers=headers).json()
        if len(response) == 0:
            #if the array is empty the length will be 0, as we don't know how many records there are this will ensure
            #that the get will run until there are no more players to grab
            break
        else:
            for data in range(len(response)):
                #iterating through the length of the response which is the number of player profiles in each response
                builder_list=[response[data]['id']]
                #first entry is the player id... very important!!!
                for i in list(response[data]['data']):
                    #data section has all of our dimensional data in either a string or dictionary that needs to be parsed
                    if type(response[data]['data'][i])== str:
                        #some of the responses are only strings, push these results straight to the builder list
                        builder_list.append(response[data]['data'][i])
                    else:
                        #other results in the data dictionary is a dictionary, lets parse these dictionaries out and append to the builder list
                        for j in response[data]['data'][i]:
                            builder_list.append(response[data]['data'][i][j])
                #finally we append the builder list to the results list, because of where it is in the loop it will contain all of the returns from the API in a friendly format
                results_list.append(builder_list)
        iteration += 1
    return results_list

def get_game_info(url):
    #easy peasy, read the csv straight into a dataframe
    df = pd.read_csv(url)
    return(df)

def create_database(db_name, engine_string):
    """Pass a name to create a Postgres Database"""
    engine = create_engine(engine_string)
    conn = engine.connect()
    conn.execute("commit")
    conn.execute("create database " + db_name)
    engine_string = engine_string + '/' + db_name
    return engine_string

def insert_data(dataframe, destination, engine_string):
    """Inserts dataframe as a table in Postgres. Complete rip and replace"""
    #this works because of the low amount of data we have, if there is more than a couple hundred thousand, this needs further tweaking
    engine = create_engine(engine_string)
    dataframe.to_sql(name = destination, con = engine, if_exists = 'replace', index = False)

def create_view(engine_string, sql):
    """Executes SQL, used for view creation here but could be used for any execution""" 
    #this will create all the views to answer the analytics questions
    engine = create_engine(engine_string)
    conn = engine.connect()
    conn.execute(sql)

def read_sql_file(sqlFile = 'ninety_eight_point_six.sql'):
    """Read a specified semicolon delimited file and returns as a list of commands"""
    #I put all the necessary sql into a sql file and this reads all of it so the python code looks neater
    fd = open(sqlFile, 'r')
    sqlFile = fd.read()
    fd.close()
    sqlCommands = sqlFile.split(';')
    return sqlCommands

def get_result_set(engine_string, sql, file_name):
    """Executes SQL Queries and stores result set in specified tab delimited file"""
    #pushes the result sets straight into tab delimited csvs for analysis
    engine = create_engine(engine_string)
    df = pd.read_sql(sql = sql, con = engine)
    df.to_csv(file_name, sep = '\t', index = False)

def main():
    engine_string = create_engine_string(user_name, password, host)
    new_engine_string = create_database('ninety_eight_point_six', engine_string)
    #new engine string is created which specifies to use the database that was created
    print('Database Created')
    results_list = get_player_info(headers, api_url)
    print('Player Info Downloaded')
    player_dataframe = pd.DataFrame(results_list, columns = column_list)
    player_dataframe.drop(columns=drop_columns, inplace = True)
    game_dataframe = get_game_info(game_url)
    print('Game History Downloaded')
    insert_data(player_dataframe, 'player_dim', new_engine_string)
    insert_data(game_dataframe, 'game_history', new_engine_string)
    print('Tables Loaded')
    sqlCommands = read_sql_file()
    for i in sqlCommands[0:-3]:
        create_view(new_engine_string,i)
    file_name = 1
    print('Views Created')
    for i in sqlCommands[-3:]:
        get_result_set(new_engine_string, i, str(file_name) + '.csv')
        file_name += 1
    print('Result Set Files Created in Working Directory')


if __name__ == "__main__":
    main()
