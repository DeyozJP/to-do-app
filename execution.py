"""
This module provides a command-line interface for managing tasks in a to-do list, 
using an SQLite3 database to ensure persistent, consistent, and high-quality data storage.

The application allows users to:
1. Add new tasks to the to-do list.
2. View all existing tasks.
3. Change the priority level of specific tasks.
4. Delete tasks by ID.
5. Exit the application.

Data consistency and quality are maintained through rigorous validation:
- Task IDs are checked to ensure they exist in the database before modification or deletion.
- Priority values are restricted to integers between 1 and 10, inclusive, ensuring valid task prioritization.
- Task names are validated to prevent empty entries, enhancing the reliability of stored data, and checked against the entries in the database to avoid the redundancy.

Upon execution, the program connects to the specified SQLite3 database (creating it if it doesn’t exist) 
and repeatedly displays a menu to the user for task management until they choose to exit.

Functions:
- execute_choice(value, task_list): Executes the task operation based on user input, validating choices as needed.
- run_application(db_name): Initializes and runs the to-do application using the specified SQLite3 database.

Dependencies:
- sqlite3 (built-in): Manages the connection to the SQLite3 database.
- sys (built-in): Allows for graceful program termination.
- todo (custom module): Contains the `ToDo` class, which defines methods for validated interaction with tasks.

Usage:
Run the script to start the to-do list application. Follow the menu prompts to interact with tasks while ensuring data consistency.
"""


import todo
import sys

if len(sys.argv) != 2:
    print ("Provide the name for the database to connect to existing one or to create new one.")
    print (("Usage: execution.py, <database_name>"))
database_name = sys.argv[1]



def execute_choice (value, task_list):
    if value == "5":
        print ("You exit the program. Bye!")

    elif value == "4":
        task_list.delete_task ()
        print ()
        task_list.print_menu ()
        
        
    elif value == "3":
        task_list.change_priority ()
        print ()
        task_list.print_menu ()
        
        
    elif value == "2":
        task_list.add_task ()
        print ()
        task_list.print_menu ()
        

    elif value == "1":
        _, records = task_list.show_tasks ()
        
        if len(records) == 0:
            print ("There is no task. ")
        for record in records:
            print (record)
        print()
        task_list.print_menu ()
       


def run_application (db_name):
    new_todo = todo.ToDo(db_name) # Creating db if db in not exsisted, connecting otherwise
    new_todo.print_menu()

    while True:
        choice = new_todo.read_user_choice ()
        if choice == "5" :
            print ("You exit the program. Bye!")
            sys.exit(0)
        else:
            execute_choice(choice, new_todo)
            

    
run_application(database_name + ".db")


    