import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = "hhru"
    allowed_domains = ["hh.ru"]
    start_urls = ["https://hh.ru/search/vacancy?hhtmFrom=vacancy&hhtmFromLabel=vacancy_search_line&search_field=name&search_field=company_name&search_field=description&text=python&enable_snippets=false&L_save_area=true"]

    def parse(self, response:HtmlResponse):

        next_page = response.xpath("//a[@data-qa='number-pages-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@data-qa='serp-item__title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse) #действия происходят в рамках той же сессии



    def vacancy_parse(self, response:HtmlResponse):
        name = response.xpath("//div[@data-qa='vacancy-title']//h1[@data-qa='title']//text()").getall()


        salary = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)




