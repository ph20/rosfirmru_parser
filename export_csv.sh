#!/bin/bash
sqlite3 company_db.sqlite <<!
.headers on
.mode csv
.output rosfirm.ru_parsed.csv
SELECT * FROM company_data;
!
