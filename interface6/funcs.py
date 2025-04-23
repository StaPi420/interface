import json
import string

def db_load():
    with open('db.json', 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.decoder.JSONDecodeError:
            return {}

def db_dump(obj):
    with open('db.json', 'w', encoding='utf-8') as f:
        json.dump(obj, f)

def login_check(log):
    response = ['', '']
    if len(log) < 5:
        response[1] = 'Логин должен быть длиннее 5 символов.\n'
    else:
        response[1] = ''
    symbols = set(string.ascii_letters + string.digits)
    for i in log:
        if i not in symbols:
            response[0] = 'Логин должен содержать только символы \n\
латиницы и цифры.\n'
            break   
    else:
        response[0] = ''
    return response

def pass_check(pas):
    response = ['', '', '', '', '']
    if len(pas) < 8:
        response[0] = "Пароль должен состоять не менее чем из 8 символов\n"
    else:
        response[0] = ''
    if any(x.isupper() for x in pas):
        response[1] = ''
    else:
        response[1] = 'Пароль должен содержать хотя бы заглавный символ\n'
    if any(x.islower() for x in pas):
        response[2] = ''
    else:
        response[2] = 'Пароль должен содержать хотя бы один строчной символ\n'
    if any(x in string.digits for x in pas):
        response[3] = ''
    else:
        response[3] = 'Пароль должен содержать хотя бы одну цифру\n' 
    if any(x in {'!', '@', '#', '$','%', '%'} for x in pas):
        response[4] = ''
    else:
        response[4] = 'Пароль должен содержать хотя бы один специальный символ\n'
    return response



    
