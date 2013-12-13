# -*- coding: utf-8 -*-
"""
  File: example_vk_1.py
  
  Deskciption: 
  Пример использования модуля vk.py - API социальной сети vkontakte.com
    
  Найти первые 100 груп с сети vkontakte по сиску строк в их названии.
  На выходе нужен текстовый файл, 1 строка - ID, Имя, Фамилия.

"""

import vk
import csv

"""  """

rest = vk.vk()

Sity_ID = '10'

# Необходимо заменить значение access_token на актуальный. 
args_cfg = '\n\
{\n\
  "method_name":"users.search", \n\
  "list_keys":["uid", "first_name", "last_name"], \n\
\
  "in_arguments_constant":\n\
    {"city":"' + Sity_ID + '", "country":"1", "access_token":"ab2c"},\n\
\
  "in_arguments_iterable": \n\
  [\n\
    {"name":"birth_year",  "begin_value":"1913", "end_value":"1913"},\n\
    {"name":"birth_month",  "begin_value":"1", "end_value":"12"},\n\
    {"name":"birth_day",  "begin_value":"1", "end_value":"31"}\n\
  ]\n\
}\n'

#args_list = vk.vk.create_arg_list(args_cfg)
data = rest.execute("groups.search", 'is_closed', 'type', 'screen_name', q="выгодные_покупки", sort='0', count='100', access_token="a2b35ae84a30ad68ac904824ce030c5b37709d1e392a6126c0e8b11043930db0c77329fd327892f7903a5")

""" Записываем собранные данные в файл """
file_id = open('test_2.csv', 'w')
csv_stream = csv.writer(file_id, delimiter=';')

title = ('is_closed', 'type', 'screen_name')

csv_stream.writerow(title)
csv_stream.writerows(data)

file_id.close()

print "\nComplied."

