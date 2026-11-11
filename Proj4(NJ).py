
import json
import time 
from functools import wraps, reduce

error_list = []

all_users , total_departments = 0,0
all_admins , total_guests = 0,0
total_users , total_logs = 0,0
total_managers = 0


with open("Technova.json", "r") as f:
    data = json.load(f)
    

def walk(data):

    if isinstance(data, dict):
        for v in data.values():
            walk(v)

    elif isinstance(data, list):
        for item in data:
            walk(item)

    else:
        print(data)


def timer(func):
    @wraps(func)
    def wrapper(*arg, **kwarg):
        t1 = time.time()
        result = func(*arg, **kwarg)
        t2 = time.time() - t1
        print(f"This {func.__name__}, ran in {t2:.4f} sec")
        return result
    return wrapper

@timer
def validate_cleaning(data):
    ##--------------(User stuff)
    for user in data["users"]:

        if isinstance(user["id"], int):
            pass

        elif isinstance(user['id'], str):
            if user["id"].lstrip('-').isdigit():
                user["id"] = int(user['id'])
                continue

    for user in data['users']:

        if isinstance(user['active'], str):
            val_lower = user['active'].strip().lower()
            if val_lower == 'true':
                user['active'] = True
                continue
            if val_lower == 'false':
                user['active'] = False 
                continue

        if isinstance(user['role'], str):
            user['role'] = user['role'].lower()


    for user in data["users"]:
        try:
    
            if len(user['name']) <= 0:
                error_list.append(user)
                
            if user["name"] != [] :
                continue
    
        except(KeyError):
            error_list.append(user)


    for user in data['users']:
        try:

            prefs = user['preferences']

            if "theme" in prefs and isinstance(prefs['theme'], str):
                prefs['theme'] = prefs['theme'].lower()
                

            if "language" in prefs and isinstance(prefs['language'], str):
                prefs['language'] = prefs['language'].lower()
                continue

        except(KeyError, TypeError):
            continue
    
    sort = []
        
    for user in data["users"]:
            
        if user['id'] not in sort:
            sort.append(user['id'])
                
        else:
            print(f"This is a dupicate user 'id':",user['id'])
            error_list.append(user['id'])
            del (user['id'], user['name'], user['email'], user['role'], user['active'])

    ##---------- department stuff

    for department in data['departments']:
        try:

            if len(department['name']) <= 0:
                print('This "department" doesn\'t have a name', department['name'])
                error_list.append(department)

            if department['name'] != []:
                continue

        except(KeyError):
            print('This "department" doesn\'t have a name', department['budget'])
            error_list.append(department)

    for department in data['departments']:

        if isinstance(department['budget'], int):
            if department['budget'] <= 0:
                print('This "department" has an invalid budget:', department['name'], department['budget'])
                department['budget']= -(department['budget'])
            continue

        if not isinstance(department['budget'], int):

            print('This "department" has an invalid budget:', department['name'], department['budget'])
            if department['budget'].lstrip('-').isdigit():
                department['budget'] = int(department['budget'])
            continue
        
        else:
            break


    valid_user_id = [user['id'] for user in data['users'] if 'id' in user]

    for department in data['departments']:

        for member in department['members']:

            if not member in valid_user_id:
                print('This "member" does not exist:', member)
                error_list.append(member)

        if department['members'] == []:
            print("This department doesn't have members:", department['name'])
            error_list.append(department['name'])

    #---------(logs stuff)

    for log in data['logs']:
    
        if isinstance(log['action'], str):

            if log['action'].lower() == 'login' or 'logout':
                log['action'] = log['action'].lower()

        if log['action'] == None:
            error_list.append(log['action'])
            print('This "event id" has and invalid login status!', log['action'])
            log['action'] = 'logout' 

    print(error_list)


@timer
def count(data):

    global all_users , total_departments, all_admins , total_guests, total_users , total_logs, total_managers

    for user in data['users']:
        total_users += 1
        
        if user['role'].lower() == 'admin':
            all_admins += 1

        if user['role'].lower() == 'manager':
            total_managers += 1

        if user['role'].lower() == 'user':
            all_users += 1

        if user['role'].lower() == 'guest':
            total_guests += 1

    for department in data['departments']:
        total_departments += 1

    for log in data['logs']:
        total_logs += 1 


def main_menu():
    while True:
        print('='*15, 'Welcome', '='*15)
        print("\n1. Analyze the json folder/file")
        print("2. Exit")
        menu = input("pick a menu: ").strip().lower()

        global all_users , total_departments, all_admins , total_guests, total_users , total_logs, total_managers
    
        if menu == "1":

            count(data)
            validate_cleaning(data)

            print('Total users:', total_users)
            print('all users:', all_users)
            print('Total managers:', total_managers)
            print('Total admins:', all_admins)
            print('Total guests:', total_guests)        
            print('Total departments:', total_departments)
            print('Total logs:', total_logs)

        elif menu == '2':
            print('Thanks for using the json analyser')
            return

        else:
            print('This input was not recognised!')
            print('try again')
    
main_menu()


with open('newfile.json', 'w') as j:
    json.dump(data, j, indent = 2)

