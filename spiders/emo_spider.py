# -*- coding: utf-8 -*-
import scrapy
from scrapyspider.items import EmojiSpiderItem


# 继承
class EmoSpider(scrapy.Spider):
    # 爬虫名称是在命令行执行爬虫时用的
    name = 'emo'
    allowed_domains = ['emoji-cheat-sheet.com']
    start_urls = ['http://www.emoji-cheat-sheet.com/', ]

    def parse(self, response):
        # self.log('A response from %s just arrived!' % response.url)
        headers = response.xpath('//h2|//h3')
        lists = response.xpath('//ul')
        all_items = []
        for header, list_cont in zip(headers, lists):
            section = header.xpath('text()').extract()[0]
            for li in list_cont.xpath('li'):
                item = EmojiSpiderItem()
                item['section'] = section
                spans = li.xpath('div/span')
                if len(spans):
                    link = spans[0].xpath('@data-src').extract()
                    if link:
                        item['emoji_link'] = response.url + link[0]
                    handle_code = spans[1].xpath('text()').extract()
                else:
                    handle_code = li.xpath('div/text').extract()
                if handle_code:
                    item['emoji_handle'] = handle_code[0]
                all_items.append(item)
        return all_items
