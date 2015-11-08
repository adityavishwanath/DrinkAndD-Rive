import json
import argparse
from json import JSONDecoder
import re
import os

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

class TestCases():    
    """
    Calculates the average time between the words (random string spoken by the individual)
    Raises a flag if the average time is above a threshold value (of 0.15s)
    Returns a flag or no flag.
    """
    @staticmethod
    def avg_time_between_words(timestamps_list):
        end_time_old = timestamps_list[0][1]
        total_time = 0
        for word, start_time, end_time in timestamps_list:
            total_time += start_time - end_time_old
            end_time_old = end_time

        avg_time = total_time/len(timestamps_list) #time between words
        if (avg_time > 0.15):
            return 1
        else:
            return 0

    """
    Tests two possible cases using a specified input.
    The sentence is :"I chose an encyclopedia at the bookstore."
    What we analyze:
        1) Big word - 'encyclopaedia'; the time to enunciate this word is tested, 
           and a flag is raised if speech is slow/unclear.
        2) Phonetics - 'chose'; the 'ch' sound in 'chose' is tested for accuracy,
           clarity and time taken to enunciate it as part of a sentence.
    Returns a flag if either of the two tests raises a flag, else returns no flag.
    """
    @staticmethod
    def big_words_and_phonetics_test(timestamps_list):
        return_value = 0
        end_time_old = timestamps_list[0][1]
        eBool = False
        cBool = False
        for word, start_time, end_time in timestamps_list:
            if word == "encyclopedia":
                eBool = True
                if (start_time - end_time_old > 1.15):
                    return_value += 1
            if word == "chose":
                cBool = True
                if (start_time - end_time_old > 0.85):
                    return_value += 1
            end_time_old = end_time
        if not (eBool and cBool):
            return 1
        else:
            return return_value

    """
    Tests for accuracy, speed and clarity in reciting the English Alphabet.
    Returns a flag if average time between characters, and average time enunciating each
    character is above a specified threshold value, else returns no flag.
    """
    @staticmethod
    def alphabet_test(timestamps_list):
        return_value = 0
        end_time_old = timestamps_list[0][1]
        total_time = 0
        for word, start_time, end_time in timestamps_list:
            total_time += start_time - end_time_old
            end_time_old = end_time

        avg_time = total_time/len(timestamps_list) #time between words
        #print(avg_time)
        if (avg_time > 0.15):
            return_value += 1

        total_time = timestamps_list[len(timestamps_list) - 1][2] - timestamps_list[0][1]
        #print(total_time)
        if (total_time > 15):
            return_value += 1

        return return_value


if __name__ == '__main__':
    script_dir = os.path.dirname(__file__)
    rel_path = "output/0.json.txt" #THIS SHOULD BE FINE?!
    abs_file_path = os.path.join(script_dir, rel_path)

    f = open(abs_file_path, 'r')
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

    #This is a list of ['word', confidence_value]
    confidence_list = text_json[len(text_json) - 1]['results'][0]['alternatives'][0]['word_confidence']

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
    print
    print
    print "TEST 1 - AVERAGE TIME BETWEEN WORDS."
    print "TEST 2 - BIG WORDS AND PHONETICS."
    print "TEST 3 - RECITATION OF THE ALPHABETS."
    choice = raw_input("PLEASE SELECT A TEST MODULE [1, 2 or 3]: ")

    sum_of_flags = 0
    if choice == '1':
        if TestCases.avg_time_between_words(timestamps_list) != 0:
            print "TEST 1: AVERAGE TIME BETWEEN WORDS - FAILED."
            sum_of_flags += TestCases.avg_time_between_words(timestamps_list)
        else:
            print "TEST 1: AVERAGE TIME BETWEEN WORDS - PASSED."
        print
    elif choice == '2':
        if TestCases.big_words_and_phonetics_test(timestamps_list) != 0:
            print "TEST 2: BIG WORDS AND PHONETICS - FAILED."
            sum_of_flags += TestCases.big_words_and_phonetics_test(timestamps_list)
        else:
            print "TEST 2: BIG WORDS AND PHONETICS - PASSED."
        print
    elif choice == '3':
        if TestCases.alphabet_test(timestamps_list) != 0:
            print "TEST 3: RECITATION OF THE ALPHABETS - FAILED."
            sum_of_flags += TestCases.alphabet_test(timestamps_list)
        else:
            print "TEST 3: RECITATION OF THE ALPHABETS - PASSED."
    else:
        print "Invalid Input!!! Program wil be terminated."    
    
    if sum_of_flags > 0:
        print "DRUNKENNESS DETECTED. DO NOT DRIVE."
       
    """
    dd_prob = sum_of_flags / 5.00; #Max 5.00 points.
    print
    print "****************************************************************"
    print "Percentage of drunkenness or drowsiness:" + str(dd_prob * 100)
    print "****************************************************************"
    print

    if dd_prob >= 0.65: #Threshold value
        #SEND A TEXT
        print "A TEXT MESSAGE WILL BE SENT."
    """