from __future__ import division
import numpy as np
import csv
from nltk.corpus import *
import re
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'[a-zA-Z]\w+')

# read the look up file for diseases and symptoms
dd = pd.read_csv("dd.csv") 
dd = dd.as_matrix()
# set no of files to read to create the dataset 
howmany=1

for hm in range(howmany):
	infection = pd.read_csv("file"+str(hm)+".csv")
	infection = infection.as_matrix()
	
	rows = infection.shape[0]
        #print rows
	cols = [0,2] # include the indices you want each index is a column header like doctor statement etc.
	start = 1001    
	end = 1002    # set this to rows if you want full file or keep it less than rows for partial file
	#print 'taking ', end
	drugs=[]
	diseases=[]
	symptoms=[]
	
	dic={}
	
	dd_rows = dd.shape[0] # use end for manual input
	for i in range(dd_rows):
		text = dd[i,0]
		out2 = tokenizer.tokenize(text)
		for j in out2:
			j=j.upper()
			dic[j]='DIS'
	
	dd_rows = dd.shape[0]
	for i in range(dd_rows):
		text = dd[i,1]
		if type(text)==str:
			out2 = tokenizer.tokenize(text)
			for j in out2:
				j=j.upper()
				dic[j]='SYM'




        # Apply Naive Bayes to the data so that we can get best possible automated labelling.
	f=open('ner categories data.csv')
	f=csv.reader(f)
	
	x=[]
	y=[]
	
	for row in f:
		temp=(re.sub('[^A-Za-z0-9]+ ', '', row[0]).upper())
		for i in temp.split():
			x.append(i)
			y.append(row[1])
	
	
	x=np.array(x).reshape(len(x),1)    
	y=np.array(y).reshape(len(y),1)
	
	
	def prob_jt_dis(word):
		sum1=0
		sum2=0
		for i in np.arange(len(x)):
			if ((str(x[i][0])==str(word))*(str(y[i][0])=='dis')):
				sum1=sum1+1
			if ((str(y[i][0])=='dis')):
				sum2=sum2+1
		return (sum1/sum2)
	
	
	def prob(word):
		sum=0
		for i in np.arange(len(x)):
			if ((str(x[i][0])==str(word))):
				sum=sum+1
		return (sum/len(x))


	def prob_jt_sym(word):
		sum1=0
		sum2=0
		for i in np.arange(len(x)):
			if ((str(x[i][0])==str(word))*(str(y[i][0])=='sym')):
				sum1=sum1+1
			if ((str(y[i][0])=='sym')):
				sum2=sum2+1
		return (sum1/sum2)
	
	
	def bayes_prob(word):
		p_sym=0.3157
		p_dis=0.6837
		res=[]
		if (prob(word)!=0.0 and prob(word)!=0):
			res.append(prob_jt_dis(word)*p_dis/prob(word))  
			res.append(prob_jt_sym(word)*p_sym/prob(word))
		else:
			res.append(0)
			res.append(0)
		return (res)


	for i in dic.keys():
	#	print i
		probl = bayes_prob(i)
		if probl[0]==0 and probl[1]==0:
			dic[i]='O'
		elif probl[0] >= probl[1]:
			dic[i] = 'DIS'
		else:
			dic[i]='SYM'
	
	# Bayes ends here

        # remove the basic words which have almost no meaning like the of for etc.
	setstopwords = set(stopwords.words('english'))
	ll = list(setstopwords)
	llnew = []
	for i in ll:
		llnew.append(i.encode('ascii','replace').upper())
	
	for i in llnew:
		dic[i]='O'
	
	#set the labels for the words
	for rs in range(start,end):
		for elem in cols:
			text = infection[rs,elem]
			if type(text)==str:
				out = tokenizer.tokenize(text)
				for i in out:
					i=i.upper()
					if i in dic:
						print i#, '\t', dic[i]
					else:
						print i#, '\t', 'O' 
