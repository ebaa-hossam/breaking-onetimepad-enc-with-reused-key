# -*- coding: utf-8 -*-
"""breaking-onetimepad.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1X6VuOgIW8isAMj6KSRWRbxDw-XZNfBk0
"""

import numpy as np

"""my approach is that i will be making use of the fact that cypher text containg english letters and spaces only

first c1 XOR c2 = m1 XOR m2

-difference between space and letter in hex is that the first hex char of space has 0 in its 2nd bit from left
-while first hex char of all leters has 1 in its 2nd bit from left

-so i can make XOR operation between all each 2 bytes in each 2 cyphers and repeat for all

-so that if the XOR result == 1 i for sure found a space in either m1 or m2 (or both bytes are same)

-to make a decision i will use a count that counts the needed XOR result with all rows in cypher so that if count > 4 now i know that this cypher text contains the space

-now i have an array of possible space positions

-XOR the matching cypher position with 20 (space) in hex to get key part

-now i have key parts so XOR again with cypher text to get plain text parts
"""

cyphertext1 = np.array(['A84537EC762D276D2804F0051C76FBB61DA962A904055BCF56D2E08BA3',
       'BF4334AA672868223800E103066AA8F709AF6FEC0E105CCB52D4E691BE',
       'B85530EE332C62612B13E7570A77ECFF12BC27EE150D51CD5FC9E19BA3',
       'A45527EF617F75672B12E7570676EDB608B26AEC401454CC13CBEA87A3',
       'BF4035EB673A277B3114F0571A61FBE219B674A9120152DD5FC1FD92A9',
       'A31022E272336B222913EB030C38FBF31FAE75EC40175ACE47D7EE8CB5'])

def get_space_position(cyphertext):
  position = np.array([0,0]) #to indicate that array takes 2 elements per row
  for j in range (0,58,2): #looping over hex characters with step 2 as space = 20
    for i in range (6): #range of number of cyphertext rows
      count = 0
      for l in range (6):
        c1 = cyphertext[i][j] #getting ith row cypher text and jth column
        c2 = cyphertext[l][j] #for comparing it with all rows in cypher text with same jth column
        text = int(c1, 16) ^ int(c2, 16)
        text =  format(text, 'X') #back to hex
        if ((text == '4') or #checking if 2nd bit from left == 1
         (text == '5') or #indicating a space is xor-ed with letter
          (text == '6') or
           (text == '7') or
            (text == 'C') or
             (text == 'D') or (text == 'E') or (text == 'F') or (text == '0')):
          count = count + 1 #count incremented for notice
          if count > 4:
            position = np.vstack((position , np.array([i,j]))) #then this position is space
            break
        else :
          break
  np.delete(position, 0, 0) #no need for initial row now

  sorted_indicesp = np.lexsort((position[:, 1], position[:, 0])) # Get the sorted indices based on the first column
  sorted_p = position[sorted_indicesp] # Sort the array based on the sorted indices
  return sorted_p #return sorted space positions array

def get_key_part(cyphertext, space_position):
  key1 = np.full((58), "*", dtype='U1') #initiating all to *
  for i in range (6): #looping through rows of cyphertext
    for m in range (len(space_position)): #looping through rows of spaces positions
      if i == space_position[m][0] : #finding the matching row cypher position with row space position
        for j in range (0,58,2): #looping through columns
          if (j) == space_position[m][1]: #finding matching column cypher position with colomn space position
            c1 = cyphertext[i][j]
            key_part1 = int(c1, 16) ^ int('2', 16) #xoring the cypher text first byte with 2 (20 for space)
            key1[j] = format(key_part1, 'X') #back to hex
            key1[j + 1] = cyphertext[i][j + 1] #no need to do another xor as xor any with 0 = any
  return key1 #returning key parts in hex

def decrypt_key(cyphertext,key):
  plaintext = np.full((6,29), "*", dtype='U1')
  for i in range (0,6):
    for m in range (0,58,2):
      if key[m] != "*" : #only if i have the key part
        c1 = cyphertext[i][m]
        c2 = cyphertext[i][m + 1]
        p1 = format((int(c1, 16) ^ int(key[m], 16)), 'X') #first hex of plain text
        p2 = format((int(c2, 16) ^ int(key[m + 1], 16)) , 'X') #second hex of plain text
        p = str(p1) + str(p2) #concatenating both hex characters to convert to ascii
        byte_string = bytes.fromhex(p) #to byte
        ascii = byte_string.decode('utf-8') #to ascii
        if ((ascii.isalpha()) or (ascii.isspace())): #checking if its alpha letters or space
          plaintext[i][int(m/2)] = ascii
  return plaintext #return plaintext in english

def decrypt_one_time_pad(cyphertext):
  spaces = get_space_position(cyphertext)
  key_parts = get_key_part(cyphertext , spaces)
  message_parts = decrypt_key(cyphertext , key_parts)

  for index in range(6):
    print(' '.join(message_parts[index]))

decrypt_one_time_pad(cyphertext1)

"""2nd step :
guessing words
1st row words:
  1st >>  buffer
  2nd >> overruns
2nd row words:
  1st >>  use
  2nd >>  two
  last >> authentication
3rd row words:
  2nd >> secure
  3rd >> coding
4th row words:
  1st >> never
  2nd >> reuse
  3rd >> one
  4th >> time
5th row words:
  1st >> update
6th row words:
  1st >> i
  4th >> secure


then using these guesses i can re update the key to find the rest
or as i did guess the rest from the context

buffer overruns are dangerous
use two factor authentication
read secure coding guidelines
never reuse one time pad ********
i shall ****** secure *********

buffer overruns are dangerous
use two factor authentication
read secure coding guidelines
never reuse one time pad *********
i shall ******* secure *********
"""