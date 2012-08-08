# Assessment maker


import sys
import os
import csv
import string
import subprocess

# open standards order file, store order of standards for rubrics
stdlistfile = open('stdlist.tex', 'r')
stdorder = []
for lines in stdlistfile:
    stdorder.append(lines[:-1])

# Print the reassessments
#
# time: 0, name: 1, section: 2, Hstd: 3, Date: 4, Actions: 5
# Pstd: 6, #: 7, didit: 8, ready: 9, Pnum: 10

# Name section

namesection = []

    
# name
name = raw_input('Assessment name: ')
section = raw_input('Class/section: ')
namesection.append('\n' + r'% Name section'+'\n' + r'\noindent \hfill {\sc {\bf {\Large ' + name + r' }}}' +'\n')
# Assessment name
#namesection.append(name + '}' + '\n')
#print row[1], r'/' ,row[2], r'/', row[6], r'/', row[10]
        #if row[3] <> '.':
        #    namesection.append(row[3] + '}' + '\n')
        #    print row[1], r'/', row[2], r'/', row[3], r'/', row[10]
# section
namesection.append(r'\noindent \hfill {\sc ' + section + r' }' + '\n' + r'\bigskip' + '\n')
        
# test namesection list
#for i in range(len(namesection)):
    #print namesection[i]


# open file
filename = ''
filename = '/Users/jgates/desktop/Assessments/' + ''.join(e for e in name if e.isalnum()) + '.tex'
#print filename
reassessfile = open(filename, 'w')
        
# write header
        
reassessfile.write(r'\input{/Users/jgates/desktop/latex/headerforinput.tex}')
reassessfile.write('\n')

# write name section
for rows in namesection:
    reassessfile.write(rows)
    reassessfile.write('\n')

# write problems
reassessfile.write(r'% Questions section' + '\n')
# which problems?
probinput = raw_input('Problem List (separate by spaces): ')
problemlist = probinput.split()
#print problemlist
# open problems and write to reassessment
# stdlist = []
for currprob in problemlist:
    probfilename = r'/Users/jgates/desktop/Latex/pics/' + currprob + r'.tex'
    probfile = open(probfilename, 'r')
    #print probfilename
    # write problem to file
    for line in probfile:
        reassessfile.write(line)
    reassessfile.write('\n')    
    probfile.close()
# Use this section later maybe for automatic standard list making
#probfile = open(probfilename, 'r')
##            # get standards list for this assessment, ones not in std file are excluded
##            stdsin = probfile.readline()
##            stdsin = probfile.readline()
##            stdtemp = stdsin[2:].split()
##            #print stdtemp
##            
##            for stds in stdtemp:
##                #if stds.upper() == stds:
##                stdlist.append(stds)
##            #print 'stripped: ', stdlist
##
##            probfile.close()
##            
##        # Remove duplicates from master tag list
##        stdlist = list(set(stdlist))
##        #print stdlist
# Get Standards Input
stdinput = raw_input('Standard List (separate by spaces): ')
stdlist = stdinput.split()

# Write standards
reassessfile.write('\n' + r'% Standards section' + '\n')
# iterate over list of all course standards
for currstan in stdorder:
    # iterate over standards in this assessment
    for stdwanted in stdlist:
          # is the standard in this position present in the reassess.?
          if currstan.upper() == stdwanted.upper():
              #print stdwanted
              stanfilename = r'standards/' + currstan + r'.tex'
              stanfile = open(stanfilename, 'r')
              #print stanfilename
              for line in stanfile:
                  reassessfile.write(line)
              reassessfile.write('\n')
# close file
reassessfile.write(r'\end{document}')
reassessfile.close()
        
# compile PDF
filename4exp = filename[:-4]
#print filename4exp
subprocess.check_output((r'/usr/local/texlive/2011/bin/universal-darwin/pdflatex', r'-aux-directory=/Users/jgates/desktop/Assessments' , r'-output-directory=/Users/jgates/desktop/Assessments' , filename4exp))
delfile = filename4exp + r'.log'
#print delfile
os.remove(delfile)

# Open document with Preview
outname = r'open ' + filename4exp + r'.pdf'
#print outname
os.system(outname)

# print PDFs
##
