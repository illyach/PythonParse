import scrapy

class ScrapemeSpider(scrapy.Spider):
    name = "scrapeme"
    allowed_domains = ["scrapeme.live"]
    start_urls = ["https://scrapeme.live/shop/"]

    def parse(self, response):
        products = response.css(".product")

        for product in products:
            name = product.css("h2::text").get()
            image = product.css("img").attrib["src"]
            price_text_elements = product.css(".price *::text").getall()
            price = "".join(price_text_elements)
            url = product.css("a").attrib["href"]

            yield {
                "name": name,
                "image": image,
                "price": price,
                "url": url,
            }

        # generate requests for next pages
        for page_number in range(2, 49):
            next_page_url = "https://scrapeme.live/shop/page/{}/".format(page_number)
            yield scrapy.Request(next_page_url)