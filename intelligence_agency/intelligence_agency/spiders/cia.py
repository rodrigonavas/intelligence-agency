import scrapy

# xpath
links_xpath = '//a[starts-with(@href, "collection/") and (parent::h3|parent::h2)]/@href'
title_xpath = '//h1[@class="documentFirstHeading"]/text()'
paragraph_xpath = '//div[@class="field-item even"]//p[not(@class)]/text()'


class SpiderCIA(scrapy.Spider):
    name = 'cia'
    start_urls = [
        'https://www.cia.gov/readingroom/historical-collections'
    ]
    custom_settings = {
        'FEED_URI': 'cia.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self, response):
        links_declassified = response.xpath(links_xpath).getall()
        for link in links_declassified:
            yield response.follow(link, callback=self.parse_link, cb_kwargs={'url': response.urljoin(link)})

    def parse_link(self, response, **kwargs):
        link = kwargs['url']
        title = response.xpath(title_xpath).get()
        paragraph = response.xpath(paragraph_xpath).getall()
        p_number = 0
        if (len(paragraph[p_number]) < 30):
            p_number += 1

        yield {
            'url': link,
            'title': title,
            'body': paragraph[p_number]
        }
