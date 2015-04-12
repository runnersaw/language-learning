# -*- coding: utf-8 -*-
import goslate
import urllib2
import csv
import random
import nltk
from nltk.corpus import wordnet as wn
import json
import sys

def load_from_text_file(language):
	global d
	d = json.load(open(language+".txt"))

def save_as_text_file(language):
	json.dump(d, open(language+".txt", "w"))

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
		t = g.translate(i, "en", "pt")
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
	x = x.replace("<strong>astrong> ","")
	x = x.replace("<strong>ostrong> ","")
	x = x.replace("</","")
	x = x.replace("so ","")
	x = x.replace("to ","")
	x = x.replace("o ","")
	x = x.replace("a ","")
	x = x.replace("to ","")
	x = x.replace("the ","")

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
	if language not in supported_languages:
		print("Language isn't supported yet")
		sys.exit()
	print("filling list of words")
	l = fill_list_of_words(language)
	print("list filled, initing dictionary")
	init_dictionary(l)
	print("dictionary allocated, setting all results")
	set_dictionary()
	print("dictionary set, saving to text file")
	save_as_text_file(language)

def word_choice_and_run_again():
	running = True
	while running:
		word = random.choice(d.keys())

		guess = clean_string(str(raw_input(word.encode(encoding, 'replace')+": ")))

		print("\n")

		if guess.lower() == "exit":
			break
		if guess.lower() == "reset":
			reset_dictionary()
			continue

		if guess.lower() in d[word]["words"]:
			print(guess+ " is correct\n")
			print("correct words: "+", ".join(d[word]["words"])+"\n")
			d[word]["right"]+=1
			if d[word]["right"] == 5: #could change
				l.remove(word)
				print(word+" is mastered")
		else:
			print(guess+" is wrong, right words are: \n"+", ".join(d[word]["words"])+"\n")
			d[word]["wrong"]+=1

		save_as_text_file(language)

if __name__ == "__main__":
	supported_languages = ["pt"]

	g = goslate.Goslate()
	encoding = "437"
	language = "pt"

	d = {}
	#construct_dictionary(language)

	load_from_text_file(language)

	word_choice_and_run_again()
