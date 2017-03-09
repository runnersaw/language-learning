
import nltk
from nltk.corpus import wordnet as wn

nltk.data.path.append('./nltk_data/')

def construct_synonyms(translate_dict):
	max_synonyms = 4
	out = {}
	for (word,translations) in translate_dict.iteritems():
		all_translations = []
		for translation in translations:
			all_translations.append(translation)
			for i,j in enumerate(wn.synsets(translation)):
				if i == max_synonyms:
					break
				for syn in j.lemma_names():
					if syn not in all_translations:
						all_translations.append(syn.lower())
			out[word] = all_translations
	return out