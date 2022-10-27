'''
Created on 20 oct 2022

@author: Dell Latitude E6540
'''

import types;
import os;
from .pythonObjClass import pythonObjClass
from .pythonObjAttr import pythonObjAttr

class pythonObjReader(object):
	'''
	classdocs
	'''
	def __init__(self, outputFolder, package, ext):
		
		self.package = package;
		self.outputFolder = outputFolder;
		
		self.package = package;
		
		self.extension = ext;
		
		self.Classes = {};


	def readObj(self,pyObj):
		
		# get main features of class
		classModule = pyObj.__class__.__module__;
		classType   = pyObj.__class__.__name__;
		classDescription = pyObj.__class__.__doc__;
		
		# check if class inherits from a superclass
		superClasses = self.checkSuperClasses(pyObj);
				
		# initialize class and add to list
		pyObjClass = pythonObjClass(classModule,classType,superClasses,classDescription);
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
				if (thisSuperClassType not in self.listOfClasses()): 
					
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
		
		if arrayType=="List":
			attrClassModif = arrayType+"<"+attrClass+">";
		elif arrayType=="Map":
			attrClassModif = arrayType+"<String,"+attrClass+">";
		else:
			attrClassModif = attrClass
			
		objAttr = pythonObjAttr(attrName, attrModule, attrClassModif);
		
		if attrClass == 'list':
			if len(thisAttribute)>0:
				objAttr = self.checkAttribute(attrName, thisAttribute[0], 'List');
			else:
				objAttr = pythonObjAttr(attrName, attrModule, "List<Object>")
				
		elif attrClass == 'dict':
			dictTypes = set(map(type,thisAttribute.values()));
			if len(dictTypes)==1:
				
				attrModule = list(dictTypes)[0].__module__;
				attrClass = list(dictTypes)[0].__name__;
				
				objAttr = self.checkAttribute(attrName, list(thisAttribute.values())[0], 'Map');
				
				
			else:
				objAttr = pythonObjAttr(attrName, attrModule, "Map<String,Object>");
					
		elif (attrModule != 'builtins') & (attrClass not in self.listOfClasses()): 
			
			## Add new class to list
			pyObjClassChild = self.readObj(thisAttribute);
					
			objAttr = pythonObjAttr(attrName, attrModule, attrClassModif);
			
		elif (attrModule == 'builtins'):
		
			pyBuiltins2Java = {"str": "String",
							   "int": "Integer",
							   "bool": "Boolean", 
							   "NoneType": "Object"};

			JavaType = pyBuiltins2Java[attrClass];
			objAttr = pythonObjAttr(attrName, attrModule, JavaType);
			
		else: # element already known
			objAttr = pythonObjAttr(attrName, attrModule, attrClassModif);
		
		return objAttr;
		

						