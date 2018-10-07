def main():
  wordDict = {}
  dataFile = open("./data/dic-ce.txt", "r", encoding='utf-8')
  for row in dataFile:
    row = row.split(',')
    wordDict[row[0]] = row[0]

if __name__ == "__main__":
  main()