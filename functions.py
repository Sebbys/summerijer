import nltk
import re
import math
import nltk
import streamlit 
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import defaultdict
nltk.download('vader_lexicon')
nltk.download('punkt')


# Fungsi untuk Menghapus Dialog pada Novel yang pada umumnya di
def diagRemove(file):
  text = open(file,'r').read()
  text = re.sub(r'“[^”]+”', '', text)
  text = text.replace("\n", " ")
  with open("novel_noDiag.txt", "w") as f:
    f.write(text)

def calc_tf(word_list):
    tf = defaultdict(int)
    for word in word_list:
        tf[word] += 1
    return tf

def calc_idf(documents):
    N = len(documents)
    idf = defaultdict(int)
    word_count = defaultdict(int)
    for document in documents:
        for word in set(document):
            word_count[word] += 1
    for word, count in word_count.items():
        idf[word] = math.log(N / count)
    return idf

def calc_tf_idf(tf, idf):
    tf_idf = defaultdict(int)
    for word, freq in tf.items():
        tf_idf[word] = freq * idf[word]
    return tf_idf

def calc_sentence_tfidf(sentence, tf_idf):
    words = word_tokenize(sentence)
    tfidf_sum = sum(tf_idf[word] for word in words if word in tf_idf)
    return tfidf_sum

def summarijer(text, n):
  text = re.sub(r'“[^”]+”', '', text)
  text = text.replace("\n", " ")
  sentences = sent_tokenize(text)
  word_lists = [word_tokenize(sentence) for sentence in sentences]
  tfs = [calc_tf(word_list) for word_list in word_lists]
  idf = calc_idf(word_lists)
  tf_idfs = [calc_tf_idf(tf, idf) for tf in tfs]
  sentence_tfidf = {sentence: calc_sentence_tfidf(sentence, tf_idf) for sentence, tf_idf in zip(sentences, tf_idfs)}
  sorted_sentences = sorted(sentence_tfidf.items(), key=lambda x: x[1], reverse=True)

  top_sentences = [sentence for sentence, tfidf in sorted_sentences[:n]]

  # Menggabungkan Kalimat yang termasuk ke dalam jumlah top_sentences
  summary = " ".join(top_sentences)
  summary = summary.replace("\n", " ")

  return summary


