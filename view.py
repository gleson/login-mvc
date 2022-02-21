from getpass import getpass
from controller import ControllerUser


if __name__ == "__main__":
    ctl = ControllerUser()
    logged = ctl.user_logout()
    while True:
        options_out = input('\nO que deseja fazer?\n'
                            '1 - Efetuar login\n'
                            '2 - Cadastrar usuário\n'
                            '0 - Encerrar\n'
                            'Escolha uma opção: ')

        if options_out == '1':
            while True:
                email = input('\nDigite o email: ')
                password = getpass(prompt='Digite a senha: ')        
                logged = ctl.user_login(email, password)
                print(logged['message'])
                current_user = ctl.read_user(id=logged['id'])
                if current_user:
                    print(f'Olá {current_user.name}. Bem vindo ao sistema!')
                else:
                    try_again = input('O login não foi conluído.\nDeseja tentar novamente? (s/n) ')
                    if try_again.lower()=='s':
                        continue
                break

        elif options_out == '2':
            while True:
                name = input('\nDigite o nome: ')
                email = input('Digite o email: ')
                print('-> A senha deve conter entre 8 e 20 caracteres, \ne mesclar letras maiúsculas, minúsculas e números.')
                password = getpass(prompt='Digite a senha: ')
                password2 = getpass(prompt='Digite novamente a senha: ')
                result = ctl.user_sign_up(name, email, password, password2)
                print(result['message'])
                if not result['sign_up']:
                    try_again = input('O cadastro não foi conluído.\nDeseja tentar novamente? (s/n) ')
                    if try_again.lower()=='s':
                        continue
                break

        elif options_out == '0':
            print('Encerrando o sistema.\n')
            break
        else:
            print('Escolha uma opção válida!')

        while logged['logged']==True:
            adm_options = ''
            if current_user.level=='admin':
                adm_options = '2 - Alterar conta de um usuário\n'
            
            options_in = input(f'\nO que deseja fazer {current_user.name}?\n'
                                '1 - Alterar minhas informações\n'
                               f'{adm_options}'
                                '0 - Efetuar Logout\n'
                                'Escolha uma opção: ')

            if options_in=='1':
                admin_options = ''
                if current_user.level=='admin':
                    admin_options = '6 - Alterar nível de acesso\n'
                while True:
                    user_options = input(f'\nO que deseja alterar {current_user.name}?\n'
                                        '1 - Alterar Nome\n'
                                        '2 - Alterar Email\n'
                                        '3 - Alterar Senha\n'
                                        '4 - Alterar status da conta\n'
                                        '5 - Deletar Conta\n'
                                       f'{admin_options}'
                                        '0 - Voltar\n'
                                        'Escolha uma opção: ')
                    print('')
                    if user_options=='1':
                        new_name = input('Digite o novo nome: ')
                        result = ctl.update_user(current_user.id, 'name', new_name)
                        print(result['message'])
                        if result['updated']:
                            current_user = ctl.read_user(id=current_user.id)
                    elif user_options=='2':
                        new_email = input('Digite o novo email: ')
                        result = ctl.update_user(current_user.id, 'email', new_email)
                    elif user_options=='3':
                        print('-> A senha deve conter entre 8 e 20 caracteres, \ne mesclar letras maiúsculas, minúsculas e números.')
                        new_password = getpass('Digite a nova senha: ')
                        result = ctl.update_user(current_user.id, 'password', new_password)

                    elif user_options=='4':
                        new_status = input('Deseja desativar a conta? (s/n): ')
                        if new_status.lower()=='s':
                            result = ctl.update_user(current_user.id, 'status', 0)
                            logged = ctl.user_logout()
                    elif user_options=='5':
                        delete = input('Tem certeza que deseja deletar sua conta? (s/n): ')
                        if delete.lower()=='s':
                            result = ctl.delete_user(current_user.id)
                            logged = ctl.user_logout()
                    elif user_options=='6' and current_user.level=='admin':
                        new_level = input('Níveis disponíveis:\n'
                                        '1 - Usuário\n'
                                        '2 - Administrador\n' 
                                        'Escolha um nível de acesso: ')
                        if new_level=='2':
                            result = ctl.update_user(current_user.id, 'level', 'admin')
                        else:
                            result = ctl.update_user(current_user.id, 'level', 'user')
                        logged = ctl.user_logout()
                    elif user_options=='0':
                        break
                    else:
                        print('Escolha uma opção válida!')
                        continue

                    if not logged['logged']:
                        print(result['message']+'\n'+logged['message'])
                    else:
                        print(result['message'])
                    break

            elif options_in=='2' and current_user.level=='admin':
                while True:
                    print('\nQual usuário deseja alterar?')
                    users = ctl.display_users(exclude=current_user.id)
                    print(users)
                    if users == '(lista de usuários vazia)':
                        break
                    try:
                        alter_user_choice = int(input('Para retornar digite 0\nDigite o número do usuário: '))
                        if alter_user_choice==0:
                            break
                        else:
                            alter_user = ctl.read_user(id=alter_user_choice)
                            user_selected = ctl.display_users(id=alter_user_choice)
                            print(f"\nInformações do usuário selecionado:\n{user_selected}")
                    except (ValueError, IndexError):
                        print('\nFavor digite uma opção válida!')
                        continue                
                    
                    user_options = input(f'O que deseja alterar do usuário {alter_user.name}?\n'
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
                        print('A senha será resetada para: Reset123')
                    elif user_options=='4':
                        current_status = 'ativar'
                        if abs(alter_user.status-1)==0:
                            current_status = 'desativar'
                        new_status = input(f'Deseja {current_status} a conta do usuário? (s/n): ')
                        if new_status.lower()=='s':
                            result = ctl.update_user(alter_user.id, 'status', abs(alter_user.status-1))
                    elif user_options=='5':
                        delete = input(f'Tem certeza que deseja deletar a conta de {alter_user.name}? (s/n): ')
                        if delete.lower()=='s':
                            result = ctl.delete_user(alter_user.id)
                    elif user_options=='6' and current_user.level=='admin':
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
                        continue

                    print(result['message'])
                    break

            elif options_in=='0':
                logged = ctl.user_logout()
                break
            else:
                print('Escolha uma opção válida!')

