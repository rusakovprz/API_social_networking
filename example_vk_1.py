# -*- coding: utf-8 -*-
"""
  File: example_vk_1.py
  
  Deskciption: 
  Пример использования модуля vk.py - API социальной сети vkontakte.com
    
  Нужно собрать список всех пользователей сети vkontakte из определенного города.
  На выходе нужен текстовый файл, 1 строка - ID, Имя, Фамилия.

"""

import vk
import csv

""" Пользователь вводит название города """

Sity_name = raw_input("Enter sity name: ") 
print "Sity_name = ", Sity_name

""" 
  Используя API vk получаем идентификатор города 
  Полагаем, что поиск осуществляем по городам России, потому соответственно
  ID страны указываем 1.  
"""
rest = vk.vk()
list_sity = rest.execute("database.getCities", 'cid', 'title', country_id='1', q=Sity_name, need_all='1', count ='10')

""" 
  Если идентификатор единственный, то используя е гоосуществляем поиск пользоватеей.
  Если идентификаторов несколько, то росим пользователя его уточнить. 
"""

if len(list_sity) == 0:
  print "Город в базеданных Vkontakte не найден."
  exit(-1)

Sity_ID = '0'

if len(list_sity) > 1:
  print " ID   Название города"
  
  for item in list_sity:
    print " %s  %s" % item
  
  Sity_ID = raw_input("\nEnter sity ID: ")

else:
  Sity_ID = list_sity[0][0]

print "Current Sity_ID = ", Sity_ID

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

args_list = vk.vk.create_arg_list(args_cfg)

data = rest.multi_threading_execute(args_list, True)

""" Записываем собранные данные в файл """
file_id = open('test.csv', 'w')
csv_stream = csv.writer(file_id, delimiter=';')

title = ("uid", "first_name", "last_name")

csv_stream.writerow(title)
csv_stream.writerows(data)

file_id.close()

print "\nComplied."

