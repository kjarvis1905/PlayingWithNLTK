import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, MetaData, BigInteger
from sqlalchemy import insert
import psycopg2
import keyring
import argparse
import config

parser = argparse.ArgumentParser()

def psql_connect():
    engine = sqlalchemy.create_engine(
        "postgresql+psycopg2://", 
        connect_args={"database": "tweetminster", 
        "user": keyring.get_password("psql", "dbuser"), 
        "password": keyring.get_password("psql", "dbuser_password"),
        "host": "localhost"}
    )
    return engine.connect()

def mk_mps_table(meta):
    mps_table = Table(
        config.mps_table_name, meta, 
        Column('id', Integer, primary_key = True, autoincrement=True),
        Column('name', String), 
        Column('constituency', String), 
        Column('party', String), 
        )

def mk_twitter_users_table(meta):
    twitter_users_table = Table(
        config.twitter_users_table_name, meta, 
        Column('id', BigInteger),
        Column('id_str', String), 
        Column('name', String), 
        Column('screen_name', String), 
        Column('friends_count', Integer),
        Column('followers_count', Integer) 
        )

class databaseHandler:
    def __init__(self):
        self.con = psql_connect()
        self.meta = MetaData(bind = self.con)
        mk_mps_table(self.meta)
        mk_twitter_users_table(self.meta)

    def prepareTable(self, tableName):
        #Check if table exists
        table = self.meta.tables[tableName]
        if table.name in self.con.engine.table_names():
            self.deleteExistingTable(table.name)
        self.meta.create_all()

    def deleteExistingTable(self, tablename):
        tables = self.con.engine.table_names()
        if tablename in tables:
            self.meta.tables[tablename].drop(checkfirst=True)
            print("Dropped table {} from database..".format(tablename))
        else:
            print("Couldn't find table {} in database".format(tablename))

    def insertValuesIntoTable(self, tableName, valuesList):
        insrt = self.meta.tables[tableName].insert().values(valuesList)
        self.con.execute(insrt)
        print("Insert successful, inserted {} records into {}".format(len(valuesList), tableName))

        
if __name__ == "__main__":
    print("Connecting to database 'tweetminster'....")
    con = psql_connect()
    meta = MetaData(bind=con)
    print("Getting version...")
    print(con.execute("SELECT version();").fetchone())
