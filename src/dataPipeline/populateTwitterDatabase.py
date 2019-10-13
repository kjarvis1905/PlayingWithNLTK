import createDatabase
import config
import startTwython

if __name__ == "__main__":
    mps_handles = startTwython.processAllTwitterHandles()
    dbhandler = createDatabase.databaseHandler()
    dbhandler.prepareTable(config.twitter_users_table_name)
    dbhandler.insertValuesIntoTable(config.twitter_users_table_name, mps_handles)
