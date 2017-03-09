# -*- coding: utf-8 -*-
import goslate
import urllib2
import csv
import random
import nltk
from nltk.corpus import wordnet as wn
import json
import sys
import copy

def load_from_text_file(language):
	global d
	try:
		d = json.load(open("user_data/"+language+".txt"))
		print("Loaded old user data")
	except:
		d = json.load(open("languages/"+language+".txt"))
		print("Loaded original data")

def save_as_text_file(language):
	json.dump(d, open("user_data/"+language+".txt", "w"))

def reset_dictionary():
	count = 0
	for i in d:
		d[i]["right"] = 0
		d[i]["wrong"] = 0

def set_dictionary():
	count = 0
	for i in d:
		d[i]["right"] = 0
		d[i]["wrong"] = 0
		t = clean_string(g.translate(i, "en", "pt"))
		d[i]["words"] = [t]
		l = get_synonyms(t.split(" ")[0], d[i]["type"])
		for j in l:
			d[i]["words"].append(j.lower())
		count += 1
		print count

def get_synonyms(s, t):
	l = []
	for i,j in enumerate(wn.synsets(s)):
		for syn in j.lemma_names():
			if syn not in l:
				l.append(syn)
	return l

def clean_string(s):
	x = s.replace("<li>","")
	x = x.replace("</li>","")
	x = x.replace("[","")
	x = x.replace("]","")
	x = x.replace("</","")
	x = x.replace("so ","")
	x = x.replace("to ","")
	x = x.replace("o ","")
	x = x.replace("a ","")
	x = x.replace("to ","")
	x = x.replace("the ","")
	x = x.replace("<strong>astrong> ","")
	x = x.replace("<strong>ostrong> ","")

	x = x.strip()
	x = x.lower()
	if type(x)!=unicode:
		x = unicode(x, "utf8")
	return x

def fill_list_of_words(language):
	l = {}
	if language=="pt":
		url = "http://hackingportuguese.com/sample-page/the-1000-most-common-verbs-in-portuguese/"
		response = urllib2.urlopen(url)
		html = response.read()
		l2 = html.split('ol>')
		x = clean_string(l2[1])
		x = x.split("\n")
		for i in x:
			if i != "":
				l[i] = "v"
		url = "http://hackingportuguese.com/sample-page/the-1000-most-common-nouns-in-portuguese/"
		response = urllib2.urlopen(url)
		html = response.read()
		l2 = html.split('ol>')
		x = clean_string(l2[1])
		x = x.split("\n")
		for i in x:
			if i != "":
				l[i] = "n"
		return l
	else:
		return

def init_dictionary(l):
	global d
	for i in l:
		d[i] = {"type":l[i]}

def construct_dictionary(language):
	print("filling list of words")
	l = fill_list_of_words(language)
	print("list filled, initing dictionary")
	init_dictionary(l)
	print("dictionary allocated, setting all results")
	set_dictionary()
	print("dictionary set, saving to text file")
	save_as_text_file(language)

def word_choice_and_run_again():
	global right
	global wrong
	global chosen_words
	running = True
	while running:
		word = random.choice(chosen_words)

		guess = clean_string(str(raw_input(word.encode(encoding, 'replace')+": ")))

		print("\n")

		if guess.lower() == "exit()":
			sys.exit()
		if guess.lower() == "reset()":
			reset_dictionary()
			continue

		if guess.lower() in d[word]["words"]:
			right+=1
			print(guess+ " is correct\n")
			print("correct words: "+", ".join(d[word]["words"])+"\n")
			d[word]["right"]+=1
			if d[word]["right"] >= 1: #could change
				chosen_words.remove(word)
				print(word.encode(encoding, 'replace')+" is mastered\n")
				if len(chosen_words) == 0:
					break
		else:
			wrong+=1
			print(guess+" is wrong, right words are: \n"+", ".join(d[word]["words"])+"\n")
			d[word]["wrong"]+=1

		save_as_text_file(language)

if __name__ == "__main__":
	supported_languages = ["pt"]

	g = goslate.Goslate()
	wrong = 0
	right = 0

	d = {}

	language = str(raw_input("What language would you like to learn?\n\n"))

	if language.lower() == "portuguese":
		language = "pt"

	if language not in supported_languages:
		print("Language isn't supported yet")
		sys.exit()

	encoding = "437"
	if language=="pt":
		encoding = "860"

	#construct_dictionary(language)

	load_from_text_file(language)

	running = True
	while running:
		words = input("How many words would you like to train on today?\n\n")
		if words == "all":
			chosen_words = d.keys()
			running = False
		else:
			try:
				words = int(words)
				chosen_words = []
				for i in range(words):
					chosen_words.append(random.choice(d.keys()))
				running = False
			except:
				print("Enter 'all' or a number, please\n\n")
				continue

	orig_list = copy.deepcopy(chosen_words)

	running = True
	while running:
		word_choice_and_run_again()
		valid = False
		while not valid:
			run = str(raw_input("(y/n) Would you like to train on these words again?\n\n"))
			if run.lower() not in ["n", "no", "y", "yes"]:
				print("Please enter y or n")
				continue
			else:
				valid = True
		if run.lower() == "n" or run.lower() == "no":
			break
		chosen_words = copy.deepcopy(orig_list)

	print("%d right, %d wrong, well done!" %(right, wrong))
