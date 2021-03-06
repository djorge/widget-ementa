# -*- coding: utf-8
#! python2
#import appex
#import codecs
import datetime
import re
import sys
#import holidays
from datetime import date
import json
import shelve
import os

shift_feriado=0
dias_feriado =[]
map_tipo_prato ={'Frito':0,'Assado':0, 'Grelhado':0 , 'Cozido':0, 'Gratin':0, 'Estufado':0}
tipo_prato = ['Frito','Assado', 'Grelhado' , 'Cozido', 'Gratin.', 'Estufado']
#prato = ['SOPA','PEIXE', 'CARNE' , 'DIETA', 'OPCAO']
map_refeicao ={'SOPA':0,'PEIXE':0, 'CARNE':0 , 'DIETA':0, 'OPÇÃO':0}
refeicao = ['SOPA','PEIXE','CARNE','DIETA','OPÇÃO']

feriados =[date(2017,4,15), date(2017,5,25)]
def get_dia(diaint,mes,ano,item_count,item):
  '''
  item pode ser ementa, refeicao, tipo
  retorna tuplo com dia a usar e numero de linha onde colocar o item
  Faz a correcao para o caso de ser feriado
  '''
  global shift_feriado
  print 'get_dia(%d,%s,%s,%d,%s)'%(diaint,mes,ano,item_count,item)
  item_max = 5
  if item in tipo_prato:
    item_max =4

  if item_count > item_max:
    diaint+=(item_count/item_max)
    print '%d=(%d/%d)=%d'%(diaint,diaint,item_count, item_count/item_max)
    itemlinha= item_count % item_max
    if itemlinha == 0:
      itemlinha= item_max
      diaint-=1
    while True:
      diaint += shift_feriado
      if date(int(ano),int(mes), diaint) in feriados:
        print '++++++++++++++++++++ %d/%d/%d'%(int(ano),int(mes),diaint)
        #dia[str(diaint)][ementalinha]['ementa'] = 'Feriado'
        shift_feriado+=1
      else:
        break
    print '%d=%d/%d'%(diaint,item_count, item_max)
    print '%d=%d%%%d'%(itemlinha,item_count, item_max)
  else:
    itemlinha = item_count
  if item in tipo_prato:
    itemlinha+=1
  return (diaint,itemlinha)
  
#for ios
#csv_file = codecs.open(file_to_open,'r','utf-8')
#for windows
#csv_file = open(file_to_open)
#print(csv_file.read())

shelve_file = shelve.open('data.dat')
ignorar = '''Nota: Os Pratos confecionados nesta ementa semanal podem conter os seguintes alergénios: cereais que contêm glúten e produtos à base destes cereais, crustáceos e produtos à base de 
crustáceos, ovos e produtos à base de ovos, peixes e produtos à base de peixe, amendoins e produtos à base de amendoins, soja e produtos à base de soja, leite e produtos à base de leite, 
frutos de casca rija e produtos à base destes frutos, aipo e produtos à base de aipo, mostarda e produtos à base de mostarda, sementes de sésamo e produtos à base de sementes de 
sésamo, dióxido de enxofre e sulfitos, tremoço e produtos à base tremoço, moluscos e produtos à base de moluscos.'''
ignorar2=['ª','Alfragide','ALMOÇO','Semana de']
ignorar3='Semana de'
numtipo_prato =0
numrefeicao=0
numcaloria=0
numementa=0
decimal= 0
ementa=0
dia = {}
#feriados = holidays.Portugal()
shift_feriado =0
'''
carne,assado, batatas, 509
{'14':{'linha1':(carne,assado,batatas,500)}}
'''

'''
{'14':{'linha1':{'refeicao':'sopa','calorias':139, 'tipo_prato':'sopa','ementa':'Feijão-verde'},
       'linha2':{'refeicao':'peixe','ementa':'Pataniscas de Bacalhau e Arroz de Tomate', 'calorias':738,'tipo_prato':'frito'}}}
'''

