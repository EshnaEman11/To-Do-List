import os
import json
from datetime import datetime

class FileHandler:
    def _init_(self, filename="tasks.json"):
        self.filename = filename
    
    def set_filename(self, filename):
        """
        Set a new filename for task operations
        
        Args:
            filename (str): Path to the JSON file
        """
        self.filename = filename
    
    def save_tasks(self, tasks):
        """
        Save tasks to a JSON file
        
        Args:
            tasks (dict): Dictionary of tasks with dates as keys
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(self.filename, 'w') as file:
                json.dump(tasks, file, indent=4)
            return True
        except Exception as e:
            print(f"Error saving tasks: {e}")
            return False
    
    def load_tasks(self):
        """
        Load tasks from a JSON file
        
        Returns:
            dict: Dictionary of tasks with dates as keys, empty dict if file doesn't exist or error occurs
        """
        if not os.path.exists(self.filename):
            return {}
        
        try:
            with open(self.filename, 'r') as file:
                tasks = json.load(file)
            return tasks
        except Exception as e:
            print(f"Error loading tasks: {e}")
            return {}
    
    def get_tasks_by_date(self, date_str):
        """
        Get tasks for a specific date
        
        Args:
            date_str (str): Date string in format 'DayName, Month Day, Year'
            
        Returns:
            list: List of tasks for the specified date, empty list if none exist
        """
        tasks = self.load_tasks()
        return tasks.get(date_str, [])
    
    def save_tasks_for_date(self, date_str, day_tasks):
        """
        Save or overwrite tasks for a specific date
        
        Args:
            date_str (str): Date string in format 'DayName, Month Day, Year'
            day_tasks (list): List of task dictionaries for the specified date
            
        Returns:
            bool: True if successful, False otherwise
        """
        all_tasks = self.load_tasks()
        all_tasks[date_str] = day_tasks
        return self.save_tasks(all_tasks)
    
    def clear_tasks_for_date(self, date_str):
        """
        Clear all tasks for a specific date
        
        Args:
            date_str (str): Date string in format 'DayName, Month Day, Year'
            
        Returns:
            bool: True if successful, False otherwise
        """
        all_tasks = self.load_tasks()
        if date_str in all_tasks:
            del all_tasks[date_str]
            return self.save_tasks(all_tasks)
        return True
    
    def clear_all_tasks(self):
        """
        Clear all tasks by creating an empty tasks file
        
        Returns:
            bool: True if successful, False otherwise
        """
        return self.save_tasks({})
        
    def backup_tasks(self):
        """
        Create a backup of the current tasks with timestamp
        
        Returns:
            tuple: (bool, str) Success status and backup filename
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = os.path.basename(self.filename).split('.')[0]
        backup_filename = f"{base_filename}backup{timestamp}.json"
        
        try:
            tasks = self.load_tasks()
            with open(backup_filename, 'w') as file:
                json.dump(tasks, file, indent=4)
            return True, backup_filename
        except Exception as e:
            print(f"Error backing up tasks: {e}")
            return False, None
    
    def get_available_dates(self):
        """
        Get a list of all dates that have tasks
        
        Returns:
            list: List of date strings
        """
        tasks = self.load_tasks()
        return sorted(list(tasks.keys()))

if __name__ == "__main__":
    # Test file handling
    handler = FileHandler()
    
    # Get current date
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    
    # Sample tasks for today
    sample_tasks = [
        {
            "time": "09:30 AM",
            "description": "Complete project documentation",
            "completed": False
        },
        {
            "time": "11:45 AM",
            "description": "Fix bug in login page",
            "completed": False
        },
        {
            "time": "02:00 PM",
            "description": "Meet with team",
            "completed": False
        }
    ]
    
    # Save sample tasks for today
    print(f"Saving sample tasks for {current_date}...")
    
    # Create task dictionary
    tasks_dict = {current_date: sample_tasks}
    
    if handler.save_tasks(tasks_dict):
        print("Tasks saved successfully!")
    
    # Test loading from a different file
    print("\nChanging filename and loading tasks...")
    handler.set_filename("different_tasks.json")
    
    # Create and save different tasks
    different_tasks = {
        current_date: [
            {
                "time": "10:00 AM",
                "description": "Different task 1",
                "completed": False
            },
            {
                "time": "03:30 PM",
                "description": "Different task 2",
                "completed": True
            }
        ]
    }
    
    if handler.save_tasks(different_tasks):
        print("Different tasks saved successfully!")
    
    # Load and display tasks from the new file
    loaded_tasks = handler.load_tasks()
    
    for date, tasks in loaded_tasks.items():
        print(f"\nTasks for {date}:")
        for i, task in enumerate(tasks, 1):
            status = "✓" if task["completed"] else "•"
            print(f"{i}. [{status}] {task['time']} - {task['description']}")
    
    # Create a backup
    print("\nCreating backup...")
    success, backup_file = handler.backup_tasks()
    if success:
        print(f"Backup created successfully! Filename: {backup_file}")