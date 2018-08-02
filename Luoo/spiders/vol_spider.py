import scrapy


class VolSpider(scrapy.Spider):
    name = 'vol'
    allowed_domains = 'www.luoo.net'
    start_urls = ['http://www.luoo.net/tag/?p=1']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

    def parse(self, response):
        max_page = int(
            response.css(
                '.paginator > .page::text'
            )[-1].extract()
        )
        yield scrapy.Request(
            'http://www.luoo.net/tag/?p=1',
            meta={
                "page": 1,
                "max_page": max_page
            },
            callback=self.get_vol_list
        )

    def get_vol_list(self, response):
        page = response.meta['page']
        max_page = response.meta['max_page']
        for item in response.css('.vol-list > .item'):
            url = item.css('a.cover-wrapper::attr(href)')[0].extract()
            vol_info = item.css('a.name::text')[0].extract()
            [vol_id, vol_name] = ' '.split(vol_info)[0]
            vol_id = int(vol_id)
            scrapy.Request(
                url,
                meta={
                    "vol_id": vol_id,
                    "vol_name": vol_name
                },
                callback=self.get_vol_info
            )
        if page < max_page:
            page += 1
            yield scrapy.Request(
                'http://www.luoo.net/tag/?p={}'.format(page),
                meta={
                    "page": page,
                    "max_page": max_page
                },
                callback=self.get_vol_list
            )

    def get_vol_info(self, response):
        vol_id = response.meta['vol_id']
        vol_name = response.meta['vol_name']
        vol_cover = response.css('img.vol-cover::attr(src)')[0].extract()
        vol_desc = '\n'.join(map(
            lambda i: i.extract(),
            response.css('div.vol-desc > p::text')
        ))
        vol_date = response.css('span.vol-date::text').extract()
        self.get_vol_tracks(response.css('li.track-item.rounded'))

    def get_vol_tracks(self, tracks):
        pass

    @staticmethod
    def is_vol_exist(vol_id):
        return False