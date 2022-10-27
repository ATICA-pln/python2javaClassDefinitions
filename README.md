# python2javaClassDefinitions
Export python class definitions to java and use them to load JSON objects

## Description

`pythonObjReader` implements methods to inspect a python object and create a java class definition to replicate the same object in java. A few options are available to include the class constructors and get/set methods for the attributes.

This repository includes a python script that instantiates a basic example of python object and writes it into a JSON file. Then, the java classes are generated automatically using `pyhtonObjReader`.

A sample java application loads the JSON file and re-instantiates the classes, this time in java, using the automatically generated model.

## Usage

`pythonObjReader`allows to connect a python and java application through a JSON link. This is useful when trying to use python libraries from a java front end. 

Other use cases: 
- Migration from python to java
- Automatic generation of classes from descriptors/metamodels
- Distributed applications
- ...
