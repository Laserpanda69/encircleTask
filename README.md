Hello Encircle Marketing!
Thank you for the opportunity to show you my work.

The main script is the scraper.py file. It takes the dimensions of the tyre as commandline arguments. 
So to use the scraper simply type into the command line 'python scraper.py 205 55 16' for a tyre of width 205 aspect raito 55 and rim size 16.

An obvious next step to make this use friendly would be to have dialogue asking for these 3 seperatly, however this would actually slow a developer down so CMD args are being used for now.

The database manager includes create and read methods but not update or delete. This is because web scrapes are snapshots of the page at the time, so only creation and reading a nessesary.

The database itself is a simple directory of CSV files named after the width, aspect ratio, and rim size of the tyres in the file. 
Further development would connect this is a more robust and larger scale sata base, possibly a local SQL instance like mySQL or a cloud database like GCP SQL or BigTable.
