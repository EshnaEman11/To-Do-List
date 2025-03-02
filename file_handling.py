import json
import os
from datetime import datetime

class FileHandler:
    def _init_(self, filename="tasks.json"):
        """Initialize FileHandler with the given filename"""
        self.filename = filename
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        if not os.path.exists(self.filename):
            return {}
        
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            # Return empty dict if file is invalid
            return {}
        except Exception as e:
            print(f"Error loading tasks: {str(e)}")
            return {}
    
    def save_tasks(self, tasks):
        """Save tasks to JSON file"""
        try:
            # Create directory if it doesn't exist
            directory = os.path.dirname(self.filename)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            with open(self.filename, 'w') as file:
                json.dump(tasks, file, indent=2)
            return True
        except Exception as e:
            print(f"Error saving tasks: {str(e)}")
            return False
    
    def backup_tasks(self):
        """Create a backup of the tasks file"""
        if not os.path.exists(self.filename):
            return False
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{os.path.splitext(self.filename)[0]}backup{timestamp}.json"
            
            with open(self.filename, 'r') as src:
                with open(backup_filename, 'w') as dest:
                    dest.write(src.read())
            return True
        except Exception as e:
            print(f"Error creating backup: {str(e)}")
            return False