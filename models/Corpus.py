import re

class Corpus (object):
  def __init__(self, input_text):
    infile = open(input_text, "r", encoding='utf-8')
    contents = infile.read()
    contents = re.sub(r'[^\w\s]','',contents)
    self.text = contents