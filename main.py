# -*- coding: utf-8 -*-
import random
import os
import copy

from file_manager import load_from_text_file, save_as_text_file

supported_languages = ['pt', 'it']

def get_language():
	while True:
		print('What language would you like to learn?')
		language = str(raw_input('> '))

		# Check for full English names
		if language.lower() == 'portuguese':
			language = 'pt'
		elif language.lower() == 'italian' or language.lower() == 'italiano':
			language = 'it'

		if language not in supported_languages:
			print(language+' is not supported. Supported languages are '+', '.join(supported_languages))
			print('')
		else:
			print('')
			return language

def get_words_to_train(translate_dict):
	while True:
		print('How many words would you like to train on today?')
		num_words = str(raw_input('> '))
		if num_words == 'all' or num_words == '0':
			return translate_dict
		else:
			try:
				num_words = int(num_words)
				words = random.sample(translate_dict.keys(), num_words)

				chosen_words = {}
				for word in words:
					chosen_words[word] = translate_dict[word]
				print('')
				return chosen_words
			except ValueError as e:
				print('Enter "all" or a number, please')
				print('')
				continue

def get_master_count():
	while True:
		print('After how many times should a word be considered mastered?')
		master_count = str(raw_input('> '))
		try:
			master_count = int(master_count)
			print('')
			return master_count
		except ValueError as e:
			print('Enter a number, please')
			print('')
			continue

def get_repeat():
	while True:
		print('(y/n) Would you like to train on these words again?')
		run = str(raw_input('> '))
		if run.lower() not in ['n','no','y','yes']:
			print('Please enter y or n')
			print('')
			continue
		print('')
		if run.lower() == "n" or run.lower() == "no":
			return False
		return True

def get_continue():
	while True:
		print('(y/n) Would you like to train on a different set of words?')
		run = str(raw_input('> '))
		if run.lower() not in ['n','no','y','yes']:
			print('Please enter y or n')
			print('')
			continue
		print('')
		if run.lower() == "n" or run.lower() == "no":
			return False
		return True

def correct_word(word, meaning, language):
	translate_dict = load_from_text_file(language)
	translate_dict[word].insert(0, meaning)
	save_as_text_file(translate_dict, language)

def run_flash_cards(chosen_words_dict, master_count, language):
	chosen_words_dict = copy.deepcopy(chosen_words_dict)
	success_dict = {}
	last_word = None
	last_guess = None

	while True:
		word = random.choice(chosen_words_dict.keys())

		print('Enter guess for: '+word)
		guess = str(raw_input('> '))

		if guess.lower() == "exit()":
			return
		if guess.lower() == "reset()":
			# TODO: Something?
			continue
		if guess.lower() == "correct()":
			if last_word != None and last_guess != None:
				correct_word(last_word, last_guess, language)
				chosen_words_dict[last_word].insert(0, last_guess)
			continue

		correct = guess.lower() in chosen_words_dict[word]
		if word not in success_dict:
			success_dict[word] = {'right':0,'wrong':0}
		if correct:
			success_dict[word]['right'] += 1
		else:
			success_dict[word]['wrong'] += 1

		last_word = word
		last_guess = guess.lower()

		if correct:
			print("Correct! Correct words: "+", ".join(chosen_words_dict[word]))

			if success_dict[word]['right'] >= master_count:
				chosen_words_dict.pop(word, None)
				print(word+" is mastered")
				if len(chosen_words_dict) == 0:
					return
		else:
			print(guess+" is wrong, right words are: \n"+", ".join(chosen_words_dict[word]))
		print('')

if __name__=="__main__":
	print('')
	print('Translation powered by Yandex.Translate http://translate.yandex.com/')
	print('')

	language = get_language()

	# Make the language dictionary if it doesn't exist
	if not os.path.exists(os.path.join('.', 'languages', language+'.txt')):
		print('Constructing words to learn from, please wait')
		from language_creator import construct_language
		translate_dict = construct_language(language)
	else:
		translate_dict = load_from_text_file(language)

	while True:
		chosen_words = get_words_to_train(translate_dict)
		master_count = get_master_count()
		print(master_count)
		while True:
			run_flash_cards(chosen_words, master_count, language)
			repeat = get_repeat()
			if not repeat:
				break

		c = get_continue()
		if not c:
			break



