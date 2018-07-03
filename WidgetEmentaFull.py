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
from datetime import date
import shelve
import os
from datetime import timedelta


'''line1text = 'ementa 1ARCTIC - Construction-ARCTIC fgjj-'
line2text = 'ementa 2 Melhoria Contínua de processos internos-'
line3text = 'ementa 3'
line4text = 'ementa 4'
line5text = 'ementa 5'

dia = {}
'''
def setbox(uiobj,color='red'):
    uiobj.border_color=color
    uiobj.border_width=0

class EmentaView (ui.View):

  def __init__(self, dia, *args, **kwargs):
    '''import feito aqui porque se for feito no cabeçalho causa o refresh da widgget'''
    import holidays
    self.feriados = holidays.Portugal()
    super().__init__(self, *args, **kwargs)
    self.dia=dia
    self.hoje = datetime.datetime.now()

    self.labels = []
    self.dia_sem_lookup = ('Seg','Ter','Qua','Qui','Sex','Sáb','Dom')
    
    linex1=4
    liney1=0.
    linex2=320-4-20
    liney2=20
    linesep = 2
    lb_break_mode = ui.LB_TRUNCATE_TAIL
    #
    self.display_view = ui.View(frame=(0, 0, 358, 220))
    self.bounds = (0, 0, 500, 220)
    setbox(self.display_view)
    self.diaidx = str(self.hoje.year) + str(self.hoje.month)+ str(self.hoje.day)
    
    self.line1lbl=self.make_label('tr',(linex1, liney1, linex2, liney2),2, lb_break_mode )
    setbox(self.line1lbl)
    self.display_view.add_subview(self.line1lbl)
    
    line1lbl=self.line1lbl

    
    #line2
    self.line2lbl= self.make_label('tr',frame=(linex1,line1lbl.y+line1lbl.height+ linesep, linex2, line1lbl.height), nlines=2,lb =lb_break_mode)
    setbox(self.line2lbl,'green')
    
    line2lbl=self.line2lbl
    setbox(line2lbl)
    self.display_view.add_subview(line2lbl)

    #line3
    self.line3lbl= self.make_label('tr',frame=(linex1, line2lbl.y+line1lbl.height+ linesep, linex2, line1lbl.height), nlines=2,lb =lb_break_mode)

    line3lbl=self.line3lbl
    setbox(self.line3lbl)
    self.display_view.add_subview(line3lbl)

    #line4
    self.line4lbl= self.make_label('tr',frame=(linex1, line3lbl.y+line3lbl.height+ linesep,linex2, line1lbl.height), nlines=2,lb =lb_break_mode)
    
    line4lbl=self.line4lbl
    setbox(self.line4lbl)
    self.display_view.add_subview(line4lbl)

    #line5
    self.line5lbl = self.make_label('tr',frame=(linex1, line4lbl.y+line4lbl.height+ linesep,linex2, line1lbl.height) ,nlines=2,lb =lb_break_mode)
    setbox(self.line5lbl)
    line5lbl=self.line5lbl
    self.display_view.add_subview(line5lbl)
    self.add_subview(self.display_view)
    self.labels.append(line1lbl)
    self.labels.append(line2lbl)
    self.labels.append(line3lbl)
    self.labels.append(line4lbl)
    self.labels.append(line5lbl)
    setbox(line5lbl)
    
    self.btx= 310
  
    
    #todo bt menos
    self.minus_btn = ui.Button(name='-', image=ui.Image('iow:ios7_minus_outline_32'), flex='hl', tint_color='#666', action=self.button_tapped)
    self.minus_btn.frame = (self.btx, 5, 32,32)
    setbox(self.minus_btn,'yellow')
    self.display_view.add_subview(self.minus_btn)
    
    #todo dia da semana
    self.dia_em=ui.Label('',frame=(self.btx+self.minus_btn.frame.width/6,self.minus_btn.frame.y+self.minus_btn.frame.height,23,23),text_color='red',font=('HelveticaNeue-Light', 18), alignment=ui.ALIGN_CENTER,text=str(self.hoje.day))
    
    setbox(self.dia_em,'blue')
    self.add_subview(self.dia_em)
    self.dia_em.hidden=True
    
    #todo bt mais
    self.plus_btn = ui.Button(name='+', image=ui.Image('iow:ios7_plus_outline_32'), flex='hl', tint_color='#666', action=self.button_tapped)
    self.plus_btn.frame = (self.btx,self.dia_em.frame.y+self.dia_em.frame.height, 32, 32)
    self.display_view.add_subview(self.plus_btn)
    
    setbox(self.plus_btn)
    #todo bt refresh
    self.refresh_btn = ui.Button(name='refresh', image=ui.Image('typb:Refresh'), flex='hl', tint_color='#666', action=self.refresh_data)
    self.refresh_btn.frame = (self.btx,self.line5lbl.y+self.line5lbl.height +5, 30, 30)
    self.display_view.add_subview(self.refresh_btn)
    setbox(self.refresh_btn)
    
    #todo texto dia da semana por extenso 
    self.dia_semana=ui.Label('wh',frame=(self.btx, self.refresh_btn.y+self.refresh_btn.height/2, 30,30),font=('HelveticaNeue-Light', 14), alignment=ui.ALIGN_CENTER,text=str(self.dia_sem_lookup[self.hoje.weekday()]))
    setbox(self.dia_semana)
    self.display_view.add_subview(self.dia_semana)
    self.dia_semana.hidden=True
    
    
    self.update_view()
    
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
      if i == 0:
        continue
        
      
      lbl.y=prev_y+line1lbl.height+ linesep
      prev_y=lbl.y
    if not self.compact:
      #self.dia_em.y= line5lbl.y+self.line5lbl.height+linesep*8
      #self.dia_semana.y=line5lbl.y+line5lbl.height+linesep
      self.dia_em.hidden=False
      self.plus_btn.hidden=False
      self.minus_btn.hidden=False
      self.dia_em.text=str(self.hoje.day)
      self.dia_semana.hidden = False
    else:
      #self.dia_em.hidden=True
      #self.minus_btn.hidden=True
      #self.plus_btn.hidden=True
      #self.dia_semana.hidden = True
      pass
      
  def set_data(self,new_data):
    self.dia= new_data
    self.update_view()
      
  def refresh_data(self,sender):
    shelve_file  = shelve.open('data')
    dia = shelve_file['dia']
    self.set_data(dia)
  
  def button_tapped(self,sender):
    if sender.name=='+':
      self.hoje +=datetime.timedelta(days=1)
    elif sender.name=='-':
      self.hoje-=datetime.timedelta(days=1)  
    self.diaidx = str(self.hoje.year) + str(self.hoje.month)+ str(self.hoje.day)
    self.update_view()
    
  def update_view(self):
    self.compact = self.height < 150
    self.dia_em.text=str(self.hoje.day)
    self.dia_semana.text=self.dia_sem_lookup[self.hoje.weekday()]
  
    for i, lbl in enumerate(self.labels):
      lbl.text=''
      if self.diaidx not in self.dia.keys() or self.hoje in self.feriados:
        lbl.text='Sem dados'
      else:
        #print('--')
        #print(self.dia[str(self.hoje.day)][i+1]['refeicao']
        #print(self.diaidx)
        refeicao = self.dia[self.diaidx][i+1]['refeicao']
        ementa = self.dia[self.diaidx][i+1]['ementa']
        calorias = str(self.dia[self.diaidx][i+1]['calorias'])
        refeicao =refeicao if len(refeicao) > 0 else ""
        #print(len(refeicao))
        #print(ementa)
        #print(len(calorias) is 0)
        #print('.')
        if len(refeicao) > 0:
          lbl.text = refeicao + '|'
        lbl.text+= ementa 
        if not self.compact:
          if calorias != '{}':
            lbl.text+='|'+calorias
      

def main():
  widget_name = __file__ + str(os.stat(__file__).st_mtime)
  v = appex.get_widget_view()
  # Optimization: Don't create a new view if the widget already shows the :launcher.
  if v is None or v.name != widget_name: 
    shelve_file  = shelve.open('data')
    dia = shelve_file['dia']
    #print('=====keys====')
    #print ('keys',dia.keys())
  
    v = EmentaView(dia)
    v.name = widget_name
    appex.set_widget_view(v)

if __name__ == '__main__':
  main()
