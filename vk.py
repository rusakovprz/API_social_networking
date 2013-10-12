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
    
  def get_user(self, user_IDs):
    """
      user_IDs -- список идентификаторов пользователей.
    
      >>> config = {}  
      >>> obj = vk(config)
  
      >>> user_IDs = [1,2]
      >>> obj.get_user(user_IDs)
      {"response":[{"uid":1,"first_name":"Павел","last_name":"Дуров"},{"uid":2,"first_name":"Александра","last_name":"Владимирова","hidden":1}]}
    """  

    connect = httplib.HTTPSConnection(self.__host)
    url = "/method/users.get?user_ids=" + self.list_IDs_to_string(user_IDs) 
     
    connect.request( "GET", url)	  
    response=connect.getresponse()
    print response.read()
    
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
    
    
if __name__ == "__main__":

  import doctest 
  print "DocTest vk.py" 
  print "  ", doctest.testmod(), "\n"

