package main;

import java.io.IOException;
import java.io.Reader;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Map;

import javax.validation.Path;

import com.google.gson.Gson;

import family_metamodel.Family;
import family_metamodel.Person;

public class MAIN {
	
	public static void main(String[] args) {
		
		System.out.println("Hello World!");
		
		Gson gson = new Gson();
		
		try {
			String WorkingDir = System.getProperty("user.dir");
			
			System.out.println("Reading json file...");
			java.nio.file.Path path = Paths.get(WorkingDir + "\\..\\py2java_folder\\myFamily.json");
			Reader reader = Files.newBufferedReader(path);
			
			System.out.println("Instantiate object...");
			Family myFamily = gson.fromJson(reader, Family.class);
			
			System.out.println("Print mother name: ");
			System.out.println("-> Mother: " + myFamily.getMother().getName());
			
			System.out.println("Check that children object is a map of <String, Person>: ");
			
			for (Map.Entry<String, Person> entry : myFamily.getChilds().entrySet()) {
				System.out.println(entry.getKey() + "/" + entry.getValue());
			}
						
			System.out.println("Print object in json...");
			String myFamilyJson = gson.toJson(myFamily);
			
			System.out.println(myFamilyJson);
			
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		
		
		
	}

}
