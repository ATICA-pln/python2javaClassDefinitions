'''
Created on 24 oct 2022

@author: Dell Latitude E6540
'''

import os;
from datetime import date;


class pythonObjClass(object):
	
	def __init__(self, objModule, objClass, objSuperClasses={}, objDescription=""):
		# Object module
		self.ObjModule = objModule;
		# Object type
		self.ObjClass = objClass;
		
		# Object superclasses
		self.ObjSuperClasses = objSuperClasses;
		
		# Description
		self.ObjDescription = objDescription;
		
		# Attributes
		self.ObjAttributes = [];
		
		
	def print_java_class(self, package, useLombok=False, printConstructorWithArgs=True, \
				printConstructorWithOutArgs=True, printGetSetters=True):
		
		# print module
		s = "package " + package + ";\n";
		s = s + "\n";
		
		# print class description
		s = s + self.print_java_description();
		
		# print imports
		s = s + self.print_java_imports();
		
		# print lombok declaration
		if useLombok:
			s = s + print_java_lombok();
		
		# print class definition	
		s = s + "public class " + self.ObjClass + " {\n";
		s = s + "\n";	
		
		for attr in self.ObjAttributes:
			s = s + attr.print_java_attribute_declaration();
		s = s + "\n";
		
		if (not useLombok):
			s = s + self.print_java_constructor(printConstructorWithArgs,printConstructorWithOutArgs);
			
		if printGetSetters:
			s = s + self.print_java_get_setter();
			
		s = s + "}";	
			
		return s	
	
	def print_java_get_setter(self):
		
		s = "";
		for attr in self.ObjAttributes:
			s = s + attr.print_java_get_set_methods()

		
		return s
	
	def print_java_constructor(self,printConstructorWithArgs,printConstructorWithOutArgs):
		
		s = "";
		if printConstructorWithOutArgs:
			#s = s + "\t// Class constructor without arguments\n"
			s = s + "\tpublic " + self.ObjClass + "(){\n"
			s = s + "\t}\n";
			s = s + "\n";
			
		if printConstructorWithArgs:
			#s = s + "\t// Class constructor with arguments\n"
			s = s + "\tpublic " + self.ObjClass + "(\n"
			
			# call to constructor
			for attr in self.ObjAttributes:
				s = s + "\t\t\t" +  attr.Class + " " +  attr.Name + ",\n";
			
			s = s[:-2] + ") {\n";
			s = s + "\t\t\n";
			
			# instantiate arguments
			for attr in self.ObjAttributes:
				s = s + "\t\tthis." +  attr.Name + " = " + attr.Name + ";\n";
			
			# close constructor
			s = s + "\t}\n";
			
			s = s + "\n";
		
		return s;
		
		
	
	def print_java_description(self):
		
		s = "/**\n"
		if self.ObjDescription is not None:
			# print class description
			s = s + "* " + self.ObjDescription.replace("\n","\n* ") + "\n"
		
		s = s + "* @author " + os.getlogin() + "\n";
		s = s + "* @version " + date.today().strftime("%Y/%m/%d") + "\n";
		s = s + "* @see " + self.ObjModule + "." + self.ObjClass + "\n";
		
		s = s + "*/\n\n"
		
		return s
	
	def print_java_imports(self):
		
		s = "";
		#s = s + "// imports\n";
		
# # import superclass
# if len(self.ObjSuperClasses)>0:
# 	superClass = self.ObjSuperClasses[list(self.ObjSuperClasses)[0]];
# 	s = s+ "import " + superClass.ObjModule + "." + superClass.ObjClass + ";\n"
#
		# import attribute classes
		
		classesToImport = {"List" : "java.util.List", "Map" : "java.util.Map"}
		
		importedClasses = [];
		for attr in self.ObjAttributes:
			
			for classToImport in classesToImport:
				if (attr.Class.find(classToImport+"<") != -1) & (classToImport not in importedClasses):
					s = s + "import " + classesToImport[classToImport] + " ;\n";
					importedClasses.append(classToImport);
		
		if len(s)>0:	
			s = s+"\n"
			
		return s
		
		
		
def print_java_lombok():
	
		args = ["NoArgsConstructor", "AllArgsConstructor"]; #RequiredArgsConstructor
		
		s = "";
		#s = s + "// lombok imports\n";
		
		# print imports
		for arg in args:
			s = s + "import lombok." + arg + ";\n"
		
		if len(s)>0:	
			s = s+"\n"
		
		# print @
		for arg in args:
			s = s + "@" + arg + "\n"
		
		if len(s)>0:	
			s = s+"\n"
		
		return s 				