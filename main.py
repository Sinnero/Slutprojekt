# Creator: Cyreus
import os
import customtkinter as ctk
import tkinter as tk

# Directory where the scripts are located.
directory = "scripts"

try:
    os.chdir(directory)

except(NotADirectoryError):
    path = os.path.join(os.getcwd(), directory)
    os.mkdir(path)
# Funktion som är till för att ladda in descriptions till alla scripts.
def load_scripts_descriptions(files_list):
    description_dict = {} # Dictionary som kommer innehålla namn och descriptions på alla scripts i scripts filen.
    for files in files_list:
        with open(files, "r") as file:
            lines = file.readlines()
            description = ""
            line = 0
            #Checkar om filen har en description som ska visas i scriptloadern eller inte.
            for item in lines:
                #Kollar om första raden i koden är kommenterad.
                if item[0] == "#":
                    description += item[1:]
                elif item[0] != "#":
                    if line == 0:
                        description = "No description" #Om ingen beskrivning hittades i början av scriptet
                    else:
                        break
                #Kollar nästa rad av script.
                line += 1
            description_dict[files] = description
    return description_dict
def load_scripts():
    script_names = []
    for filename in os.scandir(): #Går igenom alla filer i katalogen scripts.
        if filename.is_file():
            if filename.path[len(filename.path)-2:] == "py": # Kollar om filen är python.
                script_names.append(filename.path) # 8: Tar bort scripts/ i scripts/script.py
    return load_scripts_descriptions(script_names)


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")
appWidth, appHeight = 760, 600
# Class for making the main menu.
class App(ctk.CTk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Sets the title of the window to "App"
        self.title("Script loader")

        # Sets the dimensions of the window to 600x700
        self.geometry(f"{appWidth}x{appHeight}")

        # Makes the window unsizeable
        self.resizable(False, False)

        # Name Labels
        self.scriptInit = tk.StringVar(value="None")

        row_count = 2
        column_count = 0
        all_scripts = load_scripts()
        # Makes a scrollable interface that contains all scripts.
        scrollable_buttons = ctk.CTkScrollableFrame(self, height=175, width=500)
        scrollable_buttons.grid(row=1, column=0, columnspan=3)
        for script in all_scripts:
            description = str(all_scripts[script])
            # Name box for all the individual scripts
            self.scriptText = ctk.CTkRadioButton(scrollable_buttons,
                                             text=script[2:len(script)-3],
                                             variable=self.scriptInit,
                                             value=script)
            self.scriptText.grid(row=row_count, column=column_count,
                             padx=20, pady=10,
                             sticky="ew")
            # Individual description for all scripts.
            self.desc_previewLabel = ctk.CTkLabel(scrollable_buttons,
                                                  text=f'{description[0:60]}')
            self.desc_previewLabel.grid(row=row_count, column=column_count + 1,
                                        padx=0, pady=0,
                                        sticky="ew")
            row_count += 1
        # Start script Button
        self.StartScriptButton = ctk.CTkButton(self,
                                                   text="Start Selected Script",
                                                   command=self.generateResults,
                                                   width=200)
        self.StartScriptButton.grid(row=2, column=0,
                                        columnspan=2, padx=115,
                                        pady=20, sticky="ew")
        # Input label for "Input" text
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
        # Input clear button
        self.inputClearButton = ctk.CTkButton(self,
                                                   text="Clear Input",
                                                   command=self.clear_Input_Output,
                                                   width=50)
        self.inputClearButton.grid(row=int(row_count+2), column=column_count,
                                        columnspan=1, padx=10,
                                        pady=20, sticky="ew")
        # Output text

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
    # Function for copying current text displayed in output to the clipboard.
    def copyClipboard(self):
        outputText = self.outputDisplayBox.get("1.0", "end")
        print(outputText)
        os.system("echo " + str(outputText.strip()) + "| clip")
    def clear_Input_Output(self):
        self.inputEntry.delete("1.0", "end")
    def generateResults(self):
        # Funktion för att start ett error fönster om ett fel uppstår.
        def Window(Error):
            global Window
            # Creates the Tkinter window.
            Error_window = ctk.CTkToplevel(self)
            Error_window.title("Hello")
            # Function to make the Error window always on top of main script loader.
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
                # outputText funktionen kan användas i alla olika scripts som körs genom scriptloadern.
                # Det gör så att scripten kan kommunicera en text som ska visas i output fältet.
                def outputText(output):
                    self.outputDisplayBox.configure(state="normal")
                    self.outputDisplayBox.delete("0.0", "end")
                    self.outputDisplayBox.insert("0.0", output)
                    self.outputDisplayBox.configure(state="disabled")
                try:
                    exec(script.read())
                # Raise the encountered error to the user.
                except() as error:
                    Window("Error while loading: " + str(script_dir) + error)
        # Raise the encountered error to the user.
        except(FileNotFoundError) as f:
            ErrorString = str(f)[37:].strip("'")
            if ErrorString == "None":
                Window("Please select a script.")
            else:
                Window("Script got moved or deleted. \nOr the file may be corrupt.")
# Main loop to keep the window running.
if __name__ == "__main__":
    app = App()
    # Used to run the application
    app.mainloop()
#initialize script.
print(load_scripts())