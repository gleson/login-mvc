# Sistema de Login MVC
Este projeto é um Sistema MVC de Login desenvolvido em Python, com dois níveis de usuário (admin, user) e opções adicionais para o admin. As informações dos usuários são armazenadas em um banco de dados, gerenciado através de ORM.


## Tecnologias utilizadas:
- Python
- POO
- MVC
- Banco de Dados
- ORM


## Opções do Sistema:

### Tela Inicial:
- Login
- Cadastro
- Encerrar

### Após Logar:
1 Alterar minhas informações<br>
 &nbsp;1.1 Alterar Nome<br>
 &nbsp;1.2 Alterar Email<br>
 &nbsp;1.3 Alterar Senha<br>
 &nbsp;1.4 Alterar status da conta<br>
 &nbsp;1.5 Deletar Conta<br>
 &nbsp;1.6 Alterar nível de acesso (admin)<br>
 &nbsp;1.0 Voltar

2 Alterar conta de um usuário (admin)<br>
 &nbsp;2.1 Alterar Nome<br>
 &nbsp;2.2 Alterar Email<br>
 &nbsp;2.3 Resetar Senha<br>
 &nbsp;2.4 Alterar status da conta<br>
 &nbsp;2.5 Deletar Conta<br>
 &nbsp;2.6 Alterar nível de acesso<br>
 &nbsp;2.0 Voltar

3 Efetuar Logout


## Informações relevantes:
- A senha é armazenada somente após ser criptografada em sha256.
- Os campos email e senha são validados com Expressões Regulares.
- No cadastro é verificado se já existe um usuário com o nome ou email informados.
- Se não houver Admin no sistema, o primeiro usuário cadastrado receberá esse level.