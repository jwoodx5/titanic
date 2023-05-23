import psycopg2
from os import getenv
import pandas as pd


DBNAME = getenv('DBNAME')
USER = getenv('USER')
# Password from ElephantSQL
PASSWORD = getenv('PASSWORD')
# Server from ElephantSQL
HOST = getenv('HOST')


# make postgres connection and cursor

pg_conn = psycopg2.connect(
    dbname=DBNAME,
    user=USER,
    password=PASSWORD,
    host=HOST)
pg_curs = pg_conn.cursor()


def execute_query_pg(curs, conn, query):
    results = curs.execute(query)
    conn.commit()
    return results


DROP_TITANIC_TABLE = '''
    DROP TABLE IF EXISTS titanic_table;
'''

TITANIC_TABLE = """
CREATE TABLE IF NOT EXISTS titanic_table (
    "passenger_id" SERIAL PRIMARY KEY,
    "survived" INT NOT NULL,
    "pclass" INT NOT NULL,
    "name" VARCHAR(100) NOT NULL,
    "sex" VARCHAR(10) NOT NULL,
    "age" INTEGER NOT NULL,
    "siblings_spouses_aboard" INT NOT NULL,
    "parents_children_aboard" INT NOT NULL,
    "fare" FLOAT NOT NULL
);
"""

df = pd.read_csv('titanic.csv')

# removing any single quotes in the Name column
df['Name'] = df['Name'].str.replace("'", '')

if __name__ == '__main__':
    # create the table and it's associated Schema
    # Drop Table
    execute_query_pg(pg_curs, pg_conn, DROP_TITANIC_TABLE)
    # create table
    execute_query_pg(pg_curs, pg_conn, TITANIC_TABLE)

    records = df.drop_duplicates().values.tolist()

    for record in records:
        insert_statement = '''
         INSERT INTO titanic_table ( survived, pclass, name, sex, age, siblings_spouses_aboard, parents_children_aboard, fare)
        VALUES {};
        '''.format(tuple(record))
        execute_query_pg(pg_curs, pg_conn, insert_statement)
