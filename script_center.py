import os
import shutil
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Define a class 'ScriptCenter' that inherits from tk.Tk (Tkinter's main application window)


class ScriptCenter(tk.Tk):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Script Center")
        self.geometry("800x900")

        self.file_path = ""
        self.file_contents = ""

        self.selected_scripts = []

        # Create the GUI widgets by calling the 'create_widgets' method
        self.create_widgets()

    def create_widgets(self):
        ############### SELECT AND SAVE SCRIPT ###############

        # Label to display the currently selected file
        self.file_label = tk.Label(self, text="File: No file selected")
        self.file_label.pack(pady=10)

        # Frame containing buttons to browse and save script files
        self.file_button_frame = tk.Frame(self)
        self.file_button_frame.pack(side="top", padx=5, pady=5)

        # Button to browse and select a script file
        self.browse_button = tk.Button(
            self.file_button_frame, text="Browse File", command=self.browse_file)
        self.browse_button.pack(side="left", padx=5, pady=5)

        # Button to save the currently selected script file
        self.save_button = tk.Button(
            self.file_button_frame, text="Save File", command=self.save_file)
        self.save_button.pack(side="left", padx=5, pady=5)

        ############### DISPLAY AND MODIFY SCRIPT ###############

        # Frame containing the text editor to display and modify the script contents
        self.text_frame = tk.Frame(self)
        self.text_frame.pack(padx=5, pady=5)

        # Text widget to display and edit the script contents
        self.text_editor = tk.Text(self.text_frame, wrap="word", undo=True)
        self.text_editor.pack(expand=True, fill="both", padx=10, pady=5)
        # Bind Ctrl+S to save the file
        self.text_editor.bind("<Control-s>", self.save_file)

        ############### SELECT AND EXECUTE SCRIPT ###############

        # Frame for selecting and executing a script
        self.script_selection_frame = tk.Frame(self)
        self.script_selection_frame.pack(padx=5, pady=5)

        # Label to prompt for script selection
        self.script_label = tk.Label(
            self.script_selection_frame, text="Select Script:", font=("Arial", 16))
        self.script_label.pack(pady=10)

        # Combobox to display the list of loaded scripts for selection
        self.script_listbox = ttk.Combobox(
            self.script_selection_frame, values=[],
            font=("Arial", 12), state="readonly", height=5)
        self.script_listbox.pack()

        # Button to execute the selected script
        self.execute_button = tk.Button(
            self.script_selection_frame, text="Execute Script", command=self.confirm_and_execute)
        self.execute_button.pack()

        # Call the method to initially populate the combobox with loaded script files
        self.update_script_listbox()

        ############### SCRIPT OUTPUT ###############

        # Frame to display the output of the executed script
        self.output_frame = tk.Frame(self)
        self.output_frame.pack(side="bottom", padx=5, pady=5)

        # Label to display the "Output" header
        self.output_label = tk.Label(
            self.output_frame, text="Output:", font=("Arial", 16))
        self.output_label.pack(pady=10)

        # Scrollbar for the output_text
        self.output_scrollbar = tk.Scrollbar(self.output_frame)
        self.output_scrollbar.pack(side="right", fill="y")

        # Text widget to display the output of the executed script
        self.output_text = tk.Text(
            self.output_frame, wrap="word", undo=False, yscrollcommand=self.output_scrollbar.set)
        self.output_text.pack(expand=True, fill="both", padx=10, pady=5)
        self.output_scrollbar.config(command=self.output_text.yview)

    # Method to browse and select a script file
    def browse_file(self):
        # Use filedialog to ask the user to select a script file
        file_path = filedialog.askopenfilename(
            filetypes=[("Script files", "*.py;*.sh;*.ps1")]
        )
        if file_path:
            self.file_path = file_path
            self.file_label.config(text="File: " + os.path.basename(file_path))
            with open(file_path, "r") as file:
                self.file_contents = file.read()
            self.text_editor.delete(1.0, tk.END)
            self.text_editor.insert(tk.END, self.file_contents)

            # Move the selected script to the 'loaded_scripts' folder
            script_name = os.path.basename(file_path)
            target_directory = os.path.join(os.getcwd(), "loaded_scripts")
            if not os.path.exists(target_directory):
                os.makedirs(target_directory)
            target_path = os.path.join(target_directory, script_name)

            try:
                shutil.move(file_path, target_path)
                print(
                    f"Script '{script_name}' moved to 'loaded_scripts' folder.")
                # Update the combobox with the latest list of files
                self.update_script_listbox()
            except Exception as e:
                print(f"Error moving script: {e}")

    # Method to save the current script file
    def save_file(self, event=None):
        if self.file_path:
            self.file_contents = self.text_editor.get(1.0, tk.END)
            script_name = os.path.basename(self.file_path)
            target_directory = os.path.join(os.getcwd(), "loaded_scripts")

            if not os.path.exists(target_directory):
                os.makedirs(target_directory)

            target_path = os.path.join(target_directory, script_name)

            with open(target_path, "w") as file:
                file.write(self.file_contents)

            print(f"Script '{script_name}' saved in 'loaded_scripts' folder.")

    # Method to update the list of loaded scripts in the combobox
    def update_script_listbox(self):
        loaded_scripts_path = "loaded_scripts"
        file_list = os.listdir(loaded_scripts_path)
        self.script_listbox["values"] = file_list

    # Method to confirm and execute the selected script
    def confirm_and_execute(self):
        script_name = self.script_listbox.get()
        if script_name:
            # Ask for confirmation before executing the script
            if messagebox.askyesno("Confirmation", f"Are you sure you want to execute '{script_name}'?"):
                script_path = os.path.join("loaded_scripts", script_name)
                self.execute_script(script_path)

    # Method to execute a script based on its extension
    def execute_script(self, script_path):
        extension = os.path.splitext(script_path)[1].lower()

        # Check the extension and execute the corresponding script
        if extension == ".py":
            # Execute Python script
            try:
                output = subprocess.check_output(
                    ["python", script_path], stderr=subprocess.STDOUT, text=True)
            except subprocess.CalledProcessError as e:
                output = e.output
        elif extension == ".sh":
            # Execute Shell script
            try:
                output = subprocess.check_output(
                    ["bash", script_path], stderr=subprocess.STDOUT, text=True)
            except subprocess.CalledProcessError as e:
                output = e.output
        elif extension == ".ps1":
            # Execute PowerShell script
            try:
                output = subprocess.check_output(
                    ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path], stderr=subprocess.STDOUT, text=True)
            except subprocess.CalledProcessError as e:
                output = e.output
        else:
            # Unsupported script type
            messagebox.showerror(
                "Error", f"Unsupported script type: {extension}")
            return

        # Display the output of the executed script in the output_text widget
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", output)
