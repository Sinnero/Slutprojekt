import customtkinter as ctk
import random

ctk.set_appearance_mode("Dark")
hangman_window = ctk.CTkToplevel(self)
hangman_window.title("Hangman")
hangman_window.geometry("650x375"+f"+{self.winfo_x()}+{self.winfo_y()}")
hangman_window.resizable(False, False)
#Makes the window priority over main GUI.
def stay_on_top():
    global hangman_window, stay_on_top
    hangman_window.lift()
    hangman_window.after(400, stay_on_top)
stay_on_top()
possible_words_list = ["HELLO", "Test"]
random_word_selected = possible_words_list[random.randint(0, len(possible_words_list)-1)]
count = "var1"
image = ctk.CTkImage(light_image=Image.open())
label = ctk.CTkLabel(hangman_window, image=image)
label.grid(row=0, column=0)
for i in random_word_selected:
    vars()[count] = (i, ctk.CTkLabel(hangman_window, width=30, height=40, font=("Comic Sans MS Bold", 25.0), text="_"))
    vars()[count][1].grid(row=1, column=count[3:], padx=0)
    count = "var"+str(int(count[3:])+1)

print(var1+var2)