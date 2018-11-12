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


# 从左边查最大的单词匹配
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


# 从右边查最大的单词匹配
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


def vote_on_sentence(fmm_dictionary_matches, reversed_rmm_dictionary_matches):
  corpus = models.Corpus('./data/PH_corpus.segmented')
  corpus_text = corpus.text
  corpus_word_count = corpus.word_count
  fmm_cost_list = []
  rmm_cost_list = []

  # USE COST CALUCULATION TO WORK OUT WHETHER FMM OR RMM SPLIT HAS LOWEST COST
  # I HAVE ADDED A SMALL CONSTANT (1*10^-15) IN CASE THE FREQUENCY IS 0. THIS WILL PREVENT LOG(0)
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


def segment_sentence(sentence, word_dictionary):
  # FORWARD MAXIMUM MATCHING
  fmm_dictionary_matches = []
  fmm_word_to_check_in_dictionary = sentence
  while fmm_word_to_check_in_dictionary:
    word = fmm_greedy_check(fmm_word_to_check_in_dictionary, word_dictionary)
    fmm_dictionary_matches.append(word)
    fmm_word_to_check_in_dictionary = remove_first_word(word, fmm_word_to_check_in_dictionary)
  fmm_split_words = "/".join(fmm_dictionary_matches)

  # REVERSE MAXIMUM MATCHING
  rmm_dictionary_matches = []
  rmm_word_to_check_in_dictionary = sentence
  while rmm_word_to_check_in_dictionary:
    word = rmm_greedy_check(rmm_word_to_check_in_dictionary, word_dictionary)
    rmm_dictionary_matches.append(word)
    rmm_word_to_check_in_dictionary = remove_last_word(word, rmm_word_to_check_in_dictionary)
  reversed_rmm_dictionary_matches = rmm_dictionary_matches[::-1]
  rmm_split_words = "/".join(reversed_rmm_dictionary_matches)

  # 如果FMM与RMM的结果不一样，句子有歧义。执行vote_on_sentence()函数，用smallest cost（最小代价）选FMM或RMM的接过。
  cost_evaluated_words = rmm_split_words
  if not fmm_dictionary_matches == reversed_rmm_dictionary_matches:
    vote = vote_on_sentence(fmm_dictionary_matches, reversed_rmm_dictionary_matches)
    cost_evaluated_words = "/".join(vote)

  return fmm_split_words, rmm_split_words, cost_evaluated_words


def main(word_dictionary):
  user_sentence = input("\n输入一个汉语句子：\n")
  if user_sentence == '1':
    sys.exit()
  fmm_split, rmm_split, cost_evaluated_split = segment_sentence(user_sentence, word_dictionary)
  print(fmm_split, rmm_split, cost_evaluated_split)


if __name__ == "__main__":
  word_dictionary = createDictionary("./data/dic-ce.txt")
  while True:
    main(word_dictionary)