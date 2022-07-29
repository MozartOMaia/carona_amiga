# Carona Amiga

<img src="logo.png" width="200" height="200" />

>Inserir pequena descrição do projeto

# Tecnologias Utilizadas

As ferramentas a seguir estão sendo utilizadas no projeto:
 - [Python 3](https://www.python.org/)
 - [Pip 3](https://pip.pypa.io/en/stable/)
 - [Django](https://www.djangoproject.com/)
 - [virtualenv](https://pypi.org/project/virtualenv/)

# Instalação

Clone o repositório:
```bash
# Baixe o repositório em sua máquina
git clone https://github.com/tads-cnat/caronaamiga.git

# Acessa a página
cd caronaamiga
```  

Crie um ambiente virtual com virtualenv:
```bash
# Cria o ambiente virtual
virtualenv env

# Ative o ambiente o virtual
source env/bin/activate
```
Obs.: Dependendo do seu sistema operacional ou como foi instalado o ```virtualenv``` o comando pode ser diferente.

Instale as dependências:
```bash
pip3 install -r requirements.txt
```

Execute a migração do banco de dados:
```bash
python3 manage.py migrate
```

# Documentação

 + [Documento de visão](docs/README.md)
 + [Diagrama de casos de uso](docs/diagrama_de_casos_de_uso.png)
 + Detalhamento de casos de uso
   + [Criar carona](docs/criar_carona_cdu.md)
   + [Editar carona](docs/editar_carona_CDU.md)
   + [Enviar mensagem para motorista](docs/enviar_mensagem_motorista_CDU.md)
   + [Pesquisar carona](docs/pesquisar_carona_CDU.md)
 + [Diagrama de classes](docs/diagramaClasse_caronaAmiga.pdf)
 + [Diagrama de entidade relacionamento](docs/diagrama_er.png)