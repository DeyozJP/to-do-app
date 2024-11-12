# To-Do Application

This is a simple Python-based To-Do application that helps you manage your tasks through a command-line interface. It uses SQLite3 as a lightweight database to store and organize tasks. The app allows users to add, update, delete, and view tasks with basic priority levels, ensuring effective task management.

## Features

- **Add Tasks**: Enter a task name and priority, and the task will be saved to the database.
- **Update Task Priority**: Change the priority of an existing task.
- **Delete Tasks**: Remove tasks from the database using their unique ID.
- **View Tasks**: List all the tasks along with their priorities.
- **Data Validation**: Ensures correct task name, valid priority (1-10), and existing task ID before adding or updating tasks.

## Installation

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/your-username/todo-application.git

## File Structure

Here is the structure of the project:


- **`todo.py`**: This file defines the `ToDo` class and its methods for task management. It includes functions like adding a task, changing priorities, deleting tasks, and showing tasks.
- **`execution.py`**: This is the main execution file that runs the program. It interacts with the `ToDo` class, displays the menu to the user, and handles input/output.
- **`mitthal_to.db`**: A sample SQLite3 database containing initial task data for demonstration purposes.