i =1
for num in [6]:
    file = 'page_' +str(num) + '.txt'
    pageFile = open(file)
    #pageFile = codecs.open(file,'r','utf-8')

    textPage= pageFile.read()    
    
    hoje = datetime.datetime(2017,5,25)  
    
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
    maxdia = diaint
    
    if str(diaint) not in dia.keys():        
        dia[str(diaint)]= {}
        dia[str(diaint+1)]= {}
        dia[str(diaint+2)]= {}
        dia[str(diaint+3)]= {}
        dia[str(diaint+4)]= {} 
        dia[str(diaint)][ementa+5] = {}
        dia[str(diaint)][ementa+1] = {}
        dia[str(diaint)][ementa+2] = {}
        dia[str(diaint)][ementa+3] = {}
        dia[str(diaint)][ementa+4] = {}        
        dia[str(diaint)][ementa+5]['tipo_prato'] = {}
        dia[str(diaint)][ementa+1]['tipo_prato'] = {}
        dia[str(diaint)][ementa+2]['tipo_prato'] = {}
        dia[str(diaint)][ementa+3]['tipo_prato'] = {}
        dia[str(diaint)][ementa+4]['tipo_prato'] = {}        
        dia[str(diaint)][ementa+5]['calorias'] = {}
        dia[str(diaint)][ementa+1]['calorias'] = {}
        dia[str(diaint)][ementa+2]['calorias'] = {}
        dia[str(diaint)][ementa+3]['calorias'] = {}
        dia[str(diaint)][ementa+4]['calorias'] = {}
        dia[str(diaint)][ementa+5]['refeicao'] = {}
        dia[str(diaint)][ementa+1]['refeicao'] = {}
        dia[str(diaint)][ementa+2]['refeicao'] = {}
        dia[str(diaint)][ementa+3]['refeicao'] = {}
        dia[str(diaint)][ementa+4]['refeicao '] = {}

        dia[str(diaint+1)][ementa+5] = {}
        dia[str(diaint+1)][ementa+1] = {}
        dia[str(diaint+1)][ementa+2] = {}
        dia[str(diaint+1)][ementa+3] = {}
        dia[str(diaint+1)][ementa+4] = {}        
        dia[str(diaint+1)][ementa+5]['tipo_prato'] = {}
        dia[str(diaint+1)][ementa+1]['tipo_prato'] = {}
        dia[str(diaint+1)][ementa+2]['tipo_prato'] = {}
        dia[str(diaint+1)][ementa+3]['tipo_prato'] = {}
        dia[str(diaint+1)][ementa+4]['tipo_prato'] = {}        
        dia[str(diaint+1)][ementa+5]['calorias'] = {}
        dia[str(diaint+1)][ementa+1]['calorias'] = {}
        dia[str(diaint+1)][ementa+2]['calorias'] = {}
        dia[str(diaint+1)][ementa+3]['calorias'] = {}
        dia[str(diaint+1)][ementa+4]['calorias'] = {}
        dia[str(diaint+1)][ementa+5]['refeicao'] = {}
        dia[str(diaint+1)][ementa+1]['refeicao'] = {}
        dia[str(diaint+1)][ementa+2]['refeicao'] = {}
        dia[str(diaint+1)][ementa+3]['refeicao'] = {}
        dia[str(diaint+1)][ementa+4]['refeicao '] = {}
        
        dia[str(diaint+2)][ementa+5] = {}
        dia[str(diaint+2)][ementa+1] = {}
        dia[str(diaint+2)][ementa+2] = {}
        dia[str(diaint+2)][ementa+3] = {}
        dia[str(diaint+2)][ementa+4] = {}        
        dia[str(diaint+2)][ementa+5]['tipo_prato'] = {}
        dia[str(diaint+2)][ementa+1]['tipo_prato'] = {}
        dia[str(diaint+2)][ementa+2]['tipo_prato'] = {}
        dia[str(diaint+2)][ementa+3]['tipo_prato'] = {}
        dia[str(diaint+2)][ementa+4]['tipo_prato'] = {}        
        dia[str(diaint+2)][ementa+5]['calorias'] = {}
        dia[str(diaint+2)][ementa+1]['calorias'] = {}
        dia[str(diaint+2)][ementa+2]['calorias'] = {}
        dia[str(diaint+2)][ementa+3]['calorias'] = {}
        dia[str(diaint+2)][ementa+4]['calorias'] = {}
        dia[str(diaint+2)][ementa+5]['refeicao'] = {}
        dia[str(diaint+2)][ementa+1]['refeicao'] = {}
        dia[str(diaint+2)][ementa+2]['refeicao'] = {}
        dia[str(diaint+2)][ementa+3]['refeicao'] = {}
        dia[str(diaint+2)][ementa+4]['refeicao '] = {}
        
        
        dia[str(diaint+3)][ementa+1] = {}
        dia[str(diaint+3)][ementa+2] = {}
        dia[str(diaint+3)][ementa+3] = {}
        dia[str(diaint+3)][ementa+4] = {}     
        dia[str(diaint+3)][ementa+5] = {}   
        dia[str(diaint+3)][ementa+5]['tipo_prato'] = {}
        dia[str(diaint+3)][ementa+1]['tipo_prato'] = {}
        dia[str(diaint+3)][ementa+2]['tipo_prato'] = {}
        dia[str(diaint+3)][ementa+3]['tipo_prato'] = {}
        dia[str(diaint+3)][ementa+4]['tipo_prato'] = {}        
        dia[str(diaint+3)][ementa+5]['calorias'] = {}
        dia[str(diaint+3)][ementa+1]['calorias'] = {}
        dia[str(diaint+3)][ementa+2]['calorias'] = {}
        dia[str(diaint+3)][ementa+3]['calorias'] = {}
        dia[str(diaint+3)][ementa+4]['calorias'] = {}
        dia[str(diaint+3)][ementa+5]['refeicao'] = {}
        dia[str(diaint+3)][ementa+1]['refeicao'] = {}
        dia[str(diaint+3)][ementa+2]['refeicao'] = {}
        dia[str(diaint+3)][ementa+3]['refeicao'] = {}
        dia[str(diaint+3)][ementa+4]['refeicao '] = {}
        
        dia[str(diaint+4)][ementa+5] = {}
        dia[str(diaint+4)][ementa+1] = {}
        dia[str(diaint+4)][ementa+2] = {}
        dia[str(diaint+4)][ementa+3] = {}
        dia[str(diaint+4)][ementa+4] = {}        
        dia[str(diaint+4)][ementa+5]['tipo_prato'] = {}
        dia[str(diaint+4)][ementa+1]['tipo_prato'] = {}
        dia[str(diaint+4)][ementa+2]['tipo_prato'] = {}
        dia[str(diaint+4)][ementa+3]['tipo_prato'] = {}
        dia[str(diaint+4)][ementa+4]['tipo_prato'] = {}        
        dia[str(diaint+4)][ementa+5]['calorias'] = {}
        dia[str(diaint+4)][ementa+1]['calorias'] = {}
        dia[str(diaint+4)][ementa+2]['calorias'] = {}
        dia[str(diaint+4)][ementa+3]['calorias'] = {}
        dia[str(diaint+4)][ementa+4]['calorias'] = {}
        dia[str(diaint+4)][ementa+5]['refeicao'] = {}
        dia[str(diaint+4)][ementa+1]['refeicao'] = {}
        dia[str(diaint+4)][ementa+2]['refeicao'] = {}
        dia[str(diaint+4)][ementa+3]['refeicao'] = {}
        dia[str(diaint+4)][ementa+4]['refeicao '] = {}
        maxdia=diaint+4
    
    for line in textPage.split('\n'):
      line = line.strip()
      print "->",line
      if len(line.strip()) == 1:
        continue
      if len(line)==0:
        continue
      if line.strip() in ignorar:
        continue
      if line.strip() in ignorar2:
        print 'ignorar2 matched. comtinue...'
        continue      
      salta = False
      for word in ignorar2:
        if line.strip().startswith(word):
            salta = True
            break
      if salta == True:              
        continue   

      if line.strip() in tipo_prato:
        numtipo_prato+=1
        print line          
        diaint = int(dedia)
        (diaint,item_linha)=get_dia(diaint,ames,ano,numtipo_prato,line)
        print "dia[%d][%d]['tipo_prato']"%(diaint,item_linha)
        dia[str(diaint)][item_linha]['tipo_prato'] = line
        continue
        
      if line.strip() in refeicao:
        numrefeicao+=1
        diaint = int(dedia)
        #print line 
        (diaint,item_linha)=get_dia(diaint,ames,ano,numrefeicao,line)
        print "dia[%d][%d]['refeicao']"%(diaint,item_linha)  
        if diaint > maxdia:
          '''refeicao tb existe em feriados
           '''
          print '%d (dia) > %d (maxdia)'%(diaint,maxdia)
          continue
          
        dia[str(diaint)][item_linha]['refeicao'] = line
        continue
    
      if line.strip().isdigit():
        decimal+=1
        diaint = int(dedia)
        (diaint,item_linha)=get_dia(diaint,ames,ano,decimal,line)
        print "dia[%d][%d]['calorias']"%(diaint,item_linha)  
        dia[str(diaint)][item_linha]['calorias'] = line
        continue
 
      ementa+=1
      
      '''if len(dia.keys()) == 0:
        print "Vaaaaaaaaaaaaaaaaazio"
      dia['20'] = {}
      if len(dia.keys()) == 0:
        print "Vaaaaaaaaaaaaaaaaazio"
      dia['20']['21'] = {}
      dia['20']['21'][ementa] =  line      
      '''
      #print i
      #i+=1
              
      #print 'dia',dia
       
      #if ementa > 5:
        #reset
        #ementa = 1
        #diaint +=1
        #diaint = (ementa/5) 
      diaint = int(dedia)
      (diaint,ementalinha)=get_dia(diaint,ames,ano,ementa,line)
      '''
      shift_feriado =0
      if ementa >5:
        diaint+=(ementa/5)
        print '%d=%d/5'%(diaint,ementa/5)
        ementalinha= ementa % 5
        if ementalinha == 0:
          ementalinha=5 
          diaint-=1
        while True:
          diaint += shift_feriado
          if date(int(ano),int(ames), diaint) in feriados:
            print '++++++ %d/%d/%d'%(int(ano),int(ames),diaint)
            #dia[str(diaint)][ementalinha]['ementa'] = 'Feriado'
            shift_feriado+=1
          else:
            break
        print '%d=%d/5'%(diaint,ementa)
        print '%d=%d%%5'%(ementalinha,ementa)
      else:
        ementalinha = ementa'''
      
      print "dia[%s][%d]['ementa']" % ( str(diaint), ementalinha)
      dia[str(diaint)][ementalinha]['ementa'] = line
      
print'------------------------var dia'      
print 'dia',dia
jsondata = dia
json_data = json.dumps(dia)
print'------------------------json_data'
print 'json_data',json_data
print'------------------------python_value'
python_value = json.loads(json_data)
print 'python_value ',python_value

hoje = datetime.datetime(2017,4,25) 

print 'keys',dia.keys()
if str(hoje.day) in dia.keys():
    print'Parsing não é necessário .'
    
else:
    print'Parsing  é necessário.'

shelve_file['dia'] = python_value
shelve_file.close()


    