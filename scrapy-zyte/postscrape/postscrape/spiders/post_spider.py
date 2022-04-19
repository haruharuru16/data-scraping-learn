import scrapy


class PostSpider(scrapy.Spider):
    name = 'posts'

    start_urls = [
        'https://www.zyte.com/blog/',
        'https://www.zyte.com/blog/page/2/'
    ]

    def parse(self, response):
        # scraping the entire page
        # page = response.url.split('/')[-1]
        # filename = 'posts-%s.html' % page

        # with open(filename, 'wb') as f:
        #     f.write(response.body)

        for post in response.css('div.oxy-post'):
            yield {
                'post-title': post.css('a.oxy-post-title::text').get(),
                'author': post.css('div.oxy-post-meta-author.oxy-post-meta-item::text').get().replace('\n', '').replace('\t', '').replace('By ', ''),
                'link': 'https://www.zyte.com' + post.css('a.oxy-read-more').attrib['href'],
            }

        next_page = 'https://zyte.com' + \
            response.css('a.next.page-numbers').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
