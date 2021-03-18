### This is the script used to select the papers and retrieve the correspondent Medline data (Title, Abstract, etc) 
### in the literature review in the paper entitled "Artificial Intelligence in Epigenetic studies: 
### shedding light on Rare Diseases" whose authors are Sandra Brasil, Catia Neves, tatiana Rijoff, Marta Falcao, 
### Goncalo Valadao, Paula A. Videira, Vanessa dos Reis Ferreira. This script (Python 3.7.3) was run in a Linux operating system.
### At line 59 the user should replace "johndoe@mail.com" by his proper email.
### At line 60 the user should put his entrez api key

import pandas as pd
import numpy as np
import pickle
from Bio import Entrez, Medline
import time

base_path = "whateverbasepathisyours"
file_loc = base_path + "keywordsbulkmine.xls"
df = pd.read_excel(file_loc, na_values=['NA'], usecols = "A")
df=df.dropna()
rd_g = df['RD_G'].tolist()


df = pd.read_excel(file_loc, na_values=['NA'], usecols = "B")
df=df.dropna()
ai_g = df['AI_G'].tolist()


df = pd.read_excel(file_loc, na_values=['NA'], usecols = "C")
df=df.dropna()
epi_g = df['Epi_G'].tolist()


df = pd.read_excel(file_loc, na_values=['NA'], usecols = "D")
df=df.dropna()
t_g = df['T_G'].tolist()



quadrupleterms = []
for i in rd_g:
	for j in ai_g:
		for k in epi_g:
			for l in t_g:
				aterm = i.lower() + ' ' + j.lower() + ' ' + k.lower() + ' ' + l.lower()
				quadrupleterms.append(aterm)
				#print(quadrupleterms[0:3])
				
tripleterms = []
for i in rd_g:
	for j in ai_g:
		for k in epi_g:
			aterm = i.lower() + ' ' + j.lower() + ' ' + k.lower()
			tripleterms.append(aterm)
			#print(tripleterms[0:3])

allterms = quadrupleterms + tripleterms
#print(allterms)

print("############################# Finish Part1 ################################")

Entrez.email = "johndoe@mail.com"
Entrez.api_key= "put here the entrez api key"

allpmids = []

for ttt in allterms:
	handle = Entrez.esearch(db='pubmed', sort='relevance', retmax='1000', term=ttt, usehistory="n")
	pmids = Entrez.read(handle)['IdList']
	#pmids = Entrez.read(handle)
	allpmids.extend(pmids)
	print(len(allpmids))
	

allpmids = list(set(allpmids))

out_handle = open("auxiliary.txt", "w")

allpmidsaux = ','.join(allpmids)
fetch_handle = Entrez.efetch(db='pubmed', rettype='medline', retmode='text', id=allpmidsaux)
data = fetch_handle.read()
fetch_handle.close()
out_handle.write(data)
out_handle.close()


with open("auxiliary.txt") as auxilhandle:
	therecords = Medline.parse(auxilhandle)
	recordslst = list(therecords)

auxilhandle.close()

with open('papers.dat','wb') as filename:
	pickle.dump(recordslst, filename)
	
print("############################# Finish Part2 ################################")
