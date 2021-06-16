import os
import re
import sys
from datetime import timedelta, datetime



class Personal_asisstant: 

    def __init__(self):
        self.user_name = ''
        self.user_phone_number = ''
        self.user_email = ''
        self.user_birthday = ''
        self.user_note = ''
        print('Salut!')


    def requests(self):

        command = input('Enter your request: ')

        if command == 'create':
            consumer.to_create()
        elif command == 'search':
            consumer.to_search() 
        elif command == 'delete':
            consumer.to_delete()
        elif command == 'edit':
            consumer.to_edit()
        elif command == 'show':
            consumer.to_show()
        elif command == 'birthday':
            consumer.to_congratulate()
        elif command == 'exit':
            consumer.exit()       


    def name_input(self):
        self.user_name = input('Enter your name: ')
        return self.user_name


    def phone_number_input(self):

        while True:
            try:
                self.user_phone_number = input('Enter your phone number: ')
                if self.user_phone_number == (re.search(r'\+?\d?\d?\d?\d{2}\d{7}', self.user_phone_number)).group():
                    break
            except AttributeError:
                print('Incorrect, once more please')
        return self.user_phone_number

                
    def email_input(self):

        while True:
            try:
                self.user_email = input('Enter your email: ')
                if self.user_email == (re.search(r'[a-zA-Z0-9]+[._]?[a-z0-9]+[@]\w+[.]\w{2,3}', self.user_email)).group():
                    break
            except AttributeError:
                print('Incorrect, once more please')
        return self.user_email


    def birthday_input(self):
        self.user_birthday = input('Enter your B-Day (DD.MM.YYYY): ')
        return self.user_birthday


    def add_note(self):
        self.user_note = input('Enter the note: ')
        return self.user_note


    def combine_data(self):
        combine_data = consumer.name_input() + '| ' + consumer.phone_number_input() + '| ' +  consumer.email_input() + '| '\
                +  consumer.birthday_input() + '| ' + consumer.add_note() + '\n'
        return combine_data
    

    def to_create(self):

        with open('data//data-file.txt', 'a') as file:
            file.write(str(consumer.combine_data()))
            

    def is_file_empty(self):
        def inner(path):
            try:
                if os.path.isfile('data//data-file.txt') and os.path.getsize('data//data-file.txt') > 0:
                    return self('data//data-file.txt')
            except:
                print('Firstly, add some information')
            else:
                print('Firstly, add some information')

        return inner
        
    def exit(self):
        print("See ya!")
        sys.exit(0)  

    @is_file_empty
    def to_congratulate(self):
        while True:
            try:
                n = input('Please enter days left to the needed date: ')
                if n.isdigit:
                    break
            except ValueError:
                print('Please enter a valid number!')
        user_list = []
        user_date = datetime.now() + timedelta(days = int(n))
        search_pattern = datetime.strftime(user_date, '%d.%m')
        with open('data//data-file.txt', 'r') as file:
            users = file.readlines()
            for user in users:
                if re.search(search_pattern, re.split(r'\|',user)[3].strip()):
                    user_data = ', '.join(re.split(r'\|', user))
                    user_list.append(user_data) 
        if len(user_list)>0:
            result = ''.join(user_list)       
            print(f'Please do not forget to tell them happy birthday!\n{result}')
        else:
            print('No congrats on this day!')

    @is_file_empty
    def to_search(self):
        key_word = input('Please, enter the key word: ')
        user_list = []
        with open('data//data-file.txt', 'r') as file:
            users = file.readlines()
            for user in users:
                if key_word.lower() in user.lower():
                    user_data = ', '.join(re.split(r'\|', user))
                    user_list.append(user_data)
        if len(user_list)>0:
            result = ''.join(user_list)
            print(f'Found some users with matching key word "{key_word}":\n{result}')
        else:
            print('No matches!')

    @is_file_empty
    def to_show(self):
        with open('data//data-file.txt', 'r') as file:
            users = file.readlines() 
            print('-'*119)   
            header = "| {:^5} | {:^15} | {:^15} | {:^25} | {:^15} | {:^25} |".format('#', 'name', 'phone', 'e-mail', 'birthday', 'note') 
            print(header)
            print('-'*119)      
            for user in enumerate(users):
                count = user[0]
                name = re.split(r'\|',user[1])[0].strip()
                phone = re.split(r'\|',user[1])[1].strip()
                e_mail = re.split(r'\|',user[1])[2].strip()
                birthday = re.split(r'\|',user[1])[3].strip()
                note = re.split(r'\|',user[1])[4].strip()
                user_data = "| {:^5} | {:<15} | {:<15} | {:25} | {:<15} | {:<25} |".format(count, name, phone, e_mail, birthday, note) 
                print(user_data)
            print('-'*119)



consumer = Personal_asisstant()


def main():
    
    while True:
        try:
            os.mkdir('data')
        except FileExistsError:
            pass
        consumer.requests()

    
if __name__ == '__main__':
    main()