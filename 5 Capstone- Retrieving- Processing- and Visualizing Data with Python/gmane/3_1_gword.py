# look for the coomon words
import sqlite3
import time
import urllib
import zlib
import string

conn = sqlite3.connect('index.sqlite')
conn.text_factory = str
cur = conn.cursor()

cur.execute('''SELECT subject_id,subject FROM Messages
    JOIN Subjects ON Messages.subject_id = Subjects.id''')

counts = dict() # count of words
for message_row in cur :
    text = message_row[1] # pull out the words
    text = text.translate(None, string.punctuation) # clean puntuation
    text = text.translate(None, '1234567890')
    text = text.strip()
    text = text.lower()
    words = text.split() # no punctuation 
    for word in words:
        if len(word) < 4 : continue
        counts[word] = counts.get(word,0) + 1

# Find the top 100 words
words = sorted(counts, key=counts.get, reverse=True) # count the words
highest = None
lowest = None
for w in words[:70]: ## looping throught the keys the most common words
    if highest is None or highest < counts[w] :
        highest = counts[w]
    if lowest is None or lowest > counts[w] :
        lowest = counts[w]
print 'Range of counts:',highest,lowest

# Spread the font sizes across 20-100 based on the count
bigsize = 80
smallsize = 20

fhand = open('gword.js','w')
fhand.write("gword = [")
first = True
for k in words[:70]:
    if not first : fhand.write( ",\n")
    first = False
    size = counts[k]
    size = (size - lowest) / float(highest - lowest)
    size = int((size * bigsize) + smallsize)
    fhand.write("{text: '"+k+"', size: "+str(size)+"}")
fhand.write( "\n];\n")

print "Output written to gword.js"
print "Open gword.htm in a browser to view"
