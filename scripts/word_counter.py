#Counts words and characters
#of inputfield.
#Creator: Cyreus

filetxt = input_string
global output
# Counts words and characters.
number_words = str(len(filetxt.split()))
number_characters = str(len(filetxt.strip()))

# Check if atleast something was inputted. Else give feedback to user.
if number_words + number_characters == "00":
    output = "Enter text in inputfield."

# Else make string containing number of words and characters.
else:
    output = f"Words: {number_words}\nCharacters: {number_characters}"

# Use function in main.py to render output message to main window.
outputText(output)