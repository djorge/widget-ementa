# -*- coding: utf-8
#!python2

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
import sys
import base64
import clipboard
from unidecode import unidecode

#feriado_update para decidir se e feito update do contador para -1. apenas feito uma veZ pq sonhanum texto a dizer feriado ou 25 de abril ou carnaval  não ha string de refeição 
feriado_update = True
last_ementa=True
crop= False
export_text=False
shift_feriado_ementa=9
shift_feriado_tipo_prato=0
shift_feriado_calorias=0
shift_feriado_refeicao=9
dias_feriado =[]
tipo_prato = ['Frito','Assado', 'Grelhado' , 'Cozido', 'Gratin.', 'Estufado','estufado','Grelh.','EStufado','Assada','Estufadas','Gratinados','Guisado','Gratinado','grelhado','Estufada','Cebolada','Estfado','A Vapor','EStufado','Assdao','Braseado']
refeicao = ['SOPA','PEIXE','CARNE','DIETA','OPCAO']
shelve_file = shelve.open('data')
ignorar = '''Os Pratos que constam na Ementa contem ou podem conter ves gios das seguintes substancias ou produtos e seus derivados: cereais que contem gluten, crustaceos, ovos, peixe, amendoins, soja, leite, frutos de casca rija, aipo, mostarda, sementes de sesamo, dioxido de enxofre e sul tos, tremoco e/ou moluscos.'''
ignorar2=['ª','Alfragide','ALMOÇO','Semana de','Nota:','EMENTA','MB Café','2a FEIRA','3a FEIRA','4a FEIRA','5a FEIRA','6a FEIRA','Esta Ementa pode ser alterada por mo vos imprevistos.']
ignorar3='Semana de'
ignorar4='''Esta Ementa pode ser alterada por mo vos imprevistos.'''

ignorar5='''*Prato Confeccionado c/ Ovos Pasteurizados'''

ignorar6='''Os Pratos que constam na Ementa contem ou podem conter ves gios das seguintes substancias ou produtos e seus derivados: cereais que contem gluten, crustaceos, ovos, peixe, amendoins, soja, leite, frutos de casca rija, aipo, mostarda, sementes de sesamo, dioxido de enxofre e sul tos, tremoco e/ou moluscos.'''

ignorar7=['Os Pratos que constam na Ementa contêm ou podem conter vestígios das seguintes substâncias ou produtos e seus derivados: cereais que contêm glúten, crustáceos, ovos, peixe, amendoins, soja, leite, frutos de casca rija, aipo, mostarda, sementes de sésamo, dióxido de enxofre e sulfitos, tremoço e/ou moluscos.']

textos_ignorar=[ignorar,ignorar3, ignorar4, ignorar5,ignorar6,ignorar7]

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
  feriado_flag= False
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
        feriado_flag = True
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
        feriado_flag=True
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
  
  return (diaint,mesint,anoint,itemlinha,feriado_flag)

def convert(fname, pages=None):
  if not pages:
    pagenums = set()
  else:
    pagenums = set(pages)

  output = StringIO()
  manager = PDFResourceManager()
  converter = TextConverter(manager, output, laparams=LAParams())
  interpreter = PDFPageInterpreter(manager, converter)

  #infile = file(fname, 'rb')
  infile = codecs.open(fname,'rb')
  #for pageNumber, page in enumerate(PDFDocument.get_pages()):
  for page in PDFPage.get_pages(infile, pagenums):
    interpreter.process_page(page)
  infile.close()
  converter.close()
  text = output.getvalue()
  output.close()
  return text
  
def parseLine(line):
    global numtipo_prato, decimal, ignorar, ignorar2, ignorar3, refeicao, diaint,ames,ano, numcaloria, numementa, numrefeicao, numtipo_prato, last_ementa, ementa, dedia, textos_ignorar, feriado_update
    
    
    
    #print('parseline(%s)' % line)
    line = line.strip()
    if len(line.strip()) == 1:
      return 
    if len(line)==0:
      return
      
    if line.strip() in textos_ignorar:
      print 'textos_ignorar matched. comtinue...'
      return    
    if line.strip() in ignorar:
      return
    if line.strip() in ignorar2:
      print 'ignorar2 matched. comtinue...'
      return      
    if line.strip() in ignorar4:
      print 'ignorar4 matched. comtinue...'
      return     
    if line.strip() in ignorar5:
      print 'ignorar5 matched. comtinue...'
      return    
    if line.strip() in ignorar6:
      print 'ignorar6 matched. comtinue...'
      return     
    if line.strip() in ignorar7:
      print 'ignorar7 matched. comtinue...'
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
    #print('dedia',dedia)
    
    diaint = int(dedia)
    mesint = int(demes)
    anoint = int(ano)
    feriado_flag = False
    
    
    if line.strip() in tipo_prato:
      numtipo_prato+=1
      print line          
   
      (diaint,mesint, anoint, item_linha,feriado_flag)=get_dia(diaint,mesint,anoint,numtipo_prato,line)
      diaidx = str(anoint) + str(mesint)+ str(diaint)
      
      print "dia[%s][%d]['tipo_prato'] f:%d"%(diaidx,item_linha,feriado_flag)
      if feriado_flag and feriado_update:
        feriado_update=False
        numtipo_prato -=1
        return
      dia[diaidx][item_linha]['tipo_prato'] = line.decode('utf-8')
      return
      
    if line.strip() in refeicao:
      numrefeicao+=1
      #print line 
      (diaint,mesint, anoint, item_linha,feriado_flag)=get_dia(diaint,mesint,anoint,numrefeicao,line)
      diaidx = str(anoint) + str(mesint)+ str(diaint)
      print "dia[%s][%d]['refeicao'] f:%d"%(diaidx,item_linha,feriado_flag)  
      
      if int(diaidx) > maxdia:
        '''refeicao tb existe em feriados
         '''
        print '%s (dia) > %d (maxdia)'%(diaidx,maxdia)
        return 
      if feriado_flag and feriado_update:
        feriado_update=False
        numrefeicao -=1
        return
      dia[diaidx][item_linha]['refeicao'] = line.decode('utf-8')
      
      return
  
    if line.strip().isdigit():
      decimal+=1
      
      (diaint,mesint, anoint, item_linha,feriado_flag)=get_dia(diaint,mesint,anoint,decimal,line)
      diaidx = str(anoint) + str(mesint)+ str(diaint)
      print "dia[%s][%d]['calorias'] f:%d"%(diaidx,item_linha,feriado_flag)
      if feriado_flag and feriado_update:
        feriado_update=False
        item_linha-=1
        return 
      dia[diaidx][item_linha]['calorias'] = lline.decode('utf-8')
      return 
      
    ementa+=1
    
    
    (diaint,mesint, anoint, ementalinha,feriado_flag)=get_dia(diaint,mesint,anoint,ementa,line)
    
    diaidx = str(anoint) + str(mesint)+ str(diaint)
    print "dia[%s][%d]['ementa'] f:%d" % ( diaidx, ementalinha, feriado_flag)
    if feriado_flag and feriado_update:
      feriado_update=False
      ementa-=1
      return
    dia[diaidx][ementalinha]['ementa'] = line.decode('utf-8')
    #last_ementa = line
  
