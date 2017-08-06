# -*- coding: utf-8
#!python2

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
import shelve
import os
import dialogs
from datetime import timedelta
import appex

last_ementa=None
export_text=False
shift_feriado_ementa=9
shift_feriado_tipo_prato=0
shift_feriado_calorias=0
shift_feriado_refeicao=9
dias_feriado =[]
tipo_prato = ['Frito','Assado', 'Grelhado' , 'Cozido', 'Gratin.', 'Estufado','estufado','Grelh.','EStufado','Assada','Estufadas','Gratinados','Guisado','Gratinado','grelhado','Estufada']
refeicao = ['SOPA','PEIXE','CARNE','DIETA','OPÇÃO']
shelve_file = shelve.open('data')
ignorar = '''Nota: Os Pratos confecionados nesta ementa semanal podem conter os seguintes alergénios: cereais que contêm glúten e produtos à base destes cereais, crustáceos e produtos à base de 
crustáceos, ovos e produtos à base de ovos, peixes e produtos à base de peixe, amendoins e produtos à base de amendoins, soja e produtos à base de soja, leite e produtos à base de leite, 
frutos de casca rija e produtos à base destes frutos, aipo e produtos à base de aipo, mostarda e produtos à base de mostarda, sementes de sésamo e produtos à base de sementes de 
sésamo, dióxido de enxofre e sulfitos, tremoço e produtos à base tremoço, moluscos e produtos à base de moluscos.'''
ignorar2=['ª','Alfragide','ALMOÇO','Semana de','Nota:']
ignorar3='Semana de'
ignorar4='''Nota: Os Pratos confecionados nesta ementa semanal podem conter os seguintes alergénios: cereais que contêm glúten e produtos à base destes cereais, crustáceos e produtos à base de crustáceos, ovos e produtos à base de ovos, peixes e produtos à base de peixe, amendoins e produtos à base de amendoins, soja e produtos à base de soja, leite e produtos à base de leite, frutos de casca rija e produtos à base destes frutos, aipo e produtos à base de aipo, mostarda e produtos à base de mostarda, sementes de sésamo e produtos à base de sementes de sésamo, dióxido de enxofre e sulfitos, tremoço e produtos à base tremoço, moluscos e produtos à base de moluscos.'''
numtipo_prato =0
numrefeicao=0
numcaloria=0
numementa=0
decimal= 0
ementa=0
dia = {}
feriados = holidays.Portugal()


def reset_shift_feriado():
  global shift_feriado_tipo_prato,shift_feriado_calorias,shift_feriado_ementa,shift_feriado_refeicao
  shift_feriado_calorias=0
  shift_feriado_ementa=0
  shift_feriado_tipo_prato=0
  shift_feriado_refeicao=0

def shift_feriado(item):
  global shift_feriado_tipo_prato,shift_feriado_calorias,shift_feriado_ementa,shift_feriado_refeicao
  
  if item in tipo_prato:
    print('shift_feriado_tipo_prato: ',shift_feriado_tipo_prato)
    return shift_feriado_tipo_prato
  if item in refeicao:
    print('shift_feriado_refeicao: ',shift_feriado_refeicao)
    return shift_feriado_refeicao
  if item.isdigit():
    print('shift_feriado_calorias: ',shift_feriado_calorias)
    return shift_feriado_calorias
  print('shift_feriado_ementa: ',shift_feriado_ementa)
  return shift_feriado_ementa

def inc_shift_feriado(item):
  global shift_feriado_tipo_prato,shift_feriado_calorias,shift_feriado_ementa,shift_feriado_refeicao

  
  if item in tipo_prato:
    shift_feriado_tipo_prato+=1
    print('shift_feriado_tipo_prato: ',shift_feriado_tipo_prato)
    return shift_feriado_tipo_prato
  if item in refeicao:
    shift_feriado_refeicao+=1
    print('shift_feriado_refeicao: ',shift_feriado_refeicao)
    return shift_feriado_refeicao
  if item.isdigit():
    shift_feriado_calorias+=1
    print('shift_feriado_calorias: ',shift_feriado_calorias)
    return shift_feriado_calorias
  
  shift_feriado_ementa+=1
  print('shift_feriado_ementa: ',shift_feriado_ementa)
  return shift_feriado_ementa

