# language-learning
A python command line interface program to help English speakers learn words in other languages.

## Running

Run `python main.py` to run the program.

## Constructing languages

To construct new languages, add the relevant functions to `word_crawler.py`, add the language to `supported_languages` at the top of `main.py`.

For this, you will need an API key from [Yandex](https://tech.yandex.com/translate/). Then create an `api_key.py` file that just contains the line:

```
api_key = '*your_api_key_here*'
```

