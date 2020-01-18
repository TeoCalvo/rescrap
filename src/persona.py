import requests
from bs4 import BeautifulSoup
from utils import get_value_mark

class Persona:
    def __init__(self, name, url ):
        self.name = name
        self.url = url
        self.response = requests.get( self.url )
        self.bs_obj = BeautifulSoup(self.response.text, 'lxml')

    def get_basic_info( self ):
        
        resultado = self.bs_obj.find( 'div', class_='td-page-content' ).find('p').findAll( 'em' )
        data = { e.text.split(":")[0].strip(" "): e.text.split(":")[1].strip(" ") for e in resultado }
        
        if len( data ) != 4:
            resultado = self.bs_obj.find( 'div', class_='td-page-content' ).find('p').text.split("\n")
            data = { e.split(":")[0].strip(" "): e.split(":")[1].strip(" ") for e in resultado if len(e.split(":") ) == 2}
        
        return data

    def get_aparitions( self ):
        data = {}
        try:
            resultado = get_value_mark(self.bs_obj, 'h4', 'em títulos da série:')[0]
        except IndexError:
            resultado = get_value_mark(self.bs_obj, 'strong', 'em títulos da série:')[0]
                                                
        resultado = resultado.find_next().findAll('a')
        data['Aparicoes'] = [ i.text for i in resultado ]
            
        return data

    def get_biography( self ):
        try:
            resultado = get_value_mark(self.bs_obj, 'h4', 'Biografia e Participação')[0]
        except IndexError:
            resultado = get_value_mark( self.bs_obj, 'strong', 'Biografia e Participação' )[0]
        
        p = resultado.find_next() 

        try:
            data = {'Biografia':''}
            while p.name == 'p':
                data['Biografia'] += p.text
                p = p.find_next_sibling()

        except AttributeError as err:
            pass

        return data

    def get_data(self):
        self.data = self.get_basic_info()
        self.data.update( self.get_aparitions() )
        self.data.update( self.get_biography() )