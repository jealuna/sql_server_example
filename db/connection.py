import pyodbc 

class SqlConnection():
    server = ''
    database = ''
    username = ''
    password = ''

    def get_connection(self):
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self.server+';DATABASE='+self.database+';UID='+self.username+';PWD='+ self.password)
        return cnxn
