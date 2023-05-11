import os
import customtkinter as ctk
import tkinter as tk

directory = "scripts"

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
    for filename in os.scandir(directory): #Går igenom alla filer i katalogen scripts.
        if filename.is_file():
            if filename.path[len(filename.path)-2:] == "py": #Kollar om filen är python.
                script_names.append(filename.path) # 8: Tar bort scripts/ i scripts/script.py
    return load_scripts_descriptions(script_names)


def graphical_menu():

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("dark-blue")
    appWidth, appHeight = 900, 700

    class App(ctk.CTk):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            # Sets the title of the window to "App"
            self.title("GUI Application")
            # Sets the dimensions of the window to 600x700
            self.geometry(f"{appWidth}x{appHeight}")

            # Name Label
            self.nameLabel = ctk.CTkLabel(self,
                                          text="Scripts")
            self.nameLabel.grid(row=0, column=0,
                                padx=20, pady=20,
                                sticky="ew")
            self.nameLabel = ctk.CTkLabel(self,
                                          text="Description:")
            self.nameLabel.grid(row=0, column=1,
                                padx=20, pady=20,
                                sticky="ew")
            self.inputEntry = ctk.CTkEntry(self,
                                          placeholder_text="Input")
            self.inputEntry.grid(row=0, column=4,
                                columnspan=3, padx=20,
                                pady=20, sticky="ew")
            self.scriptInit = tk.StringVar(value="None")
            row_count = 3
            column_count = 0
            all_scripts = load_scripts()
            for script in all_scripts:
                description = str(all_scripts[script])
                self.script = ctk.CTkRadioButton(self,
                                                 text=script[len(directory) + 1:-3][0:20],
                                                 variable=self.scriptInit,
                                                 value=script)
                self.script.grid(row=row_count, column=column_count,
                                 padx=20, pady=10,
                                 sticky="ew")

                self.desc_previewLabel = ctk.CTkLabel(self,
                                                      text=f'"{description[0:20]}"')
                self.desc_previewLabel.grid(row=row_count, column=column_count + 1,
                                            padx=0, pady=0,
                                            sticky="ew")
                row_count += 1
            # Generate Button
            self.generateResultsButton = ctk.CTkButton(self,
                                                       text="Start Script",
                                                       command=self.generateResults)
            self.generateResultsButton.grid(row=int(row_count + 1), column=column_count + 3,
                                            columnspan=1, padx=20,
                                            pady=20, sticky="ew")
        def generateResults(self):
            def ErrorWindow(Error):
                ctk.set_appearance_mode("System")
                Error_window = tk.Toplevel(self)
                Error_window.title("Hello")
                label = ctk.CTkLabel(Error_window,
                                     width=100,
                                     height=100,
                                     text=Error)
                label.configure(font=('Helvetica bold', 26))
                label.pack()
                #close_button = ctk.CTkButton(Error_window,
                #                             text="Start Script",
                  #                           command=Error_window.destroy())
                #close_button.pack()
            try:
                with open(self.scriptInit.get(), "r") as script:
                    exec(script.read())

            except(FileNotFoundError) as f:
                ErrorString = str(f)[37:].strip("'")
                if ErrorString == "None":
                    ErrorWindow("Please select a script.")
                else:
                    ErrorWindow("Script:" + ErrorString)
                #    print(f)
                print("hello", str(f)[37:].strip("'"))



    if __name__ == "__main__":
        app = App()
        # Used to run the application
        app.mainloop()
graphical_menu()
print(load_scripts())