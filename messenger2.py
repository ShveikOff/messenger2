from time import time
from datetime import datetime
from collections import defaultdict
import uuid

class messenger: #Основной класс
    
    def __init__(self):
        
        self.chats_dict = defaultdict(object) # словарь который хранит все чаты мессенджера
        self.users_dict = defaultdict(object) # словарь который хранит всех пользователей
        self.users_dict_by_name = defaultdict(uuid.uuid5)
    
    def sign_up_request(self):
        new_user = str(input('Введите имя нового пользователя: \n'))
        new_user_password = str(input('Введите пароль: \n'))
        new_user_id = uuid.uuid5(uuid.NAMESPACE_DNS, new_user)
        temp_object = self.users()
        temp_object.set_id(new_user_id)
        temp_object.set_name(new_user)
        temp_object.set_password(new_user_password)
        if (new_user_id in self.users_dict) or (new_user in self.users_dict_by_name):
            print ('Пользователь с таким именем уже есть в системе: ')
        else:
            self.users_dict[new_user_id] = temp_object
            self.users_dict_by_name[new_user] = new_user_id
    
    def sign_in_request(self):
        user_name = str((input('Введите имя пользователя: \n')))
        password = str(input('Введите пароль: \n'))
        if user_name in self.users_dict_by_name:
            user_id = self.users_dict_by_name[user_name]
            if self.users_dict[user_id].password_chek(password):
                return (True, user_id)
            else:
                print ('Неверный пароль')
                return (False, 0)
        else:
            print ('Пользователя с таким именем не существует')
            return (False, 0)

    #запрос сообщения при мануальном указании отправителя и получателя
    
    '''
    def message_request(self): #обращение к мессенджеру для отправки сообщения,
        #где он либо использует уже существующий чат, либо дает команду на создание нового
        
        sender_id = int(input('Введите id пользователя от которого будет отправленно сообщение: \n'))
        receiver_id = int(input('Введите id пользователя которому будет отправленно сообщение: \n'))
        message_text = str(input('Введите текст сообщения: \n'))
        temp_object = self.chats() #Создает временный обьект класса chats
        temp_object_id = temp_object.set_id(sender_id, receiver_id) #рассчитывает уникальный id исходя из id собеседников
        if temp_object_id in self.chats_dict: #проверяет есть ли уже такой чат в словаре мессенджера
            self.chats_dict[temp_object_id].message(sender_id, receiver_id, message_text) #отправляется сообщение в данный чат
            self.chats_dict[temp_object_id].show() #отображаются все сообщения в чате
        else:
            self.chats_dict[temp_object_id] = temp_object #добавляет отсутствующий чат в словарь, задает параметры и совершает операции выше
            self.chats_dict[temp_object_id].set_chat_users(sender_id, receiver_id)
            self.chats_dict[temp_object_id].message(sender_id, receiver_id, message_text)
            self.chats_dict[temp_object_id].show()
    '''

    #запрос сообщения от авторизованного пользователя
    def message_request(self, sender_id): #обращение к мессенджеру для отправки сообщения,
        
        #Тут нужно выводить список контактов с id-ми

        receiver = str(input('Введите имя пользователя которому будет отправленно сообщение: \n'))#где он либо использует уже существующий чат, либо дает команду на создание нового
        
        if receiver in self.users_dict_by_name:
            receiver_id = self.users_dict_by_name[receiver]
        else:
            print ("Пользователя с таким именем не существует")

        message_text = str(input('Введите текст сообщения: \n'))
        temp_object = self.chats() #Создает временный обьект класса chats
        temp_object_id = temp_object.set_id(sender_id, receiver_id) #рассчитывает уникальный id исходя из id собеседников
        if temp_object_id in self.chats_dict: #проверяет есть ли уже такой чат в словаре мессенджера
            self.chats_dict[temp_object_id].message(sender_id, receiver_id, message_text) #отправляется сообщение в данный чат
            self.chats_dict[temp_object_id].show() #отображаются все сообщения в чате
        else:
            self.chats_dict[temp_object_id] = temp_object #добавляет отсутствующий чат в словарь, задает параметры и совершает операции выше
            self.chats_dict[temp_object_id].set_chat_users(sender_id, receiver_id)
            sender = self.users_dict[sender_id].get_username()
            self.chats_dict[temp_object_id].message(sender, receiver, message_text)
            self.chats_dict[temp_object_id].show()    

    class users:
        def __init__(self):
            self.id = None
            self.name = None
            self.chats = defaultdict(int)
            self.contacts = defaultdict(str)
            self.password = None
        
        def set_id(self, free_id):
            self.id = free_id

        def set_password(self, password):
            self.password = password
        
        def set_name(self, name):
            self.name = name

        def get_username(self):
            return self.name
        
        def password_chek(self, password):
            if self.password == password:
                return True
            return False
        
        def add_contact(self, user_id, username):
            self.contacts[user_id] = username

        def add_chat(self, chat_id):
            contrcompanion_name = messenger.users_dict[[messenger.chats_dict[chat_id].contrcompanion]]
            companion_name = messenger.users_ditc[[messenger.chats_dict[chat_id].companion]]
            if messenger.chats_dict[chat_id].companion == self.id:
                self.chats[chat_id] = contrcompanion_name
            else:
                self.chats[chat_id] = companion_name

        def show_chats(self):
            for chat_names in self.chats.values():
                print (chat_names)

        def show_contacts(self):
            for id, contact in self.contacts.items():
                print (id, contact)   
                    
    class messages: #Подкласс сообщений
        def __init__(self):
            self.sender = None
            self.receiver = None
            self.text = None
            self.message_time = datetime.now()
        
        def set_message(self, sender, receiver, text):
            self.sender = sender
            self.receiver = receiver
            self.text = text
            
        def show (self):
            print (f'[{self.message_time}] | [{self.sender}] отправил [{self.receiver}] : {self.text}')
            
    class chats: #Подкласс чатов
        def __init__(self):
            self.id = None
            self.companion = None
            self.contrcompanion = None
            self.chat_members = (self.companion, self.contrcompanion)
            self.messages_dict = defaultdict(object) 
            
        def set_chat_users(self, sender_id, receiver_id):
            self.companion = sender_id
            self.contrcompanion = receiver_id
            
        def set_id(self, sender_id, receiver_id): #Для создания уникального ID по данным собеседников
            if sender_id > receiver_id:
                unique_id = uuid.uuid5(uuid.NAMESPACE_DNS, str(sender_id) + str(receiver_id))
            else:
                unique_id = uuid.uuid5(uuid.NAMESPACE_DNS, str(receiver_id) + str(sender_id))
            self.id = unique_id
            return unique_id            
        
        def message(self, sender, receiver, text):
            temp_time = time()
            self.messages_dict[temp_time] = messenger.messages()
            self.messages_dict[temp_time].set_message(sender, receiver, text)
        
        def show(self):
            sorted_messages = sorted(self.messages_dict.keys())
            for key in sorted_messages:
                self.messages_dict[key].show()

my_messenger = messenger()
command_dict = {'sign_in':0, 'sign_up':0, 'message':0, 'exit':0}

def session (user_id):
    run = True
    while run:
        try:
            command = input('Введите комманду: \n')
            if command == 'message':
                my_messenger.message_request(user_id)
            elif command == 'exit':
                run = False
            elif command not in command_dict:
                print ('wrong command \n')
        except ZeroDivisionError:
            print("Ошибка: деление на 0!")

def autentification ():
    run = True
    while run:
        try:
            command = input('Введите комманду: \n')
            if command == 'sign_in':
                result = my_messenger.sign_in_request()
                sign_in_result = result[0]
                user_id = result[1]
                if sign_in_result:
                    session(user_id)
            elif command == 'sign_up':
                my_messenger.sign_up_request()
            elif command == 'exit':
                run = False
            elif command not in command_dict:
                print ('wrong command \n')
        except ZeroDivisionError:
            print('Ошибка: деление на 0!')
                    
autentification()

