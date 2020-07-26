# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
import requests
from nairaland.items import NairalandItem


def get_topic(soup):
    return soup.title.string


def get_view_count(d):
    e = d.split('(')[-1]
    f = int(''.join(filter(str.isdigit, e)))
    return f


def pairwise(iterable):
    a = iter(iterable)
    return zip(a, a)


def get_sub_page_count(soup, val):
    dood = soup.find_all("a", href=re.compile(val))
    need = [''.join(filter(str.isdigit, i.text)) for i in dood]
    nn = list(set([i for i in need if len(i) < 2]))
    if len(nn) == 1 and not nn[0].isdigit():
        return 1
    elif len(nn) == 0:
        return 1
    else:
        return int(max(nn))


MAX_URL = 6000000


class CrawlerSpider(scrapy.Spider):
    name = 'nairaland_crawler'
    allowed_domains = ['https://nairaland.com/']

    def start_requests(self):
        urls = [self.allowed_domains[0] + str(i) + '/' for i in range(14, MAX_URL)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        nairalandItem = NairalandItem()
        html = response.body
        url_id = response.url.split('/')[-2]
        soup = BeautifulSoup(html, "lxml")
        table = soup.find("p", {"class": "bold"})
        nairalandItem['topic'] = get_topic(soup)
        nairalandItem['topic_id'] = url_id
        nairalandItem['url'] = response.url
        if not table:
            nairalandItem['class_'] = None
            nairalandItem['view_count'] = None
            nairalandItem['comments'] = [
                {'user': None, 'text': "This topic has been deleted or removed", 'pageId': None,
                 'sex': None, 'timestamp': None}]
        else:
            nairalandItem['class_'] = table.text.split('/')[2:]
            nairalandItem['view_count'] = get_view_count(table.text.split('/')[-1])
            subpage_count = get_sub_page_count(soup, url_id)
            comments = []
            for idx in range(subpage_count):
                current_r = requests.get("https://www.nairaland.com/{0}/{1}".format(url_id, idx))
                current_soup = BeautifulSoup(current_r.content, "lxml")
                table = current_soup.find("table", {"summary": "posts"})
                for user, text in pairwise(table.findAll("tr")):
                    for td in user:
                        comment = {}
                        cr = td.find("a", {'class': 'user'})
                        cd = td.find("span", {"class": "s"})
                        sex = td.find("span", {"class": "m"})
                        attachments = text.find_all("img", {"class": "attachmentimage img"})
                        if cr:
                            comment['user'] = cr.text
                            comment['timestamp'] = cd.text
                            comment['attachments'] = [i['src'] for i in attachments if i]
                            comment['sex'] = sex.text if sex else "f"
                            comment['pageId'] = idx
                            if text.find('blockquote'):
                                quoted_text = text.find('blockquote').text
                                comment['is_quote'] = True
                                comment['text'] = text.text.replace(quoted_text, '')
                                comment['quoted_text'] = quoted_text.split(':')[-1]
                            else:
                                comment['is_quote'] = False
                                comment['text'] = text.text
                                comment['quoted_text'] = ''
                            comments.append(comment)
                nairalandItem['comments'] = comments
            yield nairalandItem
