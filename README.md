# RelRank
Ranks text files given a query string on the basis of their relevance scores. 
Also displays 
all the occurrences of the given query string, 
the first occurrence and the longest matched substring if none is present. 
Implemented using Suffix Trees.

The makedoc.py splits the file documents into separate files. The result is the files that are in the folder named 'Tales'.
A suffix tree is then constructed constructed for each of these files using the processTree() function in suffixtree.py.
The program is executed from str-run-me.py

Link for report: https://drive.google.com/file/d/0B_NxPFkhUh78TVR2T2JJVERKYzQ/view?usp=sharing
