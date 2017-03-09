
import os
import json

def languages_path():
	return os.path.join('.', 'languages')

def file_path(language):
	return os.path.join(languages_path(), language+'.txt')

def load_from_text_file(language):
	path = file_path(language)
	if os.path.exists(path):
		with open(path, 'r') as f:
			return json.load(f)
	return None

def save_as_text_file(dictionary, language):
	if not os.path.exists(languages_path()):
		os.makedirs(languages_path())
	path = file_path(language)
	with open(path, 'w+') as f:
		return json.dump(dictionary, f)