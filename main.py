import os
import customtkinter as ctk
import tkinter as tk

directory = "scripts"
try:
    os.chdir(directory)
except(NotADirectoryError):
    path = os.path.join(os.getcwd(), directory)
    os.mkdir(path)
def load_scripts_descriptions(files_list):
    description_dict = {} #Dictionary som ska innehålla namn och descriptions på alla scripts
    for files in files_list:
        with open(files, "r") as file:
            lines = file.readlines()
            description = ""
            line = 0
            for item in lines:
                if item[0] == "#":
                    description += item[1:]
                elif item[0] != "#":
                    if line == 0:
                        description = "No description" #Om
                    else:
                        break
                line += 1
            description_dict[files] = description
    return description_dict
def load_scripts():
    script_names = []
    for filename in os.scandir(): #Går igenom alla filer i katalogen scripts.
        if filename.is_file():
            if filename.path[len(filename.path)-2:] == "py": #Kollar om filen är python.
                script_names.append(filename.path)# 8: Tar bort scripts/ i scripts/script.py
    return load_scripts_descriptions(script_names)


def graphical_menu():

    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("dark-blue")
    appWidth, appHeight = 760, 700

    class App(ctk.CTk):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            # Sets the title of the window to "App"
            self.title("GUI Application")
            # Sets the dimensions of the window to 600x700
            self.geometry(f"{appWidth}x{appHeight}")

            self.resizable(False, False)

            # Name Labels
            self.nameLabel = ctk.CTkLabel(self,
                                          text="Scripts")
            self.nameLabel.grid(row=0, column=0,
                                padx=20, pady=20,
                                sticky="ew")
            self.nameLabel = ctk.CTkLabel(self,
                                          text="Description")
            self.nameLabel.grid(row=0, column=1,
                                padx=20, pady=20,
                                sticky="ew")
            self.nameLabel = ctk.CTkLabel(self,
                                          text="")
            self.nameLabel.grid(column=5)
            self.nameLabel = ctk.CTkLabel(self,
                                          text="")
            self.nameLabel.grid(column=6)
            self.scriptInit = tk.StringVar(value="None")
            row_count = 3
            column_count = 0
            all_scripts = load_scripts()
            for script in all_scripts:
                description = str(all_scripts[script])
                #Name box for all the individual scripts
                self.scriptText = ctk.CTkRadioButton(self,
                                                 text=script[2:len(script)-3],
                                                 variable=self.scriptInit,
                                                 value=script)
                self.scriptText.grid(row=row_count, column=column_count,
                                 padx=20, pady=10,
                                 sticky="ew")
                #Individual description for all scripts.
                self.desc_previewLabel = ctk.CTkLabel(self,
                                                      text=f'{description[0:55]}')
                self.desc_previewLabel.grid(row=row_count, column=column_count + 1,
                                            padx=0, pady=0,
                                            sticky="ew")
                row_count += 1
            #Start script Button
            self.StartScriptButton = ctk.CTkButton(self,
                                                       text="Start Script",
                                                       command=self.generateResults,
                                                       width=200)
            self.StartScriptButton.grid(row=1, column=column_count + 0,
                                            columnspan=1, padx=0,
                                            pady=20, sticky="ew")
            #Input label for "Input" text
            self.inputLabel = ctk.CTkLabel(self,
                                          text="Input",
                                          font=("Arial", 18))
            self.inputLabel.grid(row=int(row_count), column=0,
                                padx=0, pady=0,
                                sticky="ew")
            # Inputbox for usage in scripts
            self.inputEntry = ctk.CTkTextbox(self,
                                             width=200,
                                             height=150)
            self.inputEntry.grid(row=int(row_count + 1), column=0,
                                 columnspan=1, padx=40,
                                 pady=0, sticky="ew")
            #Input clear button
            self.inputClearButton = ctk.CTkButton(self,
                                                       text="Clear Input",
                                                       command=self.clear_Input_Output,
                                                       width=50)
            self.inputClearButton.grid(row=int(row_count+2), column=column_count,
                                            columnspan=1, padx=10,
                                            pady=20, sticky="ew")
            #Output text

            self.outputLabel = ctk.CTkLabel(self,
                                           text="Output",
                                           font=("Arial", 18))
            self.outputLabel.grid(row=int(row_count), column=1,
                                 padx=110, pady=0,
                                 sticky="ew")
            #Output Display Box
            self.outputDisplayBox = ctk.CTkTextbox(self,
                                             width=100,
                                             height=150)
            self.outputDisplayBox.grid(row=int(row_count + 1), column=1,
                                 columnspan=4, padx=0,
                                 pady=20, sticky="nsew")
            self.outputDisplayBox.insert("0.0", "Output")
            self.outputDisplayBox.configure(state="disabled")
            #Output copy to clipboard
            self.outputCopyclipboardButton = ctk.CTkButton(self,
                                                       text="Copy output to clipboard",
                                                       command=self.copyClipboard,
                                                       width=200)
            self.outputCopyclipboardButton.grid(row=int(row_count+2), column=column_count + 2,
                                            columnspan=1, padx=0,
                                            pady=20, sticky="ew")
        def copyClipboard(self):
            outputText = self.outputDisplayBox.get("1.0", "end")
            print(outputText)
            os.system("echo " + str(outputText.strip()) + "| clip")
        def clear_Input_Output(self):
            self.inputEntry.delete("1.0", "end")
        def generateResults(self):
            def Window(Error):
                global Window
                ctk.set_appearance_mode("Dark")
                Error_window = ctk.CTkToplevel(self)
                Error_window.title("Hello")
                def stay_on_top():
                    Error_window.lift()
                    Error_window.after(200, stay_on_top)
                label = ctk.CTkLabel(Error_window,
                                     width=100,
                                     height=100,
                                     text=Error)
                label.configure(font=('Helvetica bold', 26))
                label.pack()
                stay_on_top()
            script_dir = self.scriptInit.get()
            try:
                with open(script_dir, "r") as script:
                    global input_string, outputText
                    input_string = self.inputEntry.get("1.0", "end")
                    def outputText(output):
                        self.outputDisplayBox.configure(state="normal")
                        self.outputDisplayBox.delete("0.0", "end")
                        self.outputDisplayBox.insert("0.0", output)
                        self.outputDisplayBox.configure(state="disabled")
                    try:
                        exec(script.read())
                    except() as error:
                        Window("Error while loading: " + str(script_dir) + error)

            except(FileNotFoundError) as f:
                ErrorString = str(f)[37:].strip("'")
                if ErrorString == "None":
                    Window("Please select a script.")
                else:
                    Window("Script got moved or deleted:" + ErrorString)

    if __name__ == "__main__":
        app = App()
        # Used to run the application
        app.mainloop()
graphical_menu()
print(load_scripts())