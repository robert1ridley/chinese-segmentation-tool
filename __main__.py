import sys
import helper_methods.dictionary_methods as dictionary_methods
import helper_methods.segmenting_methods as segmenting_methods
import models


def main(word_dictionary, corpus):
  user_sentence = input("\n输入一个汉语句子（停止程序，输入'1'）：\n")
  if user_sentence == '1':
    sys.exit()
  fmm_split, rmm_split, cost_evaluated_split = segmenting_methods.segment_sentence(user_sentence, word_dictionary,
                                                                                   corpus)
  print("FMM split: " + fmm_split)
  print("RMM split: " + rmm_split)
  print("Chosen split: " + cost_evaluated_split)


if __name__ == "__main__":
  word_dictionary = dictionary_methods.createDictionary("./data/dic-ce.txt")
  corpus = models.Corpus('./data/PH_corpus.segmented')
  while True:
    main(word_dictionary, corpus)