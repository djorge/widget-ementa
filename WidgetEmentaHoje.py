#!python3
# -*- coding: utf-8

'''
This widget script simply shows the current contents of the clipboard.
The clipboard can be cleared by tapping the "trash" button.
'''
#ch



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

linex1=4
liney1=110
linex2=320-4-20
liney2=20
linesep = 2
tamfonte = 12
dia = {}

def make_label(pos,frame, nlines,lb):
  return ui.Label(flex=pos,frame=frame,font = ('Menlo', tamfonte), number_of_lines = nlines, background_color=(0.9,0.9, .9),border_color=(.5, .5, .5), line_break_mode=lb,border_width=1, corner_radius=5)
  pass

def clear_button_tapped(sender):
  clipboard.set('')
  sender.superview['text_label'].text = 'Clipboard:\n'

def main():
  shelve_file  = shelve.open('data')
  hoje = datetime.datetime.now()
  day=hoje.day
  #hoje = datetime.datetime(2017,5,15) 

  dia = shelve_file['dia']
  print ('keys',dia.keys())
  if str(hoje.day) in dia.keys():
    print('Parsing não é necessário .')
  else:
    print('Parsing  é necessário.')

  
  v = ui.View(frame=(0, 0, 320, 220))
  line1lbl=make_label('tr',frame=(linex1, liney1, linex2, liney2),nlines=2, lb=ui.LB_TRUNCATE_TAIL )
  line1lbl.text = dia[str(day)][1]['ementa']
  #line1lbl.text=line1text
  v.add_subview(line1lbl)

  #line2
  line2lbl= make_label('tr',frame=(linex1,line1lbl.y+line1lbl.height+ linesep, linex2, line1lbl.height), nlines=2,lb =ui.LB_TRUNCATE_TAIL)
  line2lbl.text = dia[str(day)][2]['ementa']
  #line2text
  v.add_subview(line2lbl)

  #line3

  line3lbl= make_label('tr',frame=(linex1, line2lbl.y+line1lbl.height+ linesep, linex2, line1lbl.height), nlines=2,lb =ui.LB_TRUNCATE_TAIL)
  line3lbl.text = dia[str(day)][3]['ementa']
  #line3text
  v.add_subview(line3lbl)

  #line4

  line4lbl= make_label('tr',frame=(linex1, line3lbl.y+line3lbl.height+ linesep,linex2, line1lbl.height), nlines=2,lb =ui.LB_TRUNCATE_TAIL)
  line4lbl.text = dia[str(day)][4]['ementa']
  #line4text
  v.add_subview(line4lbl)

  #line5
  line5lbl = make_label('tr',frame=(linex1, line4lbl.y+line4lbl.height+ linesep,linex2, line1lbl.height) ,nlines=2,lb =ui.LB_TRUNCATE_TAIL)
  line5lbl.text = dia[str(day)][5]['ementa']
  #line5text
  v.add_subview(line5lbl)

  '''clear_btn = ui.Button(frame=(320-44, 0, 44, 220), flex='lh')
  clear_btn.image = ui.Image.named('iow:ios7_trash_32')
  clear_btn.action = clear_button_tapped

  v.add_subview(clear_btn)
  '''
  appex.set_widget_view(v)
  shelve_file.close()

    #text = clipboard.get()
    #line1lbl.text = 'Clipboard:\n' + text

if __name__ == '__main__':
  main()

