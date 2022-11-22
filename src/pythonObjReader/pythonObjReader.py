'''
Created on 20 oct 2022

@author: Dell Latitude E6540
'''

import types;
import os;
from .pythonObjClass import pythonObjClass
from .pythonObjAttr import pythonObjAttr

#import sys
#sys.setrecursionlimit(10000)


class pythonObjReader(object):
	'''
	classdocs
	'''
	def __init__(self, outputFolder, package, ext):
		
		self.package = package;
		self.outputFolder = outputFolder;
		
		self.package = package;
		
		self.extension = ext;
		
		self.Objects = {};
		self.Classes = {};

	def readObj(self,pyObj):
		
		# get main features of class
		classModule = pyObj.__class__.__module__;
		classType   = pyObj.__class__.__name__;
		classDescription = pyObj.__class__.__doc__;
		
		if classType=="PropertyValueRecord":
			pass
		
		# check if class inherits from a superclass
		superClasses = self.checkSuperClasses(pyObj);
				
		# initialize class and add to list
		pyObjClass = pythonObjClass(classModule,classType,superClasses,classDescription);
		self.Objects[id(pyObj)] = pyObjClass;
		self.Classes[classType] = pyObjClass;
		
		print("Retrieving object definition: " + pyObjClass.ObjClass);
		
		# check class attributes
		objDict = pyObj.__dict__;
		
		for dictKey in objDict:
			attrName = dictKey;
			attrValue = pyObj.__getattribute__(attrName);
			
			objAttr = self.checkAttribute(attrName, attrValue);
			pyObjClass.ObjAttributes.append(objAttr);
		
		# Update list of classes
		self.Objects[id(pyObj)] = pyObjClass;
		self.Classes[classType] = pyObjClass;
		
		return pyObjClass
	
	def checkSuperClasses(self, pyObj):
		
		superClasses = {};
		
		for thisSuperClass in pyObj.__class__.__bases__:
			# check if the superclass has a constructor
			if (thisSuperClass != object().__class__) & \
			   (thisSuperClass.__init__.__class__ == types.FunctionType) :
				thisSuperClassType = thisSuperClass.__name__;
				# check if the superclass is already in the list
				if (thisSuperClass.__name__ not in self.listOfClasses()): 
					
					# call class constructor with dummy arguments 
					NbArgs = thisSuperClass.__init__.__code__.co_argcount;
					dummyArgs = [None] * (NbArgs-1);
					pySuperObj = thisSuperClass(*dummyArgs);
					
					# retrieve actual arguments and overwrite dummies
					for thisKey in pySuperObj.__dict__.keys():
						pySuperObj.__dict__[thisKey] = pyObj.__dict__[thisKey];
					
					# add class to reader 
					pySuperClassObj = self.readObj(pySuperObj);	
					
				else:
					pySuperClassObj = self.Classes[thisSuperClassType]
				
				superClasses[thisSuperClassType] = pySuperClassObj;
		
		return superClasses
	
	def listOfObjects(self):
		
		listAllObjects = self.Objects.keys();
	
		return listAllObjects
	
	def listOfClasses(self):
		
		listAllClasses = self.Classes.keys();
	
		return listAllClasses
	
	def printObjDef2Java(self,pyObjClass=None,useLombok=False,printConstructorWithArgs=True,\
				printConstructorWithOutArgs=True, printGetSetters=True, superclassDeclaration=None):
		
		if pyObjClass == None:
			
			for pyObjClassType in self.Classes:
				self.printObjDef2Java(self.Classes[pyObjClassType],useLombok, printConstructorWithArgs, \
										printConstructorWithOutArgs, \
										printGetSetters, superclassDeclaration);		
			
		else:
		
			if (self.package is not None) & (self.package != ""):
				outputFolder = self.outputFolder + "/" + self.package;
			# check if directory exists
			folderExist = os.path.exists(outputFolder);
			
			if (not folderExist):
				os.makedirs(outputFolder);
		
			# file name and path to file
			FILE_NAME = pyObjClass.ObjClass + "." + self.extension;
			FILE_PATH = outputFolder + "/" + FILE_NAME;
			
			# print file
			f = open(FILE_PATH,'w')
			f.write(pyObjClass.print_java_class(self.package, useLombok, \
										printConstructorWithArgs, \
										printConstructorWithOutArgs, \
										printGetSetters, superclassDeclaration))
			f.close()	
			
			print("-> New object definition: " + pyObjClass.ObjClass + " saved in " + FILE_PATH);
			
		
	def checkAttribute(self, attrName, thisAttribute, arrayType=None):
		
		attrModule = thisAttribute.__class__.__module__;
		attrClass = thisAttribute.__class__.__name__;
		
		def add_array_type(arrayType,attrClass):
			if arrayType in ("List", "HashSet", "Pair", "Triplet"):
				attrClassModif = arrayType+"<"+attrClass+">";
			elif arrayType=="Map":
				attrClassModif = arrayType+"<String,"+attrClass+">";
			else:
				attrClassModif = attrClass
			return attrClassModif
			
		objAttr = pythonObjAttr(attrName, attrModule, add_array_type(arrayType,attrClass));
		
		if attrClass == 'list':
			
			if len(thisAttribute)>0:
				
				listElemClassTypes = thisAttribute[0].__class__;
				use_superClass = False;
				
				for listElem in thisAttribute:
					if listElem.__class__ != listElemClassTypes:
						use_superClass = True;
					objAttr = self.checkAttribute(attrName, listElem, 'List');
			
				if use_superClass:
					attrModule = listElemClassTypes.__base__.__module__;
					attrClass = listElemClassTypes.__base__.__name__;
				
					objAttr = pythonObjAttr(attrName, attrModule,  add_array_type(arrayType, add_array_type("List",attrClass)));
				
			else:
				objAttr = pythonObjAttr(attrName, attrModule, add_array_type(arrayType,add_array_type("List","Object")));
				
		elif attrClass == 'set':
			objAttr = pythonObjAttr(attrName, attrModule, add_array_type(arrayType,add_array_type("HashSet","Integer")));
		
		elif attrClass == 'tuple':		
			if len(thisAttribute)==2:
				tupleType = 'Pair'
				
			elif len(thisAttribute)==3:	
				tupleType = 'Triplet'
				
			else:
				tupleType = 'JavaTuple'
				
			tupleClasses=''
			p = True
			for tuppleAttribute in thisAttribute:
				
				tmpObjAttr = self.checkAttribute('tupleAttr', tuppleAttribute);
				if p:
					tupleClasses = tmpObjAttr.Class;
					p = False;
				else:	
					tupleClasses = tupleClasses+","+tmpObjAttr.Class;
				
			
			objAttr = pythonObjAttr(attrName, attrModule, add_array_type(arrayType, add_array_type(tupleType,tupleClasses)));	
				
		elif attrClass == 'dict':
			
			dictTypes = list(set(thisAttribute.values()));
			
			if len(dictTypes)==1:
					
				attrModule = dictTypes[0].__class__.__module__;
				attrClass = dictTypes[0].__class__.__name__;
				
				objAttr = self.checkAttribute(attrName, dictTypes[0], 'Map');
				
			elif len(dictTypes)==0:	
				
				objAttr = pythonObjAttr(attrName, attrModule, add_array_type(arrayType,add_array_type('Map','Object')));
				
			else:
				
				for myType in dictTypes:
					
					if myType.__class__ != type(None):
					
						attrModule = myType.__class__.__module__;
						attrClass = myType.__class__.__name__;
					
						tmpObjAttr = self.checkAttribute(attrName, myType);
					
						attrSuperClass = myType.__class__.__base__;
					
						objAttr = pythonObjAttr(attrName, attrModule, add_array_type(arrayType,add_array_type("Map", attrSuperClass.__name__)));	
				
		elif (attrModule != 'builtins') & (id(thisAttribute) not in self.listOfObjects()): 
			
			## Add new class to list
			pyObjClassChild = self.readObj(thisAttribute);
					
			objAttr = pythonObjAttr(attrName, attrModule,  add_array_type(arrayType,attrClass));
			
		elif (attrModule == 'builtins'):
		
			pyBuiltins2Java = {"str": "String",
							   "int": "int",
							   "bool": "boolean", 
							   "NoneType": "Object"};

			JavaType = pyBuiltins2Java[attrClass];
			objAttr = pythonObjAttr(attrName, attrModule, add_array_type(arrayType,JavaType));
			
		else: # element already known
			objAttr = pythonObjAttr(attrName, attrModule,  add_array_type(arrayType,attrClass));
		
		return objAttr;
		

						