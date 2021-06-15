from datetime import timedelta, datetime
import re


def users_to_congratulate(n):
    user_list = []
    user_date = datetime.now() + timedelta(days = n)
    search_pattern = user_date.day + '.' + user_date.month
    with open('data//data-file.txt', 'a') as file:
        users = file.readlines()
        for user in users:
            if re.search(search_pattern, re.split(' ',user)[3]):
                user_list.append(re.split(' ', user)[0].strip()) 
    result = '\n'.join(user_list)       
    return f'Please do not forget to tell them happy birthday!\n{result}'

def user_search(user_name):
    user_list = []
    with open('data//data-file.txt', 'a') as file:
        users = file.readlines()
        for user in users:
            if user_name in re.split(' ', user)[0]:
                user_data = re.split(' ', user)[0].strip() + re.split(' ', user)[1].strip()
                user_list.append(user_data)
    result = '\n'.join(user_list)
    return f'Found some matches:\n{result}'

def note_search(key_word):
    user_list = []
    with open('data//data-file.txt', 'a') as file:
        users = file.readlines()
        for user in users:
            if key_word in re.split(' ', user)[-1]:
                user_data = re.split(' ', user)[0].strip() + re.split(' ', user)[-1].strip()
                user_list.append(user_data)
    result = '\n'.join(user_list)
    return f'Found some users with matching notes:\n{result}'

            


