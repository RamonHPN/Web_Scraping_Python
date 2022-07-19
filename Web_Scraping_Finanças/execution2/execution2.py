from turtle import color
import requests
import pandas as pd
from bs4 import BeautifulSoup


#Link dos principais acionistas da Intelbras
url = "https://www.fundamentus.com.br/principais_acionistas.php?papel=INTB3&tipo=1"

#Isso é necessário para acessar o site e evitar o erro 403 Forbidden Request
headers = { 
    'User-Agent'      : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 
    'Accept'          : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
    'Accept-Language' : 'en-US,en;q=0.5',
    'DNT'             : '1',  
    'Connection'      : 'close'
}

#Após configurar um agente de usuário de navegador
data = requests.get(url, headers=headers, timeout=5).text
soup = BeautifulSoup(data,"html.parser")

#Peguei o id porque há duas tabelas, você também pode usar find('table')
table = soup.find(id="acoesordinarias")

#Defino os nomes das colunas da futura tabela
df1 = pd.DataFrame(columns=['Acionista', 'Participação(%)'])

for row in table.tbody.find_all('tr'): # em html uma linha da tabela é representada pela tag <tr>
    # Obtendo todas as colunas em cada linha
    columns = row.find_all('td')  # em html uma coluna da tabela é representada pela tag <td>
    if(columns != []):
        data = columns[0].text.strip(' ')
        part = columns[1].text.strip(' ')
        df1 = pd.concat([df1, pd.DataFrame.from_records([{'Acionista': data, 'Participação(%)': part}])], ignore_index=True)


#Porcentagem
df1['Participação(%)'] = [x.replace(',', '.') for x in df1['Participação(%)']]
df1['Participação(%)'] = [x.replace('%', ' ') for x in df1['Participação(%)']]
df1 = df1.astype({"Participação(%)": float})


print('                             Ações Ordinárias')
print(' ')
print(df1.head(20))

#Peguei o id porque há duas tabelas, você também pode usar find('table')[1]
table = soup.find(id="capitaltotal")

df2 = pd.DataFrame(columns=['Acionista', 'Participação(%)'])

for row in table.tbody.find_all('tr'): # em html uma linha da tabela é representada pela tag <tr>
    # Obtendo todas as colunas em cada linha
    columns = row.find_all('td')  # em html uma coluna da tabela é representada pela tag <td>
    if(columns != []):
        data = columns[0].text.strip(' ')
        part = columns[1].text.strip(' ')
        df2 = pd.concat([df2, pd.DataFrame.from_records([{'Acionista': data, 'Participação(%)': part}])], ignore_index=True)

#Formatando números com porcentagem
df2['Participação(%)'] = [x.replace(',', '.') for x in df2['Participação(%)']]
df2['Participação(%)'] = [x.replace('%', ' ') for x in df2['Participação(%)']]
df2 = df2.astype({"Participação(%)": float})

print(' ')
print('                             Capital Total')
print(' ')
print(df2.head(20))

#Geramos dois arquivos para excel com as duas tabelas e seus dados 
df1.to_csv('Acoes_ordinarias.csv', index=False)
df2.to_csv('Capital_total.csv', index=False)

