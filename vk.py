# -*- coding: utf-8 -*-

"""
  File: vk.py
  
  Description:
    API for social network Vkontakte http://vk.com    

  Author: Rusakov Alexey <rusakovprz@rambler.ru> 

"""

import httplib
  
class vk():
  def __init__(self, configuration):
    """ Конфигурационные данные. """
    self.__configuration = configuration
    """" Имя узла предоставляющего API. """
    self.__host = 'api.vk.com'
    self.__connect = httplib.HTTPSConnection(self.__host)
  
  def __del__(self):
    pass
    
  def get_user(self, user_IDs):
    """
      user_IDs -- список идентификаторов пользователей.
    
      >>> config = {}  
      >>> obj = vk(config)
  
      >>> user_IDs = [1,2]
      >>> obj.get_user(user_IDs)
      {"response":[{"uid":1,"first_name":"Павел","last_name":"Дуров"},{"uid":2,"first_name":"Александра","last_name":"Владимирова","hidden":1}]}
    """  

    url = "/method/users.get?user_ids=" + self.list_IDs_to_string(user_IDs) 
     
    self.__connect.request( "GET", url)	  
    response=self.__connect.getresponse()
    print response.read()
    
    # TODO: print заменить на return, пи этом разобраться с кодировкой 

    
  @staticmethod  
  def list_IDs_to_string(user_IDs):
    """
    >>> vk.list_IDs_to_string([])
    ''
    >>> vk.list_IDs_to_string([1])
    '1'
    >>> vk.list_IDs_to_string([1,2,3])
    '1,2,3'
    """    
    out_string = ''
    
    for item in user_IDs:
      out_string += str(item)
      out_string += ','
    
    return out_string.rstrip(',')


  def execute(self, method_name, *return_data, **in_arguments):
    """
      Универсальный метод, который позволяет запускать вызывать любой метод API,
      с производьным числом аргументов и серриализацией возвращаемых данных.    
    
    >>> config = {}  
    >>> obj = vk(config)
    >>> user_IDs = vk.list_IDs_to_string( [1,2] )

    >>> obj.execute("users.get", user_ids=user_IDs)
    {"response":[{"uid":1,"first_name":"Павел","last_name":"Дуров"},{"uid":2,"first_name":"Александра","last_name":"Владимирова","hidden":1}]}
    
    """
    #print method_name
    #print return_data
    #print in_arguments
    
    url = "/method/" + method_name
    
    if len(in_arguments) > 0:
      url += "?"
    
    for key in in_arguments.keys():
      url += key + "=" + in_arguments[key] + ","
    
    url.lstrip(",")
    
    #print "url = ", url
    
    self.__connect.request( "GET", url)	  
    response=self.__connect.getresponse()
    print response.read()
    
    # TODO
    # - Серриализация возвращаемых данных на основании списка return_data
    # - print заменить на return, пи этом разобраться с кодировкой        
    
    
if __name__ == "__main__":

  import doctest 
  print "DocTest vk.py" 
  print "  ", doctest.testmod(), "\n"

