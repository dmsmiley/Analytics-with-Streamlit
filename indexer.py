import PyPDF2

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
cachedSW = set(stopwords.words('english'))

import re

from spellchecker import SpellChecker
spell = SpellChecker()

from collections import defaultdict

import pandas as pd

import spacy
nlp = spacy.load('en_core_web_sm')

import streamlit as st

d = defaultdict(list)

def append_value(dict_obj, key, value):
    # Check if key exist in dict or not
    if key in dict_obj:
        # Key exist in dict.
        # Check if type of value of key is list or not
        if not isinstance(dict_obj[key], list):
            # If type is not list then make it list
            dict_obj[key] = [dict_obj[key]]
        # Append the value in list
        dict_obj[key].append(value)
    else:
        # As key is not in dict,
        # so, add key-value pair
        dict_obj[key] = value

def open_text(pdf_file):
  pdf = open(pdf_file, 'rb')
  pdf_reader = PyPDF2.PdfFileReader(pdf)
  return pdf_reader


def clean_text_list(reader_file, pdf_page=1):

  page = reader_file.getPage(pdf_page)
    
  text = page.extractText().replace('\n','')
  
  text_main = re.split(r"[0-9]\.", text, 1)[0]

  text_main = re.sub(r'[0-9]', '', text_main)
  text_main = re.sub(r'([^\s\w]|_)+', '', text_main)
  text_main = text_main.lower()

  text_main = text_main.split()

  cleaned_text = []

  for x in text_main:
    if x not in cachedSW:
      cleaned_text.append(x)

  corrected_text = [spell.correction(word) for word in cleaned_text]

  corrected_text = set(corrected_text)
  return corrected_text

def loop_all_pages(pdf, dictionary, pdf_page=1, book_page=1, pdf_end=1):
  pdf_reader = open(pdf, 'rb')
  pdf_reader = PyPDF2.PdfFileReader(pdf)
  pdf_count = pdf_page
  book_count = book_page

  for x in pdf_reader.getPage(pdf_count):
    if pdf_count == pdf_end:
      break
    else:
      corrected_text = clean_text_list(pdf_reader, pdf_page=pdf_count)
      page_difference = pdf_count - book_count
      new_value = pdf_count - page_difference
      for word in corrected_text:
        append_value(dictionary, word, new_value)
      pdf_count += 1
      book_count += 1

def all_word_entity(pdf, pdf_page=1, book_page=1, pdf_end=1):
  pdf_count = pdf_page
  book_count = book_page
  entities = []

  for x in pdf.getPage(pdf_count):
    if pdf_count == pdf_end:
      break
    else:
      page = pdf.getPage(pdf_count)
      text = page.extractText().replace('\n','')
      text_main = re.split(r"[0-9]\.", text, 1)[0]
      text_main = re.sub(r'[0-9]', '', text_main)
      text_main = re.sub(r'([^\s\w]|_)+', '', text_main)
      text_main = text_main.lower()
      doc = nlp(text_main)
      new_words = [chunk.text for chunk in doc.noun_chunks]
      entities.extend(new_words)
      pdf_count += 1
      book_count += 1
  entities = [ele.replace("the ", '') for ele in entities]
  return entities

uploaded_file = st.file_uploader('Choose your .pdf file', type='pdf')

if uploaded_file is not None:
	bytes_data = uploaded_file.getvalue()
	st.write(bytes_data)

#pdf = open_text(uploaded_file)

starting_pdf_page = st.sidebar.number_input('PDF Page', step=1)

displayed_book_page = st.sidebar.number_input('Starting Displayed Page', step=1)

ending_pdf_page = st.sidebar.number_input('Ending PDF Page', step=1)

loop_all_pages(uploaded_file, d, starting_pdf_page, displayed_book_page, ending_pdf_page)

df = pd.DataFrame([(k, v) for k, v in d.items()], 
                   columns=['word', 'pages'])

all_word_entity(pdf, starting_pdf_page, displayed_book_page, ending_pdf_page)

df2 = pd.DataFrame(all_word_entity(pdf, 21, 3, 45), columns=['word'])
df2 = df2.drop_duplicates()

inner_join_df = pd.merge(df, df2, on='word', how='inner')

st.dataframe(df)