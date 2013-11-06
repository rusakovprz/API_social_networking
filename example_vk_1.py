# -*- coding: utf-8 -*-
"""
  File: example_vk_1.py
  
  Deskciption: 
  Пример использования модуля vk.py - API социальной сети vkontakte.com
    
  Нужно собрать список всех пользователей сети vkontakte из определенного города.
  На выходе нужен текстовый файл, 1 строка - 1 ID и ссылка на профиль.


  ВНИМАНИЕ!!!!!!
  
  Разработка примера не завершена.

  - Результат поиска будем сохранять в CSV- файл.
    Необходимо потренироваться в использовании соответствующей библиотеки.
    
    
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
#list_sity = rest.execute("database.getCities", 'cid', 'title', country_id='1', q=Sity_name, need_all='1', count ='10')

""" 
  Если идентификатор единственный, то используя е гоосуществляем поиск пользоватеей.
  Если идентификаторов несколько, то росим пользователя его уточнить. 
"""
#
'''
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
'''
#

""" 'uid', 'first_name', 'last_name'
  938574
"""

print rest.execute("users.search",  fields='nickname,screen_name,sex,city', city='10', country='1', count='2', offset='998', access_token='a2b35ae84a30ad68ac904824ce030c5b37709d1e392a6126c0e8b11043930db0c77329fd327892f7903a5')



""" Используя API vk наполняем список 'data' данными """

data = [('1', 'link1'), ('2', 'link2'), ('3', 'link3')] 

""" Записываем собранные данные в файл """

file_id = open('test.csv', 'w')
csv_stream = csv.writer(file_id, delimiter=';')

title = ('id', 'link')

csv_stream.writerow(title)
csv_stream.writerows(data)

file_id.close()

print "\nComplied."

