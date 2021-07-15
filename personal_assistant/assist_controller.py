from assist_model import is_file_empty_decorator, Personal_asisstant
from assist_view import ConsoleView
import os
import sys


class ConsoleController:
    def __init__(self, view, model):
        self.view = view
        self.model = model

    def add_note(self):
        self.view.requests_enter_the_note()
        return input()

    def input_birthday(self):
        while True:
            self.view.requests_enter_birthday()
            try:
                birthday = self.model.check_birthday(input())
                break
            except ValueError:
                self.view.requests_re_entry_of_the_data()

        return birthday

    def input_email(self):
        while True:
            self.view.requests_enter_email()
            try:
                email = self.model.check_email(input().strip())
                break
            except AttributeError:
                self.view.requests_re_entry_of_the_data()

        return email

    def input_name(self):
        while True:
            self.view.requests_enter_name()
            try:
                name = self.model.check_name(input())
                break
            except AttributeError:
                self.view.requests_re_entry_of_the_data()
            except ValueError:
                self.view.reports_the_existence_of_name_in_database()
        return name

    def input_phone_number(self):
        while True:
            self.view.requests_enter_phone()
            try:
                phone = self.model.check_phone_number(input())
                break
            except AttributeError:
                self.view.requests_re_entry_of_the_data()

        return phone

    def combine_data(self):
        self.model.to_create_empty_file()
        name = self.input_name()
        phone = self.input_phone_number()
        email = self.input_email()
        birthday = self.input_birthday()
        note = self.add_note()
        combine_data = self.model.combine_data(name, phone, email, birthday, note)
        self.model.to_create(combine_data)

    def describes_commands(self):
        self.view.describes_commands()

    def ends_the_program(self):
        self.view.displays_see_ya()
        sys.exit(0)

    def gets_the_name_to_make_changes_to_the_data(self):
        while True:
            self.view.requests_enter_name_to_changes_data()
            user_name = input().strip()
            # checking if name (self.user_name) exists in the book.
            if not self.model.checking_presence_of_name_in_the_database(user_name):
                self.view.reports_the_not_exist_of_name_in_database(user_name)
                continue
            break
        return user_name

    def start(self):
        self.view.start_view()

    def get_updated_name(self, command):
        updated_data = self.input_name().strip()
        return updated_data, command

    def get_updated_phone(self, command):
        updated_data = self.input_phone_number().strip()
        return updated_data, command

    def get_updated_email(self, command):
        updated_data = self.input_email().strip()
        return updated_data, command

    def get_updated_birthday(self, command):
        updated_data = self.input_birthday().strip()
        return updated_data, command

    def get_updated_note(self, command):
        """
        The function replaces or adds data to an existing note.
        :return: (dict) updated entry
        """
        while True:
            self.view.requests_command_edit_note()
            com_edit_note = input().strip().casefold()
            if com_edit_note not in ('change', 'add', 'delete'):
                print(f'Incorrect, once more please')
            else:
                break
        if com_edit_note == 'delete':
            com_edit_note = command + '_delete'
            updated_data = None
            return updated_data, com_edit_note

        updated_data = self.add_note().strip()
        if com_edit_note == 'change':
            com_edit_note = command + '_change'
        elif com_edit_note == 'add':
            com_edit_note = command + '_add'
        return updated_data, com_edit_note

    def get_updated_data(self, command_edit):
        UPDATE_DATA = {'name': self.get_updated_name,
                       'phone': self.get_updated_phone,
                       'email': self.get_updated_email,
                       'birthday': self.get_updated_birthday,
                       'note': self.get_updated_note}
        return UPDATE_DATA[command_edit](command_edit)

    @is_file_empty_decorator
    def to_get_all(self):
        users = self.model.to_get_all()
        self.view.displays_users(users)


    @is_file_empty_decorator
    def organize_to_delete(self):
        """
        Function deletes records by specified name.
        :return: None
        """
        self.model.deserialization_data()
        user_name = self.gets_the_name_to_make_changes_to_the_data()
        self.model.to_delete(user_name)
        self.model.serialization_data()
        self.view.reports_the_deletion_of_a_contact(user_name)

    @is_file_empty_decorator
    def organizes_to_congratulate(self):
        # Validating input data
        while True:
            try:
                self.view.requests_days_left_to_the_birthday()
                n = input()
                if n.isdigit:
                    break
            except ValueError:
                self.view.requests_input_number()
        user_list = self.model.to_congratulate(n)
        if user_list:
            self.view.displays_request_to_wis_happy_birthday(user_list)
        else:
            self.view.reports_no_birthdays()

    @is_file_empty_decorator
    def organize_to_edit(self):
        """
        The function edits data (name, phone, ...) by the name of the contact. Name, phone, email, birthday, note
        can only be replaced, and notes can be replaced and supplemented.
        :return: None
        """
        self.model.deserialization_data()
        user_name = self.gets_the_name_to_make_changes_to_the_data()
        record = self.model.gets_data_by_name(user_name)

        while True:
            self.view.reports_what_edit()
            command_edit = input().casefold().strip()

            try:
                # by command_edit, the corresponding function is selected, to which 1 record is transferred.
                # An updated record is returned.
                updated_data, updated_command = self.get_updated_data(command_edit)
                updated_record = self.model.get_editor_handler(updated_command)(self, record, updated_data)
                break
            except KeyError:
                self.view.requests_re_entry_of_the_data()
        self.model.updates_the_database(record, updated_record)
        self.model.serialization_data()
        self.view.reports_the_updated_of_a_contact(user_name)

    @is_file_empty_decorator
    def organizes_the_search(self):
        self.view.requests_key_word_for_search()
        key_word = input()
        user_list = self.model.to_search(key_word)
        if user_list:
            self.view.displays_matches(key_word, user_list)
        else:
            self.view.reports_no_matches()

    def get_command_handler(self, command):
        return self.COMMANDS[command]

    def requests(self):
        self.view.requests_command()
        command = input().strip().casefold()
        try:
            self.get_command_handler(command)(self)
        except KeyError:
            self.view.displays_key_error(command)

    COMMANDS = {
        'create': combine_data,
        'search': organizes_the_search,
        'delete': organize_to_delete,
        'edit': organize_to_edit,
        'show': to_get_all,
        'birthday': organizes_to_congratulate,
        'help': describes_commands,
        'exit': ends_the_program,
    }


if __name__ == '__main__':
    view = ConsoleView()
    model = Personal_asisstant()
    controller = ConsoleController(view, model)

    controller.start()

    while True:
        try:
            os.mkdir('data')
        except FileExistsError:
            pass
        controller.requests()