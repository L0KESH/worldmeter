# -*- coding: utf-8 -*-
import scrapy
import logging


class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        countries = response.xpath("//td/a")
        for r in countries:
            name = r.xpath(".//text()").get()
            link   = r.xpath(".//@href").get()

            # yield {
            #     'country_name': name,
            #     'country_link': link
            # }
            #--------> using absolute url..... opposite to relative url 
            # abs_url = f"https://www.worldometers.info{link}"
            
            # abs_url = response.urljoin(link)
            # yield scrapy.Request(url=abs_url)

            yield response.follow(url=link, callback=self.parse_country, meta={'country_name': name})

    def parse_country(self, response):
        # logging.info(response.url)
        name = response.request.meta['country_name']
        rows = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()
            yield{
                'country_name': name,
                'year': year,
                'population': population
            }