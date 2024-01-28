## Automated End to End Tokyo House Rent Analysis 
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
    and save the following inside it(fill the values based on your own system configs):

    database_info = {
    'host': 'your host',
    'dbname': 'tokyohousing',
    'user': 'your postgres username',
    'pwd': 'postgres pass',
    }

    This file is used to connect to database inside your local system (it uses the created database)

1. run the following command:   python automating.py num
   1.1    replace num with an integer, it will be the number of pages you want to script (each page contains 15 data) 

The project starts with scraping and saving the data in a postgres database called "tokyohousing";
then it initializes the MLFlow by loading the data from database, clean the data (preprocessing), save preprocessor.pkl file,
afterwards it split the data in train and test dataset and save them in two tables in tokyohousing database in postgres and it uses the train data to train the model with different algorithms and gets the best performing algorithm after performing Hyperparameter tuning and save the best performing model into a file called "model.pkl"

2.  open your prefered browser and type:    http://127.0.0.1:5000/predictdata  
you can insert the input and get the result based on model.pkl after processing the input data by preprocessor.pkl.
