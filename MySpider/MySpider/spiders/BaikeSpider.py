from typing import Any, Iterable
from scrapy.http import Request, Response
from scrapy import Spider, Selector
from urllib.parse import unquote


class BaikespiderSpider(Spider):
    name = "BaikeSpider"
    allowed_domains = ["baike.baidu.com"]
    outputFolder = "output/"
    mode = "parse"

    # * Initialize the spider with the given paths and mode
    def __init__(self, paths: str=None, mode: str="parse", **kwargs: Any):
        super().__init__(self.name, **kwargs)
        # * Crawl the page of the given path
        if paths:
            paths = paths.split(',')
            self.start_urls = [f'https://baike.baidu.com/item/{path}' for path in paths]
        else:
            self.start_urls = ['https://baike.baidu.com/item/scrapy']
        if mode != "save" and mode != "parse":
            self.log(f"\033[1;31m Invalid mode: {mode} \033[0m")
            exit(1)
        self.mode = mode
        self.callbacks = {
            "save": self.save,
            "parse": self.parse_content
        }

    def start_requests(self) -> Iterable[Request]:
        for url in self.start_urls:
            self.log(f"\033[4;32m Request path: {url} \033[0m")
            # * Set dont_filter to False to avoid multiple requests to the same page
            yield Request(url, callback=self.callbacks.get(self.mode), dont_filter=False)

    # * Save the response to a file
    def save(self, response: Response):
        self.log(f"\033[4;32m Response path: {response.url} \033[0m")
        outputFile = self.getOutputFile(response=response, format="html")
        with open(self.outputFolder + outputFile, 'wb') as f:
            f.write(response.body)

    # * parse the content of the page
    def parse_content(self, response: Response):
        selector = Selector(response=response)
        # * page title
        title = selector.xpath('//title/text()').extract_first()
        # * page description
        description = selector.xpath('//meta[@name="description"]/@content').extract_first()
        # * page Update date
        dateUpdate = selector.xpath('//meta[@itemprop="dateUpdate"]/@content').extract_first()

        outputFile = self.getOutputFile(response=response)
        with open(self.outputFolder + outputFile, 'w') as f:
            f.write(f"Title: {title}\n")
            f.write(f"Date Update: {dateUpdate}\n")
            f.write(f"Description: {description}\n")

    @staticmethod
    def getOutputFile(response: Response, format: str="txt") -> str:
        outPath = str(response.url[str(response.url).index('item/')+5:])
        if '/' in outPath:
            outPath = outPath[:outPath.index('/')] + f".{format}"
        else:
            outPath = f"{outPath}.{format}"
        return unquote(outPath)
