import os 
import sys
from subprocess import run  


def main(pages):
    global BASE_DIR
    BASE_DIR = os.getcwd()
    scrapy_path = os.path.join(BASE_DIR, "TokyoRent", "TokyoRent")
    os.chdir(scrapy_path)
    run_scrapy_file(pages)
    os.chdir(BASE_DIR)
    run_ML_file()
    run_app_file()


def run_scrapy_file(pages):
    os.environ['PAGES'] = str(pages)
    command = f'scrapy crawl Tokyohouserent -s PAGES={pages}'
    run(command , shell=True)


def run_ML_file():
    file_path = os.path.join(BASE_DIR, "TokyoRentML", "components", "data_ingestion.py")
    run(['python', file_path])


def run_app_file():

    run(['python', 'app.py'])


if __name__=='__main__':
    args = sys.argv
    if len(args) != 2 or not args[1].isdigit():
        raise Exception("You must pass the number of pages you wish to scrape")
    
    global page
    page = args[1]
    main(pages=page)

