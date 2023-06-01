#Hangman, the game.
#Creator: Axel
import os
import customtkinter as ctk
import random
import time
from PIL import Image
ctk.set_appearance_mode("Dark")
hangman_window = ctk.CTkToplevel(self)
hangman_window.title("Hangman")
hangman_window.geometry("900x375"+f"+{self.winfo_x()}+{self.winfo_y()}")
hangman_window.resizable(False, False)
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# Counts number of wrong inputs. Used for managing the displayed image.
# Counts number of correct inputs
correct_count = 0
# Image is where current gamestage image will be displayed, such as if you win or lose.
image = ctk.CTkImage(light_image=Image.open(os.getcwd()+"/assets/hangman/number1.png"),
                     size=(300, 300))
error_count = 2
label = ctk.CTkLabel(hangman_window, image=image, text="")
label.grid(row=0, column=0, padx=20, rowspan=5)
#Goes through every letter in the random word selected.

def word_selection():
    global difficulty_button, word_selected

    selected_difficulty = difficulty_button.get()

    easy = ['about', 'after', 'again', 'below', 'could', 'every', 'first',
            'found', 'great', 'house', 'large', 'learn', 'never', 'other',
            'place', 'plant', 'point', 'right', 'small', 'sound', 'spell',
            'still', 'study', 'their', 'there', 'these', 'thing', 'think',
            'three', 'water','where','which','world','would','write']

    normal = ['happy', 'family', 'friend', 'school', 'music',
              'flower', 'guitar', 'piano', 'beach', 'mountain',
              'adventure', 'challenge', 'knowledge', 'education',
              'achieve', 'aspiration', 'ambition', 'innovation',
              'colonel']

    hard = ['adventure', 'challenge', 'knowledge', 'education',
            'imagination', 'inspiration', 'motivation', 'opportunity',
            'nauseous']

    legend = ['perseverance', 'determination', 'accomplishment',
              'achievement', 'aspiration', 'ambition', 'innovation', 'colonel']

    if selected_difficulty == "Easy":
        word_selected = easy[random.randint(0, len(easy)-1)]
    elif selected_difficulty == "Normal":
        word_selected = normal[random.randint(0, len(normal) - 1)]
    elif selected_difficulty == "Hard":
        word_selected = hard[random.randint(0, len(hard) - 1)]
    else:
        word_selected = legend[random.randint(0, len(legend) - 1)]
    # Used for counting the number of letters in the selected word.
    count = "1"
    for character in word_selected:
        # Adds a label with text _ and a tuple containing information about the right letter.
        globals()["var" + count] = (character.upper(), ctk.CTkLabel(hangman_window, width=30, height=40,
                                                    font=("Comic Sans MS Bold", 25.0), text="_"))
        globals()["var" + count][1].grid(row=0, column=count, padx=0)
        count = str(int(count) + 1)

def re_run():
    global hangman_window, word_selection, \
        correct_count, error_count, image, \
        possible_words_list, random, restart_button
    correct_count = 0
    error_count = 2
    random_word_selected = possible_words_list[random.randint(0, len(possible_words_list) - 1)]
    image.configure(light_image=Image.open(os.getcwd()+"/assets/hangman/number1.png"))
    restart_button.configure(state="disabled", fg_color="gray")
    for variable in globals().copy():
        if variable[0:3] == "var":
            globals()[variable][1].destroy()
            globals().pop(variable)
        if variable[1:] == "button":
            globals()[variable].configure(state="normal", fg_color="#1f538d")
    word_selection()

def end(Win=False):
    global re_run, number_of_wins, restart_button
    #Checks if win was defined
    restart_button.configure(state="normal", fg_color="#ffd000")
    if Win == False:
        #Will display the correct word and make all buttons red.
        for i in globals():
            if i[0:3] == "var":
                globals()[i][1].configure(text=globals()[i][0])
            if i[1:] == "button":
                globals()[i].configure(state="disabled", fg_color="red")
    elif Win == True:
        #Display Win image
        image.configure(light_image=Image.open(os.getcwd() + f"/assets/hangman/number11.png"))

        #Will make a buttons green.
        for i in globals():
            if i[1:] == "button":
                globals()[i].configure(state="disabled", fg_color="green")
        number_of_wins.configure(text=f"Wins: {int(number_of_wins.cget('text')[5:])+1}")

def when_clickedd(letter):
    global image, Image, error_count, end, time, word_selected, correct_count
    found = False
    for i in globals():
        if i[0:3] == "var":
            if globals()[i][0].lower() == letter.lower():
                globals()[i][1].configure(text=globals()[i][0])
                found = True
                correct_count += 1
    if found:
        #Change color of button clicked to green if there was a match.
        globals()[letter + "button"].configure(fg_color="green", text_color="white", state="disabled")
        #Checks if every letter has been entered.
        if correct_count == len(word_selected):
            end(Win=True)
    else:
        #Change color of button clicked to red if there wasn't a match.
        globals()[letter + "button"].configure(fg_color="red", text_color="white", state="disabled")
        if error_count <= 8:
            image.configure(light_image=Image.open(os.getcwd() + f"/assets/hangman/number{error_count}.png"))
            error_count += 1
        else:
            image.configure(light_image=Image.open(os.getcwd() + f"/assets/hangman/number{error_count}.png"))
            end()
    return None
def run_buttons():
    global alphabet, when_clickedd, re_run, number_of_wins, \
        restart_button, difficulty_button
    # Rowcount for placing out the alphabetic buttons.
    alphabet_rowcount = 1
    # Columncount for placing out the alphabetic buttons.
    alphabet_columncount = 1
    # Goes through every letter in the alphabet.
    for letter in alphabet:
        # The command each alphabetic button will run when clicked.
        the_command = lambda letter = letter: when_clickedd(letter)
        globals()[letter+"button"] = ctk.CTkButton(hangman_window, text=letter, command=the_command,
                                                height=40, width=30)
        globals()[letter + "button"].grid(row=alphabet_rowcount, column=alphabet_columncount)
        if alphabet_columncount > 12:
            alphabet_rowcount += 1
            alphabet_columncount = 0
        alphabet_columncount += 1
    # Adds button for restarting the game.
    restart_button = ctk.CTkButton(hangman_window, text="Restart", command=re_run, height=40, width=120,
                                   state="disabled", fg_color="gray", font=("Arial", 25))
    restart_button.grid(row=6, column=1, columnspan=4, rowspan=2)
    # Difficulty selection label and button.
    difficulty_label = ctk.CTkLabel(hangman_window, text="Word Difficulty", height=20, width=90)
    difficulty_label.grid(row=6, column=5, columnspan=4)
    difficulty_button = ctk.CTkOptionMenu(hangman_window, values=["Easy", "Normal", "Hard", "Legend"],
                                          height=20, width=90)
    difficulty_button.grid(row=7, column=5, columnspan=4)
    # Label for counting wins.
    number_of_wins = ctk.CTkLabel(hangman_window, text="Wins: 0")
    number_of_wins.grid(row=6, column=0)
    print(number_of_wins.cget("text"))
def stay_on_top():
    global hangman_window, stay_on_top
    hangman_window.lift()
    hangman_window.after(400, stay_on_top)
def close():
    outputText("Hello")
    for i in globals().copy():
        if i[0:3] == "var":
            globals().pop(i)
        elif i[1:] == "button":
            globals().pop(i)
    hangman_window.destroy()

stay_on_top()
run_buttons()
word_selection()
# Bind exit window to a function.
hangman_window.protocol("WM_DELETE_WINDOW", close)