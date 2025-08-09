# database manager required basic CRUD operations
import csv

class databaseManager():
    def __init__(self, dir):
        self.directory: str = dir
        
    def create(self, file, line):
        with open(self.directory + f"/{file}", newline='') as datafile:
            writer = csv.writer(datafile)
            writer.writerow(line)
        
    def read(self, file, index):
        with open(self.directory + f"/{file}", newline='') as datafile:
            writer = csv.reader(datafile)
            return writer.read(index)

    # update and delete have not been implemented as they are not needed, but are included to demonstrate database infrastructure 

    def update():
        pass

    def delete():
        pass
    
    