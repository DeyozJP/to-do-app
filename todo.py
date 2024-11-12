"""
This module implements a command-line ToDo application that uses an SQLite3 database 
for persistent task management, supporting task addition, viewing, priority modification, 
and deletion with data validation to ensure consistency and quality.

Classes:
- ToDo: Represents the core functionality for managing tasks, with methods to:
  - Create and connect to the database.
  - Validate task attributes such as task ID, name, and priority.
  - Display tasks stored in the database.
  - Add new tasks with a name and priority.
  - Modify the priority of existing tasks.
  - Delete tasks by ID.

Methods:
- create_task_table: Ensures the tasks table exists in the database.
- validate_priority, validate_task_name, validate_id: Validate task attributes 
  for data quality and consistency.
- show_tasks, find_task: Retrieve tasks or check if a specific task exists.
- change_priority, add_task, delete_task: Perform task operations with user input 
  and data validation.
- print_menu, read_user_choice: Display the menu and handle user input choices.

Usage:
- Run this script and follow the prompts to interact with the to-do list.
- Choose from the menu options to add, view, update, or delete tasks.
"""

import sqlite3
import sys

class ToDo:
    """
    Represents a to-do list application that uses an SQLite3 database to manage tasks.

    Attributes:
    - db_name (str): Name of the SQLite3 database file.

    Methods:
    - create_new_todo: Establishes a connection to the database.
    - create_task_table: Creates a tasks table if it doesn't already exist.
    """

    def __init__(self, db_name):
        self.create_new_todo(db_name)
        self.c = self.conn.cursor()
        self.create_task_table ()

    def create_new_todo(self, db_name):
        self.conn = sqlite3.connect(db_name)

    def create_task_table(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS tasks(
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            priority INTEGER NOT NULL);""")
    
    def validate_priority (self, priority):
        """
        Validates and converts the priority input to an integer within the allowed range.

        Parameters:
        - priority (str): The priority value input by the user.

        Returns:
        - int: The priority as an integer if valid, otherwise None with an error message.
        """

        try:
            if priority == "":
                raise ValueError('Priority must not be empty. Enter the priority!')
        except ValueError as e:
            print (e)
            return None
        try:
            priority = int(priority)
        except ValueError as e:
            print ('Invalid input. Please enter a number between 1..10 inclusive.')
            return None

        if not (1 <= priority <= 10):
            print(f'The priority must be the integer between 1..10 inclusive.')
            return None
        
        return priority


    def validate_task_name (self, name):
        """
        Validates the task name, ensuring it is not empty and does not duplicate an existing task.

        Parameters:
        - name (str): The task name input by the user.

        Returns:
        - str: The task name if valid; otherwise, None with an error message.
        """
        try:
            # Validate if the name is not empty string.
            if name == "":
                raise ValueError ("Task name must not be empty.")
                
            # Validate is the name already in the task list. 
            if self.find_task(name):
                raise ValueError (f"The {name} is already in the todo list.")
        except ValueError as e:
            print (e)
            return None
        else:
            return name


    def validate_id (self, id):
        """
        Validates a task ID, ensuring it is not empty, is an integer, and exists in the database.

        Parameters:
        - id (str): The task ID input by the user.

        Returns:
        - int: The validated ID if it is valid and exists in the database; otherwise, None with an error message.
        """

        try:
            if id == "":
                raise ValueError ("the id must not be empty. Please enter an id! ")
        except ValueError as e:
            print (e)
            return None
        try:
            id = int(id)
        except ValueError:
            print ("Invalid id. Please enter a integer number")
            return None
        try:  
            _, records = self.show_tasks()
            id_list = [record[0] for record in records]
            if id not in id_list:
                raise ValueError (f'The id {id} is not in the database.')
        except ValueError as e:
            print (e)
            return None
        return id
        

    def show_tasks(self):
        """
        Fetches and returns all tasks from the database.

        Retrieves all tasks stored in the database, returning both a list of task names and a list of full records.

        Returns:
        - tuple: A tuple containing:
            - list: A list of task names.
            - list: A list of tuples, each representing a complete task record (id, name, priority).
        """
        task_name = []
        self.c.execute ("SELECT * FROM tasks")
        records = self.c.fetchall()
        for record in records:
            task_name.append(record[1])
        return task_name, records


    def find_task (self, name):
        """
        Searches for a task by name in the database.

        Iterates over all tasks to find a record that matches or contains the specified name, ignoring case and extra spaces.

        Args:
            name (str): The name (or partial name) of the task to search for.

        Returns:
            tuple or None: The full task record (id, name, priority) if found; otherwise, None.
        """

        present_record = None
        _, records = self.show_tasks()
        for record in records:
            if name in record[1].strip().lower():
                present_record = record

        return present_record
    
    
    def change_priority(self):
        """
        Prompts the user to change the priority of an existing task in the database.

        The method repeatedly asks for a new priority and task ID until valid inputs are provided. It then updates the priority of the task with the specified ID in the database.

        Raises:
            ValueError: If the user inputs invalid priority or task ID.

        Side Effects:
            Modifies the 'tasks' table in the database by updating the priority for the specified task.
        """

        try:
            while True:
                new_priority = input("Enter a new priority: ")
                # Validate new priority.
                validated_new_priority = self.validate_priority(new_priority)
                if validated_new_priority is not None:
                    break

            while True:
                id = input("Enter the task id: ")
                validated_id = self.validate_id(id)
                if validated_id is not None:
                    break

            # if validated_new_priority is not None and validated_id is not None:
            self.c.execute("UPDATE tasks SET priority = ? WHERE id = ?", (validated_new_priority, validated_id))
            self.conn.commit()
        except ValueError as e:
            print (e)
        except:
            print ("Error!")
        else:
            print(f'New priority "{validated_new_priority}" has been updated in the task id: "{validated_id}".')
    

    def add_task(self):
        """
        Prompts the user to enter a task name and priority, validates the inputs, and adds the task to the database.

        The method ensures that the task name is unique and that the priority is within the acceptable range (1 to 10). If valid inputs are provided, the task is inserted into the 'tasks' table in the database.

        Raises:
            Exception: If there is an error during task addition (e.g., database issues).

        Side Effects:
            Adds a new task to the 'tasks' table in the database with the specified name and priority.
        """

        try:
            while True:
                # Take input for task name.
                name = input("Enter a task name: ").strip().lower()
                # Validate name.
                validated_name = self.validate_task_name(name)
                if validated_name is not None:
                    break

            while True:
            # Take input for priority.
                priority = input("Enter a priority: ")
                # Validate priority
                validated_priority = self.validate_priority(priority)
                if validated_priority is not None:
                    break
        except Exception as e:
            print (e)
            return none
        else:
            # If the validation is passed, entered the name and priority in the database.
            self.c.execute("INSERT INTO tasks (name, priority) VALUES (?, ?)", (validated_name, validated_priority))
            self.conn.commit()
            print (f'{name}, and {priority} has been successfully entered into the database.')
    
    
    def delete_task (self):
        """
        Prompts the user to enter a task ID, validates the ID, and deletes the corresponding task from the database.

        The method checks if the provided ID exists in the database and ensures it is a valid integer. If the ID is valid, the task is removed from the 'tasks' table. If validation fails, no task is deleted.

        Raises:
            ValueError: If the provided ID is invalid or not found in the database.

        Side Effects:
            Deletes a task from the 'tasks' table in the database.
        """

        try:
            id_to_delete = input("Enter id to delete: ")
            validated_id = self.validate_id(id_to_delete)
        except ValueError as e:
            print (e)
        else:
            if validated_id is not None:
                self.c.execute("DELETE FROM tasks WHERE id =?", (validated_id,))
                self.conn.commit()
                print (f'The entries with "{validated_id}" has been deleted.')
            else:
                print ('None of the entries have been deleted.')

    def print_menu (self):
        """
        Prints the header and main menu options for the ToDo application.

        This method displays a formatted header followed by a list of menu options that allow the user to interact with the ToDo application. The options include viewing tasks, adding a task, changing task priority, deleting a task, and exiting the application.

        Side Effects:
            Prints the menu and header to the console.
        """
        # Print header.
        print ("+" +"-" * 50 + "+")
        print ("|                  ToDo Application                |")
        print ("+" +"-" * 50 + "+")
        print ("M E N U")
        print ("1. Show tasks")
        print ("2. Add Task")
        print ("3. Change priority")
        print ("4. Delete task")
        print ("5. Exit")

    def read_user_choice (self):
        """
        Reads and validates the user's menu choice input.

        This method prompts the user to enter a choice between 1 and 5, corresponding to the available options in the ToDo application. If the input is invalid (either non-numeric or outside the valid range), an error message is displayed, and the input is not accepted.

        Returns:
            str: The validated user choice as a string.

        Side Effects:
            Prints error messages to the console if the input is invalid.
        """

        try:
            choice  = int(input("Enter your choice(0..5):  "))
            if choice not in list(range(1, 6)):
                raise ValueError ("Enter a number to choose an option as shown in menu.")
        except ValueError as e:
            print (e)
        return str(choice)




