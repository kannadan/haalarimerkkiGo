# -*- coding: utf-8 -*-

import shutil
from shutil import copyfile
import os
from os import listdir
from os.path import isfile, join
import random
from decimal import *
getcontext().prec = 2

list_of_files = []
temp_for_teaching = []
temp_for_testing = []
testing_folder = ''
teaching_folder = ''
directory = ''

def AskDirectory():
    print("Give a path to the folder containing files: ")
    directory = input()
    return directory
    

def listFiles(directory): #Makes a list of filenames from choosed directory
    while True:
        try:
            list_of_files = [f for f in listdir(directory) if isfile(join(directory, f))]
            if len(list_of_files) == 0:
                print("Folder not containing files.")
                return
            elif len(list_of_files) > 0:
                list_of_files.append("end_of_list")
                return list_of_files          
        except WindowsError:
            print("Invalid path.")
            return
          
def CheckDirectory(): #Checks the directory for errors and retuns the list of files in it
    while True:
        try:
            directory = AskDirectory()        #directory = 'C:\KuvaArkisto' 
            list_of_files = listFiles(directory)
            if len(list_of_files) > 0:
                return (directory, list_of_files)    
        except TypeError:
            continue
        except UnicodeEncodeError:
            print("Bad filename. <UnicodeEncodeError>")
            continue

def AskDestination(): #Destination folder where the files will be moved after separation
    print("Give a destination path for the sorted folder: ")
    destination = input()
    return destination
    
def CreateTestingFolder(destination):
    testing_folder = destination+'\\'+'Haalarimerkki_testing'
    if not os.path.exists(testing_folder):
        os.makedirs(testing_folder)       
    return testing_folder
    
def CreateTeachingFolder(destination):
    teaching_folder = destination+'\\'+'Haalarimerkki_teaching'
    if not os.path.exists(teaching_folder):
        os.makedirs(teaching_folder)  
    return teaching_folder

def simplifyPatchName(file_name): #Simplifies filename by leaving only letters and dots
    sorter_variable = file_name
    patch_name = ""
    for i in sorter_variable:
        if i.isalpha() or i == ".":
            patch_name += i
        else:
            pass
    return patch_name    
    
    
def compareAndMove(list_of_files, patch_name, temp_for_teaching): #requires filenames to be in name order
    counter = 0
    for i in range(0, len(list_of_files)):
        to_compare = simplifyPatchName(list_of_files[i])
        if to_compare == "end_of_list":
            return
        if to_compare[0:len(patch_name)] == patch_name:
            temp_for_teaching.append(list_of_files[i])

            counter+=1

        else:
            for i in range(counter):
                del list_of_files[0]
            return temp_for_teaching
           
def sortTestAndTeach(temp_for_teaching, temp_for_testing):
    while(Decimal(len(temp_for_testing))/Decimal(len(temp_for_teaching)) < Decimal(3)/Decimal(7)):
        random_file = random.choice(temp_for_teaching)
        temp_for_testing.append(random_file)
        temp_for_teaching.remove(random_file)
    return
    

            
            
def moveFilesToFolder(directory,temp_for_testing, temp_for_teaching, testing_folder, teaching_folder):  
    for i in range(len(temp_for_testing)):
        shutil.copy2(directory+'\\'+temp_for_testing[i], testing_folder)
    for i in range(len(temp_for_teaching)):
        shutil.copy2(directory+'\\'+temp_for_teaching[i], teaching_folder)
    return

def countFiles(folder):
    file_count = len([f for f in listdir(folder) if isfile(join(folder, f))])
    return file_count
    
###CODE STARTS HERE###

directory, list_of_files = CheckDirectory()
# print("list of files", list_of_files)
print("Directory containing", len(list_of_files)-1, "files")
destination = AskDestination()
testing_folder = CreateTestingFolder(destination)
print("Created destination folder", testing_folder)
teaching_folder = CreateTeachingFolder(destination)
print("Created destination folder", teaching_folder)

while (len(list_of_files)) > 1:
    patch_name = simplifyPatchName(list_of_files[0])
    temp_for_teaching = compareAndMove(list_of_files, patch_name, temp_for_teaching)
    sortTestAndTeach(temp_for_teaching, temp_for_testing)
    moveFilesToFolder(directory,temp_for_testing, temp_for_teaching, testing_folder, teaching_folder)
    temp_for_teaching = []
    temp_for_testing = []

#printing stats here
test_file_count = countFiles(testing_folder)
print(testing_folder, "containing", test_file_count, "files")
teach_file_count = countFiles(teaching_folder)
print(teaching_folder, "containing", teach_file_count, "files")
total_files = test_file_count+teach_file_count
print("Testing folder containing", Decimal(test_file_count)/Decimal(total_files)*100,"% of the files")
print("Teaching folder containing", Decimal(teach_file_count)/Decimal(total_files)*100,"% of the files")