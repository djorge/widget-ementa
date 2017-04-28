# -*- coding: utf-8
#! python2
#import appex
#import codecs
import datetime
import re
import sys

#for ios
#csv_file = codecs.open(file_to_open,'r','utf-8')
#for windows
#csv_file = open(file_to_open)
#print(csv_file.read())
map_tipo_prato ={'Frito':0,'Assado':0, 'Grelhado':0 , 'Cozido':0, 'Gratin':0, 'Estufado':0}
tipo_prato = ['Frito','Assado', 'Grelhado' , 'Cozido', 'Gratin', 'Estufado']
#prato = ['SOPA','PEIXE', 'CARNE' , 'DIETA', 'OPCAO']
map_refeicao ={'SOPA':0,'PEIXE':0, 'CARNE':0 , 'DIETA':0, 'OPÇÃO':0}
refeicao = ['SOPA','PEIXE','CARNE','DIETA','OPÇÃO']
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
ementa=1
dia = {}


'''
carne,assado, batatas, 509
{'14':{'linha1':(carne,assado,batatas,500)}}
'''

'''
{'14':{'linha1':{'refeicao':'sopa','calorias':139, 'tipo_prato':'sopa','ementa':'Feijão-verde'},
       'linha2':{'refeicao':'peixe','ementa':'Pataniscas de Bacalhau e Arroz de Tomate', 'calorias':738,'tipo_prato':'frito'}}}
'''


