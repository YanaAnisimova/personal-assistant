from datetime import timedelta, datetime
import re


def to_congratulate():
    n = input('Please enter days left to the needed date: ')
    user_list = []
    user_date = datetime.now() + timedelta(days = n)
    search_pattern = user_date.day + '.' + user_date.month
    with open('data//data-file.txt', 'a') as file:
        users = file.readlines()
        for user in users:
            if re.search(search_pattern, re.split(',',user)[3]):
                user_list.append(re.split(',', user)[0].strip()) 
    result = '\n'.join(user_list)       
    print(f'Please do not forget to tell them happy birthday!\n{result}')

def search():
    user_name = input('Please, enter user name: ')
    user_list = []
    with open('data//data-file.txt', 'a') as file:
        users = file.readlines()
        for user in users:
            if user_name in re.split(',', user)[0]:
                user_data = re.split(',', user)[0].strip() + re.split(',', user)[1].strip()
                user_list.append(user_data)
    result = '\n'.join(user_list)
    print(f'Found some matches:\n{result}')

def note():
    key_word = input('Please, enter the key word for search: ')
    user_list = []
    with open('data//data-file.txt', 'a') as file:
        users = file.readlines()
        for user in users:
            if key_word in re.split(',', user)[-1]:
                user_data = re.split(',', user)[0].strip() + re.split(',', user)[-1].strip()
                user_list.append(user_data)
    result = '\n'.join(user_list)
    print(f'Found some users with matching notes:\n{result}')

            


