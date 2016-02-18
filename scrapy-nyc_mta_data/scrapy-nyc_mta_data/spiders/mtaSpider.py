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

			item['name'] = ''.join(station.xpath('./td[1]/div/*/text()[1]').extract())
			if((item['name'].isspace()) 
				or (item['name'] == '')):
				item['name'] = ''.join(station.xpath('./td[1]/div/*/a/text()').extract())
			
			imgsrcPath = './td[1]/div/*/img'
			item['lines'] = ''.join(station.xpath(imgsrcPath+'/@src').extract())
			if((item['lines'].isspace()) 
				or (item['lines'] == '')):
				imgsrcPath = './td[1]/div/img'
			
			subway_lines = station.xpath(imgsrcPath)
			lines = []

			for line in subway_lines:
				tempLine = ''.join(line.xpath('./@src').extract())
				"""tempLine.index(tempLine, beg=len(tempLine)-6 end=len(tempLine)-4)"""
				lines.append(tempLine[len(tempLine)-5:len(tempLine)-4])

			item['lines'] = lines

			item['2009_ridership'] = ''.join(station.xpath('./td[2]/text()').extract())
			item['2010_ridership'] = ''.join(station.xpath('./td[3]/text()').extract())
			item['2011_ridership'] = ''.join(station.xpath('./td[4]/text()').extract())
			item['2012_ridership'] = ''.join(station.xpath('./td[5]/text()').extract())
			item['2013_ridership'] = ''.join(station.xpath('./td[6]/text()').extract())
			item['2014_ridership'] = ''.join(station.xpath('./td[7]/text()').extract())
			item['2013-14_diff'] = ''.join(station.xpath('./td[8]/text()').extract())
			item['change'] = ''.join(station.xpath('./td[9]/text()').extract())
			item['2014_rank'] = ''.join(station.xpath('./td[10]/text()').extract())

			station_info['station'] = item

			if(item['name'] != ''):
				items.append(station_info)
			
			

		return items
