package family_metamodel;

/**
* 
* 	classdocs
* 	
* @author Dell Latitude E6540
* @version 2022/10/24
* @see test.python.src.FamilyClassDef.Family
*/

import java.util.Map ;

public class Family {

	Person father;
	Person mother;
	Map<String,Person> childs;

	public Family(){
	}

	public Family(
			Person father,
			Person mother,
			Map<String,Person> childs) {
		
		this.father = father;
		this.mother = mother;
		this.childs = childs;
	}

	public Person getFather() {
		return father;
	}

	public void  setFather(Person father) {
		this.father = father;
	}

	public Person getMother() {
		return mother;
	}

	public void  setMother(Person mother) {
		this.mother = mother;
	}

	public Map<String,Person> getChilds() {
		return childs;
	}

	public void  setChilds(Map<String,Person> childs) {
		this.childs = childs;
	}

}