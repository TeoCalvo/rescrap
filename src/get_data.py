from bs4 import BeautifulSoup
import requests
from tqdm import tqdm

def get_value_mark(bs_obj, mark, value, *args ):
    values = [value] + list(args)
    result = [ i for i in bs_obj.findAll( mark ) if i.text in values ]
    return result

def get_personas_list( url='http://www.residentevildatabase.com/personagens/' ):

    def names_from_section(section):
        return { i.text: { 'url': i['href']} for i in section.find_next().findAll( 'a' ) }

    response = requests.get(url)
    bs_obj = BeautifulSoup( response.text, 'lxml' )
    secoes = bs_obj.find_all("h3", style='padding-left: 30px;')
    data = {}
    for i in secoes:
        data.update( names_from_section(i) )

    return data

class Persona:
    def __init__(self, url):
        self.url = url

    def get_basic_info( self ):
        resultado = self.bs_obj.find( 'div', class_='td-page-content' ).find('p').findAll( 'em' )
        data = { e.text.split(":")[0].strip(" "): e.text.split(":")[1].strip(" ") for e in resultado }
        return data

    def get_aparitions( self ):
        data = {}        
        try:
            resultado = get_value_mark(self.bs_obj, 'h4', 
                                                'Aparições em títulos da série:',
                                                'Aparições (Menções) em títulos da série:')[0].find_next().findAll('a')
            data['Aparicoes'] = [ i.text for i in resultado ]
        except IndexError:
            pass
        return data

    def get_biography( self ):

        data = { 'Biografia': '' }
        key_values = ['Biografia e Participação na Série*:']
        try:
            resultado = get_value_mark(self.bs_obj, 'h4', 'Biografia e Participação na Série:', *key_values)[0]
        except IndexError:
            return data
        p = resultado.find_next() 
        try:
            while p.name == 'p':
                data['Biografia'] += p.text
                p = p.find_next_sibling()
        except AttributeError:
            pass        
        return data

    def get_data(self):
        self.response = requests.get( self.url )
        self.bs_obj = BeautifulSoup(self.response.text, 'lxml')
        self.data = self.get_basic_info()
        self.data.update( self.get_aparitions() )
        self.data.update( self.get_biography() )

all_persons = get_personas_list()

for i in tqdm(all_persons):
    print( i )
    person = Persona( all_persons[i]['url'] )
    person.get_data()
    print(person.response)
    all_persons[i].update( person.data )