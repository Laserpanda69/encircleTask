# database manager required basic CRUD operations
import csv
import os

class databaseManager():
    def __init__(self, dir):
        self.directory: str = dir
        
        
    # public CRUD methods that check file exisits that call private methods that do not
        
    def create(self, tyre_info: tuple, line:tuple):
        file = f"w{tyre_info[0]}ar{tyre_info[1]}r{tyre_info[2]}.csv"
        print(file)
        
        if not os.path.isfile(self.directory +"/"+file):
            self.make_file_for_dimensions_(file)
            
        self.create_(file=file, line=line)
        
    def read(self, tyre_info:tuple , index):
        file = f"w{tyre_info[0]}ar{tyre_info[1]}r{tyre_info[2]}.csv"
    
        self.read_(file, index)

    # update and delete have not been implemented as they are not needed, but are included to demonstrate database infrastructure 

    def update():
        pass

    def delete():
        pass
    
    # PRIVATE METHODS
    
    def create_(self, file:str, line:tuple):
        with open(self.directory + f"/{file}", 'a', newline='') as datafile:
            writer = csv.writer(datafile)
            writer.writerow(line)
        
    def read_(self, file:str , index:int):
        with open(self.directory + f"/{file}", 'r', newline='') as datafile:
            writer = csv.reader(datafile)
            return writer.read(index)
        
    def make_file_for_dimensions_(self, file:str):
        print(file)
        with open(self.directory + f"/{file}", 'w', newline='') as datafile:
            writer = csv.writer(datafile)
            writer.writerow(["website", "brand", "pattern", "size", "seasonality", "price"])
    
    