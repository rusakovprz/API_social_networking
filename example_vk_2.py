# -*- coding: utf-8 -*-
"""
  File: example_vk_1.py
  
  Deskciption: 
  Пример использования модуля vk.py - API социальной сети vkontakte.com
    
  Найти первые 100 груп с сети vkontakte по ключевым словам в их названии.
  На выходе нужен текстовый файл, содержащий статус, тип, и короткий адрес групп.

"""

import vk
import csv

rest = vk.vk()

# Необходимо заменить значение access_token на актуальный. 
data = rest.execute("groups.search", 'is_closed', 'type', 'screen_name', q="выгодные_покупки", sort='0', count='100', access_token="ab2c")

""" Записываем собранные данные в файл """
file_id = open('test_2.csv', 'w')
csv_stream = csv.writer(file_id, delimiter=';')

title = ('is_closed', 'type', 'screen_name')
csv_stream.writerow(title)

csv_stream.writerows(data)

file_id.close()

print "\nComplied."

