#!python3
# -*- coding: utf-8

'''
This widget script simply shows the current contents of the clipboard.
The clipboard can be cleared by tapping the "trash" button.
'''



import appex, ui
import sys
import re
import datetime
import holidays
from datetime import date
import shelve
import os
import dialogs
from datetime import timedelta


line1text = 'ementa 1ARCTIC - Construction-ARCTIC fgjj-'
line2text = 'ementa 2 Melhoria Contínua de processos internos-'
line3text = 'ementa 3'
line4text = 'ementa 4'
line5text = 'ementa 5'

dia = {}



class EmentaView (ui.View):

  def __init__(self, dia, *args, **kwargs):
    super().__init__(self, *args, **kwargs)
    self.dia=dia
    self.hoje = datetime.datetime.now()
    #self.day=19
    #hoje.day
    self.labels = []
    self.dia_sem_lookup = ('Segunda','Terça','Quarta','Quinta','Sexta','Sábado','Domingo')
    
    linex1=4
    liney1=0.
    linex2=320-4-20
    liney2=20
    linesep = 2
    lb_break_mode = ui.LB_TRUNCATE_TAIL
    #
    self.display_view = ui.View(frame=(0, 0, 320, 220))
    self.bounds = (0, 0, 500, 220)
    
    self.line1lbl=self.make_label('tr',(linex1, liney1, linex2, liney2),2, lb_break_mode )
    self.line1lbl.text = self.dia[str(self.hoje.day)][1]['ementa']
    self.display_view.add_subview(self.line1lbl)
    
    line1lbl=self.line1lbl

    #line2
    self.line2lbl= self.make_label('tr',frame=(linex1,line1lbl.y+line1lbl.height+ linesep, linex2, line1lbl.height), nlines=2,lb =lb_break_mode)
    self.line2lbl.text = self.dia[str(self.hoje.day)][2]['ementa']
    
    line2lbl=self.line2lbl
    self.display_view.add_subview(line2lbl)

    #line3
    self.line3lbl= self.make_label('tr',frame=(linex1, line2lbl.y+line1lbl.height+ linesep, linex2, line1lbl.height), nlines=2,lb =lb_break_mode)
    self.line3lbl.text = self.dia[str(self.hoje.day)][3]['ementa']
    line3lbl=self.line3lbl
    self.display_view.add_subview(line3lbl)

    #line4
    self.line4lbl= self.make_label('tr',frame=(linex1, line3lbl.y+line3lbl.height+ linesep,linex2, line1lbl.height), nlines=2,lb =lb_break_mode)
    self.line4lbl.text = self.dia[str(self.hoje.day)][4]['ementa']
    line4lbl=self.line4lbl
    self.display_view.add_subview(line4lbl)

    #line5
    self.line5lbl = self.make_label('tr',frame=(linex1, line4lbl.y+line4lbl.height+ linesep,linex2, line1lbl.height) ,nlines=2,lb =lb_break_mode)
    self.line5lbl.text = self.dia[str(self.hoje.day)][5]['ementa']
    line5lbl=self.line5lbl
    self.display_view.add_subview(line5lbl)
    self.add_subview(self.display_view)
    self.labels.append(line1lbl)
    self.labels.append(line2lbl)
    self.labels.append(line3lbl)
    self.labels.append(line4lbl)
    self.labels.append(line5lbl)
    
    self.dia_semana=ui.Label('wh',frame=(0, self.line5lbl.y+self.line5lbl.height, 300, 16),font=('HelveticaNeue-Light', 14), alignment=ui.ALIGN_CENTER,text=str(self.dia_sem_lookup[self.hoje.weekday()]))
    self.display_view.add_subview(self.dia_semana)
    self.dia_semana.hidden=True
    self.dia_em=ui.Label('wh',frame=(0, self.line5lbl.y+self.line5lbl.height+linesep, 300, 32),font=('HelveticaNeue-Light', 32), alignment=ui.ALIGN_CENTER,text=str(self.hoje.day))
    self.add_subview(self.dia_em)
    self.dia_em.hidden=True
    
    self.minus_btn = ui.Button(name='-', image=ui.Image('iow:ios7_minus_outline_32'), flex='hl', tint_color='#666', action=self.button_tapped)
    self.minus_btn.frame = (20, self.display_view.bounds.height-60, 64, 64)
    self.display_view.add_subview(self.minus_btn)
    self.plus_btn = ui.Button(name='+', image=ui.Image('iow:ios7_plus_outline_32'), flex='hl', tint_color='#666', action=self.button_tapped)
    self.plus_btn.frame = (320-110,self.display_view.bounds.height-60 , 64, 64)
    self.display_view.add_subview(self.plus_btn)
  
  def make_label(self,pos,frame, nlines,lb):
    tamfonte = 12
    return ui.Label(flex=pos,frame=frame,font = ('Menlo', tamfonte), number_of_lines = nlines, background_color=(0.9,0.9, .9),border_color=(.5, .5, .5), line_break_mode=lb,border_width=1, corner_radius=5)
  pass

  def layout(self):
    self.compact = self.height < 150
    linex1=4
    liney1=0
    linex2=320-4-20
    liney2=20 if self.compact else 20*1.5 
    linesep = 2
    tamfonte = 12 if self.compact else 12.5
    
    line1lbl =self.line1lbl
    line2lbl =self.line2lbl
    line3lbl =self.line3lbl
    line4lbl =self.line4lbl
    line5lbl =self.line5lbl
    lb_break_mode = ui.LB_TRUNCATE_TAIL if self.compact else ui.LB_WORD_WRAP
    self.line1lbl.line_break_mode = lb_break_mode
    prev_y=line1lbl.y
    
    for i, lbl in enumerate(self.labels):
      lbl.height = liney2
      lbl.line_break_mode = lb_break_mode
      lbl.font = ('Menlo', tamfonte)
      ementa = self.dia[str(self.hoje.day)][i+1]['ementa']
      if self.compact:
        lbl.text = ementa
      else:
        refeicao = self.dia[str(self.hoje.day)][i+1]['refeicao']
        calorias = str(self.dia[str(self.hoje.day)][i+1]['calorias'])
        refeicao =refeicao if len(refeicao) > 0 else ""
        lbl.text = refeicao + '|' + ementa + '|' + calorias
        '''self.dia[str(self.hoje.day)][i+1]['refeicao']+ '|'+self.dia[str(self.hoje.day)][i+1]['ementa']+'|'+str(self.dia[str(self.hoje.day)][i+1]['calorias'])'''
      if i == 0:
        continue
      
      lbl.y=prev_y+line1lbl.height+ linesep
      prev_y=lbl.y
    if not self.compact:
      self.dia_em.y= line5lbl.y+self.line5lbl.height+linesep*8
      self.dia_semana.y=line5lbl.y+line5lbl.height+linesep
      self.dia_em.hidden=False
      self.plus_btn.hidden=False
      self.minus_btn.hidden=False
      self.dia_em.text=str(self.hoje.day)
      self.dia_semana.hidden = False
    else:
      self.dia_em.hidden=True
      self.minus_btn.hidden=True
      self.plus_btn.hidden=True
      self.dia_semana.hidden = True
  
  def button_tapped(self,sender):
    if sender.name=='+':
      self.hoje +=datetime.timedelta(days=1)
    elif sender.name=='-':
      self.hoje-=datetime.timedelta(days=1)  
    self.update_view()
    
  def update_view(self):
    self.dia_em.text=str(self.hoje.day)
    self.dia_semana.text=self.dia_sem_lookup[self.hoje.weekday()]
  
    for i, lbl in enumerate(self.labels):
      if str(self.hoje.day) not in self.dia.keys():
        lbl.text='Não há ementa'
      else:
        print('--')
        #print(self.dia[str(self.hoje.day)][i+1]['refeicao'])
        refeicao = self.dia[str(self.hoje.day)][i+1]['refeicao']
        ementa = self.dia[str(self.hoje.day)][i+1]['ementa']
        calorias = str(self.dia[str(self.hoje.day)][i+1]['calorias'])
        refeicao =refeicao if len(refeicao) > 0 else ""
        #print(len(refeicao))
        #print(ementa)
        #print(calorias)
        #print('.')
        lbl.text = refeicao + '|' + ementa + '|' + calorias
        
      '''self.dia[str(self.hoje.day)][i+1]['refeicao'] + '|'+self.dia[str(self.hoje.day)][i+1]['ementa']+'|'+str(self.dia[str(self.hoje.day)][i+1]['calorias'])'''
      

def main():
  shelve_file  = shelve.open('data')
  dia = shelve_file['dia']
  
  print('=====dia=====')
  print ('dia',dia['19'])
  print('=====keys====')
  print ('keys',dia.keys())
  
  #hoje = datetime.datetime(2017,5,15)
  shelve_file.close()

  

  # Optimization: Don't create a new view if the widget already shows the calculator.
  widget_name = __file__ + str(os.stat(__file__).st_mtime)
  widget_view = appex.get_widget_view()
  if widget_view is None or       widget_view.name != widget_name:
    widget_view = EmentaView(dia)
    widget_view.name = widget_name
    appex.set_widget_view(widget_view)

if __name__ == '__main__':
  main()

