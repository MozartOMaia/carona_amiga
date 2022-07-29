# Carona Amiga
## Especificação de caso de uso

## Pesquisar Carona

Histórico de revisão

| Data | Versão | Descrição | Autor |
|--|--|--|--|
| 01/2021 | 1.0 | Criação de "Pesquisar Carona" | Mozart Maia |


## Resumo
No caso de uso "Pesquisar Carona" o ator Passageiro ou Motorista irá pesquisar por uma carona, com base nos filtros estabelecidos por ele mesmo.

## Atores
Passageiro ou Motorista

## Pré-condições

 - Usuário deve estar logado no sistema

## Pós-condições
O usuário descobrirá todas as caronas que estiverem disponíveis com base em seu filtro, inclusive se não houver nenhuma.

## Fluxo de evento
### Fluxo básico

 1. Usuário, após logar no Carona Amiga, será apresentado à tela inicial, que também é a tela de Pesquisar Caronas
 2. Sistema disponibilizará três filtros para exibir caronas: “Saindo de”, “Indo para” e “Data”
 3. Usuário preenche os filtros: todos ou apenas os que escolher
 4. Passageiro clica no botão de pesquisar (lupa)
 5. Sistema exibe uma lista de resultados, com dados como: nome do motorista, nota do motorista, endereço de saída, endereço de destino, dias da semana que a carona ocorre, vagas na carona e horário
 6. Sistema exibe número de caronas disponíveis com base nos filtros

### Fluxo de erro - Sistema não consegue exibir resultado 
Após o passo 4 do fluxo básico

 1. Sistema por algum motivo não consegue acessar os dados das caronas no banco de dados
 2. Sistema exibe mensagem de erro: "Não conseguimos exibir resultados no momento. Por favor, tente mais tarde".

### Fluxo alternativo - Sistema não possui resultados com base nos filtros

Em qualquer momento após o passo 4 do fluxo básico

 1. Sistema exibe a mensagem “Nenhuma carona disponível com essas características” na própria página

## Protótipo(s) de interface do CDU
![inicial](https://user-images.githubusercontent.com/37476677/148705376-ed0f5385-fbf2-418b-a008-4c7da0640357.png)
![resultados](https://user-images.githubusercontent.com/37476677/148705421-2eb20eac-c993-47a6-9c20-b00d5fe32306.png)

