from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
from persona import Persona

class Scrapper:

    def __init__(self, url='http://www.residentevildatabase.com/personagens/'):
        self.url = url

    def get_personas_list( self ):

        def names_from_section(section):
            return { i.text: { 'url': i['href'] , 'nome':i.text} for i in section.find_next().findAll( 'a' ) }

        response = requests.get(self.url)
        bs_obj = BeautifulSoup( response.text, 'lxml' )
        secoes = bs_obj.find_all("h3", style='padding-left: 30px;')
        data = {}
        for i in secoes:
            data.update( names_from_section(i) )

        self.data = data

    def get_all_personas_data(self):
        for i in tqdm(self.data):
            person = Persona( self.data[i]['nome'], self.data[i]['url'] )
            person.get_data()
            self.data[i].update( person.data )

scrap = Scrapper()
scrap.get_personas_list()
scrap.get_all_personas_data()
print(scrap.data)