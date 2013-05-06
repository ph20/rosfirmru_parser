#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3 as sqlite
import re

class CompanyDB():
    def __init__(self, db_file_name = 'company_db.sqlite'):
        self.__sqlconn = None
        self.__dbcursor = None
        self.__conn_db(db_file_name)
        self.__db_file_name = db_file_name
        self.__parsed_url_list = []

    def __conn_db(self,
                  dbname = 'company_db.sqlite', ## имя БД по умолчанию в которой будет хранитса информацыя о полученых сообщениях
    ):

        self.__sqlconn = sqlite.connect(dbname)
        self.__dbcursor = self.__sqlconn.cursor()
        ## проверка создана ли таблица с сообщениями если не создана то создаетса
        self.__dbcursor.execute("""SELECT name FROM sqlite_master WHERE name='company_data' """)
        if self.__dbcursor.fetchone():
            pass
        else:
            ## таблица для хранения последней статистике по ящику
            self.__dbcursor.execute("""CREATE  TABLE "main"."company_data" ("id" INTEGER PRIMARY KEY  NOT NULL  UNIQUE , "url_card" TEXT, "website" TEXT, "rating" TEXT, "name" TEXT, "email" TEXT, "tel" TEXT, "person" TEXT, "address" TEXT)""")
            self.__sqlconn.commit()

    def norm_url(self, url, NORM_PATERN = re.compile('(http:\/\/)?(www\.)?(.+)')):
        """
        Нормализует урл для стандартного вида в БД
        """
        return NORM_PATERN.match(url).group(3).rstrip('/')

    def check_url(self, url):
        """
        Проверяет присутствие url компании в БД
        урл вБД записываетса без http:// www и закривающего слеша
        Если отсутствует то возвращает 0
        Если присутствует возвращает id записи
        """
        #url = self.norm_url(url)
        self.__dbcursor.execute("""SELECT "id" FROM "company_data" WHERE "url_card"=?""", (url,))
        fetched = self.__dbcursor.fetchone()
        if fetched:
            return fetched[0]
        else:
            return 0

    def get_parsed_url(self):
        """
        Возвращает кортеж url спаршенных данных
        """
        self.__dbcursor.execute("""SELECT DISTINCT "url_card" FROM "company_data" WHERE "name"!='' """)
        return set([url[0] for url in self.__dbcursor.fetchall()])




    def save_comp_card(self, url_card, rating=0, website='', name ='', email='', tel='', person='', address=''):
        """
        Сохраняет в БД урл имя локального файла и firm_rank
        """
        #url_card = self.norm_url(url_card)
        self.__dbcursor.execute("""INSERT INTO "main"."company_data" ("url_card", "website", "rating", "name", "email", "tel", "person", "address") VALUES (?1,?2,?3,?4,?5,?6,?7,?8)""",
                                (url_card, website, rating, name, email, tel, person, address))
        self.__sqlconn.commit()



