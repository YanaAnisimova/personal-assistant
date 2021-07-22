from assist_model import *
from assist_view import *
import os
import sys


class ConsoleController:
    def __init__(self, command_birthday, command_create, command_delete, command_help, command_edit, command_exit,
                 command_search, command_show, view):
        self.command_birthday = command_birthday
        self.command_create = command_create
        self.command_delete = command_delete
        self.command_help = command_help
        self.command_edit = command_edit
        self.command_exit = command_exit
        self.command_search = command_search
        self.command_show = command_show
        self.view = view

    def start(self):
        self.view.start_view()

    def requests(self):
        self.view.requests_command()
        command = input().strip().casefold()
        try:
            self.get_command_handler(command)(self)
        except KeyError:
            self.view.displays_key_error(command)

    def get_command_handler(self, command):
        return self.COMMANDS[command]

    def organizes_the_congratulate(self):
        self.command_birthday.organizes_the_congratulate()

    def organizes_the_create(self):
        self.command_create.organizes_the_create()

    def organizes_the_delete(self):
        self.command_delete.organizes_the_delete()

    def organizes_the_help(self):
        self.command_help.organizes_the_help()

    def organizes_the_edit(self):
        self.command_edit.organizes_the_edit()

    def organizes_the_exit(self):
        self.command_exit.organizes_the_exit()

    def organizes_the_search(self):
        self.command_search.organizes_the_search()

    def organizes_the_show(self):
        self.command_show.organizes_the_show()

    COMMANDS = {
        'birthday': organizes_the_congratulate,
        'create': organizes_the_create,
        'delete': organizes_the_delete,
        'help': organizes_the_help,
        'edit': organizes_the_edit,
        'exit': organizes_the_exit,
        'search': organizes_the_search,
        'show': organizes_the_show,
    }


class CommandBirthday:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    @is_file_empty_decorator
    def organizes_the_congratulate(self):
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
            self.view.display_who_to_wish_happy_birthday(user_list)
        else:
            self.view.reports_no_birthdays()


class CommandCreate:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def organizes_the_create(self):
        EmptyFile.to_create_empty_file()
        name = self.input_name()
        phone = self.input_phone_number()
        email = self.input_email()
        birthday = self.input_birthday()
        note = self.add_note()
        combine_data = self.model.combine_data(name, phone, email, birthday, note)
        self.model.to_create_record(combine_data)

    def add_note(self):
        self.view.requests_enter_the_note()
        return input()

    def input_birthday(self):
        while True:
            self.view.requests_enter_birthday()
            try:
                birthday = ValidationCheck.check_birthday(input())
                break
            except ValueError:
                self.view.requests_re_entry_of_the_data()
        return birthday

    def input_email(self):
        while True:
            self.view.requests_enter_email()
            try:
                email = ValidationCheck.check_email(input().strip())
                break
            except AttributeError:
                self.view.requests_re_entry_of_the_data()
        return email

    def input_name(self):
        while True:
            self.view.requests_enter_name()
            try:
                name = ValidationCheck.check_name(input())
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
                phone = ValidationCheck.check_phone_number(input())
                break
            except AttributeError:
                self.view.requests_re_entry_of_the_data()
        return phone


class CommandDelete:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    @is_file_empty_decorator
    def organizes_the_delete(self):
        """
        Function deletes records by specified name.
        :return: None
        """
        database = Serialization.deserialization_data()
        user_name = CommandEdit.gets_the_name_to_make_changes_to_the_data(self, database)
        updated_database = self.model.to_delete(user_name, database)
        Serialization.serialization_data(updated_database)
        self.view.reports_the_deletion_of_a_contact(user_name)


class CommandHelp:
    def __init__(self, view):
        self.view = view

    def organizes_the_help(self):
        self.view.describes_commands()


class CommandEdit:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    @is_file_empty_decorator
    def organizes_the_edit(self):
        """
        The function edits data (name, phone, ...) by the name of the contact. Name, phone, email, birthday, note
        can only be replaced, and notes can be replaced and supplemented.
        :return: None
        """
        database = Serialization.deserialization_data()
        user_name = self.gets_the_name_to_make_changes_to_the_data(database)
        record = self.model.gets_data_by_name(user_name, database)
        while True:
            self.view.requests_what_edit()
            command_edit = input().casefold().strip()

            try:
                # by command_edit, the corresponding function is selected, to which 1 record is transferred.
                # An updated record is returned.
                updated_data, updated_command = self.get_updated_data(command_edit)
                updated_record = self.model.get_editor_handler(updated_command)(self, record, updated_data)
                break
            except KeyError:
                self.view.requests_re_entry_of_the_data()
        updated_database = self.model.updates_the_database(record, updated_record, database)
        Serialization.serialization_data(updated_database)
        self.view.reports_the_updated_of_a_contact(user_name)

    def get_updated_name(self, command):
        updated_data = CommandCreate.input_name(self).strip()
        return updated_data, command

    def get_updated_phone(self, command):
        updated_data = CommandCreate.input_phone_number(self).strip()
        return updated_data, command

    def get_updated_email(self, command):
        updated_data = CommandCreate.input_email(self).strip()
        return updated_data, command

    def get_updated_birthday(self, command):
        updated_data = CommandCreate.input_birthday(self).strip()
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

        updated_data = CommandCreate.add_note(self).strip()
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

    def gets_the_name_to_make_changes_to_the_data(self, database):
        while True:
            self.view.requests_enter_name_to_changes_data()
            user_name = input().strip()
            # checking if name (self.user_name) exists in the book.
            if not RecordEditor().checking_presence_of_name_in_the_database(user_name, database):
                self.view.reports_the_not_exist_of_name_in_database(user_name)
                continue
            break
        return user_name


class CommandExit:
    def __init__(self, view):
        self.view = view

    def organizes_the_exit(self):
        self.view.displays_see_ya()
        sys.exit(0)


class CommandSearch:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    @is_file_empty_decorator
    def organizes_the_search(self):
        self.view.requests_key_word_for_search()
        key_word = input()
        user_list = self.model.to_search(key_word)
        if user_list:
            self.view.displays_matches(key_word, user_list)
        else:
            self.view.reports_no_matches()


class CommandShow:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    @is_file_empty_decorator
    def organizes_the_show(self):
        users = self.model.to_get_all()
        self.view.displays_users(users)


if __name__ == '__main__':
    command_birthday = CommandBirthday(BirthdayPeople(), ConsoleBirthdayCommandNotifications())
    command_create = CommandCreate(RecordCreator(), ConsoleCreateCommandNotifications())
    command_delete = CommandDelete(RecordForDeletion(), ConsoleDeleteCommandNotifications())
    command_help = CommandHelp(ConsoleHelpCommandNotifications())
    command_edit = CommandEdit(RecordEditor(), ConsoleEditCommandNotifications())
    command_exit = CommandExit(ConsoleExitCommandNotifications())
    command_search = CommandSearch(RecordSearcher(), ConsoleSearchCommandNotifications())
    command_show = CommandShow(DatabaseContent(), ConsoleShowCommandNotifications())
    view = ConsoleControllerNotifications()

    controller = ConsoleController(command_birthday, command_create, command_delete, command_help, command_edit,
                                   command_exit, command_search, command_show, view)

    controller.start()

    while True:
        try:
            os.mkdir('data')
        except FileExistsError:
            pass
        controller.requests()