i =1
for num in [2]:
    file = 'page_' +str(num) + '.txt'
    pageFile = open(file)
    #pageFile = codecs.open(file,'r','utf-8')

    textPage= pageFile.read()    
    
    hoje = datetime.datetime(2017,4,21)
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
    
    if len(dia) == 0:
        dia[str(diaint)]= {}
        dia[str(diaint+1)]= {}
        dia[str(diaint+2)]= {}
        dia[str(diaint+3)]= {}
        dia[str(diaint+4)]= {} 
        dia[str(diaint)][ementa] = {}
        dia[str(diaint)][ementa+1] = {}
        dia[str(diaint)][ementa+2] = {}
        dia[str(diaint)][ementa+3] = {}
        dia[str(diaint)][ementa+4] = {}        
        dia[str(diaint)][ementa]['tipo_prato'] = {}
        dia[str(diaint)][ementa+1]['tipo_prato'] = {}
        dia[str(diaint)][ementa+2]['tipo_prato'] = {}
        dia[str(diaint)][ementa+3]['tipo_prato'] = {}
        dia[str(diaint)][ementa+4]['tipo_prato'] = {}        
        dia[str(diaint)][ementa]['calorias'] = {}
        dia[str(diaint)][ementa+1]['calorias'] = {}
        dia[str(diaint)][ementa+2]['calorias'] = {}
        dia[str(diaint)][ementa+3]['calorias'] = {}
        dia[str(diaint)][ementa+4]['calorias'] = {}
        dia[str(diaint)][ementa]['refeicao'] = {}
        dia[str(diaint)][ementa+1]['refeicao'] = {}
        dia[str(diaint)][ementa+2]['refeicao'] = {}
        dia[str(diaint)][ementa+3]['refeicao'] = {}
        dia[str(diaint)][ementa+4]['refeicao '] = {}

        dia[str(diaint+1)][ementa] = {}
        dia[str(diaint+1)][ementa+1] = {}
        dia[str(diaint+1)][ementa+2] = {}
        dia[str(diaint+1)][ementa+3] = {}
        dia[str(diaint+1)][ementa+4] = {}        
        dia[str(diaint+1)][ementa]['tipo_prato'] = {}
        dia[str(diaint+1)][ementa+1]['tipo_prato'] = {}
        dia[str(diaint+1)][ementa+2]['tipo_prato'] = {}
        dia[str(diaint+1)][ementa+3]['tipo_prato'] = {}
        dia[str(diaint+1)][ementa+4]['tipo_prato'] = {}        
        dia[str(diaint+1)][ementa]['calorias'] = {}
        dia[str(diaint+1)][ementa+1]['calorias'] = {}
        dia[str(diaint+1)][ementa+2]['calorias'] = {}
        dia[str(diaint+1)][ementa+3]['calorias'] = {}
        dia[str(diaint+1)][ementa+4]['calorias'] = {}
        dia[str(diaint+1)][ementa]['refeicao'] = {}
        dia[str(diaint+1)][ementa+1]['refeicao'] = {}
        dia[str(diaint+1)][ementa+2]['refeicao'] = {}
        dia[str(diaint+1)][ementa+3]['refeicao'] = {}
        dia[str(diaint+1)][ementa+4]['refeicao '] = {}
        
        dia[str(diaint+2)][ementa] = {}
        dia[str(diaint+2)][ementa+1] = {}
        dia[str(diaint+2)][ementa+2] = {}
        dia[str(diaint+2)][ementa+3] = {}
        dia[str(diaint+2)][ementa+4] = {}        
        dia[str(diaint+2)][ementa]['tipo_prato'] = {}
        dia[str(diaint+2)][ementa+1]['tipo_prato'] = {}
        dia[str(diaint+2)][ementa+2]['tipo_prato'] = {}
        dia[str(diaint+2)][ementa+3]['tipo_prato'] = {}
        dia[str(diaint+2)][ementa+4]['tipo_prato'] = {}        
        dia[str(diaint+2)][ementa]['calorias'] = {}
        dia[str(diaint+2)][ementa+1]['calorias'] = {}
        dia[str(diaint+2)][ementa+2]['calorias'] = {}
        dia[str(diaint+2)][ementa+3]['calorias'] = {}
        dia[str(diaint+2)][ementa+4]['calorias'] = {}
        dia[str(diaint+2)][ementa]['refeicao'] = {}
        dia[str(diaint+2)][ementa+1]['refeicao'] = {}
        dia[str(diaint+2)][ementa+2]['refeicao'] = {}
        dia[str(diaint+2)][ementa+3]['refeicao'] = {}
        dia[str(diaint+2)][ementa+4]['refeicao '] = {}
        
        dia[str(diaint+3)][ementa] = {}
        dia[str(diaint+3)][ementa+1] = {}
        dia[str(diaint+3)][ementa+2] = {}
        dia[str(diaint+3)][ementa+3] = {}
        dia[str(diaint+3)][ementa+4] = {}        
        dia[str(diaint+3)][ementa]['tipo_prato'] = {}
        dia[str(diaint+3)][ementa+1]['tipo_prato'] = {}
        dia[str(diaint+3)][ementa+2]['tipo_prato'] = {}
        dia[str(diaint+3)][ementa+3]['tipo_prato'] = {}
        dia[str(diaint+3)][ementa+4]['tipo_prato'] = {}        
        dia[str(diaint+3)][ementa]['calorias'] = {}
        dia[str(diaint+3)][ementa+1]['calorias'] = {}
        dia[str(diaint+3)][ementa+2]['calorias'] = {}
        dia[str(diaint+3)][ementa+3]['calorias'] = {}
        dia[str(diaint+3)][ementa+4]['calorias'] = {}
        dia[str(diaint+3)][ementa]['refeicao'] = {}
        dia[str(diaint+3)][ementa+1]['refeicao'] = {}
        dia[str(diaint+3)][ementa+2]['refeicao'] = {}
        dia[str(diaint+3)][ementa+3]['refeicao'] = {}
        dia[str(diaint+3)][ementa+4]['refeicao '] = {}
        
        dia[str(diaint+4)][ementa] = {}
        dia[str(diaint+4)][ementa+1] = {}
        dia[str(diaint+4)][ementa+2] = {}
        dia[str(diaint+4)][ementa+3] = {}
        dia[str(diaint+4)][ementa+4] = {}        
        dia[str(diaint+4)][ementa]['tipo_prato'] = {}
        dia[str(diaint+4)][ementa+1]['tipo_prato'] = {}
        dia[str(diaint+4)][ementa+2]['tipo_prato'] = {}
        dia[str(diaint+4)][ementa+3]['tipo_prato'] = {}
        dia[str(diaint+4)][ementa+4]['tipo_prato'] = {}        
        dia[str(diaint+4)][ementa]['calorias'] = {}
        dia[str(diaint+4)][ementa+1]['calorias'] = {}
        dia[str(diaint+4)][ementa+2]['calorias'] = {}
        dia[str(diaint+4)][ementa+3]['calorias'] = {}
        dia[str(diaint+4)][ementa+4]['calorias'] = {}
        dia[str(diaint+4)][ementa]['refeicao'] = {}
        dia[str(diaint+4)][ementa+1]['refeicao'] = {}
        dia[str(diaint+4)][ementa+2]['refeicao'] = {}
        dia[str(diaint+4)][ementa+3]['refeicao'] = {}
        dia[str(diaint+4)][ementa+4]['refeicao '] = {}
    
    for line in textPage.split('\n'):
      print "->",line
      if len(line.strip()) == 1:
        continue
      if len(line)==0:
        continue
      if line in ignorar:
        continue
      if line in ignorar2:
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
        #print line        
        for x in tipo_prato: 
            if line.strip() == x:   
                print "dia[%d][%d]['tipo_prato']"%(diaint, numtipo_prato)
                dia[str(diaint)][numtipo_prato]['tipo_prato'] = line
        if numtipo_prato ==5:
            numtipo_prato=0
        continue
        
      if line.strip() in refeicao:
        numrefeicao+=1
        #print line
        for x in refeicao: 
            if line.strip() == x:       
                dia[str(diaint)][numrefeicao]['refeicao'] = line
        if numrefeicao ==5:
            numrefeicao=0
        continue
    
      if line.strip().isdigit():
        decimal+=1
        dia[str(diaint)][decimal]['calorias'] = line
        if decimal ==5:
            decimal=0
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
       
      if ementa == 6:
        #reset
        ementa = 1
        diaint +=1

      print "str(diaint): %s, len: %r" % ( str(diaint), len(dia[str(diaint)]))
      if len(dia[str(diaint)]) ==0:
        dia[str(diaint)][ementa]= {}
      if(len(dia[str(diaint)][ementa]) == 0):
        dia[str(diaint)][ementa] = {}
      dia[str(diaint)][ementa]['ementa'] = line
      
