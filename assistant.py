import os
import re
import sys


class Personal_asisstant: 

    def __init__(self):
        self.user_name = ''
        self.user_phone_number = ''
        self.user_email = ''
        self.user_birthday = ''
        self.user_note = ''
        self.data = []
        print('Salut!')

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
        elif command == 'exit':
            consumer.exit()

    def is_file_empty(self, func):
        def inner(path):
            try:
                if os.path.isfile('data//data-file.txt') and os.path.getsize('data//data-file.txt') > 0:
                    return self('data//data-file.txt')
            except:
                print('Firstly, add some information')
            else:
                print('Firstly, add some information')

        return inner

    def to_edit_name(self, record):
        """
        Function updates name.
        :param record: a line from the contact book, the data to be changed.
        :return: (dict) updated entry
        """
        self.user_name = self.name_input().strip()
        record['name'] = self.user_name
        return record

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
        com_edit_note = input('Сhange or add notes?:  ').strip().casefold()
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

    def decerialization_data(self):
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

    def cerialization_data(self):
        """
        The function transfers the contact book data from the program to a file.
        :return: None
        """
        with open('data//data-file.txt', 'w') as file:
            for record in self.data:
                file.write('| '.join(record.values()))

    @is_file_empty
    def to_edit(self):
        """
        The function edits data (name, phone, ...) by the name of the contact. Name, phone, email, birthday, note
        can only be replaced, and notes can be replaced and supplemented.
        :return: None
        """
        self.decerialization_data()
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
        self.cerialization_data()

    @is_file_empty
    def to_delete(self):
        """
        Function deletes records by specified name.
        :return: None
        """
        self.decerialization_data()
        self.user_name = input('Enter a name to delete data: ').strip()

        # checking if name (self.user_name) exists in the book.
        if not any(record['name'].strip().casefold() == self.user_name.casefold() for record in self.data):
            print(f'Name "{self.user_name}" does not exist in the contact book.')

        for record in self.data:
            if record['name'].strip().casefold() == self.user_name.casefold():
                self.data.remove(record)
                print(f'The contact named "{record["name"]}" has been deleted.')
        self.cerialization_data()


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

        
    def exit(self):
        print("See ya!")
        sys.exit(0)  



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