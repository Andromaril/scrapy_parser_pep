import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):

    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        all_peps = response.css('a.reference.external::attr(href)')
        for pep in all_peps:
            yield response.follow(pep, callback=self.parse_pep)

    def parse_pep(self, response):
        path = '//*[@id="pep-page-section"]/header/ul/li[3]//text()'
        number = [x.replace('PEP ', '').strip()
                  for x in response.xpath(path).extract()]
        data = {
            'number': number,
            'name': response.css('h1.page-title::text').get(),
            'status': response.css('dt:contains("Status") + dd::text').get()
        }
        yield PepParseItem(data)