#feriados =[date(2017,4,15), date(2017,5,25)]
def get_dia(diaint,mes,ano,item_count,item):
  '''
  item pode ser ementa, refeicao, tipo
  retorna tuplo com dia a usar e numero de linha onde colocar o item
  Faz a correcao para o caso de ser feriado
  '''
  print 'get_dia(%d,%d,%d,%d, %s)'%(diaint,mes,ano,item_count,item)
  item_max = 5
  if item in tipo_prato:
    item_max =4

  if item_count > item_max:   
    #diaint+=(item_count/item_max)
    dt = datetime.datetime(ano, mes, diaint)+datetime.timedelta(days=item_count/item_max)
    diaint = dt.day
    mesint = dt.month
    anoint = dt.year
    print '%d=(%d/%d)=%d'%(diaint,item_count,item_max, item_count/item_max)
    itemlinha= item_count % item_max
    if itemlinha == 0:
      itemlinha= item_max
      dt+=datetime.timedelta(days=-1)
      diaint = dt.day
      anoint = dt.year
      #diaint-=1
    while True:
      dt+= datetime.timedelta(days=shift_feriado(item))
      diaint = dt.day
      mesint = dt.month
      anoint = dt.year
      #diaint += shift_feriado
      if date(int(ano),mesint, diaint) in feriados:
        print ',1++++++++++++++++++++ %d/%d/%d'%(int(ano),mesint,diaint)
        #dia[str(diaint)][ementalinha]['ementa'] = 'Feriado'
        inc_shift_feriado(item)
      else:
        break
    print '%d=%d/%d'%(diaint,item_count, item_max)
    print '%d=%d%%%d'%(itemlinha,item_count, item_max)
  else:
    dt = datetime.datetime(ano, mes, diaint)
    while True:
      shift = shift_feriado(item)
      dt+= datetime.timedelta(days=shift)
      diaint = dt.day
      mesint = dt.month
      anoint = dt.year
      #diaint += shift_feriado
      if date(anoint,mesint, diaint) in feriados:
        print '2++++++++++++++++++++ %d/%d/%d'%(ano,mesint,diaint)
        #dia[str(diaint)][ementalinha]['ementa'] = 'Feriado'
        inc_shift_feriado(item)
      else:
        break
    itemlinha = item_count
    if item in tipo_prato:
      itemlinha+=1
    
    print '%d%d%d=%d'%(diaint,mesint,anoint,item_count)
    print '%d=%d%%%d'%(itemlinha,item_count, item_max)
  
  return (diaint,mesint,anoint,itemlinha)

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
  
def parseLine(line):
    global numtipo_prato, decimal, ignorar, ignorar2, ignorar3, refeicao, diaint,ames,ano, numcaloria, numementa, numrefeicao, numtipo_prato, last_ementa, ementa
    
    #print(demes)
    
    diaint = int(dedia)
    mesint = int(demes)
    anoint = int(ano)
    
    print('parseline(%s)' % line)
    line = line.strip()
    if len(line.strip()) == 1:
      return 
    if len(line)==0:
      return
    if line.strip() in ignorar:
      return
    if line.strip() in ignorar2:
      print 'ignorar2 matched. comtinue...'
      return      
    if line.strip() in ignorar4:
      print 'ignorar4 matched. comtinue...'
      return      
    salta = False
    for word in ignorar2:
      if line.strip().startswith(word):
          salta = True
          break
    if salta == True:              
      return   
    if last_ementa == line:
      '''duplicado, bug do parser pdf'''
      print('line duplicated')
      return
    last_ementa=line
    if line.strip() in tipo_prato:
      numtipo_prato+=1
      print line          
   
      (diaint,mesint, anoint, item_linha)=get_dia(diaint,mesint,anoint,numtipo_prato,line)
      diaidx = str(anoint) + str(mesint)+ str(diaint)
      
      print "dia[%s][%d]['tipo_prato']"%(diaidx,item_linha)
      dia[diaidx][item_linha]['tipo_prato'] = line.decode('utf-8')
      return
      
    if line.strip() in refeicao:
      numrefeicao+=1
      #print line 
      (diaint,mesint, anoint, item_linha)=get_dia(diaint,mesint,anoint,numrefeicao,line)
      diaidx = str(anoint) + str(mesint)+ str(diaint)
      print "dia[%s][%d]['refeicao']"%(diaidx,item_linha)  
      
      if int(diaidx) > maxdia:
        '''refeicao tb existe em feriados
         '''
        print '%s (dia) > %d (maxdia)'%(diaidx,maxdia)
        return 
        
      dia[diaidx][item_linha]['refeicao'] = line.decode('utf-8')
      
      return
  
    if line.strip().isdigit():
      decimal+=1
      
      (diaint,mesint, anoint, item_linha)=get_dia(diaint,mesint,anoint,decimal,line)
      diaidx = str(anoint) + str(mesint)+ str(diaint)
      print "dia[%s][%d]['calorias']"%(diaidx,item_linha)  
      dia[diaidx][item_linha]['calorias'] = line.decode('utf-8')
      return 
      
    ementa+=1
    
    
    (diaint,mesint, anoint, ementalinha)=get_dia(diaint,mesint,anoint,ementa,line)
    
    diaidx = str(anoint) + str(mesint)+ str(diaint)
    print "dia[%s][%d]['ementa']" % ( diaidx, ementalinha)
    dia[diaidx][ementalinha]['ementa'] = line.decode('utf-8')
    #last_ementa = line
  
