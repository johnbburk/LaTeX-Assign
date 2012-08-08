# Problem DB builder and inspector
# Prints PDF of problems in DB matching search string(s)

import glob
import os
import subprocess

def searchlist(list, value):
    for i in range(len(list)):
        if list[i] == value:
            return 'yes'
    else:
        return 'no'   

# Build DB
# Find .tex files
os.chdir("/Users/jgates/desktop/latex/pics")

masterqlist = []
masternumlist = []

for files in glob.glob("*.tex"):
    jim = files[:-(len(files)-1)].isdigit() * 2 #why couldn't I just ask if files[:-(len(files)-1)].isdigit() = 'True'?
    if jim == 2:
        masterqlist.append(files)

# Build dictionary with Q # as key, associated tags as list inside
problemDB = dict()
# Build dictionary with Q # as key, description as list inside
descriptionDB = dict()
# Define master tag list
MasterTag = []

# for each file:
for i in range(len(masterqlist)):
    #define filename
    filename = masterqlist[i]
    # open it
    currfile = open(filename, 'r')
    # make key, add to masternumlist
    currkey = masterqlist[i][:-4]
    masternumlist.append(currkey)
    # read tags
    tagline = currfile.readline()
    tagline = currfile.readline()
    tagline = tagline[2:]
    # read description
    desc = currfile.readline()[2:]
    descriptionDB[currkey]=desc
    # read image file
    
    # make tags into a list, add to master tag list
    tags = tagline.split()
    for i in range(len(tags)):
        MasterTag.append(tags[i])
    # add problem to DB
    problemDB[currkey]=tags
    # close file
    currfile.close()

# Remove duplicates from master tag list
MasterTag = list(set(MasterTag))
print MasterTag
    
# print problemDB.items()
print 'There are', len(problemDB), 'problems in the database.'

# Get search tags
Tagtemp = raw_input('Search tags? (separate with spaces) ')
Searchtags = Tagtemp.split()
# print Searchtags

# Find problems
# define list holding problem numbers of the query results
Queryresults = masternumlist

# Perform search for all tags in list (must be present in each) [debugging comments below!)
for j in range(len(Searchtags)):
    #print 'Searching for: ', Searchtags[j]
    for i in Queryresults[:]:
        #print i
        #print 'Pnum: ', i, problemDB[i]
        #print 'Stag: ', Searchtags[j]
        if searchlist(problemDB[i],Searchtags[j]) == 'no':
            #print 'no'
            #print i
            #print Queryresults
            #print masternumlist
            Queryresults.remove(i)
            #print Queryresults
            #print masternumlist
        #else:
            #print 'yes'
# Display problem list
for i in range(len(Queryresults)):
    print Queryresults[i], r':', descriptionDB[Queryresults[i]], r' (', ','.join(problemDB[Queryresults[i]]), r')'

# Print LaTeX document with query results
# open tex file
if Tagtemp <> '':
    outname = Tagtemp + r'.tex'
else:
    outname = 'AllProblems.tex'
fileout = open(outname, 'w')
# write header
fileout.write(r'\input{/Users/jgates/desktop/latex/headerforinput.tex}')
fileout.write('\n' + '\n')
if Tagtemp <> '':
    fileout.write('{\Large Problems tagged with standards:}'+ Tagtemp +'\n' + '\\bigskip \n')
else:
    fileout.write('{\Large All problems:}'+ Tagtemp +'\n' + '\\bigskip \n')
# open and include problems in list (w/page breaks)
for i in range(len(Queryresults)):
    pfilename = Queryresults[i] + '.tex'
    pfile =open(pfilename, 'r')
    for thisline in pfile:  
        #print thisline[20:27]
        #raw_input ("")
        if thisline[1:6] == 'vfill' :
            fileout.write(r'\bigskip ')
            #print 'vfill'
        elif thisline[20:27] == 'ProbNum': 
            pnumline= r'{\bf \Large{' + Queryresults[i] + r'.' + thisline[28:]
            fileout.write(pnumline)
            #print pnumline
        elif thisline[1:7] == 'vspace':
            fileout.write(r'\bigskip ')
            #print 'vspace'
        elif thisline[1:8] == 'newpage':
            fileout.write(r'\vspace{6mm}')
            #print 'newpage'    
        else:
            fileout.write(thisline)
    pfile.close()

fileout.write(r'\end{document}')
fileout.close()

# Render PDF
subprocess.check_output((r'/usr/local/texlive/2011/bin/universal-darwin/pdflatex', r'-aux-directory=/Users/jgates/desktop/latex/aux' , r'-output-directory=/Users/jgates/desktop' , outname))
delfile = r'/Users/jgates/desktop/' + outname[:-4] + r'.log'
os.remove(delfile)        

# Open document with Preview
outname = r'open /Users/jgates/desktop/' + outname[:-4] + r'.pdf'
os.system(outname)
    
# Display standard count

# Open problems



