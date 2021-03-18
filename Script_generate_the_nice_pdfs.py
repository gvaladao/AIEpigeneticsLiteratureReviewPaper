### This is the script used to format in nice pdf files the information retrieved from Pubmed for 
### the literature review  paper entitled "Artificial Intelligence in Epigenetic studies: 
### shedding light on Rare Diseases" whose authors are Sandra Brasil, Catia Neves, tatiana Rijoff, Marta Falcao, 
### Goncalo Valadao, Paula A. Videira, Vanessa dos Reis Ferreira. It requires Latex.



import os
from pylatex import Document, Section, Subsection, Command, LargeText
from pylatex.utils import italic, NoEscape, bold
#from Bio import Entrez, Medline
# import bio
import pickle
os.chdir(os.path.dirname('whatecer directory the file papers.dat is'))
with open("papers.dat", "rb") as fp:   # Unpickling
   papers = pickle.load(fp)


i = 0
for p in papers:
  doc = Document()
  doc.preamble.append(Command('title',p['TI']))
  doc.preamble.append(Command('author',';  '.join(p['FAU'])))
  doc.preamble.append(Command('date',p['EDAT']))
  #doc.append(NoEscape(r'\maketitle'))
  with doc.create(Section('A second section')):
    doc.append(NoEscape(r'\maketitle'))
    doc.append(LargeText(bold('Abstract\n\n')))
    doc.append('\n')
    doc.append(p['AB'])
    doc.append('\n\n\n\n')
    doc.append('Mesh Terms\n')
    if 'MH' in p:
      doc.append(p['MH'])
      doc.append('\n\n')
    doc.append(p['SO'])
    doc.append('\n\n')
    doc.append('PMID: ' + p['PMID'])
    doc.append('\n\n')
    if 'PMC' in p:
      doc.append('PMC: ' + p['PMC'])
    doc.generate_pdf(str(i+1), clean_tex=True)
    
  i = i+1
  print(i)
  #if i > 0:
  #  break

