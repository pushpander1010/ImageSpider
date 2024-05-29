import scrapy
from ImageBot.items import ImageItem


class SpiderSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = []
    start_urls = ["https://www.amazon.in"]

    def parse(self, response):
        raw_img_urls=response.css('img::attr(src)').getall()
        img_urls=[]
        for raw_url in raw_img_urls:
            img_urls.append(response.urljoin(raw_url))
        ImgItem=ImageItem()
        ImgItem['image_urls']=img_urls
        ImgItem['len']=len(img_urls)
        yield ImgItem

