import os

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
            description_dict[files[len(directory)+1:-3]] = description
    return description_dict
def load_scripts():
    script_names = []
    for filename in os.scandir(directory): #Går igenom alla filer i katalogen scripts.
        if filename.is_file():
            if filename.path[len(filename.path)-2:] == "py": #Kollar om filen är python.
                script_names.append(filename.path) # 8: Tar bort scripts/ i scripts/script.py
    return load_scripts_descriptions(script_names)

with open("graphical_menu.py", "r") as file:
    dicti = load_scripts()
    exec(file.read())
print(load_scripts())