from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    search_query = request.form.get('search_query')

    # Inicializar o driver do navegador
    driver = webdriver.Chrome()

    # Acessar o site
    driver.get("https://search.odin.io/")

    # Aguardar o campo de pesquisa ficar visível
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'searchInput'))
    )

    # Encontrar o campo de pesquisa e digitar o que o usuário deseja
    search_input = driver.find_element(By.ID, 'searchInput')
    search_input.send_keys(search_query)

    # Enviar a pesquisa pressionando Enter
    search_input.send_keys(Keys.ENTER)

    # Aguardar o site carregar os resultados
    time.sleep(5)

    # Capturar o conteúdo da página
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # Extrair os dados dos artigos
    articles = soup.find_all("article", class_="bg-primary-card")
    data = []

    for article in articles:
        ip = article.find("span", class_="font-mono").text.strip() if article.find("span", class_="font-mono") else None
        provider = article.find("div", class_="text-gray-700").text.strip() if article.find("div", class_="text-gray-700") else None
        asn = article.find("div", class_="font-medium").text.strip() if article.find("div", class_="font-medium") else None
        location = article.find("div", title="Location").text.strip() if article.find("div", title="Location") else None
        last_updated = article.find("div", title="Last Updated At").text.strip() if article.find("div", title="Last Updated At") else None
        services = [s.text.strip() for s in article.find_all("div", class_="font-mono")]

        data.append({
            "IP": ip,
            "Provider": provider,
            "ASN": asn,
            "Location": location,
            "Last Updated": last_updated,
            "Services": services,
        })

    driver.quit()

    # Retornar os dados como JSON
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
