import re
from abc import ABC, abstractmethod


class ViewInterface(ABC):
    @abstractmethod
    def displays_see_ya(self):
        pass

    @abstractmethod
    def describes_commands(self):
        pass

    @abstractmethod
    def displays_key_error(self, command):
        pass

    @abstractmethod
    def displays_matches(self, key_word, user_list):
        pass

    @abstractmethod
    def displays_request_to_wis_happy_birthday(self, user_list):
        pass

    @abstractmethod
    def displays_users(self, users):
        pass

    @abstractmethod
    def requests_days_left_to_the_birthday(self):
        pass

    @abstractmethod
    def requests_command_edit_note(self):
        pass

    @abstractmethod
    def requests_enter_the_note(self):
        pass

    @abstractmethod
    def requests_enter_birthday(self):
        pass

    @abstractmethod
    def requests_enter_email(self):
        pass

    @abstractmethod
    def requests_enter_name(self):
        pass

    @abstractmethod
    def requests_enter_phone(self):
        pass

    @abstractmethod
    def requests_enter_name_to_changes_data(self):
        pass

    @abstractmethod
    def requests_input_number(self):
        pass

    @abstractmethod
    def requests_key_word_for_search(self):
        pass

    @abstractmethod
    def requests_re_entry_of_the_data(self):
        pass

    @abstractmethod
    def requests_command(self):
        pass

    @abstractmethod
    def reports_no_birthdays(self):
        pass

    @abstractmethod
    def reports_no_matches(self):
        pass

    @abstractmethod
    def reports_the_deletion_of_a_contact(self, user_name):
        pass

    @abstractmethod
    def reports_the_updated_of_a_contact(self, user_name):
        pass

    @abstractmethod
    def reports_the_existence_of_name_in_database(self):
        pass

    @abstractmethod
    def reports_the_not_exist_of_name_in_database(self, name):
        pass

    @abstractmethod
    def reports_what_edit(self):
        pass

    @abstractmethod
    def start_view(self):
        pass


class ConsoleView(ViewInterface):
    def displays_see_ya(self):
        print(f'See ya!')

    def describes_commands(self):
        print('Hi, I\'m\' a bot. And I can:')
        print('<create>   /save contacts with names, addresses, phone numbers, '
              'emails and birthdays to the contact book;')
        print('<birthday> /display a list of contacts who have a birthday after a '
              'specified number of days from the current date;')
        print('<search>   /search for contacts and notes from the contact book;')
        print('<edit>     /edit entries from the contact book, edit and delete notes;')
        print('<delete>   /delete entries from the contact book;')
        print('<show>     /display all contents of the contact book;')
        print('<exit>     /exit the program')

    def displays_key_error(self, command):
        print(f'Command "{command}" does not exist. Please try again')

    def displays_matches(self, key_word, user_list):
        print(f'Found some users with matching key word "{key_word}":\n')
        ConsoleView.displays_users(user_list)

    def displays_request_to_wis_happy_birthday(self, user_list):
        print(f'Please do not forget to tell them happy birthday!\n')
        ConsoleView.displays_users(user_list)

    def displays_users(self, users):
        """
        Function prints from user list
        :param users: a list with lines from data-file.txt
        :return: prints formatted table with user information from list
        """
        print('-' * 119)
        header = "| {:^5} | {:^15} | {:^15} | {:^25} | {:^15} | {:^25} |".format('#', 'name', 'phone', 'e-mail',
                                                                                 'birthday', 'note')
        print(header)
        print('-' * 119)
        # Getting user data from line
        for user in enumerate(users):
            count = user[0] + 1
            name = re.split(r'\|', user[1])[0].strip()
            phone = re.split(r'\|', user[1])[1].strip()
            e_mail = re.split(r'\|', user[1])[2].strip()
            birthday = re.split(r'\|', user[1])[3].strip()
            note = re.split(r'\|', user[1])[4].strip()
            user_data = "| {:^5} | {:<15} | {:<15} | {:25} | {:<15} | {:<25} |".format(count, name, phone, e_mail,
                                                                                       birthday, note)
            print(user_data)
        print('-' * 119)

    def requests_days_left_to_the_birthday(self):
        print('Please enter days left to the needed date: ', end='')

    def requests_command_edit_note(self):
        print('Change, add or delete notes?:  ', end='')

    def requests_enter_the_note(self):
        print('Enter the note: ', end='')

    def requests_enter_birthday(self):
        print('Enter your B-Day (DD.MM.YYYY): ', end='')

    def requests_enter_email(self):
        print('Enter your email: ', end='')

    def requests_enter_name(self):
        print('Enter your name: ', end='')

    def requests_enter_phone(self):
        print('Enter your phone number: ', end='')

    def requests_enter_name_to_changes_data(self):
        print('Enter a name to make data changes: ', end='')

    def requests_input_number(self):
        print('Please enter a valid number!', end='')

    def requests_key_word_for_search(self):
        print('Please, enter the key word: ', end='')

    def requests_re_entry_of_the_data(self):
        print('Incorrect, once more please!')

    def requests_command(self):
        print('Enter your request: ', end='')

    def reports_no_birthdays(self):
        print('No congrats on this day!')

    def reports_no_matches(self):
        print('No matches!')

    def reports_the_deletion_of_a_contact(self, user_name):
        print(f'The contact named "{user_name}" has been deleted.')

    def reports_the_updated_of_a_contact(self, user_name):
        print(f'Updated contact details with name "{user_name}".')

    def reports_the_existence_of_name_in_database(self):
        print('This name already exists in contact book!')

    def reports_the_not_exist_of_name_in_database(self, name):
        print(f'Name "{name}" does not exist in the contact book.')

    def reports_what_edit(self):
        print(f'What edit? (name/phone/email/birthday/note):  ', end='')

    def start_view(self):
        print('Salut! Enter \'help\' to see the commands')