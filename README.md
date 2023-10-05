# :bookmark: Workout Day

:label: Tecnologia Principal: Python
<br> :label: Tecnologia Secundária: HTML e CSS
<br> :bricks: Framework: Flask e Django
<br> :classical_building: Software: Docker
<br> :luggage: Banco de Dados: MySQL
<br> :page_facing_up: Padronização: pep8
<br> :book: Documentação: <a href='https://api.postman.com/collections/10550152-b5e1a690-b023-49b4-aef0-f847c685f197?access_key=PMAT-01HABB0PBFM6AV4YF6MPWEZCYJ'> Figma </a> e <a href='https://api.postman.com/collections/10550152-b5e1a690-b023-49b4-aef0-f847c685f197?access_key=PMAT-01HABB0PBFM6AV4YF6MPWEZCYJ'> Postman

## :dart: Sobre

Projeto desenvolvido para a matéria Projeto Software da faculdade Impacta, seu objetivo é auxiliar no acompanhamento de treinos realizados por um usuário, podendo acrescentar e consultar tempo de execução, alterar e deletar se for necessário.

## :building_construction: Instalação do projeto

### :classical_building: Rodar o Docker

- Para criar e iniciar os contêineres:
```
docker-compose up
```

- Para paralisar e remover todos os contêineres:
```
docker-compose down
```

- Para iniciar os contêineres:
```
docker-compose start
```

- Para paralisar os contêineres:
```
docker-compose stop
```

### :test_tube: Acesso ao banco de dados

- Abrir o terminal do container do MySQL
- Conectar com usuário root
```
mysql -u root -p
```

- Digitar a senha do banco
```
123456
```

- Acessar o database correto
```
USE workoutDay;
```

## :door: Portas do Projeto

#### :label: Aplicação

http://localhost:5000/

#### :label: Banco de Dados

127.0.0.1:3309
