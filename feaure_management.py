import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, filedialog
import file_handling
from datetime import datetime
import calendar
import os

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Tasks dictionary with dates as keys
        self.tasks = {}
        self.current_date = self.get_formatted_date()
        
        # Load tasks if available
        self.file_handler = file_handling.FileHandler()
        self.tasks = self.file_handler.load_tasks()
        
        self.create_widgets()
        
    def get_formatted_date(self):
        """Returns current date in format: DayName, Month Day, Year"""
        now = datetime.now()
        return now.strftime("%A, %B %d, %Y")
        
    def get_formatted_time(self):
        """Returns current time in format: HH:MM AM/PM"""
        now = datetime.now()
        return now.strftime("%I:%M %p")
    
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title label
        title_label = tk.Label(main_frame, text="Task Manager", font=("Arial", 16, "bold"))
        title_label.pack(pady=5)

        self.date_label = tk.Label(main_frame, text=self.current_date, font=("Arial", 12))
        self.date_label.pack(pady=5)
        
        # File operations frame
        file_frame = tk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=5)
        
        # Load file button
        load_file_button = tk.Button(file_frame, text="Load From File", command=self.load_from_file)
        load_file_button.pack(side=tk.LEFT, padx=5)
        
        # Save to file button
        save_file_button = tk.Button(file_frame, text="Save To File", command=self.save_to_file)
        save_file_button.pack(side=tk.LEFT, padx=5)
        
        # Current file label
        self.file_label = tk.Label(file_frame, text=f"Current file: {self.file_handler.filename}", font=("Arial", 10))
        self.file_label.pack(side=tk.LEFT, padx=10)
        
        # Date selector frame
        date_frame = tk.Frame(main_frame)
        date_frame.pack(fill=tk.X, pady=5)
        
        # Load tasks by date button
        load_date_button = tk.Button(date_frame, text="Load Date", command=self.load_date)
        load_date_button.pack(side=tk.LEFT, padx=5)
        
        # Combobox for available dates
        self.date_combo = ttk.Combobox(date_frame, width=30)
        self.date_combo.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.update_date_combo()
        
        # Task input frame
        input_frame = tk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        # Task entry
        self.task_entry = tk.Entry(input_frame, width=50)
        self.task_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.task_entry.bind("<Return>", lambda event: self.add_task())
        
        # Add button
        add_button = tk.Button(input_frame, text="Add Task", command=self.add_task)
        add_button.pack(side=tk.LEFT, padx=5)
        
        # Task listbox frame
        list_frame = tk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Task listbox with time column
        self.task_listbox = tk.Listbox(
            list_frame, 
            selectmode=tk.SINGLE, 
            width=60, 
            height=15,
            font=("Arial", 12),
            yscrollcommand=scrollbar.set
        )
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.task_listbox.yview)
        
        # Populate listbox with tasks for current date
        self.refresh_task_list()
        
        # Button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        # Remove button
        remove_button = tk.Button(button_frame, text="Complete Task", command=self.remove_task)
        remove_button.pack(side=tk.LEFT, padx=5)
        
        # Edit button
        edit_button = tk.Button(button_frame, text="Edit Task", command=self.edit_task)
        edit_button.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        clear_button = tk.Button(button_frame, text="Clear Day's Tasks", command=self.clear_day_tasks)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # Clear all button
        clear_all_button = tk.Button(button_frame, text="Clear All Tasks", command=self.clear_all_tasks)
        clear_all_button.pack(side=tk.LEFT, padx=5)
    
    def load_from_file(self):
        """Load tasks from a selected JSON file"""
        file_path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Select Task File to Load"
        )
        
        if file_path:
            # Set the new file in file handler
            self.file_handler.set_filename(file_path)
            
            # Load tasks from the selected file
            self.tasks = self.file_handler.load_tasks()
            
            # Update UI
            self.refresh_task_list()
            self.update_date_combo()
            self.file_label.config(text=f"Current file: {os.path.basename(file_path)}")
            
            messagebox.showinfo("Success", f"Tasks loaded from {os.path.basename(file_path)}")
    
    def save_to_file(self):
        """Save tasks to a selected JSON file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save Tasks To File"
        )
        
        if file_path:
            # Set the new file in file handler
            old_filename = self.file_handler.filename
            self.file_handler.set_filename(file_path)
            
            # Save to the selected file
            if self.file_handler.save_tasks(self.tasks):
                self.file_label.config(text=f"Current file: {os.path.basename(file_path)}")
                messagebox.showinfo("Success", f"Tasks saved to {os.path.basename(file_path)}")
            else:
                # Revert to old filename if save failed
                self.file_handler.set_filename(old_filename)
                messagebox.showerror("Error", "Failed to save tasks to file!")
    
    def update_date_combo(self):
        """Update the date combobox with available dates from tasks"""
        dates = list(self.tasks.keys())
        # Always add current date if not in list
        if self.current_date not in dates:
            dates.append(self.current_date)
        dates.sort(key=lambda date: datetime.strptime(date, "%A, %B %d, %Y"), reverse=True)
        self.date_combo['values'] = dates
        self.date_combo.set(self.current_date)
    
    def load_date(self):
        """Load tasks for the selected date"""
        selected_date = self.date_combo.get()
        if selected_date:
            self.current_date = selected_date
            self.date_label.config(text=self.current_date)
            self.refresh_task_list()
    
    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            current_time = self.get_formatted_time()
            
            # Initialize date entry if it doesn't exist
            if self.current_date not in self.tasks:
                self.tasks[self.current_date] = []
            
            # Add task with timestamp
            self.tasks[self.current_date].append({
                "time": current_time,
                "description": task,
                "completed": False
            })
            
            self.refresh_task_list()
            self.task_entry.delete(0, tk.END)
            self.update_date_combo()
        else:
            messagebox.showwarning("Warning", "Please enter a task!")
    
    def edit_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            if self.current_date in self.tasks and index < len(self.tasks[self.current_date]):
                task = self.tasks[self.current_date][index]
                task_desc = task["description"]
                
                # Ask for new task description
                new_desc = simpledialog.askstring("Edit Task", "Edit task description:", 
                                                 initialvalue=task_desc)
                
                if new_desc and new_desc.strip():
                    self.tasks[self.current_date][index]["description"] = new_desc.strip()
                    self.refresh_task_list()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to edit!")
    
    def remove_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            if self.current_date in self.tasks and index < len(self.tasks[self.current_date]):
                task = self.tasks[self.current_date][index]
                task_desc = task["description"]
                
                if messagebox.askyesno("Confirm", f"Mark '{task_desc}' as completed?"):
                    # Mark as completed (or remove if preferred)
                    self.tasks[self.current_date][index]["completed"] = True
                    self.refresh_task_list()
                    messagebox.showinfo("Success", "Task marked as completed!")
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to complete!")
    
    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        if self.current_date in self.tasks:
            for task in self.tasks[self.current_date]:
                prefix = "✓ " if task["completed"] else "• "
                task_text = f"{task['time']} - {prefix}{task['description']}"
                self.task_listbox.insert(tk.END, task_text)
                
                # Gray out completed tasks
                if task["completed"]:
                    self.task_listbox.itemconfig(tk.END-1, fg="gray")
    
    def save_tasks(self):
        if self.file_handler.save_tasks(self.tasks):
            messagebox.showinfo("Success", "Tasks saved successfully!")
        else:
            messagebox.showerror("Error", "Failed to save tasks!")
    
    def clear_day_tasks(self):
        if messagebox.askyesno("Confirm", f"Are you sure you want to clear all tasks for {self.current_date}?"):
            if self.current_date in self.tasks:
                del self.tasks[self.current_date]
                self.refresh_task_list()
                self.save_tasks()
                self.update_date_combo()
                messagebox.showinfo("Success", f"All tasks for {self.current_date} cleared!")
    
    def clear_all_tasks(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear ALL tasks for ALL dates?"):
            self.tasks = {}
            self.refresh_task_list()
            self.save_tasks()
            self.update_date_combo()
            messagebox.showinfo("Success", "All tasks cleared!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()