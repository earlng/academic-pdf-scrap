#counts the number of sentences in a provided file. File format must be based on Google Drive excel (important for the column numbers).
import csv
import nltk

nltk.download('punkt')
from nltk.tokenize import sent_tokenize

file="corrected_output.csv"

statements={}

with open(file, 'rt', encoding='utf-8') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  line_count = 0
  for row in csv_reader:
    if line_count == 0:
      line_count +=1
    else:
      identifier=row[4]
      bis=row[6]
      statements[identifier]={"bis":bis}

#the final output will be a dictionary with structure of [{"identifier": "xyz", "bis": "Ipsum lorem", "count": 3}]
final_output=[]

for entry in statements:
    number_of_sentences = len(sent_tokenize(statements[entry]["bis"]))
    entry = {"identifier": entry, "bis": statements[entry]["bis"], "sentence count": number_of_sentences}
    final_output.append(entry)

csv_columns = ["identifier", "bis", "sentence count"]

with open("sentence_count.csv", "w", newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for data in final_output:
        writer.writerow(data)