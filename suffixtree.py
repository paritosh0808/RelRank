from operator import itemgetter, attrgetter, methodcaller
import os
import re

class SuffixTree(object): 

    count = 0
    acc_match= ''
    lowest_match_index = 0
    length = 0;
    leaf_node_index= None

    class Node(object):
        def __init__(self, lab,index):
            self.lab = lab # label on path leading to this node
	    self.index = index # index for only leaf node
            self.out = {}  # outgoing edges; maps characters to nodes
	
	    #print 'Adding a new node:', lab, index
    
    def __init__(self, s):
        """ Make suffix tree, without suffix links, from s in quadratic time
            and linear space """
        s += '$'

	#print 'String is ', s
	self.length = len(s)

        self.root = self.Node(None, 0)
        self.root.out[s[0]] = self.Node(s,0) # trie for just longest suf
	#print self.root.lab, self.root.out
	# self.root.out.update = {s[0], self.Node(s)}
        # add the rest of the suffixes, from longest to shortest
        for i in xrange(1, len(s)):
	    #print 'next char is ', i, s[i]
            cur = self.root
	    #print cur.lab, cur.out
            j = i
            while j < len(s):
		#print 'while j < len(s) loop with j= ', j, s[j]
		#print cur.lab, cur.out
                if s[j] in cur.out:
		    #print 'Found edge with char'
                    child = cur.out[s[j]]
                    lab = child.lab

		    #print 'child is ', child.lab

                    # Walk along edge until we exhaust edge label or
                    # until we mismatch
                    k = j+1 
                    while k-j < len(lab) and s[k] == lab[k-j]:
			#print 'k= ', k, 'and s[k] = ', s[k]
                        k += 1
                    if k-j == len(lab):
			#print 'exhusted edge'
                        cur = child # we exhausted the edge
                        j = k
                    else:
			#print 'fell of in the middle of edge'
                        # we fell off in middle of edge
                        cExist, cNew = lab[k-j], s[k]
			#print "cExist & cNew = ", cExist, cNew
			# create "mid": new node bisecting edge
                        mid = self.Node(lab[:k-j], 0)
                        mid.out[cNew] = self.Node(s[k:], i)
			
			# original child becomes mid's child
                        mid.out[cExist] = child
			#print "Mid is ", mid.lab, mid.out

			# original child's label is curtailed
                        child.lab = lab[k-j:]
			#print "orgincal child is now ", child.lab, child.out

                        # mid becomes new child of original parent
                        cur.out[s[j]] = mid
			#print "cur node is now ", cur.lab, cur.out
                else:
                    # Fell off tree at a node: make new edge hanging off it
		    #print 'Did not find edge with char'
                    cur.out[s[j]] = self.Node(s[j:], i)
		    #print 'Updated ', cur.lab, cur.out
    
    def followPath(self, s):
        """ Follow path given by s.  If we fall off tree, return None.  If we
            finish mid-edge, return (node, offset) where 'node' is child and
            'offset' is label offset.  If we finish on a node, return (node,
            None). """
        cur = self.root
        i = 0
	self.acc_match = ''
        while i < len(s):
            c = s[i]
            if c not in cur.out:
		#print 'fell of at a node'
                return (0,None, None) # fell off at a node
            child = cur.out[s[i]]
            lab = child.lab
            j = i+1
            while j-i < len(lab) and j < len(s) and s[j] == lab[j-i]:
                j += 1
            if j-i == len(lab):
		#print 'exhausted edge'
                cur = child # exhasted edge
		self.acc_match += lab 
                i = j
            elif j == len(s):
		self.acc_match += lab[:j-i]
		#print'exhausted query string in middle of edge'
                return (1, child, j-i) # exhausted query string in middle of edge
            else:
		self.acc_match += lab[:j-i]
		#print 'fell off in the middle of the edge'
                return (0, child, None) # fell off in the middle of the edge
	#print 'exhausted query string at internal node'
        return (1, cur, None) # exhausted query string at internal node
    
    def hasSubstring(self, s):
        """ Return true iff s appears as a substring """
        found, node, off = self.followPath(s)
        return node is not None
    
    def hasSuffix(self, s):
        if node is None:
            return False # fell off the tree
        if off is None:
            # finished on top of a node
            return '$' in node.out
        else:
            # finished at offset 'off' within an edge leading to 'node'
            return node.lab[off] == '$'

    def print_node(self, node):
	print node.lab, node.index, node.out
	for key in node.out: 
		self.print_node(node.out[key])

    def count_leaves(self, node): 
	#print node.lab, node.out
	if bool(node.out): 	
		for key in  node.out:
			self.count_leaves(node.out[key])
	else:
		print 'Match found in the following file at index', node.index
		if node.index < self.lowest_match_index:
			self.lowest_match_index = node.index
		self.count = self.count + 1	
	return self.count

    def count_leaves_lowest(self, node): 
	#print node.lab, node.out
	if bool(node.out): 	
		for key in  node.out:
			self.count_leaves_lowest(node.out[key])
	else:
		#print 'match @', node.index
		if node.index < self.lowest_match_index:
			self.lowest_match_index = node.index
		self.count = self.count + 1	
	return self.count

    def all_count(self, s):
	#print 'Looking for match for', s
	self.count = 0
	found, node, off = self.followPath(s)
	#print off
	if found is not 0:
		self.lowest_match_index = self.length + 1
		self.count_leaves(node)
		#print 'Lowest index matched', self.lowest_match_index		
		#print 'matched ', self.acc_match
	#else:
		#print 'no occurance found'
		#print 'closest matched',  None if self.acc_match is '' else self.acc_match
	return (found, self.lowest_match_index, self.count)	


    def first_count(self, s):
	#print 'Looking for match for', s
	self.count = 0
	found, node, off = self.followPath(s)
	#print off
	if found is not 0:
		self.lowest_match_index = self.length + 1
		self.count_leaves_lowest(node)
		#print 'Lowest index matched', self.lowest_match_index		
		#print 'matched ', self.acc_match
	#else:
		#print 'no occurance found'
		#print 'closest matched',  None if self.acc_match is '' else self.acc_match
	return (found, self.lowest_match_index, self.acc_match)

    def first_leaf(self, node):
		#print node		
		if bool(node.out): 	
			#for key in  node.out:
			#print node.out.values()[0]
			self.first_leaf(node.out.values()[0])
		else:
			self.leaf_node_index = node.index			
			print 'match @', self.leaf_node_index
			return 
		

    def first_match(self,s):
		print 'Looking for first match for', s
		self.leaf_node_index = None
		found, node, off = self.followPath(s)
		#print node
		#if node is not None:
		if found is not 0:
			#self.lowest_match_index = self.length + 1
			self.first_leaf(node)
			#print 'leaf node index is', self.leaf_node_index
			#print self.first_leaf(node), 'is the index of the first ocurrence'
			print 'First occurence at index:', self.leaf_node_index		
			#print 'matched ', self.acc_match
		else:
			print 'no occurance found'
			self.first_leaf(node)
			#print 'leaf node index is', self.leaf_node_index
			#print self.first_leaf(node), 'is the index of the first ocurrence'
			#print 'First occurence at index:', self.leaf_node_index		
			print 'closest matched',  None if self.acc_match is '' else self.acc_match, 'found at index', self.leaf_node_index


