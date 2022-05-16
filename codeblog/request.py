from codeblog import app
import urllib.request,json
from .quote import Quotes


#getting random quotes
base_url = 'http://quotes.stormconsultancy.co.uk/random.json'

def get_quotes():
    '''
    Function that gets the random quotes json
    '''
    get_quotes_url = base_url
    
    with urllib.request.urlopen(get_quotes_url) as url:
        get_quotes_data = url.read()
        get_quotes_response = json.loads(get_quotes_data)
        
        quotes_results = None
        
        if get_quotes_response['']:
            quotes_results_list = get_quotes_response['']
            
            quotes_results = process_results(quotes_results_list)
            
    return quotes_results

def process_results(quotes_list):
    '''
    Function that processes the quotes results and transfrms them into an object
    '''
    quotes_results = []
    for quotes_item in quotes_list:
        author = quotes_item.get('author')
        quote = quotes_item.get('quote')
        
        quotes_object = Quotes(author, quote)
        
        quotes_results.append(quotes_object)
    return quotes_results