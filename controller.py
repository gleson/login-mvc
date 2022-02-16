from models import User
from db import *
from datetime import datetime
import re
import hashlib


def encrypt_password(password):
    if len(password) == 0:
        print('A senha não pode ficar vazia!\n')
    elif len(password) < 8:
        print('A senha possui menos de 8 caracteres.\n')
    elif len(password) > 20:
        print('A senha possui mais de 20 caracteres.\n')
    elif not re.search("[a-z]", password):
        print('A senha não possui letras minúsculas.\n')
    elif not re.search("[A-Z]", password):
        print('A senha não possui letras maiúsculas.\n')
    elif not re.search("[0-9]", password):
        print('A senha não possui números.\n')
    else:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    return False

def check_email(email):
    if(re.search('^[a-z0-9]+[.\-_]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email)):   
        return True
    return False


class ControllerUser:

    def user_sign_up(self, name, email, password, password2):
        x = DbUser.read()

        admin_verify = list(filter(lambda x: x.level=='admin', x))
        name_verify = list(filter(lambda x: x.name==name, x))
        email_verify = list(filter(lambda x: x.email==email, x))
        level='user'

        if not admin_verify:
            print('\nNão existe um administrador no sistema.\nO usuário atual receberá privilégios de Admin.\n')
            level = 'admin'

        if not name:
            print('\nO nome do não pode ficar vazio!\n')
        elif name_verify:
            print('\nJá existe um usuário com esse nome! Favor escolha outro nome.\n')
        elif not check_email(email):
            print('\nFavor digite um email válido!\n')
        elif email_verify:
            print('\nJá existe um usuário com esse email! Favor escolha outro.\n')
        elif password != password2:
            print('\nAs senhas digitadas são diferentes!\n')
        else:
            encrypted_password = encrypt_password(password)
            if encrypted_password:
                DbUser.create(name, email, encrypted_password, level, 1, datetime.now())
                print('\nUsuário cadastrado com sucesso!\n')
                return True
        return False


    def user_login(self, email, password):
        user_name, user_level = None, None
        x = DbUser.read()
        if not email:
            print('\nFavor preencha o email.\n')
        elif not password:
            print('\nFavor preencha a senha.\n')
        else:
            user_info = list(filter(lambda x: x.email==email, x))
            if not user_info:
                print('\nEmail incorreto!\n')
            else:
                encrypted_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
                if user_info[0].password != encrypted_password:
                    print('\nSenha incorreta!\n')
                elif user_info[0].status == 0:
                    print('\nSua conta foi desativada!\nFavor solicitar a reativação a um administrador.\n')
                else:
                    print('\nUsuário logado com sucesso!\n')
                    return user_info[0].name, user_info[0].level
        return user_name, user_level


    def user_logout(self):
        print('\nUsuário deslogado com sucesso!\n')
        return None, None


    def update_user(self, id, field, value):
        x = DbUser.read()
        user_info = list(filter(lambda x: x.id==id, x))
        update = False

        if field=='name':
            name_verify = list(filter(lambda x: x.name==value, x))
            if user_info[0].name==value:
                print('Favor digite um nome diferente do atual!\n')
            elif name_verify:
                print('Já existe um usuário com esse nome!\n')
            else:
                update = True
        elif field=='email':
            email_verify = list(filter(lambda x: x.email==value, x))
            if email_verify:
                print('Já existe um usuário com esse email!\n')
            elif user_info[0].email==value:
                print('Favor digite um email diferente do atual!\n')
            else:
                update = check_email(value)
                if not update:
                    print('Favor digite um email válido!')
                
        elif field=='password':
            value = encrypt_password(value)
            if user_info[0].password==value:
                print('Favor digite uma senha diferente da atual!\n')
            else:
                update = True
        elif field=='level':
            if user_info[0].level==value:
                print('Favor escolha um nível de acesso diferente do atual!\n')
            else:
                update = True
        elif field=='status':
            if user_info[0].status==value:
                print('Favor escolha um status diferente do atual!\n')
            else:
                update = True
        else:
            print('Escolha um campo válido!\n')
        
        if update:
            result = DbUser.update(id, field, value)
            if result:
                print(f'\nAtualização realizada com sucesso!\n')
            else:
                print('\nHouve um erro na gravação, tente novamente.\n')
            return result
        else:
            print(f'\nO campo {field} não foi alterado!')
            return False

    def delete_user(self, id):
        user_info = DbUser.delete(id)
        if user_info:
            print('\nUsuário deletado com sucesso!\n')
        else:
            print('\nUsuário não encontrado!\n')
        return user_info

    def read_users(self, id=None, name=None):
        x = DbUser.read()
        if id:
            x = list(filter(lambda x: x.id==id, x))
        elif name:
            x = list(filter(lambda x: x.name==name, x))
        return x


    def display_users(self, id=None, name=None, exclude=None):
        x = ControllerUser().read_users(id, name)

        for i in x:
            if exclude==i.id:
                continue
            if id or name:
                if i.status == 0:
                    status = 'desativado'
                elif i.status == 1:
                    status = 'ativado'
                print(f'{i.id} - {i.name}, {i.level}, {status}, {i.email}')
            else:
                print(f'{i.id: <4}-  {i.name}')

        
        return x[0]

