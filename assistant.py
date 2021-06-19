import os
import re
import sys
from datetime import timedelta, datetime


def is_file_empty_decorator(function):
    def inner(*args):
        if os.path.isfile('data//data-file.txt') and os.path.getsize('data//data-file.txt') > 0:
            return function(*args)
        else:
            print('Firstly, add some information')

    return inner


class Personal_asisstant: 

    def __init__(self):
        self.user_name = ''
        self.user_phone_number = ''
        self.user_email = ''
        self.user_birthday = ''
        self.user_note = ''
        self.data = []
        print('Salut! Enter \'help\' to see the commands')

    def requests(self):

        command = input('Enter your request: ').strip().casefold()

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
        elif command == 'help':
            consumer.help()
        elif command == 'exit':
            consumer.exit()
        else:
            print('Please try again')

    def to_edit_name(self, record):
        """
        Function updates name.
        :param record: a line from the contact book, the data to be changed.
        :return: (dict) updated entry
        """
        self.user_name = self.name_input().strip()
        record['name'] = self.user_name
        return record

    def help(self):
        print('Hi, I\'m\' a bot. And I can:')
        print('<create>   /save contacts with names, addresses, phone numbers, emails and birthdays to the contact book;')
        print('<birthday> /display a list of contacts who have a birthday after a specified number of days from the current date;')
        print('<search>   /search for contacts and notes from the contact book;')
        print('<edit>     /edit entries from the contact book, edit and delete notes;')
        print('<delete>   /delete entries from the contact book;')
        print('<show>     /display all contents of the contact book;') 
        print('<exit>     /exit the program')  


    def to_edit_phone(self, record):
        """
        Function updates phone number.
        :param record: a line from the contact book, the data to be changed.
        :return: (dict) updated entry
        """
        self.user_phone_number = self.phone_number_input().strip()
        record['phone'] = self.user_phone_number
        return record

    def to_edit_email(self, record):
        """
        Function updates email.
        :param record: (dict) a line from the contact book, the data to be changed.
        :return: (dict) updated entry
        """
        self.user_email = self.email_input().strip()
        record['email'] = self.user_email
        return record

    def to_edit_birthday(self, record):
        """
        Function updates birthday.
        :param record: (dict) a line from the contact book, the data to be changed.
        :return: (dict) updated entry
        """
        self.user_birthday = self.birthday_input().strip()
        record['birthday'] = self.user_birthday
        return record

    def to_edit_note(self, record):
        """
        The function replaces or adds data to an existing note.
        :param record: (dict) a line from the contact book, the data to be changed.
        :return: (dict) updated entry
        """
        while True:
            com_edit_note = input('Change, add or delete notes?:  ').strip().casefold()
            if com_edit_note not in ('change', 'add', 'delete'):
                print(f'Incorrect, once more please')
            else:
                break
        if com_edit_note == 'delete':
            record['note'] = '\n'
            return record
        self.user_note = self.add_note().strip()
        if com_edit_note == 'change':
            record['note'] = self.user_note + '\n'
            return record
        elif com_edit_note == 'add':
            record['note'] = record['note'].replace('\n', '') + self.user_note + '\n'
            return record
        else:
            print(f'Incorrect, once more please')

    EDITOR = {'name': to_edit_name,
              'phone': to_edit_phone,
              'email': to_edit_email,
              'birthday': to_edit_birthday,
              'note': to_edit_note}

    def get_editor_handler(self, com_edit):
        """
        The function selects the function signature according to the command (com_edit).
        :param com_edit: a command entered by the user indicates what needs to be edited
        (name/phone/email/birthday/note).
        :return: function signature.
        """
        return self.EDITOR[com_edit]

    def deserialization_data(self):
        """
        The function reads the contact book data from the file and writes to program as:
        self.data = [{'name': name, 'phone': phone, 'email': email, 'birthday': birthday, 'note': note}, ...]
        :return: None
        """
        with open('data//data-file.txt', 'r') as file:
            self.data = []
            keys = ['name', 'phone', 'email', 'birthday', 'note']
            for row in file:
                record = {}
                row = row.split('| ')
                # vocabulary formation {keys[0]: row[0], keys[1]: row[1], ...}
                for key, value in zip(keys, row):
                    record[key] = value
                self.data.append(record)

    def serialization_data(self):
        """
        The function transfers the contact book data from the program to a file.
        :return: None
        """
        with open('data//data-file.txt', 'w') as file:
            for record in self.data:
                file.write('| '.join(record.values()))

    @is_file_empty_decorator
    def to_edit(self):
        """
        The function edits data (name, phone, ...) by the name of the contact. Name, phone, email, birthday, note
        can only be replaced, and notes can be replaced and supplemented.
        :return: None
        """
        self.deserialization_data()
        self.user_name = input('Enter a name to edit data:  ').strip()

        # checking if name (self.user_name) exists in the book.
        if not any(record['name'].strip().casefold() == self.user_name.casefold() for record in self.data):
            print(f'Name "{self.user_name}" does not exist in the contact book.')
        for record in self.data:
            if record['name'].strip().casefold() == self.user_name.casefold():
                command_edit = input('What edit? (name/phone/email/birthday/note):  ').strip()
                try:
                    # by command_edit, the corresponding function is selected, to which 1 record is transferred.
                    # An updated record is returned.
                    updated_record = self.get_editor_handler(command_edit)(self, record)
                    self.data[self.data.index(record)] = updated_record
                    print(f'Updated contact details with name "{record["name"]}".')
                except KeyError:
                    print(f'Incorrect, once more please')
        self.serialization_data()

    @is_file_empty_decorator
    def to_delete(self):
        """
        Function deletes records by specified name.
        :return: None
        """
        self.deserialization_data()
        self.user_name = input('Enter a name to delete data: ').strip()

        # checking if name (self.user_name) exists in the book. any() - return True, if at least one element
        # in the sequence True.
        if not any(record['name'].strip().casefold() == self.user_name.casefold() for record in self.data):
            print(f'Name "{self.user_name}" does not exist in the contact book.')

        for record in self.data:
            if record['name'].strip().casefold() == self.user_name.casefold():
                self.data.remove(record)
                print(f'The contact named "{record["name"]}" has been deleted.')
        self.serialization_data()


    def name_input(self):
        self.deserialization_data()
        while True:
            try:
                self.user_name = input('Enter your name: ')       
                if not any(record['name'].strip() == self.user_name for record in self.data):
                    return self.user_name
                else:
                    print('This name already exists in contact book!')
            except AttributeError:
                print('Please try again!')        
                

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

        while True:
            try:
                self.user_birthday = input('Enter your B-Day (DD.MM.YYYY): ')
                if datetime.strptime(self.user_birthday, '%d.%m.%Y'):
                    break
            except ValueError:
                print("Incorrect date, try again!")
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

        
    def exit(self):
        print("See ya!")
        sys.exit(0)  

    def print_users(self, users):
        """
        Function prints from user list
        :param user: a list with lines from data-file.txt
        :return: prints formatted table with user information from list
        """
        print('-'*119)   
        header = "| {:^5} | {:^15} | {:^15} | {:^25} | {:^15} | {:^25} |".format('#', 'name', 'phone', 'e-mail', 'birthday', 'note') 
        print(header)
        print('-'*119)  
        #Getting user data from line    
        for user in enumerate(users):
            count = user[0]+1
            name = re.split(r'\|',user[1])[0].strip()
            phone = re.split(r'\|',user[1])[1].strip()
            e_mail = re.split(r'\|',user[1])[2].strip()
            birthday = re.split(r'\|',user[1])[3].strip()
            note = re.split(r'\|',user[1])[4].strip()
            user_data = "| {:^5} | {:<15} | {:<15} | {:25} | {:<15} | {:<25} |".format(count, name, phone, e_mail, birthday, note) 
            print(user_data)
        print('-'*119)

    @is_file_empty_decorator
    def to_congratulate(self):
        """
        Function prints list of users from user list, whose birthday is in n days from current date
        """
        #Validating input data
        while True:
            try:
                n = input('Please enter days left to the needed date: ')
                if n.isdigit:
                    break
            except ValueError:
                print('Please enter a valid number!')
        user_list = []
        user_date = datetime.now() + timedelta(days = int(n)) #Getting needed date
        search_pattern = datetime.strftime(user_date, '%d.%m')
        with open('data//data-file.txt', 'r') as file:
            users = file.readlines() #Reading from file
            for user in users:
                if re.search(search_pattern, re.split(r'\|',user)[3].strip()):
                    user_list.append(user) 
        if len(user_list)>0:
            print(f'Please do not forget to tell them happy birthday!\n')
            self.print_users(user_list)
        else:
            print('No congrats on this day!')

    @is_file_empty_decorator
    def to_search(self):
        """
        Function prints list of users from user list that match some key word
        """
        key_word = input('Please, enter the key word: ')
        user_list = []
        with open('data//data-file.txt', 'r') as file:
            users = file.readlines() #Reading from file
            for user in users:
                if key_word.lower() in user.lower(): #Searching for matches
                    user_list.append(user)
        if len(user_list)>0:
            print(f'Found some users with matching key word "{key_word}":\n')
            self.print_users(user_list)
        else:
            print('No matches!')

    @is_file_empty_decorator
    def to_show(self):
        with open('data//data-file.txt', 'r') as file:
            users = file.readlines() 
            self.print_users(users)



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