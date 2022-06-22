from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
from bs4 import BeautifulSoup as bs

import json

def main():
    # Recebe o url da página
    url = ('https://vestibular.ufop.br/resultvest/2022_1/ListaEspera/2022-1ListaEspera.html') 

    # Input do curso desejado
    inputUser = int(input('Digite a posicao do curso: '))

    # Disabilita o browser preview
    option = Options()
    option.handles = False

    # Cria uma instância do navegador (Google Chrome)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)

    # Recebe o url da página 
    driver.get(url)

    # Simula o click de um usuário no link solicitado
    driver.find_element(by=By.XPATH, value=f"/html/body/table[1]/tbody/tr[{inputUser}]/td/font/font/a").click()

    # Recebe o elemento da página que contém a tabela de resultados
    element = driver.find_element(by=By.CLASS_NAME, value="body")

    # Recebe o conteúdo da tabela de resultados em formato HTML
    html_content = element.get_attribute('outerHTML')

    # Divide o conteúdo em linhas
    soup = bs(html_content, 'html.parser')
    # Recebe apenas as linhas da tabela
    table = soup.find('tbody')

    # Cria um dataframe vazio com as colunas especificadas 
    df = pd.DataFrame(columns=['Nome', 'Inscrito Cota Escola Publica', 'AC', 'L1', 'L2', 'L5', 'L6', 'L9', 'L10', 'L13', 'L14', 'Classificacao Geral', 'Nota'])

    # Percorre todas as linhas da tabela
    for i in range(len(table.find_all('tr'))):
        row = table.find_all('tr')[i]
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        df.loc[i] = cols

    # Organiza o dataframe
    df.sort_values(by=['Nota'], inplace=True, ascending=False)

    # Transforma o dataframe em um dict 
    listaEspera = {}
    listaEspera['ListaEspera'] = df.to_dict('records')

    # Fecha o navegador
    driver.quit()
    
    # Salva o dict em um arquivo JSON
    js = json.dumps(listaEspera)
    
    # Abre o arquivo JSON para escrita
    FileJson = open('../data/data.json', 'w')
    # Escreve o conteúdo do dict no arquivo JSON
    FileJson.write(js)
    # Fecha o arquivo JSON
    FileJson.close()

    # json to csv
    df.to_csv('../data/data.csv', index=False)
    df.to_excel('../data/data.xlsx', index=False)

main()