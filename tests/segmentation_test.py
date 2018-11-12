import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from helper_methods import dictionary_methods as dictionary_methods
from helper_methods import segmenting_methods as segmenting_methods
import models
import re


def test_sentence_segmentation():
  word_dictionary = dictionary_methods.createDictionary("../data/dic-ce.txt")
  corpus = models.Corpus('../data/PH_corpus.segmented')
  corpus_file = open('../data/sentences.txt')

  fmm_match_count = 0
  rmm_match_count = 0
  vote_match_count = 0
  total_sentences = 0

  lines = corpus_file.readlines()
  print('Calculating ...')
  for line in lines:
    total_sentences += 1
    line = line.strip()
    full_line = re.sub(' +', '', line)
    true_split = re.sub(' +', '/', line)
    fmm, rmm, vote = segmenting_methods.segment_sentence(full_line, word_dictionary, corpus)
    if true_split == fmm:
      fmm_match_count += 1
    if true_split == rmm:
      rmm_match_count += 1
    if true_split == vote:
      vote_match_count += 1

  print("FMM Accuracy: " + str((fmm_match_count / total_sentences)*100) + "%")
  print("RMM Accuracy: " + str((rmm_match_count / total_sentences) * 100) + "%")
  print("Post-Cost-Calculation Accuracy: " + str((vote_match_count / total_sentences) * 100) + "%")


test_sentence_segmentation()