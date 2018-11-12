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