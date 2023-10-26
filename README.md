# breaking-onetimepad-enc-with-reused-key
One-Time Pad (OTP) encryption is theoretically unbreakable when used properly. However, This code describes a method for breaking OTP encryptions. The code takes advantage of the fundamental weakness of reusing OTP keys, and knowing a small part of the plaintext, this can be leveraged to break the encryption.

# approach
my approach is that i will be making use of the fact that cypher text containg english letters and spaces only

first c1 XOR c2 = m1 XOR m2

-difference between space and letter in hex is that the first hex char of space has 0 in its 2nd bit from left -while first hex char of all leters has 1 in its 2nd bit from left

-so i can make XOR operation between all each 2 bytes in each 2 cyphers and repeat for all

-so that if the XOR result == 1 i for sure found a space in either m1 or m2 (or both bytes are same)

-to make a decision i will use a count that counts the needed XOR result with all rows in cypher so that if count > 4 now i know that this cypher text contains the space

-now i have an array of possible space positions

-XOR the matching cypher position with 20 (space) in hex to get key part

-now i have key parts so XOR again with cypher text to get plain text parts
