import customtkinter as ctk
import tkinter as tk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")
appWidth, appHeight = 600, 700
class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('300x100')
        self.title('Toplevel Window')

        ctk.CTkButton(self,
                text='Close',
                command=self.destroy).pack(expand=True)

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
        self.scriptInit = tk.StringVar(value="None")
        row_count = 3
        column_count = 0
        if "dicti" not in globals():
            dicti = {'test': 'No description', 'test2': 'Hejsan', 'test23': 'Hejsan', 'test24': 'Hejsan', 'test32': 'Hejsan', 'test22': 'Hejsan', 'test112': 'Hejsan', 'test232': 'Hejsan', 'test25': 'Hejsan'}
        for script in dicti:
            self.script = ctk.CTkRadioButton(self,
                                                      text=script[0:20],
                                                      variable=self.scriptInit,
                                                      value=script)
            self.script.grid(row=row_count, column=column_count,
                                      padx=20, pady=10,
                                      sticky="ew")

            self.genderLabel = ctk.CTkLabel(self,
                                            text=f'"{dicti[script][0:20]}"')
            self.genderLabel.grid(row=row_count, column=column_count+1,
                                  padx=0, pady=0,
                                  sticky="ew")
            row_count += 1
        # Generate Button
        self.generateResultsButton = ctk.CTkButton(self,
                                                   text="Generate Results",
                                                   command=self.generateResults)
        self.generateResultsButton.grid(row=int(row_count+1), column=column_count+3,
                                        columnspan=1, padx=20,
                                        pady=20, sticky="ew")
        self.openDescriptionButton = ctk.CTkButton(self,
                                                    text='Open a window',
                                                    command=self.open_window)
        self.openDescriptionButton.grid(row=int(row_count+2), column=column_count+4,
                                        columnspan=1, padx=20,
                                        pady=20, sticky="ew")
    def open_window(self):
        window = Window(self)
        window.grab_set()

    def generateResults(self):
        print(self.scriptInit.get())
if __name__ == "__main__":
    app = App()
    # Used to run the application
    app.mainloop()