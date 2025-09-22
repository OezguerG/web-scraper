
import scrapy

class BoxOfficeSpider(scrapy.Spider):
    name = "boxoffice"
    start_urls = [
        "https://www.boxofficemojo.com/chart/ww_top_lifetime_gross/",
        "https://www.boxofficemojo.com/chart/ww_top_lifetime_gross/?offset=200",
        "https://www.boxofficemojo.com/chart/ww_top_lifetime_gross/?offset=400"
        ]
    
    def parse(self, response):
        # Chat-GPT: for-loop and rank

        for row in response.css("tr"):
            rank = row.css("td:nth-child(1)::text").get()
            title = row.css("td.a-text-left.mojo-field-type-title a.a-link-normal::text").get()
            url = row.css("td.a-text-left.mojo-field-type-title a.a-link-normal::attr(href)").get()

            if title and url and rank:
                yield {
                    'Rank': rank.strip(),
                    'Title': title.strip(),
                    'Url': response.urljoin(url.strip()),
                }
