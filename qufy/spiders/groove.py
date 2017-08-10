# coding: utf-8

import urllib
from urllib import quote

import scrapy
from scrapy import Request
from tornado.escape import utf8, to_unicode

class GrooveSpider(scrapy.Spider):
    name = "Groove"

    __base_url = "http://www.microsoft.com"
    __search_url = "http://www.microsoft.com/en-us/store/search/music?q={}&type=album"
    __headers = {"Host": "www.microsoft.com", "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "deflate", "Referer": "http://www.microsoft.com/", "Connection": "keep-alive", "Upgrade-Insecure-Requests": "1", "Cache-Control": "max-age=0"}

    def start_requests(self):

        album_name = 'loose change'
        artist_names = ', '.join(['Ed Sheeran', ])
        album_encoded = utf8(album_name + ', ' + artist_names)

        search_url = self.__search_url.format(quote(album_encoded))

        yield Request(
            url=search_url,
            headers=self.__headers,
            meta={
                'dont_merge_cookies': True,
                "release_feedback": feedback,
                },
            )

    def parse(self, response):

        album_name_list  = response.xpath('//a[@data-selector="details-link" and @itemprop="url" and @title!=""]/@title').extract()
        album_url_list   = response.xpath('//a[@data-selector="details-link" and @itemprop="url" and @title!=""]/@href').extract()
        artist_name_list = response.xpath('//a[@data-selector="subdetails-link" and @data-bi-name!="" and @class="x-hidden-focus" and ../@class="media-subheader"]/@data-bi-name').extract()

        albums = zip(album_name_list, album_url_list, artist_name_list)

        for item in albums:
            if self.format_compare_key(utf8(item[0])) == self.format_compare_key(utf8('loose change')):
                extracted_artist_names = set(self.format_compare_key(utf8(item[2])).split(','))
                local_artist_names = set([self.format_compare_key(utf8(artist)) for artist in ['Ed Sheeran', ]])
                if len(local_artist_names.intersection(extracted_artist_names)) > 0:
                    print urllib.basejoin(self.__base_url, item[1])
                    break
