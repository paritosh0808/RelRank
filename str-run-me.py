import suffixtree

print "Building Tree.."
stree, fn_list = suffixtree.processTree()
while(1):
	qstring = input("Enter the query string: ")
	flag = input("Press 1. to find all the occurences of the query string, 2 for the first occurence and 3 to list documents by relevance: ")
	if flag == 1:
		suffixtree.all_occurence(qstring, fn_list, stree)
	elif flag == 2:	
		suffixtree.first_occurence(qstring, fn_list, stree)
	else:
		suffixtree.relevance(qstring, fn_list, stree) 

#print 'Printing Tree'
#stree.print_node(stree.root)
#stree.all_count('b')
#stree.first_count('bbbd')
#stree.first_match('ab');