def get_file_from_user():
    pdf_files = [f for f in os.listdir(os.curdir) if f.endswith('.txt')]
    return dialogs.list_dialog(title='txt de ementa', items=pdf_files)

def replaceByNewLine(line, text ):
    uline = unidecode(line.strip())
    f = uline.find(text)
    
    if f > -1:
        uline = uline.replace(text, '\n'+ text[:-2] + '\n')
  
    return  uline
    '''
    p1 = ''
    if f > -1: 
        print('uline f:{} {}'.format(f,uline))
        if f > 0:
            p1 = line[0:f-1]+'\n'
            print('line p1 {}'.format(p1))
        p2= line[f:f+len(text)]
        print('line p2 {}'.format(p2))
        p3= '\n'+line[f+1+len(text):]
        print('line p3 {}'.format(p3))
        line2=p1+p2+p3
        print('line2: {}'.format(line2))
        return line2   
        #uline = uline.replace('-','\n')
    
    return uline
    #print('replaceByNewLine({},"{}")'.format
    '''

filename=''
'''
if appex.is_running_extension():
  file_paths = appex.get_file_paths()
  for i, file in enumerate(file_paths):
    if file.endswith('.txt'):
    	print('++++++++',file)
    	filename=file
else:
  filename = get_file_from_user()
if filename is None:
  exit()
  
'''
print('===============================')
file1 = 'ementaSIBS.pdf'
file2='ementaSIBScomferiadoaumaquarta.pdf'
feriados = holidays.Portugal() #
print date(2017, 4, 14) in feriados # True
#todo here
ementaText=''
if(len(sys.argv))>1:
   ementaText = base64.b64decode(sys.argv[1]).decode('utf-8')
else:
   ementaText = base64.b64decode(clipboard.get().decode('utf-8'))
   #print ementaText

dedia=''
linhai=0
for textPage in iter(ementaText.splitlines()):
  linhai+=1
  if linhai == 12:
      pass
      #sys.exit()
  #print('textpage raw {}'.format(textPage))
  #print textPage 
  #print ('before  replace: {}'.format(textPage))
  #textPage = unicodedata.normalize('NFD',textPage)
  #print('after normalize= {}'.format(textPage))
  textPage = replaceByNewLine(textPage,'SOPA--')
  textPage = replaceByNewLine(textPage,'CARNE--')
  textPage = replaceByNewLine(textPage,'PEIXE--')
  textPage = replaceByNewLine(textPage,'DIETA--')
  textPage = replaceByNewLine(textPage,'OPCAO--')

  #print('linha ',linhai)
  #print ('after replace: {}'.format(textPage))
  if len(textPage) == 0 or len(textPage)== 1:
    continue
 # hoje = datetime.datetime.now()
  hoje = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month,datetime.datetime.now().day,0,0,0)
  
  semana = re.compile(r'SEMANA DE (\d\d) A (\d\d)/(\d\d)/(\d\d\d\d)')
  dias = semana.search(textPage)
    
  if dias is not None:
      dedia = dias.group(1)
      #demes = dias.group(2)
      adia = dias.group(2)
      ames = dias.group(3)
      ano = dias.group(4)
      demes=ames
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
            continue
  if textPage.find('\n') > -1:
      for line in textPage.split('\n'):
        line = line.strip()
        if len(line) == 0 or len(line)== 1:
            continue
        #print('text page line {}'.format(line))
        if line.find('destes  cereais') >-1:
          para = True
        if export_text == True:
          print line
          continue
        parseLine(line)
  else:
      #print('textpage: {}'.format(textPage))
      parseLine(textPage)
    
      
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


    
