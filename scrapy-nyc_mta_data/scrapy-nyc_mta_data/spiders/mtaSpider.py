import scrapy
import logging
from scrapy.selector import Selector

class StackOverflowSpider(scrapy.Spider):
    name = 'mta'
    allowed_domains = ["mta.info"]
    start_urls = ['http://web.mta.info/nyct/facts/ridership/ridership_sub_annual.htm']

    def parse(self, response):
		stations = response.xpath('//table[@id="subway"]/tr')
		items = []
		

		for station in stations:
			item = {}
			station_info = {}

			item['name'] = station.xpath('./td[1]/div/strong/text()').extract()
			item['2009_ridership'] = station.xpath('./td[2]/text()').extract()
			item['2010_ridership'] = station.xpath('./td[3]/text()').extract()
			item['2011_ridership'] = station.xpath('./td[4]/text()').extract()
			item['2012_ridership'] = station.xpath('./td[5]/text()').extract()
			item['2013_ridership'] = station.xpath('./td[6]/text()').extract()
			item['2014_ridership'] = station.xpath('./td[7]/text()').extract()
			item['2013-14_diff'] = station.xpath('./td[8]/text()').extract()
			item['change'] = station.xpath('./td[9]/text()').extract()
			item['2014_rank'] = station.xpath('./td[10]/text()').extract()

			station_info['station'] = item

			if(item['name'] != []):
				items.append(station_info)
			
			

		return items

    def parse_question(self, response):
        yield {
            'title': response.css('.title a::text').extract()[0],
            'votes': response.css('.question .vote-count-post::text').extract()[0],
            'body': response.css('.question .post-text').extract()[0],
            'tags': response.css('.question .post-tag::text').extract(),
            'link': response.url,
        }