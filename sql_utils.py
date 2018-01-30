'''
Some custom utility functions for common postgres procedures

Jan 18 2018 - BH
'''
import pandas as pd
import psycopg2

def pg2pd_join(table1, table2, on1, on2):
    '''
    select and join data from two postgres tables
    return as pandas dataframe
    '''
    # open db connection
    dbname = 'bart_db'
    username = 'bkhurley'
    con = None
    con = psycopg2.connect(database=dbname, user=username)

    # query the data & store in a dataframe
    sql_query = "SELECT * FROM %s INNER JOIN %s ON (%s = %s);" % (table1, table2, on1, on2)
    join_df = pd.read_sql_query(sql_query,con)
    con.close() #close dn connection
    return join_df


def pg2pd_join_two_cols(table1, table2, on1, on2):
    '''
    join tables on two columns
    on1 and on2 should be lists containing the two column names
    '''
    # open db connection
    dbname = 'bart_db'
    username = 'bkhurley'
    con = None
    con = psycopg2.connect(database=dbname, user=username)
    # query db and return in a df
    sql_query = "SELECT * FROM %s INNER JOIN %s ON (%s = %s AND %s = %s);" % (table1, table2, on1[0], on2[0], on1[1], on2[1])
    join_twocol_df = pd.read_sql_query(sql_query,con)
    con.close() #close dn connection
    return join_twocol_df