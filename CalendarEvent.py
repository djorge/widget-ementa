# coding: utf-8
#!python27
import datetime
from datetime import date
from objc_util import *
		
class TipoFalta:
	Ferias, Dispensa, Nada = range(3)

class CalendarEvent:
	def __init__(self):
		# EKEventStore = calendar database
		#global store
		
		self.store = ObjCClass('EKEventStore').alloc().init()

		# Once Pythonista has been authorized, this code does not need to be executed
		#------- begin of commented code
		'''access_granted = threading.Event()
		def completion(_self, granted, _error):
			access_granted.set()
		completion_block = ObjCBlock(completion, argtypes=[c_void_p, c_bool, c_void_p])
		store.requestAccessToEntityType_completion_(0, completion_block)
		access_granted.wait()'''
		#------- end of commented

	def EventsFromDay(self, dt):
		#global store
		dt1 = dt.strftime('%Y%m%d')
		# Convert string yyyymmdd to NSdate
		dateFormat = ObjCClass('NSDateFormatter').alloc().init()
		dateFormat.setDateFormat_('yyyyMMdd HH:mm')
		date1 = dateFormat.dateFromString_(dt1+' 00:01') 
		date2 = dateFormat.dateFromString_(dt1+' 23:59') 
		#print('event begin:{} event end:{}'.format(date1,date2))
	
		predicate = self.store.predicateForEventsWithStartDate_endDate_calendars_(date1, date2, None)
		self.events = self.store.eventsMatchingPredicate_(predicate)
		self.events_array = [] 
		if len(self.events) >0:
			for event in self.events:
				title='{}'.format(event.title())
				
				#print('%s:',title)
	
				if title == 'Férias':
					return TipoFalta.Ferias
				elif title == 'Dispensa':
					return TipoFalta.Dispensa
		return TipoFalta.Nada
'''
cal = CalendarEvent()

if (cal.EventsFromDay(datetime.datetime(2017,9,4)))== TipoFalta.Ferias:
	print('Férias')
'''
