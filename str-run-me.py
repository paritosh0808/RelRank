import suffixtree
import sys

list1 = sys.argv
#print list1
stree, fn_list = suffixtree.processTree()
qstring = list1[2]
flag = list1[1]
if flag == '1':
	suffixtree.all_occurence(qstring, fn_list, stree)
elif flag == '2':	
	suffixtree.first_occurence(qstring, fn_list, stree)
elif flag == '3':
	suffixtree.relevance(qstring, fn_list, stree) 

#print 'Printing Tree'
#stree.print_node(stree.root)
#stree.all_count('b')
#stree.first_count('bbbd')
#stree.first_match('ab');q
