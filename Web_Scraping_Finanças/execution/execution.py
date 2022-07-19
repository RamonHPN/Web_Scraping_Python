import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

#Link do site Fundamentus: Proventos do Banco Inter
url = "https://www.fundamentus.com.br/proventos.php?papel=BIDI4&tipo=2"

#Isso é necessário para acessar o site e evitar o erro 403 Forbidden Request
headers = { 
    'User-Agent'      : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 
    'Accept'          : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
    'Accept-Language' : 'en-US,en;q=0.5',
    'DNT'             : '1',  
    'Connection'      : 'close'
}
data = requests.get(url, headers=headers, timeout=5).text
soup = BeautifulSoup(data,"html.parser")

#Pego as tags <table>
table = soup.find('table')

#Defino os nomes das colunas
df = pd.DataFrame(columns=['Data', 'Valor', 'Tipo', 'Data de Pagamento', 'Por quantas ações'])

for row in table.tbody.find_all('tr'): # em html uma linha da tabela é representada pela tag <tr>
    # Obtendo todas as colunas em cada linha
    columns = row.find_all('td')  # em html uma coluna da tabela é representada pela tag <td>
    if(columns != []):
        data = columns[0].text.strip(' ')
        valor = columns[1].text.strip(' ')
        tipo = columns[2].text.strip(' ')
        data_pagamento = columns[3].text.strip(' ')
        quantidade_acoes = columns[4].text.strip(' ')
        df = pd.concat([df, pd.DataFrame.from_records([{'Data': data,  'Valor': valor, 'Tipo': tipo, 'Data de Pagamento': data_pagamento, 'Por quantas ações': quantidade_acoes}])], ignore_index=True)
        
#Formatando a data d/m/a
df['Data'] = pd.to_datetime(df['Data'], format="%d/%m/%Y", errors='ignore')

#Valor
df['Valor'] = [x.replace(',', '.') for x in df['Valor']]
df = df.astype({"Valor": float})

#Data de Pagamento
temp = pd.to_datetime(df["Data de Pagamento"], format="%d/%m/%Y", errors='coerce')
df["Data de Pagamento"] = df["Data de Pagamento"].where(temp.isna(), temp.dt.date)

#Tipo: Tudo maiusculo
df['Tipo'] = df['Tipo'].str.upper()

#Por quantas ações
df = df.astype({"Por quantas ações": int})

print('                             PROVENTOS')
print(' ')
print(df.head(20))

#Gerando um arquivo para excel
df.to_csv('Proventos_BIDI4.csv', index=False)

#Gráfico de proventos (É necessário fechar a janela desse gráfico para que outra janela seja aberta)
plt.plot(df['Data'], df['Valor']/df['Por quantas ações'], label='BIDI4')
plt.title("Proventos por cada ação de BIDI4")
plt.ylabel("Valor Recebido (R$)")
plt.xlabel("Ano")
plt.legend()
plt.show()

#Gráfico de proventos anuais (Esse só será mostrado quando o outro for fechado)
df_anual = df.set_index('Data')
dividendos = (df_anual['Valor']/df_anual['Por quantas ações']).resample('Y').sum()
plt.plot(dividendos.index.year[:-1], dividendos[:-1], label='BIDI4')
plt.title("Proventos anuais por cada ação de BIDI4")
plt.ylabel("Valor Recebido (R$)")
plt.xlabel("Ano")
plt.legend()
plt.show()