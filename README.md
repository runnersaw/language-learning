# language-learning

A Python command line interface program to help English speakers learn words in other languages.

## Running

Run `python main.py` to run the program.

Typical output looks like:

```
What language would you like to learn?
> it

How many words would you like to train on today?
> 3

Enter guess for: andare
> go
Correct! Correct words: go, spell, tour, turn
```

When entering guesses, you can also enter two other functions:

- `exit()`. If you enter `exit()`, the program will exit the current set of translations.
- `correct()`. If you enter `correct()`, the program will add the last guess as a translation of the last word. This is useful if, for example, you know that the definition of 'potere' is 'can', but the program didn't have that as a definition. If you guess 'can', and it tells you it is wrong, you can enter `correct()` in order to add 'can' as a translation of 'potere'.

## Constructing languages

To construct new languages, add the relevant functions to grab a list of common foreign words to `word_crawler.py`, add the language to `supported_languages` at the top of `main.py`.

For this, you will need an API key from [Yandex](https://tech.yandex.com/translate/). Then create an `api_key.py` file that just contains the line:

```
api_key = '*your_api_key_here*'
```

