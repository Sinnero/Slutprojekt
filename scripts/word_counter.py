#Counts words and characters
#of inputfield
filetxt = input_string
print(filetxt)
global output
number_words = str(len(filetxt.split()))
number_characters = str(len(filetxt.strip()))

if number_words + number_characters == "00":
    output = "Enter text in inputfield."
else:
    output = f"Words: {number_words}\nCharacters: {number_characters}"
outputText(output)