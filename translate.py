
from api import translate_word
from word_crawler import *

def translate(words, language):
	out = {}
	count = 0
	num_words = len(words)

	for word in words:
		translation = translate_word(word, language)
		out[word] = translation
		count += 1

		if num_words > 100 and count % (num_words / 100) == 0:
			print(str(count * 100 / num_words) + '% done, completed '+str(count)+'words')

	return out

if __name__=="__main__":
	translate(get_italian_words(), 'it')