print 'dia',dia
#print 'map_tipo_prato',map_tipo_prato
#print 'map_refeicao',map_refeicao
#print 'numrefeicao',numrefeicao


teste_map1 = {'14':{'linha1':{'refeicao':'sopa','calorias':139, 'tipo_prato':'sopa','ementa':'Feijão-verde'},
                   'linha2':{'refeicao':'peixe','ementa':'Pataniscas de Bacalhau e Arroz de Tomate', 'calorias':738,'tipo_prato':'frito'},
                   'linha3':{'refeicao':'CARNE','ementa':'Pá de Porco à Padeiro, Arroz de Forno e Caldo Verde', 'calorias':683,'tipo_prato':'Assado'},
                   'linha4':{'refeicao':'DIETA','ementa':'Espetada de Aves Grelhada, Molho de Limão e Esparguete', 'calorias':706,'tipo_prato':'Grelhado'},
                   'linha5':{'refeicao':'OPÇÃO','ementa':'Lasanha de Espinafres', 'calorias':702,'tipo_prato':'Assado'}
                  },
             '16':{'linha1':{'refeicao':'sopa','calorias':127, 'tipo_prato':'sopa','ementa':'Nabiças c/ Massinhas'},
                   'linha2':{'refeicao':'peixe','ementa':'Solha à Delicia c/ Banana e Puré', 'calorias':593,'tipo_prato':'Assado'},
                   'linha3':{'refeicao':'CARNE','ementa':'Saltaricos de Carne de Porco c/ Pickles e Cogumelos', 'calorias':804,'tipo_prato':'Assado'},
                   'linha4':{'refeicao':'DIETA','ementa':'Borrego Estufado ao Natural e Arroz Branco', 'calorias':544,'tipo_prato':'Estufado'},
                   'linha5':{'refeicao':'OPÇÃO','ementa':'Strudel de Legumes', 'calorias':746,'tipo_prato':'Assado'}
                  }
            }

teste_map = {'14':{'1':{'refeicao1':'sopa','calorias1':139, 'tipo_prato1':'sopa','ementa1':'Feijão-verde'},
                   '2':{'refeicao2':'peixe','ementa2':'Pataniscas de Bacalhau e Arroz de Tomate', 'calorias2':738,'tipo_prato2':'frito'},
                   '3':{'refeicao3':'CARNE','ementa3':'Pá de Porco à Padeiro, Arroz de Forno e Caldo Verde', 'calorias3':683,'tipo_prato3':'Assado'},
                   '4':{'refeicao4':'DIETA','ementa4':'Espetada de Aves Grelhada, Molho de Limão e Esparguete', 'calorias4':706,'tipo_prato4':'Grelhado'},
                   '5':{'refeicao5':'OPÇÃO','ementa5':'Lasanha de Espinafres', 'calorias5':702,'tipo_prato':'Assado'}
                  },
             '16':{'1':{'refeicao':'sopa','calorias':127, 'tipo_prato':'sopa','ementa':'Nabiças c/ Massinhas'},
                   '2':{'refeicao':'peixe','ementa':'Solha à Delicia c/ Banana e Puré', 'calorias':593,'tipo_prato':'Assado'},
                   '3':{'refeicao':'CARNE','ementa':'Saltaricos de Carne de Porco c/ Pickles e Cogumelos', 'calorias':804,'tipo_prato':'Assado'},
                   '4':{'refeicao':'DIETA','ementa':'Borrego Estufado ao Natural e Arroz Branco', 'calorias':544,'tipo_prato':'Estufado'},
                   '5':{'refeicao':'OPÇÃO','ementa':'Strudel de Legumes', 'calorias':746,'tipo_prato':'Assado'}
                  }
            }            

#print teste_map['14']['5']
#teste_map['14']['5']['tipo_prato'] = 'udpated'
#print 'teste_map',teste_map
#print '--------------'
#print teste_map['14']['5']
#print teste_map['16']['5'] 
