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


class Serialization:
    @staticmethod
    def deserialization_data():
        """
        The function reads the contact book data from the file and writes to program as:
        self.data = [{'name': name, 'phone': phone, 'email': email, 'birthday': birthday, 'note': note}, ...]
        :return: None
        """
        with open('data//data-file.txt', 'r') as file:
            database = []
            keys = ['name', 'phone', 'email', 'birthday', 'note']
            for row in file:
                record = {}
                row = row.split('| ')
                # vocabulary formation {keys[0]: row[0], keys[1]: row[1], ...}
                for key, value in zip(keys, row):
                    record[key] = value
                database.append(record)
        return database

    @staticmethod
    def serialization_data(database):
        """
        The function transfers the contact book data from the program to a file.
        :return: None
        """
        with open('data//data-file.txt', 'w') as file:
            for record in database:
                file.write('| '.join(record.values()))


class RecordEditor:
    def replaces_name(self, record, updated_data):
        """
        Function updates name.
        :param record: (dict) a line from the contact book, the data to be changed.
        :return: (dict) updated entry
        """
        record['name'] = updated_data
        return record

    def replaces_phone(self, record, updated_data):
        """
        Function updates phone number.
        :param record: (dict) a line from the contact book, the data to be changed.
        :return: (dict) updated entry
        """
        record['phone'] = updated_data
        return record

    def replaces_email(self, record, updated_data):
        """
        Function updates email.
        :param record: (dict) a line from the contact book, the data to be changed.
        :return: (dict) updated entry
        """
        record['email'] = updated_data
        return record

    def replaces_birthday(self, record, updated_data):
        """
        Function updates birthday.
        :param record: (dict) a line from the contact book, the data to be changed.
        :return: (dict) updated entry
        """
        record['birthday'] = updated_data
        return record

    def note_delete(self, record, updated_data=None):
        record['note'] = '\n'
        return record

    def note_replaces(self, record, updated_data):
        record['note'] = updated_data + '\n'
        return record

    def note_add(self, record, updated_data):
        record['note'] = record['note'].replace('\n', ' ') + updated_data + '\n'
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

    def checking_presence_of_name_in_the_database(self, name, database):
        """
        Checking if name (self.user_name) exists in the book. any() - return True, if at least one element
        in the sequence True.
        """
        return any(record['name'].strip().casefold() == name.casefold() for record in database)

    def gets_data_by_name(self, user_name, database):
        for record in database:
            if record['name'].strip().casefold() == user_name.casefold():
                return record

    def updates_the_database(self, record, updated_record, database):
        """
        The function updates record.
        :return: None
        """
        database[database.index(record)] = updated_record
        return database


class ValidationCheck:
    @staticmethod
    def check_birthday(user_birthday):
        try:
            if datetime.strptime(user_birthday, '%d.%m.%Y'):
                return user_birthday
        except ValueError:
            raise ValueError

    @staticmethod
    def check_email(user_email):
        try:
            if user_email == (re.search(r'[a-zA-Z0-9]+[._]?[a-z0-9]+[@]\w+[.]\w{2,3}', user_email)).group():
                return user_email
            raise AttributeError
        except AttributeError:
            raise AttributeError

    @staticmethod
    def check_name(user_name):

        with open('data/data-file.txt', 'r') as file:
            users = file.readlines()
        try:
            if not any(re.split('\| ', user)[0].strip().casefold() == user_name.casefold() for user in users):
                return user_name
            raise ValueError
        except AttributeError:
            raise AttributeError

    @staticmethod
    def check_phone_number(user_phone_number):
        try:
            if user_phone_number == (re.search(r'\+?\d?\d?\d?\d{2}\d{7}', user_phone_number)).group():
                return user_phone_number
            raise AttributeError
        except AttributeError:
            raise AttributeError


class EmptyFile:
    @staticmethod
    def to_create_empty_file():
        with open('data//data-file.txt', 'a') as file:
            file.write('')


class RecordCreator:
    @staticmethod
    def combine_data(name, phone, email, birthday, note):
        return name + '| ' + phone + '| ' + email + '| ' + birthday + '| ' + note + '\n'

    def to_create_record(self, combine_data):
        with open('data//data-file.txt', 'a') as file:
            file.write(str(combine_data))


class RecordForDeletion:
    def to_delete(self, user_name, database):
        """
        Function deletes records by specified name.
        :return: None
        """
        for record in database:
            if record['name'].strip().casefold() == user_name.casefold():
                database.remove(record)
        return database


class BirthdayPeople:
    def to_congratulate(self, n):
        """
        Function return list of users from user list, whose birthday is in n days from current date
        """
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


class RecordSearcher:
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


class DatabaseContent:
    def to_get_all(self):
        with open('data//data-file.txt', 'r') as file:
            return file.readlines()


