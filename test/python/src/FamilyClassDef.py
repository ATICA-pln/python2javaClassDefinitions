'''
Created on 21 oct 2022

@author: Dell Latitude E6540
'''

import json

class Family(object):
	'''
	classdocs
	'''

	def __init__(self, father, mother, childs):
		'''
		Constructor
		'''
		self.father = father
		self.mother = mother
		self.childs = childs
		

		
class Person(object):
	
	def __init__(self, name, age):
		
		self.name = name
		self.age = age
		