def get_pdf_from_user():
    pdf_files = [f for f in os.listdir(os.curdir) if f.endswith('.pdf')]
    return dialogs.list_dialog(title='pdf de ementa', items=pdf_files)

filename=''
if appex.is_running_extension():
  file_paths = appex.get_file_paths()
  for i, file in enumerate(file_paths):
    if file.endswith('.pdf'):
    	print(file)
    	filename=file
else:
  filename = get_pdf_from_user()
if filename is None:
  exit()
file1 = 'ementaSIBS.pdf'
file2='ementaSIBScomferiadoaumaquarta.pdf'
feriados = holidays.Portugal() #
print date(2017, 4, 14) in feriados # True
for pagenum in [0,1,2,3,4,5,6,7,8,9,10]:
  if pagenum !=4 :
    #continue
    pass

  print('page-----------'+str(pagenum))
  page=[pagenum]
  textPage = convert(filename, page)
  if len(textPage) == 0 or 'Alfragide'   not in textPage:
    continue
  #print(text)
 # hoje = datetime.datetime.now()
  hoje = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month,datetime.datetime.now().day,0,0,0)
  semana = re.compile(r'Semana de (\d\d)/(\d\d) a (\d\d)/(\d\d)/(\d\d\d\d)')
  dias = semana.search(textPage)
  
  
  dedia = dias.group(1)
  demes = dias.group(2)
  adia = dias.group(3)
  ames = dias.group(4)
  ano = dias.group(5)
  de = datetime.datetime(int(ano),int(demes),int(dedia), 0, 0, 0)
  a = datetime.datetime(int(ano), int(ames), int(adia), 0, 0, 0)
  diaint = int(dedia)
  mesint = int(demes)
  anoint = int(ano)
  diaidx = ano + demes + dedia
  maxdia = int(diaidx)
    
  if diaidx not in dia.keys(): 
      #reset counters
      reset_shift_feriado()
      numtipo_prato=0
      decimal=0
      ementa=0
      numrefeicao=0
      
      for i in range(0,5):
        dt = datetime.datetime(anoint,mesint,diaint  )+datetime.timedelta(days=i)
        diai = str(dt.year) + str(dt.month) + str(dt.day)
        print('->%s',diai)
      
        dia[diai]= {}        
        dia[diai][ementa+1] = {}
        dia[diai][ementa+2] = {}
        dia[diai][ementa+3] = {}
        dia[diai][ementa+4] = {}        
        dia[diai][ementa+5] = {}
        
        dia[diai][ementa+1]['tipo_prato'] = {}
        dia[diai][ementa+2]['tipo_prato'] = {}
        dia[diai][ementa+3]['tipo_prato'] = {}
        dia[diai][ementa+4]['tipo_prato'] = {}        
        dia[diai][ementa+5]['tipo_prato'] = {}
        
        dia[diai][ementa+1]['calorias'] = {}
        dia[diai][ementa+2]['calorias'] = {}
        dia[diai][ementa+3]['calorias'] = {}
        dia[diai][ementa+4]['calorias'] = {}
        dia[diai][ementa+5]['calorias'] = {}
        
        dia[diai][ementa+1]['refeicao'] = {}
        dia[diai][ementa+2]['refeicao'] = {}
        dia[diai][ementa+3]['refeicao'] = {}
        dia[diai][ementa+4]['refeicao'] = {}
        dia[diai][ementa+5]['refeicao'] = {}
        
        maxdia=int(diai)
  
  print('maxdia: %d',maxdia)    
  print(dia.keys())
  for line in textPage.split('\n'):
    line = line.strip()
    if export_text == True:
      print line
      continue
    '''bug do parser quando retorna por exemplo Grelhado 721'''   
    if len(filter(None,line.split(' ')))==2:
        tempAr = line.split(' ')
        tempAr=filter(None, tempAr)
        if (tempAr[0] in tipo_prato and tempAr[1].isdigit()) or (tempAr[0].isdigit() and tempAr[1] in tipo_prato):
            print('&&&&&&&&&&&')
            print('0:',tempAr[0])
            print('1:',tempAr[1])
            parseLine(tempAr[0])
            parseLine(tempAr[1])
            continue
    print "->",line
    
    parseLine(line)
    
      
print'------------------------var dia'      
print 'dia',dia
print 'keys',dia.keys()
'''jsondata = dia
json_data = json.dumps(dia)
print'------------------------json_data'
print 'json_data',json_data
print'------------------------python_value'
python_value = json.loads(json_data)
print 'python_value ',python_value
'''

shelve_file['dia'] = dia
shelve_file.close()


    
