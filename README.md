## End to End Tokyo House Rent Analysis 
In this project:
1.  We scrape the data for available houses to rent from "https://apartments.gaijinpot.com/en/rent" website
2.  Save the scraped data in a database inside postgresql (make sure to create the database manually to make connection to it)
3.  Then we create a MLFlow to analyze the acquired data and built the best fit model on it to use for prediction
4.  Create a django webapplication to get user-input to make predictions and give recommendations