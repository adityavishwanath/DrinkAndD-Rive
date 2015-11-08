import json
import argparse
from json import JSONDecoder
import re

FLAGS = re.VERBOSE | re.MULTILINE | re.DOTALL
WHITESPACE = re.compile(r'[ \t\n\r]*', FLAGS)

class ConcatJSONDecoder(json.JSONDecoder):
    def decode(self, s, _w=WHITESPACE.match):
        s_len = len(s)

        objs = []
        end = 0
        while end != s_len:
            obj, end = self.raw_decode(s, idx=_w(s, end).end())
            end = _w(s, end).end()
            objs.append(obj)
        return objs


f = open('9.json.txt', 'r') #file name will change!
text = f.read()
f.close()

text_json = json.loads(text, cls=ConcatJSONDecoder)

#This is the confidence value of the string in total.
total_confidence = text_json[len(text_json) - 1]['results'][0]['alternatives'][0]['confidence']

if total_confidence <= 0.64:
    print "*****BAD INPUT: TOO MUCH NOISE. PLEASE TRY AGAIN.*****"
    exit()

#This is a list of ['word', start_time, end_time]
timestamps_list = text_json[len(text_json) - 1]['results'][0]['alternatives'][0]['timestamps']
#print(timestamps_list)

#This is a list of ['word', confidence_value]
confidence_list = text_json[len(text_json) - 1]['results'][0]['alternatives'][0]['word_confidence']
#print (confidence_list)

"""
TODO:
1. Eliminate the words from timestamps_list that have a confidence value (which you can get from confidence_list) lower than 0.65 (our threshold)
2. Find the average time difference between a word and the next word. (start_time(word n+1) - end_time(word n), for all n words in the new timestamps_list)
"""
for word, confidence in confidence_list:
    if confidence < 0.65:
        confidence_list.remove([word, confidence])

for word, start_time, end_time in timestamps_list:
    b = False
    for x in confidence_list:
        if x[0] == word:
            b = True
    if not b:
        timestamps_list.remove([word, start_time, end_time])

end_time_old = timestamps_list[0][1]
total_time = 0
for word, start_time, end_time in timestamps_list:
    total_time += start_time - end_time_old
    end_time_old = end_time

avg_time = total_time/len(timestamps_list)
