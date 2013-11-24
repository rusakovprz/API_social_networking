# -*- coding: utf-8 -*-

"""
  File: vk.py
  
  Description:
    API for social network Vkontakte http://vk.com/dev    

  Author: Rusakov Alexey <rusakovprz@rambler.ru> 

"""

import httplib
import json
import threading
import progressbar
import copy
  
class vk():
  def __init__(self):
    
    """" Имя узла предоставляющего API. """
    self.__host = 'api.vk.com'
    self.__connect = httplib.HTTPSConnection(self.__host)
    """ Количество записей полученных для последнего запроса """    
    self.__counts_records = None
    
    """ Блокировщик, используется в многопоточной реализации execute, 
      для защиты массива в который 'собираются' все дянные полученные
      от сервера из нескольких потоков. """
    self.locker = threading.Lock()
    
      
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


  def multi_threading_execute(self, args_list, process_bar=False):
    """
      Многопоточный вариант метода execute().
      args_list -- 
      process_bar -- 
            
    >>> rest = vk()
    >>> args_list=[('users.get', ['uid', 'first_name', 'last_name'], {'user_ids':'1'} ), ('users.get', ['uid', 'first_name', 'last_name'], {'user_ids':'2'} ) ]
    >>> rest.multi_threading_execute(args_list)
    [(1, u'\u041f\u0430\u0432\u0435\u043b', u'\u0414\u0443\u0440\u043e\u0432'), (2, u'\u0410\u043b\u0435\u043a\u0441\u0430\u043d\u0434\u0440\u0430', u'\u0412\u043b\u0430\u0434\u0438\u043c\u0438\u0440\u043e\u0432\u0430')]
    """
    
    output_data = []
    locker = threading.Lock()
    thread_list =[]
    
    if process_bar:
      self.progress_bar = progressbar.ProgressBar(maxval=len(args_list),
                                       widgets=['Count complied request: ',
                                       progressbar.SimpleProgress(),  '  ',
                                       progressbar.Bar(left='[', marker='+', right=']')]).start()
      self.coun_threads_complied = 0;

    for item in args_list:
      method_name, list_keys, in_arguments = item 
      t = threading.Thread(target = self.fork_execute, args=(method_name, list_keys, in_arguments, output_data, process_bar))
      t.daemon = True
      t.start()
      thread_list.append(t)

    for thread in thread_list:
      thread.join()  

    return output_data
        

  def fork_execute(self, method_name, list_keys, in_arguments, output_array, process_bar):
    """
      Реализация потока. Выполняет один запрос к серверу и добавляет 
      полученные данные в список output_array, выполняющий роль 
      аккумулятораполученных данных в нескольких потоках.
      method_name -- 
      list_keys -- 
      in_arguments --    
      process_bar -- 
    """  
    self.locker.acquire(True)
    response = self.execute_3(method_name, list_keys, in_arguments )
    
    if str(type(response)) == "<type 'list'>":    
      for item in response:
        output_array.append(item)
    else:
      """ 
        в случае если не заданы список возвращаемых данных (полей),
        list_keys = [] execute_3 вернёт строку. 
      """
      output_array.append(response)
      
    self.locker.release()
    if process_bar:
      self.coun_threads_complied += 1
      self.progress_bar.update(self.coun_threads_complied)


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


  @staticmethod  
  def create_arg_list(json_string):
    """
      
    """
    cfg = json.loads(json_string)
    if not vk.check_structure(cfg):
      raise BaseException("Неверная структура конфигурационных данных.")
    
    """ Создаёт список 'values' на основе 'begin_value' и 'end_value' 
        для значений секции 'in_arguments_iterable'. 
    """
    for item in cfg.get("in_arguments_iterable"):
      if not item.has_key("values") and (item.has_key("begin_value") and item.has_key("end_value")):
        item["values"] = vk.numeric_list_to_str_list( range( int(item.get("begin_value")), int(item.get("end_value"))+1 ) )
    
    """ Значения аргументов постоянные для всех запросов. """
    args_const = (cfg.get('method_name'), cfg.get('list_keys'), cfg.get('in_arguments_constant') )
    
    """ 'Матрица' изменяемых значений. """
    matrix = []
    for argument in cfg.get('in_arguments_iterable'):
      line = []
      for item in argument.get('values'):
        line.append( (argument.get('name'), item) )
      matrix.append(line)
    
    r_matrix = vk.recursive_matrix([], matrix, [])
    
    """ Собственно сам список аргументов """
    args_list = []
    for string in r_matrix:
      args = copy.deepcopy(args_const)
      for item in string:
        args[2][item[0]] = item[1]
      args_list.append(args)
    
    return args_list
    
    
  @staticmethod  
  def check_structure(structure):
    """
      Проверяет корректность структуры опписывающей набор данных для генерации
      данных args_list используемых во время вызова  multi_threading_execute()
    
      structure -- входная конфигурационная структура
    
      Возвращает:
      True - если структура корректна.
      False - если структура не корректна.
    
  """
    if structure.keys() == [u'method_name', u'in_arguments_iterable', u'in_arguments_constant', u'list_keys']:
      return True
    else:
      return False


  @staticmethod
  def numeric_list_to_str_list(in_list):
    """
      Преобразует список целочисленных хначений в список их строковых представлений.
    
    >>> vk.numeric_list_to_str_list([1, 2, 3])
    ['1', '2', '3']
    """
    out_list = []
    for item in in_list:
      out_list.append(str(item))  
    return out_list


  @staticmethod
  def recursive_matrix(head, in_matrix, out_matrix):
    """
      Создаёт список всех возможных комбинаций аргументов.
    """
    if len(in_matrix) >= 1: 
      for item in in_matrix[0]:
        """ формируем 'голову' """
        h = list(head)
        h.append( (item[0], item[1]) )
        """ делаем рекурсию """
        vk.recursive_matrix(h, in_matrix[1:], out_matrix)
    elif len(in_matrix) == 0:
      out_matrix.append(head)   
    return out_matrix



if __name__ == "__main__":

  import doctest 
  print "DocTest vk.py" 
  print "  ", doctest.testmod(), "\n"

