import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from datetime import datetime
import file_handling

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("500x450")
        
        # Initialize file handler
        self.file_handler = file_handling.FileHandler("tasks.json")
        
        # Tasks dictionary with dates as keys
        self.tasks = self.file_handler.load_tasks()
        self.current_date = self.get_formatted_date()
        
        self.create_widgets()
        self.load_tasks_for_date(self.current_date)
    
    def get_formatted_date(self, date_obj=None):
        """Returns date in format: YYYY-MM-DD"""
        if date_obj is None:
            date_obj = datetime.now()
        return date_obj.strftime("%Y-%m-%d")
    
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title and date
        tk.Label(main_frame, text="To-Do List", font=("Arial", 16, "bold")).pack(pady=5)
        self.date_label = tk.Label(main_frame, text=f"Date: {self.current_date}", font=("Arial", 12))
        self.date_label.pack(pady=5)
        
        # Date selection frame
        date_frame = tk.Frame(main_frame)
        date_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(date_frame, text="Today", command=self.set_today).pack(side=tk.LEFT, padx=5)
        tk.Button(date_frame, text="Choose Date", command=self.choose_date).pack(side=tk.LEFT, padx=5)
        tk.Button(date_frame, text="Tomorrow", command=self.set_tomorrow).pack(side=tk.LEFT, padx=5)
        
        # Task entry
        entry_frame = tk.Frame(main_frame)
        entry_frame.pack(fill=tk.X, pady=10)
        
        self.task_entry = tk.Entry(entry_frame, width=40)
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.task_entry.bind("<Return>", lambda event: self.add_task())
        
        tk.Button(entry_frame, text="Add Task", command=self.add_task).pack(side=tk.LEFT, padx=5)
        
        # Task listbox
        list_frame = tk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.task_listbox = tk.Listbox(
            list_frame, 
            width=50, 
            height=15,
            font=("Arial", 12),
            selectmode=tk.SINGLE,
            yscrollcommand=scrollbar.set
        )
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.task_listbox.yview)
        
        # Button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(button_frame, text="Mark Complete", command=self.mark_complete).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Delete Task", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Clear Display", command=self.clear_display).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Save", command=self.save_tasks).pack(side=tk.LEFT, padx=5)
    
    def load_tasks_for_date(self, date):
        """Load tasks for a specific date"""
        self.task_listbox.delete(0, tk.END)
        if date in self.tasks:
            for task in self.tasks[date]:
                status = "✓ " if task["completed"] else "• "
                self.task_listbox.insert(tk.END, f"{status}{task['text']}")
                if task["completed"]:
                    self.task_listbox.itemconfig(tk.END-1, fg="gray")
    
    def set_today(self):
        """Set the current date to today"""
        self.current_date = self.get_formatted_date()
        self.date_label.config(text=f"Date: {self.current_date}")
        self.load_tasks_for_date(self.current_date)
    
    def set_tomorrow(self):
        """Set the current date to tomorrow"""
        tomorrow = datetime.now().replace(day=datetime.now().day + 1)
        self.current_date = self.get_formatted_date(tomorrow)
        self.date_label.config(text=f"Date: {self.current_date}")
        self.load_tasks_for_date(self.current_date)
    
    def choose_date(self):
        """Let user choose a specific date"""
        date_str = simpledialog.askstring("Choose Date", "Enter date (YYYY-MM-DD):")
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                self.current_date = self.get_formatted_date(date_obj)
                self.date_label.config(text=f"Date: {self.current_date}")
                self.load_tasks_for_date(self.current_date)
            except ValueError:
                messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
    
    def add_task(self):
        """Add a new task for the current date"""
        task_text = self.task_entry.get().strip()
        if task_text:
            if self.current_date not in self.tasks:
                self.tasks[self.current_date] = []
            
            self.tasks[self.current_date].append({
                "text is this:": task_text,
                "completed": False
            })
            
            self.load_tasks_for_date(self.current_date)
            self.task_entry.delete(0, tk.END)
            self.save_tasks()
        else:
            messagebox.showwarning("Warning", "Please enter a task!")
    
    def mark_complete(self):
        """Mark the selected task as completed"""
        try:
            selected_index = self.task_listbox.curselection()[0]
            if self.current_date in self.tasks and selected_index < len(self.tasks[self.current_date]):
                self.tasks[self.current_date][selected_index]["completed"] = True
                self.load_tasks_for_date(self.current_date)
                self.save_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task!")
    
    def delete_task(self):
        """Delete the selected task"""
        try:
            selected_index = self.task_listbox.curselection()[0]
            if self.current_date in self.tasks and selected_index < len(self.tasks[self.current_date]):
                del self.tasks[self.current_date][selected_index]
                self.load_tasks_for_date(self.current_date)
                self.save_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task!")
    
    def clear_display(self):
        """Clear the display without deleting tasks from file"""
        self.task_listbox.delete(0, tk.END)
    
    def save_tasks(self):
        """Save tasks to file"""
        self.file_handler.save_tasks(self.tasks)

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()