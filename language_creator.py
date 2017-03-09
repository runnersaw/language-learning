
from word_crawler import get_words
from translate import translate
from synonyms import construct_synonyms
from file_manager import save_as_text_file

def construct_language(language):
	print('Getting words')
	foreign_words = get_words(language)
	print('Translating words')
	translate_dict = translate(foreign_words, language)
	print('Getting English synonyms')
	full_dict = construct_synonyms(translate_dict)
	print('Saving language')
	save_as_text_file(full_dict, language)
	return full_dict