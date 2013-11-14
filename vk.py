# -*- coding: utf-8 -*-

"""
  File: vk.py
  
  Description:
    API for social network Vkontakte http://vk.com/dev    

  Author: Rusakov Alexey <rusakovprz@rambler.ru> 

"""

import httplib
import json
  
class vk():
  def __init__(self):
    
    """" Имя узла предоставляющего API. """
    self.__host = 'api.vk.com'
    self.__connect = httplib.HTTPSConnection(self.__host)
    self.__counts_records = None
    
      
  def __del__(self):
    self.__connect.close()
    

  def execute(self, method_name, *list_keys, **in_arguments):
    """
      Универсальный метод, который позволяет вызывать любой метод API,
      с производьным числом аргументов и сериализацией возвращаемых данных.    
      (Нативная реализация Python-функции с переменным числом аргументов)
      
      method_name  -- название метода 
      list_keys    -- список полей, которые необходимо вернуть 
      in_arguments -- аргументы вызываемого метода
      
      list_keys используется для сериализаци данных полученный от REST-сервера.
      Если list_keys отсутствует, метод вернёт ответ полученный от REST-сервера,
      иначе будет возвращен список кортежей, каждый элемент кортежа содержит
      данные соответствующие ключам list_keys.  
       
    >>> obj = vk()
    >>> user_IDs = vk.list_IDs_to_string( [1,2] )
    >>> print obj.execute("users.get", user_ids=user_IDs)
    {"response":[{"uid":1,"first_name":"Павел","last_name":"Дуров"},{"uid":2,"first_name":"Александра","last_name":"Владимирова","hidden":1}]}
      
    >>> ret = obj.execute("users.get", 'uid', 'last_name', user_ids=user_IDs)
    >>> print ret
    [(1, u'\u0414\u0443\u0440\u043e\u0432'), (2, u'\u0412\u043b\u0430\u0434\u0438\u043c\u0438\u0440\u043e\u0432\u0430')]
    
    """
    
    return self.execute_3(method_name, list_keys, in_arguments)


  def execute_3(self, method_name, list_keys, in_arguments):
    """
      Универсальный метод, который позволяет вызывать любой метод API,
      с производьным числом аргументов и сериализацией возвращаемых данных.    
      (Реализация Python-функции с фиксированным числом аргументов. 
       Используется как альтернатива мметода execute() в многопоточной реализации.)
      
      method_name  -- название метода (type - string)
      list_keys    -- список полей, которые необходимо вернуть (type - List) 
      in_arguments -- аргументы вызываемого метода (type - Dictonary)
      
      list_keys используется для сериализаци данных полученный от REST-сервера.
      Если list_keys отсутствует, метод вернёт ответ полученный от REST-сервера,
      иначе будет возвращен список кортежей, каждый элемент кортежа содержит
      данные соответствующие ключам list_keys.  
    """
        
    url = "/method/" + method_name
    
    if len(in_arguments) > 0:
      url += "?"
    
    for key in in_arguments.keys():
      url += key + "=" + in_arguments[key] + "&"
    url = url.rstrip("&")
    
    self.__connect.request( "GET", url)	  
    response=self.__connect.getresponse()
    
    answer = response.read()
    json_data = json.loads( answer )
    
    if json_data.has_key('response'):
      
      """ 
        Определяем и сохраняем значение количества полученных записей. 
        
        FIXME: Возвращаемые структуры зависят от метода и содержимого ответов.
               Этот код следует переделать в рамках #10 
      """
      content = json_data.get('response')
            
      if len(content) == 0:
        self.__counts_records = 0
      else:
        
        if "<type 'list'>" == str(type(content)):
          if "<type 'int'>" == str( type(content[0]) ):
            self.__counts_records = content[0]
          else:
            self.__counts_records = (len(content))
        
        elif "<type 'dict'>" == str(type(content)): 
          self.__counts_records = len(content)
      
        else:
          pass
          
      """ Возвращаем данные полученные в ответе на запрос """
      
      if len(list_keys) == 0:
        return answer
      else:
        return  self.serialization(json_data.get('response'), list_keys)
            
    elif json_data.has_key("error"):
      error_string = 'От REST-server Получена ошибка.\n'
      error_string += 'error_code     = ' + str(json_data.get('error').get('error_code')) + '\n'
      error_string += 'error_msg      = ' + str(json_data.get('error').get('error_msg')) + '\n'
      error_string += 'request_params = ' + str(json_data.get('error').get('request_params')) + '\n'
      raise BaseException(error_string)


  def get_count(self):
    """
      Возвращает количество найденных записей для выборки определенного
      подмножества, полученных в результате последнего вызова метода execute.
      
      Уточнение: Количество найденных и возвращённых записей в большенстве случаев не зовпадают.
      Наёденных всегда больше.
    """
    
    return self.__counts_records


  @staticmethod  
  def list_IDs_to_string(user_IDs):
    """
      Преобразует список целочисленных идентификаторов в строку, 
      записывая их через запятую.
    
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


  @staticmethod  
  def serialization(data, list_keys):
    """
      Преобразует именованные списки в кортежи. В кортежи попадают только те
      элементы списка ключи которых совпадают со значениями элементов 
      списка list_keys  
      
      data      -- входные данные
      list_keys -- Список ключей, соответствующие которым данные попадают в 
      элементы выходных кортежей
    
    >>> data = []
    >>> keys = []
    >>> vk.serialization(data, keys )
    []
        
    >>> data = [{'key1':'value11', 'key2':'value12', 'key3':'value13'}, {'key1':'value21', 'key2':'value22', 'key3':'value23'}]
    >>> keys = []
    >>> vk.serialization(data, keys )
    [('value13', 'value12', 'value11'), ('value23', 'value22', 'value21')]
    
    >>> keys = ['key1', 'key2', 'key3']
    >>> vk.serialization(data, keys )
    [('value11', 'value12', 'value13'), ('value21', 'value22', 'value23')]
    
    >>> keys = ['key1', 'key3']
    >>> vk.serialization(data, keys )
    [('value11', 'value13'), ('value21', 'value23')]
        
    >>> keys = ['key3', 'key2', 'key1']
    >>> vk.serialization(data, keys )
    [('value13', 'value12', 'value11'), ('value23', 'value22', 'value21')]
       
    """    
    
    if len(data) == 0:
      return []
    
    if len(list_keys) == 0:
      list_keys = data[0].keys()

    return_list = []
    
    for index in range(len(data)):
      tmp_list = []
      try:
        for key in list_keys:
          value = data[index].get(key)
          tmp_list.append(value)
        return_list.append(tuple(tmp_list))      
      except:
        pass
      
    return return_list 



if __name__ == "__main__":

  import doctest 
  print "DocTest vk.py" 
  print "  ", doctest.testmod(), "\n"

