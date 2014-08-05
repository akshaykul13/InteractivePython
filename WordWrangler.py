"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    current_item = None
    list2 = []
    for item in list1:
        if current_item == None:
            current_item = item
            list2.append(item)
        else:
            if item != current_item:
                list2.append(item)
                current_item = item
    return list2

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    list3 = []
    for item1 in list1:
        if item1 in list2:
            list3.append(item1)
    return list3

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in both list1 and list2.

    This function can be iterative.
    """ 
    list1_index = 0
    list2_index = 0
    list3 = []
    while list1_index != len(list1) and list2_index != len(list2):
        #print "Loop:"
        if list1[list1_index] <= list2[list2_index]:
            list3.append(list1[list1_index])
            list1_index += 1
        else:
            list3.append(list2[list2_index])
            list2_index += 1
        #print list3
    if list1_index == len(list1):
        for item in list2[list2_index:]:
            list3.append(item)
    else:
        for item in list1[list1_index:]:
            list3.append(item)
    return list3
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    #print "Merge_Sort:"
    #print list1
    if len(list1) == 1 or len(list1) == 0:
        #print "Returned" + str(list1)
        return list1
    else:
        #print "Split lists:" + str(list1[0:len(list1)/2]) + " and " + str(list1[len(list1)/2:])         
        return merge(merge_sort(list1[0:len(list1)/2]), merge_sort(list1[len(list1)/2:]))    

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    list3 = []    
    #print "Word: " + str(word) + " Length: " + str(len(word))
    if len(word) == 0:
        list3.append("")
        return list3
    if len(word) == 1:
        list3.append("")
        list3.append(word)
        #print list3
        return list3
    
    first, rest = word[:1], word[1:]        
    rest_strings = gen_all_strings(rest)
    for rest_word in rest_strings:
        list3.append(rest_word)
        for index in range(len(rest_word)+1):            
            list3.append(rest_word[:index] + first + rest_word[index:])            
    return list3

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """    
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)

    list3 = []
    for line in netfile.readlines():
        list3.append(line[:-1])
    return list3

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
# run()

#print load_words("assets_scrabble_words3.txt")    
#print gen_all_strings('ab')
