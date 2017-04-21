# -*- coding: utf-8
from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import sys
import re
import datetime
import holidays
from datetime import date

def convert(fname, pages=None):
  if not pages:
    pagenums = set()
  else:
    pagenums = set(pages)

  output = StringIO()
  manager = PDFResourceManager()
  converter = TextConverter(manager, output, laparams=LAParams())
  interpreter = PDFPageInterpreter(manager, converter)

  infile = file(fname, 'rb')
  #for pageNumber, page in enumerate(PDFDocument.get_pages()):
  for page in PDFPage.get_pages(infile, pagenums):
    interpreter.process_page(page)
  infile.close()
  converter.close()
  text = output.getvalue()
  output.close()
  return text

file1 = 'ementaSIBS.pdf'
file2='ementaSIBScomferiadoaumaquarta.pdf'
feriados = holidays.Portugal() #
print date(2017, 4, 14) in feriados # True
for pagenum in [0,1,2,3,4,5,6,7,8,9,10]:
  if pagenum != 4:
    continue
  print('page-----------'+str(pagenum))
  page=[pagenum]
  text = convert(file1, page)
  if len(text) == 0:
    continue
  #print(text)
 # hoje = datetime.datetime.now()
  hoje = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month,datetime.datetime.now().day,0,0,0)
  semana = re.compile(r'Semana de (\d\d)/(\d\d) a (\d\d)/(\d\d)/(\d\d\d\d)')
  dias = semana.search(text)
  print(dias.group())
  print(dias.group(1))
  print(dias.group(2))
  print(dias.group(3))
  print(dias.group(4))
  print(dias.group(5))
  
  dedia = dias.group(1)
  demes = dias.group(2)
  adia = dias.group(3)
  ames = dias.group(4)
  ano = dias.group(5)
  de = datetime.datetime(int(ano),int(demes),int(dedia), 0, 0, 0)
  a = datetime.datetime(int(ano), int(ames), int(adia), 0, 0, 0)
  print hoje
  print de
  print a
  if hoje >= de and hoje <= a and 'Alfragide' in text:
    print(text)
    if 'OPÇÃO' in text:
      print 'opção found'
#a = convert('ementaSIBS.pdf',   pages=[1,2,3,4,5,6,7,8,9,10])
#print(a)

# encontrar pagina que contem a semana onde se encontra o dia de hoje e que tenha a string 'alfragide'

# encontrar ementa do dia correspondente

# mandar para outpur

