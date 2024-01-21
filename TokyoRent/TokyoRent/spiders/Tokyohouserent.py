import scrapy
import random
import time


class TokyohouserentSpider(scrapy.Spider):
    name = "Tokyohouserent"
    allowed_domains = ["apartments.gaijinpot.com"]
    start_urls = ["https://apartments.gaijinpot.com"]
    count = 0

    def parse(self, response):
        apartments = response.xpath("//div[contains(@class,'property-listing')]")

        for apartment in apartments:
            yield{
                'detail': apartment.xpath(".//div[@class='listing-item listing-title']//span[@itemprop='address']/text()").getall(),
                'price': apartment.xpath("./div[@class='listing-body']/div[@class='listing-right-col']/div[@class='listing-item'][1]/text()[normalize-space()]").get().replace('\n', '').replace('\t', ''),
                'size': apartment.xpath(".//div[@class='listing-info']/div[@class='listing-right-col']/div[@class='listing-item'][1]/text()[normalize-space()]").get().replace('\n', '').replace('\t', ''),
                'deposite': apartment.xpath(".//div[@class='listing-info']/div[@class='listing-right-col']/div[@class='listing-item'][2]/text()[normalize-space()]").get().replace('\n', '').replace('\t', ''),
                'key money': apartment.xpath(".//div[@class='listing-info']/div[@class='listing-right-col']/div[@class='listing-item'][3]/span[@class='']/text()[normalize-space()]").get().replace('\n', '').replace('\t', ''),
                'floor': apartment.xpath(".//div[@class='listing-info']/div[@class='listing-right-col']/div[@class='listing-item'][4]/text()[normalize-space()]").get().replace('\n', '').replace('\t', ''),
                'year built': apartment.xpath(".//div[@class='listing-info']/div[@class='listing-right-col']/div[@class='listing-item'][5]/text()[normalize-space()]").get(),
                'nearest station': apartment.xpath(".//div[@class='listing-info']/div[@class='listing-right-col']/div[@class='listing-item'][6]/span[@itemprop='name']/text()").get(),
            }

        next_page = response.xpath(".//li[@class='pagination-next']/a/@href").get()
        if next_page is not None and self.count<400:
            self.count += 1
            time.sleep(random.uniform(1, 2))
            next_page_url = 'http://apartments.gaijinpot.com' + next_page
            yield response.follow(next_page_url, callback=self.parse)
