import scrapy


class TokyohouserentSpider(scrapy.Spider):
    name = "Tokyohouserent"
    allowed_domains = ["apartments.gaijinpot.com"]
    start_urls = ["https://apartments.gaijinpot.com/en/rent"]

    def parse(self, response):
        pass
