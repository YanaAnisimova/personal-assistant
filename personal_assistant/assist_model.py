import os
import re
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

    def replaces_name(self, record, updated_data):
        """
        Function updates name.
        :param record: (dict) a line from the contact book, the data to be changed.
        :return: (dict) updated entry
        """
        self.user_name = updated_data
        record['name'] = self.user_name
        return record


    def replaces_phone(self, record, updated_data):
        """
        Function updates phone number.
        :param record: (dict) a line from the contact book, the data to be changed.
        :return: (dict) updated entry
        """
        self.user_phone_number = updated_data
        record['phone'] = self.user_phone_number
        return record

    def replaces_email(self, record, updated_data):
        """
        Function updates email.
        :param record: (dict) a line from the contact book, the data to be changed.
        :return: (dict) updated entry
        """
        self.user_email = updated_data
        record['email'] = self.user_email
        return record

    def replaces_birthday(self, record, updated_data):
        """
        Function updates birthday.
        :param record: (dict) a line from the contact book, the data to be changed.
        :return: (dict) updated entry
        """
        self.user_birthday = updated_data
        record['birthday'] = self.user_birthday
        return record

    def note_delete(self, record, updated_data=None):
        record['note'] = '\n'
        return record

    def note_replaces(self, record, updated_data):
        self.user_note = updated_data
        record['note'] = self.user_note + '\n'
        return record

    def note_add(self, record, updated_data):
        self.user_note = updated_data
        record['note'] = record['note'].replace('\n', ' ') + self.user_note + '\n'
        return record

    EDITOR = {'name': replaces_name,
              'phone': replaces_phone,
              'email': replaces_email,
              'birthday': replaces_birthday,
              'note_delete': note_delete,
              'note_change': note_replaces,
              'note_add': note_add}

    def get_editor_handler(self, com_edit):
        """
        The function selects the function signature according to the command (com_edit).
        :param com_edit: a command entered by the user indicates what needs to be edited
        (name/phone/email/birthday/note).
        :return: function signature.
        """
        return self.EDITOR[com_edit]

    def gets_data_by_name(self, user_name):
        self.user_name = user_name

        for record in self.data:
            if record['name'].strip().casefold() == self.user_name.casefold():
                return record

    def updates_the_database(self, record, updated_record):
        """
        The function updates record.
        :return: None
        """
        self.data[self.data.index(record)] = updated_record

    def checking_presence_of_name_in_the_database(self, name):
        """
        Checking if name (self.user_name) exists in the book. any() - return True, if at least one element
        in the sequence True.
        """
        return any(record['name'].strip().casefold() == name.casefold() for record in self.data)

    def to_delete(self, user_name):
        """
        Function deletes records by specified name.
        :return: None
        """
        self.user_name = user_name

        for record in self.data:
            if record['name'].strip().casefold() == self.user_name.casefold():
                self.data.remove(record)

    def check_name(self, name):

        with open('data/data-file.txt', 'r') as file:
            users = file.readlines()
        try:
            self.user_name = name
            if not any(re.split('\| ', user)[0].strip().casefold() == self.user_name.casefold() for user in users):
                return self.user_name
            raise ValueError
        except AttributeError:
            raise AttributeError

    def check_phone_number(self, phone):
        try:
            self.user_phone_number = phone
            if self.user_phone_number == (re.search(r'\+?\d?\d?\d?\d{2}\d{7}', self.user_phone_number)).group():
                return self.user_phone_number
            raise AttributeError
        except AttributeError:
            raise AttributeError

    def check_email(self, email):
        try:
            self.user_email = email
            if self.user_email == (re.search(r'[a-zA-Z0-9]+[._]?[a-z0-9]+[@]\w+[.]\w{2,3}', self.user_email)).group():
                return self.user_email
            raise AttributeError
        except AttributeError:
            raise AttributeError

    def check_birthday(self, birthday):
        try:
            self.user_birthday = birthday
            if datetime.strptime(self.user_birthday, '%d.%m.%Y'):
                return self.user_birthday
        except ValueError:
            raise ValueError

    @staticmethod
    def combine_data(name, phone, email, birthday, note):
        return name + '| ' + phone + '| ' + email + '| ' + birthday + '| ' + note + '\n'

    def to_create_empty_file(self):
        with open('data//data-file.txt', 'a') as file:
            file.write('')

    def to_create(self, combine_data):
        with open('data//data-file.txt', 'a') as file:
            file.write(str(combine_data))

    def to_congratulate(self, n):
        # """
        # Function return list of users from user list, whose birthday is in n days from current date
        # """
        user_list = []
        user_date = datetime.now() + timedelta(days=int(n))  # Getting needed date
        search_pattern = datetime.strftime(user_date, '%d.%m')
        with open('data//data-file.txt', 'r') as file:
            users = file.readlines()  # Reading from file
            for user in users:
                if re.search(search_pattern, re.split(r'\|', user)[3].strip()):
                    user_list.append(user)
        if len(user_list) > 0:
            return user_list

    def to_search(self, key_word):
        """
        Function return list of users from user list that match some key word
        """
        user_list = []
        with open('data//data-file.txt', 'r') as file:
            users = file.readlines()  # Reading from file
            for user in users:
                if key_word.lower() in user.lower():  # Searching for matches
                    user_list.append(user)
        if len(user_list) > 0:
            return user_list

    def to_get_all(self):
        with open('data//data-file.txt', 'r') as file:
            return file.readlines()


