import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

#Link do site investidor10: Criptomoedas mais negociadas
url = "https://investidor10.com.br/criptomoedas/"

#Isso é necessário para acessar o site e evitar o erro 403 Forbidden Request
headers = { 
    'User-Agent'      : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 
    'Accept'          : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
    'Accept-Language' : 'en-US,en;q=0.5',
    'DNT'             : '1',  
    'Connection'      : 'close'
}
data = requests.get(url, headers=headers).text
soup = BeautifulSoup(data,"html.parser")

#Pego as tags <table>
table = soup.find('table')

#Defino os nomes das colunas
df = pd.DataFrame(columns=['Nome', 'Cotação(dolar)', 'Cotação(reais)', 'Var.24H', 'Var.12M','Captalização'])

for row in table.tbody.find_all('tr'): # em html uma linha da tabela é representada pela tag <tr>
    # Obtendo todas as colunas em cada linha
    columns = row.find_all('td')  # em html uma coluna da tabela é representada pela tag <td>
    if(columns != []):
        data = columns[2].text.strip(' ')
        valor = columns[3].text.strip(' ')
        valor2 = columns[4].text.strip(' ')
        v24 = columns[5].text.strip(' ')
        v12 = columns[9].text.strip(' ')
        cap = columns[11].text.strip(' ')
        #No site tinha varias colunas com diferentes atributos
        #peguei apenas o que me interessava.


        df = pd.concat([df, pd.DataFrame.from_records([{'Nome': data,  'Cotação(dolar)': valor, 'Cotação(reais)': valor2, 'Var.24H': v24, 'Var.12M': v12,'Captalização': cap}])], ignore_index=True)

#Nome das criptomoedas
df['Nome'] = [x.replace('\n', ' ') for x in df['Nome']]

print(' ')
print('                                         CRIPTOMOEDAS MAIS NEGOCIADAS')
print(' ')
print(df.head(20))

#Gerando um arquivo para excel
df.to_csv('Criptomoedas.csv', index=False)

