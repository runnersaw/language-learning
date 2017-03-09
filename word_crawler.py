
from lxml import html
import requests

def get_portuguese_words():
	out = []

	url = "http://hackingportuguese.com/sample-page/the-1000-most-common-verbs-in-portuguese/"
	page = requests.get(url)
	tree = html.fromstring(page.content)
	words = tree.xpath('//div[@class="entry-content"]/ol')[0].getchildren()
	for word in words:
		out.append(word.text.encode('utf-8').strip('[').strip(']'))

	url = "http://hackingportuguese.com/sample-page/the-1000-most-common-nouns-in-portuguese/"
	page = requests.get(url)
	tree = html.fromstring(page.content)
	words = tree.xpath('//div[@class="entry-content"]/ol')[0].getchildren()
	for word in words:
		out.append(word.text.encode('utf-8').strip('[').strip(']'))

	return out

def get_italian_words():
	out = []

	words_per_page = 50
	desired_words = 1000

	for i in range(desired_words / words_per_page):
		url = "http://www.italian-verbs.com/italian-verbs/italian-verbs-top.php?pg="+str(i)
		page = requests.get(url)
		tree = html.fromstring(page.content)
		words = tree.xpath('//tbody[@id="zebra"]/tr/td/a')
		for word in words:
			out.append(word.text.encode('utf-8'))

	url = "http://1000mostcommonwords.com/1000-most-common-italian-words/"
	page = requests.get(url)
	tree = html.fromstring(page.content)
	elements = tree.xpath('//div[@class="entry-content"]/table/tbody/tr')
	for element in elements:
		child = element.getchildren()[1]
		if child.text == None:
			continue
		text = child.text.encode('utf-8')
		if text not in out:
			out.append(text)


	url = "https://en.wiktionary.org/wiki/User:Matthias_Buchmeier/Italian_frequency_list-1-5000"
	page = requests.get(url)
	tree = html.fromstring(page.content)
	words = tree.xpath('//div[@id="mw-content-text"]/p/a')
	for word in words:
		text = word.text.encode('utf-8')
		if text not in out:
			out.append(text)

	return out

def get_words(language):
	if language == 'it':
		return get_italian_words()
	elif language == 'pt':
		return get_portuguese_words()
	else:
		return []

if __name__=="__main__":
	print(len(get_portuguese_words()))
	print(len(get_italian_words()))

