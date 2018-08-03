#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 13:48:12 2018

@author: ashkar
"""

import csv
import re
import xlrd
import time

start = time.time()

def isEveryElementEmpty(lst):
    '''A row is input as a list of strings. Returns True if a row is empty. Stops checking
    and returns False immediately after finding a non-empty cell'''
    temp_bool = True
    
    for i in lst:
        if len(i.replace(" ", "")) != 0:
            temp_bool = False
            break
    
    '''The boolean is returned as a list'''
    return [temp_bool]

def isExistsNullHeader_s_MidWay(lst, start):
    '''Returns True if null headers exist in the midway (i.e. if there are one 
    or more empty headers between two non-empty headers). This function is to
    be executed only if an empty header is encountered immediately after a non-
    empty header'''
    temp_bool = False
    
    for i in range(start, len(lst)):
        ''''start' is the index of the first empty header found following non-
        empty headers'''
        if len(lst[i].replace(" ", "")) != 0:
            '''The boolean becomes True if a non-empty header is encountered 
            after one or more empty headers'''
            temp_bool = True
            break
        
    return [temp_bool]

def isExistsDuplicate(lst):
    '''Returns True if duplicate headers exist'''
    temp_bool = False
    j = 0
    header_indices = []
    distinct_list = []
    pre_temp = []
    length_of_list = len(lst)
    
    for i in range(length_of_list):
        temp = lst[i].replace(" ", "")
        temp_lowercase = temp.lower()
        pre_temp.append(temp_lowercase)
        
        if len(temp_lowercase) == 0:
            '''This condition is executed if current cell is empty'''
            if (0 < i < (length_of_list - 1) and len(pre_temp[i-1]) != 0
                    and isExistsNullHeader_s_MidWay(lst, i)[0]):
                '''This condition is executed if the current cell is neither 
                first nor last cell, the previous cell is non-empty and there 
                is a non-empty cell after zero or more empty cells. (Note that 
                current cell is empty)'''
                
                print("Error! Empty header found midway")
                j += 1
                break
        else:
            '''This condition is executed if current cell is non-empty. The 
            following block checks whether the headers are unique or not. 
            Compares with 'distinct_list' and appends to it if unique (Indices 
            of unique headers are also saved for later purposes). If the list 
            contains the same element that is being checked, then 'temp_bool' 
            is made True and program returns the error of duplicate header.'''
            if (len(temp_lowercase) != 0 
                    and temp_lowercase not in distinct_list):
                
                distinct_list.append(temp_lowercase)
                header_indices.append(i)
            
            elif (len(temp_lowercase) != 0 
                      and temp_lowercase in distinct_list):
                
                temp_bool = True
                break
            
    return [temp_bool, j, header_indices, distinct_list]

def generateHeaderTypeList(lst):
    '''Initiates a list equal to the length of lst. This list will be updated 
    by checking the types of each non-header cell'''
    header_type = ["not updated" for i in range(len(lst))]
    
    return [header_type]

def isAgainstHeaderIndices(lst, header_indices, header_type):
    '''Returns True if a non-empty cell without a header is found'''
    temp_bool = False
    i = 0
    single_row = []
    
    while i < len(lst):
        element = lst[i]
        temp = element.replace(" ", "")
        
        if len(temp) != 0 and i not in header_indices:
            '''Checks the indices of non-empty cells against the indices in 
            'header_indices'. If it doesn't coincide, returns True and breaks
            '''
            temp_bool = True
            break
        
        else:
            '''If the index coincides with the corresponding element in 
            'header_indices', the following block is executed. The 
            'header_type' list which was initiated by the function,
            'generateHeaderTypeList(lst)' is updated based on regular 
            expressions for number format, date format and string format'''
            
            if re.search(r'^((\$|Rs|USD|LKR)?(\d+,?)*\d*(\.\d+)|(\$|Rs|USD|LKR)\
                             ?(\d+,?)*\d+(\.\d+)?|(\d+,?)*\d*(\.\d+)(\$|Rs|USD|\
                             LKR)?|(\d+,?)*\d+(\.\d+)?(\$|Rs|USD|LKR)?)|(-\d+)(\.\d+)?$', temp):
                
                '''If the current cell satisfies the number format...'''
                if header_type[i] == "DATE":
                    header_type[i] = "STRING"
                elif header_type[i] == "STRING":
                    header_type[i] = "STRING"
                else:
                    header_type[i] = "NUMBER"
                    
            elif re.search(r'^(\d{2}/\d{2}/\d{4}|\d{2}-\d{2}-\d{4}|\d{2}/\d{2}/\
                               \d{2}|\d{2}-\d{2}-\d{2}|\d{4}/\d{2}/\d{2}|\d{4}-\
                               \d{2}-\d{2})$', temp):
                
                '''If the current cell satisfies the date format...'''
                if header_type[i] == "NUMBER":
                    header_type[i] = "STRING"
                elif header_type[i] == "STRING":
                    header_type[i] = "STRING"
                else:
                    header_type[i] = "DATE"
                    
            else:
                '''If the current cell doesn't satisfy any of the above 
                formats...'''
                header_type[i] = "STRING"
            
            '''The checked element is added to 'single_row' which will be added
            to a 2D-list which is the refined output'''
            single_row.append(element)
        
        i += 1
    
    return [temp_bool, single_row, header_type]
    
#def execute(row, i):

            
#    return [i, list_isExistsDuplicate,list_isAgainstHeaderIndices, data_list]
file_name = "namak.csv"
#file_name = "Sample_xls.xls"
#file_name = "file_example_XLSX_5000.xlsx"
#file_name = "SampleXLSFile_6800kb.xls"

len_file_name = len(file_name)
i = 0

if file_name[len_file_name-1:len_file_name-4:-1][::-1] == "csv":
    with open(file_name, newline = '') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',', quotechar='"')
#        list_execute = execute(reader)
        headers_list = []
        data_list = []
        
        for row in reader:
            '''i == 0/1 cases are considered to handle header and non-header rows 
            as two different cases'''
            if i == 0:
                list_isEveryElementEmpty = isEveryElementEmpty(row)
                
                if not list_isEveryElementEmpty[0]:
                    '''Following block is executed if the encountered row is 
                    non-empty'''
                    
                    list_isExistsDuplicate = isExistsDuplicate(row)
                    
                    if list_isExistsDuplicate[0]:
                        '''Checks if duplicate header exists and if it does, the 
                        program ceases to run. Also whether any empty header is
                        found in the middle'''
                        
                        print("Error! Duplicate Header")
                        break
                    else:
                        '''if no duplicate header exists...'''
                        if len(list_isExistsDuplicate[2]) > 100:
                            '''Checks the length of 'header_indices' which is the 
                            number of columns. More than 100 is not allowed'''
                            
                            print("Error! More than 100 columns found")
                            break
                        else:
                            '''If the constraint of number of columns is 
                            satisfied, the following block is executed. Also since 
                            all conditions for headers are satisfied by now, the 
                            'header_type' list is initiated'''
                            
                            list_generateHeaderTypeList = \
                                generateHeaderTypeList(row)
                            
                            if list_isExistsDuplicate[1] == 0:
                                '''The list of headers is added to the 2D 
                                'data_list' if j == 0 (i.e. 
                                list_isExistsDuplicate[1] == 0). j == 1 means 
                                "Empty header found midway". This j == 0 condition 
                                is to avoid "Element under non-existent header" 
                                case being raised'''
                                
                                headers_list += list_isExistsDuplicate[3]
                            
                            '''After the first non-empty row (i.e. header row) is 
                            read, i is incremented so that on the next loop, the 
                            block for normal rows (i.e. elif i==1 block) will be 
                            executed'''
                            i += 1
                else:
                    '''continues without doing anything until finding a non-empty 
                    row'''
                    continue
            
            elif i == 1:
                '''This block is executed for the non-header rows'''
                list_isEveryElementEmpty = isEveryElementEmpty(row)
                
                '''Executing isAgainstHeaderIndices(lst, header_indices, 
                header_type) function and saving its returned list with a 
                variable. Note that 'header_type' list is also updated by the same 
                function while checking whether each cell goes against headers'''
                
                list_isAgainstHeaderIndices = \
                    isAgainstHeaderIndices(row, 
                                           list_isExistsDuplicate[2], 
                                           list_generateHeaderTypeList[0])
                
                if list_isEveryElementEmpty[0]:
                    '''continue without doing anything until finding a non-empty
                    row'''
                    
                    continue
                
                elif list_isAgainstHeaderIndices[0]:
                    '''This block is executed if element exists under empty 
                    header'''
                    
                    if list_isExistsDuplicate[1] == 0:
                        '''list_isExistsDuplicate[1] == 1 is the "Empty header 
                        found midway" error. list_isExistsDuplicate[1] == 0 is 
                        "Element under non-existent header" error'''
                        
                        print("Error! Element under non-existent header")
                    
                    '''i is incremented inorder to avoid the output of the results 
                    despite having errors. Results will be output only if i == 1 
                    (i.e. not if i == 0 or i == 2)'''
                    i += 1
                    break
                
                '''The row is added to the 2D 'data_list' '''
                data_list.append(list_isAgainstHeaderIndices[1]\
                                 [list_isExistsDuplicate[2][0]:])

elif file_name[len_file_name-1:len_file_name-4:-1][::-1] == "xls" or file_name[len_file_name-1:len_file_name-5:-1][::-1] == "xlsx":
    wb = xlrd.open_workbook(file_name)
    if wb.nsheets > 1:
        print ("Error! More than one sheets")
    else:
        headers_list = []
        data_list = []
        sheet = wb.sheet_by_index(0)
        for row_num in range(sheet.nrows):
            row = list(map(str, sheet.row_values(row_num)))
            
            if i == 0:
                list_isEveryElementEmpty = isEveryElementEmpty(row)
                
                if not list_isEveryElementEmpty[0]:
                    '''Following block is executed if the encountered row is 
                    non-empty'''
                    
                    list_isExistsDuplicate = isExistsDuplicate(row)
                    
                    if list_isExistsDuplicate[0]:
                        '''Checks if duplicate header exists and if it does, the 
                        program ceases to run. Also whether any empty header is
                        found in the middle'''
                        
                        print("Error! Duplicate Header")
                        break
                    else:
                        '''if no duplicate header exists...'''
                        if len(list_isExistsDuplicate[2]) > 100:
                            '''Checks the length of 'header_indices' which is the 
                            number of columns. More than 100 is not allowed'''
                            
                            print("Error! More than 100 columns found")
                            break
                        else:
                            '''If the constraint of number of columns is 
                            satisfied, the following block is executed. Also since 
                            all conditions for headers are satisfied by now, the 
                            'header_type' list is initiated'''
                            
                            list_generateHeaderTypeList = \
                                generateHeaderTypeList(row)
                            
                            if list_isExistsDuplicate[1] == 0:
                                '''The list of headers is added to the 2D 
                                'data_list' if j == 0 (i.e. 
                                list_isExistsDuplicate[1] == 0). j == 1 means 
                                "Empty header found midway". This j == 0 condition 
                                is to avoid "Element under non-existent header" 
                                case being raised'''
                                
                                headers_list += list_isExistsDuplicate[3]
                            
                            '''After the first non-empty row (i.e. header row) is 
                            read, i is incremented so that on the next loop, the 
                            block for normal rows (i.e. elif i==1 block) will be 
                            executed'''
                            i += 1
                else:
                    '''continues without doing anything until finding a non-empty 
                    row'''
                    continue
            
            elif i == 1:
                '''This block is executed for the non-header rows'''
                list_isEveryElementEmpty = isEveryElementEmpty(row)
                
                '''Executing isAgainstHeaderIndices(lst, header_indices, 
                header_type) function and saving its returned list with a 
                variable. Note that 'header_type' list is also updated by the same 
                function while checking whether each cell goes against headers'''
                
                list_isAgainstHeaderIndices = \
                    isAgainstHeaderIndices(row, 
                                           list_isExistsDuplicate[2], 
                                           list_generateHeaderTypeList[0])
                
                if list_isEveryElementEmpty[0]:
                    '''continue without doing anything until finding a non-empty
                    row'''
                    
                    continue
                
                elif list_isAgainstHeaderIndices[0]:
                    '''This block is executed if element exists under empty 
                    header'''
                    
                    if list_isExistsDuplicate[1] == 0:
                        '''list_isExistsDuplicate[1] == 1 is the "Empty header 
                        found midway" error. list_isExistsDuplicate[1] == 0 is 
                        "Element under non-existent header" error'''
                        
                        print("Error! Element under non-existent header")
                    
                    '''i is incremented inorder to avoid the output of the results 
                    despite having errors. Results will be output only if i == 1 
                    (i.e. not if i == 0 or i == 2)'''
                    i += 1
                    break
                
                '''The row is added to the 2D 'data_list' '''
                data_list.append(list_isAgainstHeaderIndices[1]\
                                 [list_isExistsDuplicate[2][0]:])
else:
    print ("Unsupported file type!")
    
if i == 1 and list_isExistsDuplicate[1] == 0:
    '''Results will be output only if i == 1 and list_isExistsDuplicate[1] == 0
    (i.e. j == 0). Others are error cases'''
    
    print (list_isAgainstHeaderIndices[2][list_isExistsDuplicate[2][0]:])
    print (headers_list)
    print (data_list)
    
print ("\n", time.time() - start)

#if list_execute[0] == 1 and list_execute[1][1] == 0:
#    '''Results will be output only if i == 1 and list_isExistsDuplicate[1] == 0
#    (i.e. j == 0). Others are error cases'''
#    
#    print(list_execute[2][2][list_execute[1][2][0]:])
#    print(list_execute[3])