def processTree():
	fn_list = []
	fn_list.append("")
	files = [f for f in os.listdir('.') if (os.path.isfile(f) and (re.match(r'.*\.txt',f)	))]
	for each in files:
		fn_list.append(each)
	print "The text files in this directory are",files
	stree = []
	stree.append(None) 
	for i in range(1,len(fn_list)):
		#fn_list.append('Tales/aesop' + str(i) + '.txt')
		#print "Searching in file", fn_list[i]
		f = open(fn_list[i])
		#print f.readline()
		stree.append(SuffixTree(f.read()))
		#print stree[i]
		f.close()
	return (stree, fn_list)

def first_occurence(qstring, fn_list, stree):
	for i in range(1,len(fn_list)):                
		f = open(fn_list[i])
		result, index, match_string = stree[i].first_count(qstring)
		if result is 1:
			print "\nMatch found in the following file at index", index
			f.seek(0, 0)
			print f.name
		else:
			print "\nMatch NOT found in the following file"
			print f.name
			print "The closest match was",None if match_string is '' else match_string
			print ""
		
		f.close()	


def all_occurence(qstring, fn_list, stree):
	for i in range(1,len(fn_list)):                
		f = open(fn_list[i])
		result, index, all_count = stree[i].all_count(qstring)
		if result is 1:
			print "Match found in the following file at index", index
			print "Total",all_count,"matches found"
			f.seek(0, 0)
			print f.name
		#else:
		#	print "Match NOT found in the following tale"
		#	print f.readline()
		#	print "The closest match was",None if match_string is '' else match_string


def relevance(qstring, fn_list, stree):
	#print len(fn_list)
	qwords = qstring.split()
	rel_score = [0 for x in range(len(fn_list))]
	score_card = []

	for i in range(1, len(fn_list)):
		f = open(fn_list[i])
		# first algo: relevance by exact match
		result, index, all_count = stree[i].first_count(qstring)
		if result is 1:
			rel_score[i] += stree[i].count * 100;
			
		else:
			#second algO: relevance by match of # of words anywhere in the tale
			words_match_count = 0
			for j in range(len(qwords)):
				result, index, all_count = stree[i].first_count(qwords[j])
				if result is 1:
					words_match_count += 1;

			#if words_match_count == len(qwords):
			#	rel_score[i] += 50;

			if words_match_count != 0:
				rel_score[i] += int(50*words_match_count/len(qwords)) ;

		f.seek(0)
		score_card.append((fn_list[i], f.readline(), rel_score[i]))

		f.close()

	sorted_sc = sorted(score_card, key=itemgetter(2,1), reverse = True)	
	print"Top relevant matches are:"
	top = min(10, len(sorted_sc))
	for i in range(top):
		print sorted_sc[i][2],'=>', sorted_sc[i][0]
		




