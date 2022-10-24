package family_metamodel;

/**
* @author Dell Latitude E6540
* @version 2022/10/24
* @see test.python.src.FamilyClassDef.Person
*/

public class Person {

	String name;
	Integer age;

	public Person(){
	}

	public Person(
			String name,
			Integer age) {
		
		this.name = name;
		this.age = age;
	}

	public String getName() {
		return name;
	}

	public void  setName(String name) {
		this.name = name;
	}

	public Integer getAge() {
		return age;
	}

	public void  setAge(Integer age) {
		this.age = age;
	}

}