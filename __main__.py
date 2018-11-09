import sys
import models
import math
import numpy as np


def createDictionary(filename):
  word_dict = {}
  dataFile = open(filename, "r", encoding='utf-8')
  for row in dataFile:
    row = row.split(',')
    word_dict[row[0]] = row[0]
  return word_dict


def is_word_in_dictionary(word, chinese_dictionary):
  dictSearch = chinese_dictionary.get(word, False)
  if dictSearch:
    return True
  return False


def remove_last_char(word):
  word_with_final_char_removed = word[:-1]
  return word_with_final_char_removed


def remove_first_char(word):
  word_with_first_char_removed = word[1:]
  return word_with_first_char_removed


def remove_first_word(term_to_remove, full_string):
  full_string = full_string[len(term_to_remove):]
  return full_string


def remove_last_word(term_to_remove, full_string):
  full_string = full_string[:-len(term_to_remove)]
  return full_string


def fmm_greedy_check(term, word_dictionary):
  word_to_check_in_dictionary = term
  is_dictionary_match = False
  while not is_dictionary_match and word_to_check_in_dictionary:
    is_dictionary_match = is_word_in_dictionary(word_to_check_in_dictionary, word_dictionary)
    if not is_dictionary_match:
      word_to_check_in_dictionary = remove_last_char(word_to_check_in_dictionary)
  if not is_dictionary_match:
    word_to_check_in_dictionary = term[0]
    is_dictionary_match = True
  return word_to_check_in_dictionary


def rmm_greedy_check(term, word_dictionary):
  word_to_check_in_dictionary = term
  is_dictionary_match = False
  while not is_dictionary_match and word_to_check_in_dictionary:
    is_dictionary_match = is_word_in_dictionary(word_to_check_in_dictionary, word_dictionary)
    if not is_dictionary_match:
      word_to_check_in_dictionary = remove_first_char(word_to_check_in_dictionary)
  if not is_dictionary_match:
    word_to_check_in_dictionary = term[-1]
    is_dictionary_match = True
  return word_to_check_in_dictionary


# def vote_fmm_rmm(fmm_list, rmm_list):
#   corpus = models.Corpus('./data/PH_corpus.segmented')
#   fmm_counts = {
#     'not_in_dict': 0,
#     'single_character_words': 0
#   }
#   rmm_counts = {
#     'not_in_dict': 0,
#     'single_character_words': 0
#   }
#
#   for term in fmm_list:
#     if len(term) == 1:
#       fmm_counts['single_character_words'] += 1
#     elif corpus.text.count(term) == 0:
#       fmm_counts['not_in_dict'] += 1
#   print(fmm_counts)
#
#   for term in rmm_list:
#     if len(term) == 1:
#       rmm_counts['single_character_words'] += 1
#     elif corpus.text.count(term) == 0:
#       rmm_counts['not_in_dict'] += 1
#   print(rmm_counts)
#
#   # Check whether one result has more words not in the corpus
#   if fmm_counts['not_in_dict'] != rmm_counts['not_in_dict']:
#     if fmm_counts['not_in_dict'] < rmm_counts['not_in_dict']:
#       return fmm_list
#     else:
#       return rmm_list
#
#   # Check whether one result has more single character words
#   elif fmm_counts['single_character_words'] != rmm_counts['single_character_words']:
#     if fmm_counts['single_character_words'] < rmm_counts['single_character_words']:
#       return fmm_list
#     else:
#       return rmm_list
#
#   else:
#     return rmm_list


def vote_on_sentence(fmm_dictionary_matches, reversed_rmm_dictionary_matches):
  corpus = models.Corpus('./data/PH_corpus.segmented')
  corpus_text = corpus.text
  corpus_word_count = corpus.word_count
  fmm_cost_list = []
  rmm_cost_list = []
  constant = 1*(math.pow(10, -15))
  for word in fmm_dictionary_matches:
    word_freq = corpus_text.count(word) + constant
    cost = -(math.log(word_freq/corpus_word_count))
    fmm_cost_list.append(cost)
  for item in reversed_rmm_dictionary_matches:
    word_freq = corpus_text.count(item) + constant
    cost = -(math.log(word_freq / corpus_word_count))
    rmm_cost_list.append(cost)
  if np.mean(fmm_cost_list) < np.mean(rmm_cost_list):
    return fmm_dictionary_matches
  else:
    return reversed_rmm_dictionary_matches


def main():
  word_dictionary = createDictionary("./data/dic-ce.txt")
  user_sentence = input("\nEnter a Chinese sentence (enter '1' to exit program): \n")
  if user_sentence == '1':
    sys.exit()
  
  # FMM
  fmm_dictionary_matches = []
  fmm_word_to_check_in_dictionary = user_sentence
  while fmm_word_to_check_in_dictionary:
    word = fmm_greedy_check(fmm_word_to_check_in_dictionary, word_dictionary)
    fmm_dictionary_matches.append(word)
    fmm_word_to_check_in_dictionary = remove_first_word(word, fmm_word_to_check_in_dictionary)
  split_words = "/".join(fmm_dictionary_matches)
  print ("FMM: " + split_words)

  # RMM
  rmm_dictionary_matches = []
  rmm_word_to_check_in_dictionary = user_sentence
  while rmm_word_to_check_in_dictionary:
    word = rmm_greedy_check(rmm_word_to_check_in_dictionary, word_dictionary)
    rmm_dictionary_matches.append(word)
    rmm_word_to_check_in_dictionary = remove_last_word(word, rmm_word_to_check_in_dictionary)
  reversed_rmm_dictionary_matches = rmm_dictionary_matches[::-1]
  split_words = "/".join(reversed_rmm_dictionary_matches)
  print ("RMM: " + split_words)

  if not fmm_dictionary_matches == reversed_rmm_dictionary_matches:
    # decision = vote_fmm_rmm(fmm_dictionary_matches, reversed_rmm_dictionary_matches)
    # decision_split = "/".join(decision)
    # print("FINAL DECISION: " + decision_split)
    vote = vote_on_sentence(fmm_dictionary_matches, reversed_rmm_dictionary_matches)
    print("HEURISTICS VOTE: " + "/".join(vote))

if __name__ == "__main__":
  while True:
    main()