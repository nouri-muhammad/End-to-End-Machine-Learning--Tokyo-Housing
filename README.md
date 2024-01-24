## End to End Tokyo House Rent Analysis 
In this project:
1.  We scrape the data for available houses to rent from "https://apartments.gaijinpot.com/en/rent" website
2.  Save the scraped data in a database inside postgresql (make sure to create the database manually to make connection to it)
3.  Then we create a MLFlow to analyze the acquired data and built the best fit model on it to use for prediction
4.  Using Flask to get user input and make predictions 

# How to run
*  create a database named "tokyohousing" inside postgresql. 

** create a file named "databaseinfo.py" in two directories:
    TokyoRentML/databaseinfo.py
    TokyoRent/TokyoRent/databaseinfo.py
    and save the following inside it:

    database_info = {
    'host': 'your host',
    'dbname': 'tokyohousing',
    'user': 'your postgres username',
    'pwd': 'postgres pass',
    }

    This file is used to connect to database inside your local system (it uses the created database)

1.  move to the following directory: TokyTokyoRent/TokyoRent/
2.  run: scrapy crawl Tokyohouserent 
    it scrapes the data, clean and save it inside a table called "rent" inside a database named tokyohousing.
3. get back to the main directory and run: python TokyoRentML/components/data_ingestion.py
   It reads the data from postgres, does all the preprocessing and saves the process into a file called "preprocessor.pkl" then splits the data in train and test sets; save them in two tables inside tokyohousing database. Then uses the train data to train the model and gets the best result and save the best performing model into a file called "model.pkl"
4. run:  python app.py
   in the browser search:   http://127.0.0.1:5000/predictdata
   you can insert the input and get the result using model.pkl after processing the input data by preprocessor.pkl.