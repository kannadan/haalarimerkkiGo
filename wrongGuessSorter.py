#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
This program takes as an input a .txt file containing lines such as
'Path: testi3/friday800.jpg	Guess: heijastin'
and creates a statistics 'filename'_results.txt file containing
lines of how many times a patch was guessed wrong as each wrong guess.'''

import os

def getFile():
    filename = raw_input("Give the filepath> ")
    return filename

def readLines(filename):
    file = open(filename, "r")
    for line in file:
        readLine(line)
    file.close()
    return

def readLine(line):
    correct = ''
    guess = ''
    line = line.split("/")[1]
    for char in line:
        if char.isdigit():
            break
        else:
            correct += char
    guess = line.split(": ")[1]
    guess = guess.split("\n")[0]
    saveResult(correct, guess)
    return

def saveResult(correct, guess): # saves the result to dictionary
    if correct not in dict:
        dict[correct] = []
        dict[correct].append(guess)
        dict[correct].append(1)
    if correct in dict:
        if guess in dict[correct]:
            index = dict[correct].index(guess)
            dict[correct][index+1] += 1
        else:
            dict[correct].append(guess)
            dict[correct].append(1)
    return

def printResults():
    for key, value in dict.iteritems():
        while value:
            spaces = 16-len(key)-len(value[0])
            print key, "was guessed as", value.pop(0), spaces*" ", value.pop(0), "times."
        print
    return

def writeToFile(filename, dict):
    filename2 = filename.split(".")[0]+"_results.txt"
    while True:
        if os.path.exists(filename2):
            print "Filename {} already exists. Overwrite y/n?".format(filename2)
            verification = raw_input("> ")
            if verification == "y":
                break
            if verification == "n":
                print "Give a new name for {}.".format(filename2)
                filename2 = raw_input()
            else:
                continue
        else:
            break

    file2 = open(filename2, "w+")
    for key, value in dict.iteritems():
        while value:
            spaces = 16-len(key)-len(value[0]) # to even out the columns
            to_file = "{} was guessed as {} {} {} times.\n".format(key, value.pop(0), spaces*" ", value.pop(0))
            file2.write(to_file)
        file2.write("\n")
    file2.close()
    print "Succesfully created {}.".format(filename2)
    return

dict = {}
while True:
    try:
        filename = getFile()
        readLines(filename)
        break
    except IOError:
        print "File does not exist."
writeToFile(filename, dict)