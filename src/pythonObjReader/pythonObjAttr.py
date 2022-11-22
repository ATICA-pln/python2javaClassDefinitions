'''
Created on 24 oct 2022

@author: Dell Latitude E6540
'''

class pythonObjAttr(object):
	
	def __init__(self, attrName, attrModule, attrType):
		# Attribute name
		
		if attrName == 'package': # reserved keyword in Java, not to be used
			attrName = 'myPackage'; 
		
		self.Name = attrName;
		# Attribute type
		self.ClassModule = attrModule;
		self.Class = attrType;		
		
	def print_java_attribute_declaration(self):
		
		s = "";
		# s = s + "\t// Class attribute " + self.Name + ";\n"
		s = s + "\t" + self.Class + " " +self.Name + ";\n";
		#s = s + "\t\n"
	
		return s
	
	def print_java_get_set_methods(self):
		
		attrName = self.Name[0].upper() + self.Name[1:];
		
		s = "";
		
		# print get
		
		if self.Class == 'boolean':
			getFunc = 'is'
		else:
			getFunc = 'get'
			
		s = s + "\tpublic " +  self.Class + " " + getFunc + attrName + "() {\n";
		s = s + "\t\treturn " + self.Name + ";\n";
		s = s + "\t}\n\n"
		
		# print set
		s = s + "\tpublic void set" + attrName + "(" + \
						self.Class + " " + self.Name + ") {\n";
		s = s + "\t\tthis." + self.Name + " = " + self.Name + ";\n";
		s = s + "\t}\n\n"
		
		return s