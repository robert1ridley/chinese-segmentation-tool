import sys

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
  while not is_dictionary_match and not word_to_check_in_dictionary == '':
    is_dictionary_match = is_word_in_dictionary(word_to_check_in_dictionary, word_dictionary)
    if not is_dictionary_match:
      word_to_check_in_dictionary = remove_last_char(word_to_check_in_dictionary)
  return is_dictionary_match, word_to_check_in_dictionary

def rmm_greedy_check(term, word_dictionary):
  word_to_check_in_dictionary = term
  is_dictionary_match = False
  while not is_dictionary_match and not word_to_check_in_dictionary == '':
    is_dictionary_match = is_word_in_dictionary(word_to_check_in_dictionary, word_dictionary)
    if not is_dictionary_match:
      word_to_check_in_dictionary = remove_first_char(word_to_check_in_dictionary)
  return is_dictionary_match, word_to_check_in_dictionary

def main():
  word_dictionary = createDictionary("./data/dic-ce.txt")
  user_sentence = input("\nEnter a Chinese sentence (enter '1' to exit program): \n")
  if user_sentence == '1':
    sys.exit()
  
  # FMM
  fmm_dictionary_matches = []
  fmm_word_to_check_in_dictionary = user_sentence
  parse_error = False
  while not fmm_word_to_check_in_dictionary == '' and not parse_error:
    match, word = fmm_greedy_check(fmm_word_to_check_in_dictionary, word_dictionary)
    if match:
      fmm_dictionary_matches.append(word)
      fmm_word_to_check_in_dictionary = remove_first_word(word, fmm_word_to_check_in_dictionary)
    else:
      print ("There was an error parsing the sentence.")
      parse_error = True
  split_words = "/".join(fmm_dictionary_matches)
  print ("FMM: " + split_words)

  # RMM
  rmm_dictionary_matches = []
  rmm_word_to_check_in_dictionary = user_sentence
  parse_error = False
  while not rmm_word_to_check_in_dictionary == '' and not parse_error:
    match, word = rmm_greedy_check(rmm_word_to_check_in_dictionary, word_dictionary)
    if match:
      rmm_dictionary_matches.append(word)
      rmm_word_to_check_in_dictionary = remove_last_word(word, rmm_word_to_check_in_dictionary)
    else:
      print ("There was an error parsing the sentence.")
      parse_error = True
  reversed_rmm_dictionary_matches = rmm_dictionary_matches[::-1]
  split_words = "/".join(reversed_rmm_dictionary_matches)
  print ("RMM: " + split_words)

if __name__ == "__main__":
  while True:
    main()