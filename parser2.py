import json
import argparse
from json import JSONDecoder
import re
import os

FLAGS = re.VERBOSE | re.MULTILINE | re.DOTALL
WHITESPACE = re.compile(r'[ \t\n\r]*', FLAGS)

"""
SENTENCE: I **chose** an **encyclopedia** at the bookstore.
"""

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

script_dir = os.path.dirname(__file__)
rel_path = "output/0.json.txt"
abs_file_path = os.path.join(script_dir, rel_path)

f = open(abs_file_path, 'r') #file name will change!
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

avg_time = total_time/len(timestamps_list) #time between words

#NOW CHECK FOR TIME SPENT ON EACH WORD.