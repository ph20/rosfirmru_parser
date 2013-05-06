#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
from grab.spider import Spider, Task, Data
import config
from company_db import CompanyDB
from grab.tools.logs import default_logging

comp_db = CompanyDB(config.DB_FILE)
TEL_CLEAR_PATTERN = re.compile('; :\n; ')

class RosfirmCrawler(Spider):

    initial_urls = config.INITIAL_URLS
    parsed_urls = comp_db.get_parsed_url() ## кортеж уже спаршеных ссылок карточек компаний
    def prepare(self):
        pass

    def task_initial(self, grab, task):
        for url_level_1 in grab.xpath_list('//div[@class="alphabeticalIndex typical"]//h4/a[not(@onclick)]/@href'):
            yield Task('level_1', url=grab.make_url_absolute(url_level_1), priority = 95)

    def task_level_1(self, grab, task):
        for url_level_2 in grab.xpath_list('//div[@class="alphabeticalIndex typical"]//h4/a[not(@onclick)]/@href'):
            yield Task('level_2', url=grab.make_url_absolute(url_level_2), priority = 75)

    def task_level_2(self, grab, task):

        next_page_list = grab.xpath_list('//a[@class="next"]/@href')
        if next_page_list:
            next_page_url = grab.make_url_absolute(next_page_list[0])
            yield Task('level_2', url=next_page_url, priority = 80)

        for elem in grab.xpath_list('//div[@class="goodsElement listType company"]'):
            rating_company = elem.xpath('*/div[@class="rating_company"]/div/@class')
            if rating_company:
                rating_company = rating_company[0]
            else:
                rating_company = 0

            url_card_company = elem.xpath('div[@class="goodsDescription"]//a/@href')[0]
            url_card_company = grab.make_url_absolute(url_card_company)
            url_card_company = url_card_company.rstrip('/')  + '/contacts.htm'
            if not(url_card_company in self.parsed_urls):
                yield Task('level_3', url=url_card_company, priority = 25, rating = rating_company)
                self.parsed_urls.add(url_card_company)

    def task_level_3(self, grab, task):
        try:
            company_name = grab.xpath_text('//div[@class="company_name"]')
        except:
            company_name = ''

        if company_name:
            try: adr = grab.xpath_text('//span[@class="adr"]')
            except: adr = ''

            try:
                tel = '; '.join(grab.xpath_list('//div[@class="center_cont"]//span[@class="tel"]//text()'))
                tel = TEL_CLEAR_PATTERN.sub(' ', tel)
            except: tel = ''


            try: website = grab.tree.xpath('//span[contains(text(), $text)]/parent::p/a/@href', text="Сайт:")[0]
            except: website = ''

            try: person = grab.tree.xpath('//span[contains(text(), $text)]/parent::p/text()', text="Руководитель")[0]
            except: person = ''

            comp_db.save_comp_card(url_card = task.url,
                                   rating=task.get('rating'),
                                   website=website,
                                   name =company_name,
                                   email='',
                                   tel=tel,
                                   person=person,
                                   address=adr)
        else:
            comp_db.save_comp_card(url_card = task.url, rating=task.get('rating'))
            #yield Task('level_3', url=task.url, priority = 15, refresh_cache=True, rating = task.get('rating'))

def start_parsing():
    default_logging(grab_log=config.GRAB_LOG, network_log=config.NETWORK_LOG)
    bot = RosfirmCrawler(thread_number=config.THREAD_NUMBER)
    #    bot = ProffNoCrawler(thread_number=config.THREAD_NUMBER)
    #bot.setup_queue('mysql', database='proff_no', use_compression=True, user='proff_no', passwd='proff_no_u7Hy4')
    bot.setup_cache('mysql',
                    database=config.MYSQL_DB,
                    use_compression=True,
                    user=config.MYSQL_USER,
                    passwd=config.MYSQL_PASS)
    if config.DEBUG:
        bot.setup_grab(log_dir=config.LOG_DIR)
    bot.load_proxylist(config.PROXY_LIST, 'text_file', proxy_type='http')
    try:
        bot.run()
        print bot.render_stats() ## вывод статистики в случае render_stats_on = 1
        bot.save_list('fatal', config.FATAL_ERROR_DUMP)
    except KeyboardInterrupt:
        if config.DEBUG:
            bot.save_list('fatal', config.FATAL_ERROR_DUMP)
        print bot.render_stats()
    sys.exit()

if __name__ == '__main__':
    start_parsing()





