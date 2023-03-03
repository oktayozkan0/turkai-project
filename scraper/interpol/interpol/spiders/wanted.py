import scrapy
from ..items import InterpolItem


class WantedSpider(scrapy.Spider):
    name = "wanted"

    def start_requests(self):
        yield scrapy.Request(
            "https://www.interpol.int/How-we-work/Notices/View-Red-Notices",
            callback=self.search_by_nationalities
        )

    def search_by_nationalities(self, response):
        data = response.xpath(
            "//select[@id='arrestWarrantCountryId']/option/@value"
        ).getall()
        for d in data:
            yield scrapy.Request(
                f"https://ws-public.interpol.int/notices/v1/red?arrestWarrantCountryId={d}&&resultPerPage=160&page=1",
                callback=self.paging_if_necessary
            )

    def paging_if_necessary(self, response):
        data = response.json()
        # yields items of first page
        for d in data["_embedded"]["notices"]:
            item = InterpolItem()
            item["forename"] = d.get("forename")
            item["name"] = d.get("name")
            item["date_of_birth"] = d.get("date_of_birth")
            item["entity_id"] = d.get("entity_id")
            try:
                item["thumbnail"] = d.get("_links").get("thumbnail").get("href")
            except:
                item["thumbnail"] = None
            entity_id = d.get('entity_id').replace('/','-')
            item["url"] = f"https://www.interpol.int/How-we-work/Notices/View-Red-Notices#{entity_id}"
            yield item

        # yields scrapy request if page has more than 1 page
        if int(data["_links"]["last"]["href"][-1]) > 1:
            total_page = int(data["_links"]["last"]["href"][-1])
            for i in range(2, total_page+1):
                url_as_list = list(response.url)
                url_as_list[-1] = str(i)
                url = "".join(url_as_list)
                yield scrapy.Request(url, callback=self.final_parse)

    def final_parse(self, response):
        data = response.json()
        for d in data["_embedded"]["notices"]:
            item = InterpolItem()
            item["forename"] = d.get("forename")
            item["name"] = d.get("name")
            item["date_of_birth"] = d.get("date_of_birth")
            item["entity_id"] = d.get("entity_id")
            try:
                item["thumbnail"] = d.get("_links").get("thumbnail").get("href")
            except:
                item["thumbnail"] = None
            item["url"] = response.url
            yield item
