import scrapy, json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import unidecode


class MySpider(scrapy.Spider):
    name = 'my_spider'

    def __init__(self):
        self.start_urls = ["https://o.fortboyard.tv/gains.php"]
        self.option = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options= self.option)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, meta={'driver': self.driver})

    def parse(self, response):
        def isCinqDernieresAnnees(equipe_year):
            return int(re.search(r'\((\d{4})\)', equipe_year).group(1)) > 2018
        
        # Utilisez Selenium pour trouver l'élément image cliquable par XPath
        driver = response.meta['driver']
        driver.get(self.start_urls[0])
        clickable_image = driver.find_element(By.XPATH, '//*[@id="corps_index_gauche"]/div[2]/ul/li[2]/a/img')

        # Cliquez sur l'image
        clickable_image.click()

        # Attendre que la page se charge avec le nouveau contenu
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//table[@class="TableGains"]/tbody/tr/td[2]/a'))
        )

        # Une fois que la nouvelle page est chargée, récupérez le contenu
        table_data = driver.find_elements(By.XPATH, '//table[@class="TableGains"]/tbody/tr/td[2]/a')
        
        nom_equipes = [element.text for element in table_data if element.text != "" and isCinqDernieresAnnees(element.text)]

        lien_details_equipes = [element.get_attribute("href") for element in table_data if element.text != ""]
        
        for equipe, lien in zip(nom_equipes, lien_details_equipes):
            yield scrapy.Request(url=lien+"#Resume", callback=self.parse_subpage, meta={'equipe': equipe})
        
        # Fermez le navigateur Selenium
        driver.quit() 
    
    def parse_subpage(self, response):
        list_membres = response.xpath('//td[@style="text-align: center;"]/a/text()').extract()
        list_epreuves_keys = response.xpath(
				'//h2[@class="titrePartie" and text()="Quête des clés"]'
				+'/following-sibling::div'
				+'/div[@class="resumeBloc2 type_epreuves"]'
				+'/div[@class="nomEpreuve"]/a/text()'
				).extract()
        list_epreuves_jug = response.xpath(
                '//h2[@class="titrePartie" and text()="Salle du Jugement"]'
				+'/following-sibling::div'
				+'/div[@class="resumeBloc2 type_cage" or @class="resumeBloc2 type_jeux_blanche"]'
				+'/div[@class="nomEpreuve"]/a/text()'
				).extract()
        list_epreuves_indcs = response.xpath(
                '//h2[@class="titrePartie" and text()="Quête des indices"]'
				+'/following-sibling::div'
				+'/div[@class="resumeBloc2 type_aventures"]'
				+'/div[@class="nomEpreuve"]/a/text()'
				).extract()
        list_epreuves_conseil = response.xpath('//h2[@class="titrePartie" and text()="Salle du Conseil"]'
				+'/following-sibling::div'
				+'/div[@class="resumeBloc2 type_defis"]'
				+'/div[@class="nomEpreuve"]/a/text()'
				).extract()
        
        list_epreuves_success = response.xpath('//div[@class="statut"]/span/text()').extract()
        if response.xpath('//h2[@style="font-size: 2.8em;"]/text()'):
            Gain = response.xpath('//h2[@style="font-size: 2.8em;"]/text()').extract()[0] 
        else:
            li_elements = response.xpath('//div[@class="blocSDTGain2"]/ul/li/text()')
            Gain = "".join(li.extract() if li.extract() != "O" else "0" for li in li_elements)
        Temp = response.xpath('//div[@class="sdt_temps"]/text()').extract()

        list_membres = [str(unidecode.unidecode(membre)) for membre in list_membres]
        list_epreuves_keys = [str(unidecode.unidecode(epreuve)) for epreuve in list_epreuves_keys]
        list_epreuves_jug = [str(unidecode.unidecode(epreuve)) for epreuve in list_epreuves_jug]
        list_epreuves_indcs = [str(unidecode.unidecode(epreuve)) for epreuve in list_epreuves_indcs]
        list_epreuves_conseil = [str(unidecode.unidecode(epreuve)) for epreuve in list_epreuves_conseil]
        list_epreuves_success = [str(unidecode.unidecode(successfulness)) for successfulness in list_epreuves_success]
        Gain = Gain.replace(' \u20ac','').replace("\u0080","")

        yield {
            'Equipe' : str(unidecode.unidecode(response.meta['equipe'])),
            'Membres': list_membres,
            'Epreuves_part' : [ 
                {
                     
                    "Quete des cles" : list_epreuves_keys,
                    "Salle du jugement" : list_epreuves_jug,
                    "Quete des indices" : list_epreuves_indcs,
                    "Salle du conseil" : list_epreuves_conseil,
                    
                }                 
            ],
            'Reussites' : list_epreuves_success,            
            'Gain' : Gain,
            "Temps" : Temp

        }
