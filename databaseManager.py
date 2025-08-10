# database manager required basic CRUD operations
import csv
import os

class databaseManager():
    def __init__(self, dir):
        self.directory: str = dir
        
        
    # public CRUD methods that check file exisits that call private methods that do not
    # The database being used is made of a directory containing CSV files
    # The CSV files are named after the width, aspect ratio, and rim size within
        
    def create(self, tyre_info: tuple, line:tuple):
        file = f"w{tyre_info[0]}ar{tyre_info[1]}r{tyre_info[2]}.csv"
        
        # If a tyre entry needs to be entered but the apprapriate file doesn't exist, creates the file
        if not os.path.isfile(self.directory +"/"+file):
            self.make_file_for_dimensions_(file)
            
        # Creates the entry after the file it goes in has been insured to exist
        self.create_(file=file, line=line)
        
    def read(self, tyre_info:tuple , index: int) -> tuple:
        file = f"w{tyre_info[0]}ar{tyre_info[1]}r{tyre_info[2]}.csv"
        
        # Returns none if a file for the requested tyre information does not exist (i.e. there are no entries)
        if not os.path.isfile(self.directory +"/"+file):
            return None
    
        return self.read_(file, index)

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
            reader = csv.reader(datafile)
            header_offset = 1
            for i, line in enumerate(reader):
                # header_offset is used to offset the 0 index from the header to the first tyre entry
                if index == i+header_offset:
                    return line
            # List comprehention lines = [line for line in reader] was used initially
            # However this was decided against as iterating through the whole reader
            # Would be innefficient for large datasets and small search indexes
                
        
    def make_file_for_dimensions_(self, file:str):
        print(file)
        with open(self.directory + f"/{file}", 'w', newline='') as datafile:
            writer = csv.writer(datafile)
            # Writes the header into the datafile
            writer.writerow(["website", "brand", "pattern", "size", "seasonality", "price"])
    
    