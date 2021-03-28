import nltk

nltk.download("stopwords")
# --------#

from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation

# Create lemmatizer and stopwords list
mystem = Mystem()
russian_stopwords = stopwords.words("russian")


# Preprocess function
def preprocess_list(text):
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in russian_stopwords
              and token != " "
              and token.strip() not in punctuation]
    return tokens


def preprocess_text(text):
    text = " ".join(preprocess_list(text))
    return text


def preprocess_set(text):
    return set(preprocess_list(text))


def allWordsInCommand(command: str, lexems: list):
    return len(preprocess_set(command) & set(lexems)) == len(lexems)
