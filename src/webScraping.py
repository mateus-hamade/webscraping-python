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

    # Inicia o driver
    driver = getDriver(url)

    # Recebe o número do curso desejado
    course = getCourse(driver)

    # Recebe o conteúdo da tabela de resultados em formato HTML
    htmlContent = getHtmlContent(driver, course)

    # Processa o conteúdo da tabela
    listaEspera, df = dataProcessing(htmlContent)

    # Cria os arquivos
    createFiles(listaEspera, df)

    # Fecha o navegador
    driver.quit()

def getDriver(url):
    option = Options()
    option.add_argument("--headless")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)

    driver.get(url)

    return driver

def getCourse(driver):
    count = 1
    
    # Busca todos os cursos disponíveis
    cursos = driver.find_element(by=By.XPATH, value='/html/body/table[1]/tbody')
    
    # imprime os cursos disponíveis
    print('Cursos disponíveis:')
    for i in cursos.find_elements(by=By.TAG_NAME, value='tr'):
        print(f'{count}. ' + i.text)
        count += 1
    
    # Recebe do usuário o curso desejado
    course = int(input('\nDigite o número do curso desejado: '))

    return course

def getHtmlContent(driver, course):
    # Simula o click de um usuário no link solicitado
    driver.find_element(by=By.XPATH, value=f"/html/body/table[1]/tbody/tr[{course}]/td/font/font/a").click()

    # Recebe o elemento da página que contém a tabela de resultados
    element = driver.find_element(by=By.CLASS_NAME, value="body")

    # Recebe o conteúdo da tabela de resultados em formato HTML
    htmlContent = element.get_attribute('outerHTML')

    return htmlContent

def dataProcessing(htmlContent):
    
    # Divide o conteúdo em linhas
    soup = bs(htmlContent, 'html.parser')
    # Recebe apenas as linhas da tabela
    table = soup.find('tbody')

    # Cria um dataframe vazio com as colunas especificadas 
    df = pd.DataFrame(columns=['Nome', 'Escola Publica', 'AC', 'L1', 'L2', 'L5', 'L6', 'L9', 'L10', 'L13', 'L14', 'Classificacao Geral', 'Nota'])

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

    return listaEspera, df

def createFiles(listaEspera, df):
    # Salva o dict em um arquivo JSON
    js = json.dumps(listaEspera)
    
    # Abre o arquivo JSON para escrita
    FileJson = open('./data/data.json', 'w')
    # Escreve o conteúdo do dict no arquivo JSON
    FileJson.write(js)
    # Fecha o arquivo JSON
    FileJson.close()

    # json to csv
    df.to_csv('./data/data.csv', index=False)
    df.to_excel('./data/data.xlsx', index=False)
    
main()