from models import User
from db import *
from datetime import datetime
import re
import hashlib


def encrypt_password(password):
    if len(password) == 0:
        message = 'A senha não pode ficar vazia!'
    elif len(password) < 8:
        message = 'A senha possui menos de 8 caracteres.'
    elif len(password) > 20:
        message = 'A senha possui mais de 20 caracteres.'
    elif not re.search("[a-z]", password):
        message = 'A senha não possui letras minúsculas.'
    elif not re.search("[A-Z]", password):
        message = 'A senha não possui letras maiúsculas.'
    elif not re.search("[0-9]", password):
        message = 'A senha não possui números.'
    else:
        return {'password': hashlib.sha256(password.encode('utf-8')).hexdigest(), 'message': 'Verificação da senha, Ok!'}
    return {'password': None, 'message': f'\n{message}\n'}

def check_email(email):
    if(re.search('^[a-z0-9]+[.\-_]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email)):   
        return True
    return False


class ControllerUser:

    def user_sign_up(self, name, email, password, password2):
        admin_verify = DbUser.read_one(level='admin')
        name_verify = DbUser.read_one(name=name)
        email_verify = DbUser.read_one(email=email)

        message = ''

        if not name:
           message ='O nome do não pode ficar vazio!'
        elif name_verify:
            message ='Já existe um usuário com esse nome! Favor escolha outro nome.'
        elif not check_email(email):
            message ='Favor digite um email válido!'
        elif email_verify:
            message ='Já existe um usuário com esse email! Favor escolha outro.'
        elif password != password2:
            message ='As senhas digitadas são diferentes!'
        else:
            encrypted_password = encrypt_password(password)
            message = encrypted_password['message']
            if encrypted_password['password']:
                if not admin_verify:
                    message = '\nComo não existe um administrador no sistema,\no usuário atual receberá privilégios de Admin.'
                    level = 'admin'
                else:
                    level='user'
                DbUser.create(name, email, encrypted_password['password'], level, 1, datetime.now())
                message = 'Usuário cadastrado com sucesso!'+message
                return {'sign_up': True, 'message': f'\n{message}\n'}
        return {'sign_up': False, 'message': f'\n{message}\n'}


    def user_login(self, email, password):

        if not email:
            message = 'Favor preencha o email.'
        elif not password:
            message = 'Favor preencha a senha.'
        else:
            user = DbUser.read_one(email=email)
            if not user:
                message = 'Email não encontrado!'
            else:
                encrypted_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
                if user.password != encrypted_password:
                    message = 'Senha incorreta!'
                elif user.status == 0:
                    message = 'Sua conta foi desativada!\nFavor solicitar a reativação a um administrador.'
                else:
                    message = 'Usuário logado com sucesso!'
                    return {'logged': True, 'id': user.id, 'message': f'\n{message}'}
        return {'logged': False, 'id': None, 'message': f'\n{message}\n'}


    def user_logout(self):
        return {'logged': False, 'id': None, 'message': '\nUsuário deslogado com sucesso!\n'}


    def update_user(self, id, field, value):
        user_info = DbUser.read_one(id=id)
        update = False
        message = ''

        if field=='name':
            name_verify = DbUser.read_one(name=value)
            if user_info.name==value:
                message = 'Favor digite um nome diferente do atual!'
            elif name_verify:
                message = 'Já existe um usuário com esse nome!'
            else:
                update = True
        elif field=='email':
            email_verify = DbUser.read_one(email=value)
            if email_verify:
                message = 'Já existe um usuário com esse email!'
            elif user_info.email==value:
                message = 'Favor digite um email diferente do atual!'
            else:
                update = check_email(value)
                if not update:
                    message = 'Favor digite um email válido!'
        elif field=='password':
            result = encrypt_password(value)
            value = result['password']
            if user_info.password==value:
                message = 'Favor digite uma senha diferente da atual!'
            else:
                message = result['message']
                update = True
        elif field=='level':
            if user_info.level==value:
                message = 'Favor escolha um nível de acesso diferente do atual!'
            else:
                update = True
        elif field=='status':
            if user_info.status==value:
                message = 'Favor escolha um status diferente do atual!'
            else:
                update = True
        else:
            message = 'Escolha um campo válido!'
        
        if update:
            result = DbUser.update(id, field, value)
            if result:
                message = 'Atualização realizada com sucesso!'
            else:
                message += '\nHouve um erro na gravação, tente novamente.'
            return {'updated': result, 'message': f'\n{message}\n'}
        else:
            message += '\nO campo não foi alterado!'
            return {'updated': False, 'message': f'\n{message}\n'}


    def delete_user(self, id):
        user_info = DbUser.delete(id)
        if user_info:
            return {'deleted': True, 'message': '\nUsuário deletado com sucesso!'}
        return {'deleted': False, 'message': 'Usuário não encontrado!\n'}


    def read_user(self, id=None, name=None, email=None, level=None):
        try:
            return DbUser.read_one(id=id, name=name, email=email, level=level)
        except:
            return False


    def display_users(self, id=None, exclude=None):
        x = DbUser.read()
        message = ''
        for i in x:
            if exclude==i.id:
                continue
            if id and id==i.id:
                if i.status == 0:
                    status = 'desativado'
                elif i.status == 1:
                    status = 'ativado'
                message = f'{i.id} - {i.name}, {i.level}, {status}, {i.email}\n'
                break
            else:
                message += f'{i.id: <4}-  {i.name}\n'

        if message:
            return message
        return '(lista de usuários vazia)'

