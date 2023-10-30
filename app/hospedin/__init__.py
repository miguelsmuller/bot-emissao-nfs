import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class Hospedin():
    def __init__(self, destination_folder, periodo):
        self.destination_folder = destination_folder
        self.periodo = periodo

        options = Options()
        options.add_experimental_option("prefs", {
            "download.default_directory": destination_folder
        })
        # options.add_argument('--headless')

        self.driver = webdriver.Chrome(options=options)

        os.makedirs(destination_folder, exist_ok=True)

    def find_element(self, element):
        element = self.driver.find_element(by=By.XPATH, value=element)
        return element

    def run(self):
        self.driver.get("https://pms.hospedin.com/login")

        # Login no PMS
        self.find_element('//*[@id="user_email"]').send_keys("")
        self.find_element('//*[@id="user_password"]').send_keys("")
        self.find_element('//*[@id="new_user"]/button').click()

        # Direciona para o relatório de hospedagem
        self.find_element('//*[@id="navbar-mobile"]/ul[2]/li/a').click()
        time.sleep(1)
        self.find_element('//*[@id="navbar-mobile"]/ul[2]/li/div/a[4]').click()
        time.sleep(1)
        self.find_element('/html/body/div[2]/div/div[2]/div/div[2]/div/div/a').click()
        time.sleep(3)

        # Define as colunas de exibição
        self.find_element('/html/body/div[2]/div/div[2]/div/div/div[2]/div/div/div[1]/a[2]').click()
        time.sleep(1)
        self.find_element('//*[@id="collapseColumns"]/form/div[1]/div/div/div/div[4]/div').click()
        time.sleep(1)
        self.find_element('//*[@id="collapseColumns"]/form/div[1]/div/div/div/div[14]/div').click()
        time.sleep(1)
        self.find_element('//*[@id="collapseColumns"]/form/div[2]/div[2]/button').click()
        time.sleep(3)

        # Define as opções de filtro
        self.find_element('/html/body/div[2]/div/div[2]/div/div/div[2]/div/div/div[1]/a[1]').click()
        time.sleep(1)
        self.find_element('//*[@id="created_at"]')\
            .clear()
        self.find_element('//*[@id="created_at"]')\
            .send_keys(self.periodo)
        time.sleep(1)
        self.find_element('//*[@id="form-filter"]/div[4]/fieldset[2]/button').click()
        time.sleep(3)

        # Copia o conteúdo da tabela
        table_element = self.find_element('/html/body/div[2]/div/div[2]/div/div/div[2]/div/div/div[4]/table')
        table_html = table_element.get_attribute("outerHTML")
        table_html = table_html if table_html is not None else ""

        with open(f"{self.destination_folder}/hospedagens.txt", "w", encoding="utf-8") as arquivo:
            arquivo.write(table_html)

        # Download dos hóspedes
        toogle = self.find_element('//*[@id="navbar-mobile"]/ul[1]/li[1]/a')

        if "is-active" not in toogle.get_attribute("class"):  # type: ignore
            toogle.click()

        self.find_element('//*[@id="main-menu-navigation"]/li[6]/a').click()
        self.find_element('//*[@id="list"]/div/div/div/div[1]/div/ul/li[2]/a').click()
        time.sleep(10)
