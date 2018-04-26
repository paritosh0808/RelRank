f = file("AesopTales.txt")

counter = 1
wfilename = 'aesop'+ str(counter) + '.txt'
#print wfilename

wf = file(wfilename, "w")

found_first = -1
found_second = -1
for line in f:
	#print line
	wf.write(line)

	if found_first != 1:
		found_first = 0


#	if found_first is 1 and line.isspace() found_seond = 1
#	found_first = 0	
	if line.isspace():
		if found_first == 1:
			found_second = 1
		else:
			found_first = 1
	else:
		found_first = -1
		found_second = -1
		

	if found_second == 1:
		wf.close()	

		counter += 1	
		wfilename = 'aesop'+ str(counter) + '.txt'
		#print wfilename

		wf = file(wfilename, "w")
	
	#print found_first, found_second

	#print found_first

f.close()
wf.close()

#with open("AesopTales.txt") as f:
	
#	while counter != 2
#		for line in f:
			
#		with open("tale1.txt", "w") as f1:
#		    f1.writelines(lines)
