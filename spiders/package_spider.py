# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapyspider.items import PythonPackageItem


class PackageSpider(CrawlSpider):
    name = 'package'
    allowed_domains = ['pypi.org']
    start_urls = [
        'https://pypi.org/search/?q=scrapy',
        'https://pypi.org/search/?q=scrapying',
    ]
    rules = (
        Rule(LinkExtractor(
            allow=[r'/project/[\w-]+/[\d\.]*', ],
            restrict_xpaths=['//ul/li', ],
        ), follow=True, callback='parse_package',
        ),
    )

    # 清洗
    def grab_data(self, response, xpath_sel):
        data = response.xpath(xpath_sel).extract()
        # 多个元素的列表不处理
        if len(data) > 1:
            return data
        elif len(data) == 1:
            if data[0].isdigit():
                return int(data[0])
            return data[0].strip()
        else:
            return []
        return []

    # 去重并清洗
    def uniq_data(self, lists):
        # 去重
        lists = list(set(lists))
        # 多个元素列表不处理
        if len(lists) > 1:
            return lists
        elif len(lists) == 1:
            if lists[0].isdigit():
                return int(lists[0])
            return lists[0].strip()
        else:
            return []
        return []

    def parse_package(self, response):
        item = PythonPackageItem()
        item['package_page'] = response.url
        # item['package_name'] = response.xpath('//div[@class="package-header__left"]/h1/text()').extract()
        item['package_name'] = self.grab_data(response, '//div[@class="package-header__left"]/h1/text()')
        # item['package_short_description'] = response.xpath('//p[@class="package-description__summary"]/text()')
        # .extract()
        item['package_short_description'] =\
            self.grab_data(response, '//p[@class="package-description__summary"]/text()')
        # item['home_page'] = response.xpath('//div/a/text()[contains(., "Homepage")]/../@href').extract()
        item['home_page'] = self.grab_data(response, '//div/a/text()[contains(., "Homepage")]/../@href')
        # 去重
        item['home_page'] = self.uniq_data(item['home_page'])
        item['python_version'] = []
        # versions = response.xpath('//dd/a[contains(text(), "Python ::")]/text()').extract()
        versions = self.grab_data(response, '//dd/a[contains(text(), "Python ::")]/text()')
        for v in versions:
            version_number = v.split("::")[-1]
            item['python_version'].append(version_number.strip())
        # 去重
        item['python_version'] = self.uniq_data(item['python_version'])
        # item['package_downloads'] =
        # response.xpath('//tbody/tr/td/a[contains(@href, "files.pythonhosted.org")]/@href').extract()
        item['package_downloads'] =\
            self.grab_data(response, '//tbody/tr/td/a[contains(@href, "files.pythonhosted.org")]/@href')
        return item
