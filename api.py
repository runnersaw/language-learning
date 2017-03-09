
from api_key import api_key
import requests

def translate_word(text, language):
	url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key='+api_key+'&text='+text+'&lang='+language+'-en'
	r = requests.get(url)
	words = r.json()['text']
	return words

if __name__=="__main__":
	print(translate('parlare', 'it'))

