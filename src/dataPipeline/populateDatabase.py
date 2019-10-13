import createDatabase
import createMPs
import config

if __name__ == "__main__":
    mps_list = createMPs.getMPsAsDict()
    dbhandler = createDatabase.databaseHandler()
    dbhandler.prepareTable(config.mps_table_name)
    dbhandler.insertValuesIntoTable(config.mps_table_name, mps_list)
