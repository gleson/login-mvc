from getpass import getpass
from controller import ControllerUser


if __name__ == "__main__":
    user_name = None
    while True:
        ctl = ControllerUser()
        options_out = input('\nO que deseja fazer?\n'
                            '1 - Efetuar login\n'
                            '2 - Cadastrar usuário\n'
                            '0 - Encerrar\n'
                            'Escolha uma opção: ')

        if options_out == '1':
            while True:
                email = input('Digite o email: ')
                password = getpass(prompt='Digite a senha: ')        
                user_name, user_level = ctl.user_login(email, password)
                if user_name:
                    print(f'Olá {user_name}. Bem vindo ao sistema!')
                else:                
                    try_again = input('O login não foi conluído.\nDeseja tentar novamente? (s/n) ')
                    if try_again.lower()=='s':
                        continue
                break

        elif options_out == '2':
            while True:
                name = input('\nDigite o nome: ')
                email = input('Digite o email: ')
                print('-> A senha deve conter entre 8 e 20 caracteres, e mesclar letras maiúsculas, minúsculas e números.')
                password = getpass(prompt='Digite a senha: ')
                password2 = getpass(prompt='Digite novamente a senha: ')
                result = ctl.user_sign_up(name, email, password, password2)
                if not result:
                    try_again = input('O cadastro não foi conluído.\nDeseja tentar novamente? (s/n) ')
                    if try_again.lower()=='s':
                        continue
                break

        elif options_out == '0':
            print('Encerrando o sistema.\n')
            break
        else:
            print('Escolha uma opção válida!')

        while user_name:
            current_user = ctl.read_users(name=user_name)[0]
            adm_options = ''
            if user_level=='admin':
                adm_options = '2 - Alterar conta de um usuário\n'
            
            options_in = input(f'\nO que deseja fazer {user_name}?\n'
                                '1 - Alterar minhas informações\n'
                            f'{adm_options}'
                                '0 - Efetuar Logout\n'
                                'Escolha uma opção: ')

            if options_in=='1':
                adm_01_options = ''
                if user_level=='admin':
                    adm_01_options = '6 - Alterar nível de acesso\n'
                while True:
                    user_options = input(f'\nO que deseja alterar {user_name}?\n'
                                        '1 - Alterar Nome\n'
                                        '2 - Alterar Email\n'
                                        '3 - Alterar Senha\n'
                                        '4 - Alterar status da conta\n'
                                        '5 - Deletar Conta\n'
                                        f'{adm_01_options}'
                                        '0 - Voltar\n'
                                        'Escolha uma opção: ')
                    print('')
                    if user_options=='1':
                        new_name = input('Digite o novo nome: ')
                        result = ctl.update_user(current_user.id, 'name', new_name)
                        if result:
                            user_name = new_name
                    elif user_options=='2':
                        new_email = input('Digite o novo email: ')
                        ctl.update_user(current_user.id, 'email', new_email)
                    elif user_options=='3':
                        new_password = getpass('Digite a nova senha: ')
                        ctl.update_user(current_user.id, 'password', new_password)
                    elif user_options=='4':
                        new_status = input('Deseja desativar a conta? (s/n): ')
                        if new_status.lower()=='s':
                            ctl.update_user(current_user.id, 'status', new_status)
                            user_name, user_level = ctl.user_logout()
                            break
                    elif user_options=='5':
                        delete = input('Tem certeza que deseja deletar sua conta? (s/n): ')
                        if delete.lower()=='s':
                            ctl.delete_user(current_user.id)
                            user_name, user_level = ctl.user_logout()
                            break
                    elif user_options=='6' and user_level=='admin':
                        new_level = input('Níveis disponíveis:\n'
                                        '1 - Usuário\n'
                                        '2 - Administrador\n' 
                                        'Escolha um nível de acesso: ')
                        if new_level=='2':
                            ctl.update_user(current_user.id, 'level', 'admin')
                        else:
                            ctl.update_user(current_user.id, 'level', 'user')
                        user_name, user_level = ctl.user_logout()
                        break
                    elif user_options=='0':
                        break
                    else:
                        print('Escolha uma opção válida!')

            elif options_in=='2' and user_level=='admin':
                while True:
                    print('\nQual usuário deseja alterar?')
                    ctl.display_users(exclude=current_user.id)
                    try:
                        alter_user_choice = int(input('Para retornar digite: 0\nDigite o número do usuário: '))
                        if alter_user_choice==0:
                            break
                        else:
                            alter_user = ctl.read_users(id=alter_user_choice)[0]
                            print(f'Usuário {alter_user.name} selecionado.')
                    except (ValueError, IndexError):
                        print('\nFavor digite uma opção válida!')
                        continue                
                    
                    user_options = input(f'\nO que deseja alterar do usuário {alter_user.name}?\n'
                                        '1 - Alterar Nome\n'
                                        '2 - Alterar Email\n'
                                        '3 - Resetar Senha\n'
                                        '4 - Alterar status da conta\n'
                                        '5 - Deletar Conta\n'
                                        '6 - Alterar nível de acesso\n'
                                        '0 - Voltar\n'
                                        'Escolha uma opção: ')
                    print('')
                    result = False
                    if user_options=='1':
                        new_name = input('Digite o novo nome: ')
                        result = ctl.update_user(alter_user.id, 'name', new_name)
                    elif user_options=='2':
                        new_email = input('Digite o novo email: ')
                        result = ctl.update_user(alter_user.id, 'email', new_email)
                    elif user_options=='3':
                        result = ctl.update_user(alter_user.id, 'password', 'Reset123')
                        print('Senha resetada para: Reset123')
                    elif user_options=='4':
                        current_status = 'ativar'
                        if abs(alter_user.status-1)==0:
                            current_status = 'desativar'
                        new_status = input(f'Deseja {current_status} a conta? (s/n): ')
                        if new_status.lower()=='s':
                            result = ctl.update_user(alter_user.id, 'status', abs(alter_user.status-1))
                    elif user_options=='5':
                        delete = input(f'Tem certeza que deseja deletar a conta de {alter_user.name}? (s/n): ')
                        if delete.lower()=='s':
                            result = ctl.delete_user(alter_user.id)
                    elif user_options=='6' and user_level=='admin':
                        new_level = input('Níveis disponíveis:\n'
                                        '1 - Usuário\n'
                                        '2 - Administrador\n' 
                                        'Escolha um nível de acesso: ')
                        if new_level=='2':
                            result = ctl.update_user(alter_user.id, 'level', 'admin')
                        else:
                            result = ctl.update_user(alter_user.id, 'level', 'user')
                    elif user_options=='0':
                        break
                    else:
                        print('Escolha uma opção válida!')
                    if result:
                        break

            elif options_in=='0':
                user_name, user_level = ctl.user_logout()
                break
            else:
                print('Escolha uma opção válida!')

