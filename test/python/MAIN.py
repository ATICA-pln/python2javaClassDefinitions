## python2javaClassDefinitions
# Test example

# import paths
import __paths

# import example classes
from test.python.src.FamilyClassDef import Family
from test.python.src.FamilyClassDef import Person

# import library that will be used to transform the object to json
import jsonpickle

# import pythonObjReader
from src.pythonObjReader.pythonObjReader import pythonObjReader

def instantiate_object():

	# Very simple example object
	father = Person("Joe",59)
	mother = Person("Karen",58)
	
	childs = {"Paul": Person("Paul",29), "Jane": Person("Jane",27), "Willy": Person("Willy",23)}
	
	myFamily = Family(father, mother, childs)
	
	return myFamily


def print_pyobj2json(pyObj,file_path):

	data = jsonpickle.encode(pyObj);
	
	f = open(file_path,'w')
	data = f.write(data)
	f.close()


def print_pyclassdef(pyObj,folder_path,package,extension):
	
	pyObjReader = pythonObjReader(folder_path,package,extension);
	pyObjReader.readObj(pyObj);
	pyObjReader.printObjDef2Java(useLombok=False,printConstructorWithArgs=True,\
				printConstructorWithOutArgs=True, printGetSetters=True);
	
	
## test
if __name__ == "__main__":
	
	myObj = instantiate_object();
	
	file = "../py2java_folder/myFamily.json"
	print_pyobj2json(myObj,file);
	
	java_classes_folder = "../java/src"
	java_package = "family_metamodel"
	print_pyclassdef(myObj,java_classes_folder,java_package,"java");
	
	