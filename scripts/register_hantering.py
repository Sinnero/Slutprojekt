import json
globals()
ctk.set_appearance_mode("Dark")
selection_window = ctk.CTkToplevel(self)#95244
selection_window.title("Registry management")
options = ["Enter new person", "Remove person", "Search for person's phone number",
           "Search for person's date of birth", "See who has given phone number",
           "See who has given date of birth", "Print all people (in alphabetical order)",
           "Change working registry", "Exit"]
registry_file = "assets/register_hantering.reg"
selection_window.geometry("275x650"+f"+{self.winfo_x()}+{self.winfo_y()}")
selection_window.resizable(False, False)
#Used to load the current register.
def load_registret():
    global registry_file, json, outputText
    try:
        with open(registry_file, "r") as file:
            registret_string = file.read()
            registret = json.loads(registret_string)
            return registret
    except:
        with open(registry_file, "w") as file:
            yes_no = ctk.CTkInputDialog(text="This file is not an registry.\nDo you want to make it one? Yes/No", title="Test").get_input()
            print(yes_no)
            if yes_no.lower() == "yes":
                file.write("{}")
                return {}
            elif yes_no.lower() == "no":
                outputText("Registry assignment terminated.")
                selection_window.destroy()
            else:
                outputText("Error, only Yes/No answers are accepted.")
                selection_window.destroy()
#Will print the specified register to the file.
def dump_registret_file(registret):
    global json, registry_file
    with open(registry_file, "w") as file:
        json.dump(registret, file)

#Makes the window priority over main GUI.
def stay_on_top():
    global selection_window, stay_on_top
    selection_window.lift()
    selection_window.after(400, stay_on_top)

#Function where usage of name, SSN or Phone input fields are used.
def init_window(commit, Entry_Activated=False, Phone_Activated=False, SSN_Activated=False, Name_Activated=False, placeholder_SSN="YYYYMMDDNNNN"):
    def close():
        selection_window.deiconify()
        enter_window.destroy()
        return None
    # Will hide main Registry manager window.
    selection_window.withdraw()
    ctk.set_appearance_mode("Dark")
    enter_window = ctk.CTkToplevel(selection_window)
    enter_window.title("Selection")
    enter_window.geometry("300x250" + f"+{selection_window.winfo_x()}+{selection_window.winfo_y()}")
    SSN_Entry = ctk.CTkEntry(enter_window, placeholder_text=placeholder_SSN, height=50, width=150)
    Name_Entry = ctk.CTkEntry(enter_window, placeholder_text="Name", height=50, width=150)
    DoneButton = ctk.CTkButton(enter_window, text="Execute",
                               command=lambda: commit(name=Name_Entry.get(), SSN=SSN_Entry.get(), phone=Phone_Entry.get()), width=150, height=50,
                               hover_color="green")
    CloseButton = ctk.CTkButton(enter_window, text="Close", command=lambda: close(), width=75, height=50,
                                hover_color="red")
    Phone_Entry = ctk.CTkEntry(enter_window, placeholder_text="Phone NR", height=50, width=150)
    Entry_Message = ctk.CTkTextbox(enter_window, width=150, height=100)
    Entry_Message.configure(state="disabled")
    CloseButton.grid(row=0, column=1, padx=8)
    if Entry_Activated == True:
        Entry_Message.grid(row=1, column=1, padx=8)
    if Phone_Activated == True:
        if SSN_Activated == False:
            Phone_Entry.grid(row=0, column=0)
        else:
            Phone_Entry.grid(row=2, column=0)
    if SSN_Activated == True:
        SSN_Entry.grid(row=0, column=0)
    if Name_Activated == True:
        Name_Entry.grid(row=1, column=0)
    DoneButton.grid(row=3, column=0)
    enter_window.resizable(False, False)
    enter_window.protocol("WM_DELETE_WINDOW", commit)
    return enter_window, close, Entry_Message, SSN_Entry, Name_Entry, Phone_Entry
#Function for entering a new person into database.
def Enter_new_person():
    #Global dependecies that is used.
    global load_registret, dump_registret_file, init_window
    #Function when something has been comitted to registry. Or if there was an error
    def commited(error=None, message=None):
        #Check if the function was called with an error. Then output the window.
        if error != None:
            Entry_Message.configure(state="normal")
            Entry_Message.delete("0.0", "end")
            Entry_Message.insert("0.0", error)
            Entry_Message.configure(state="disabled")
        #If there was no Error just remove current text inputs from Entryfields.
        else:
            Entry_Message.configure(state="normal")
            Entry_Message.delete("0.0", "end")
            Entry_Message.insert("0.0", message)
            Entry_Message.configure(state="disabled")
            SSN_Entry.delete("0", "end")
            Name_Entry.delete("0", "end")
            Phone_Entry.delete("0", "end")
    #Function for when something is to be added to the database.
    def commit(SSN, name, phone):
        #Check if there is something inside SSN and Name.
        if SSN == "" or name == "":
            #If not return error.
            commited("Please enter SSN and Name")
            return None
        if len(SSN) != 12:
            #If SSN
            commited("Incorrect SSN format.")
            return None
        else:
            registret = load_registret()
            registret[SSN] = {"name": name, "phone": phone}
            dump_registret_file(registret)
            commited(message=name + " was added.")
    #Get tuple from init_window function, to use inside Entry_window function.
    enter_window, close, Entry_Message, SSN_Entry, Name_Entry, Phone_Entry = init_window(commit, Entry_Activated=True, Phone_Activated=True,
                                                                                         SSN_Activated=True, Name_Activated=True)
def Remove_person():
    global load_registret, dump_registret_file, init_window
    def commit(name, SSN, phone=None):
        if name != "" and SSN != "":
            change_text("You can't enter both SSN and name.")
            close()
            return None
        if name != "":
            registret = load_registret()
            SSN_to_delete = {}
            #Goes through everyone in database.
            for SSN in registret:
                #If there is a match.
                if registret[SSN]["name"] == name:
                    #Add name found to dict.
                    SSN_to_delete[SSN] = name
            #Print out all possible matches and let the user choose from them.
            if len(SSN_to_delete) > 1:
                String_of_names = ""
                for SSN in SSN_to_delete:
                    SSN = SSN
                    String_of_names += f"(Name: {SSN_to_delete[SSN]}\n SSN: {SSN}) \n"
                change_text(f"Please specify which SSN of these ({len(SSN)}) you want to delete: \n" + String_of_names)
                close()
            #If there only is one match then remove it from the list.
            else:
                try:
                    del registret[SSN]
                    dump_registret_file(registret)
                    change_text(name + " has been removed.")
                #If it's not even in the list raise an error.
                except:
                    change_text("Name has already been removed.")
                close()
        elif SSN != "":
            try:
                registret = load_registret()
                del registret[SSN]
                try:
                    dump_registret_file(registret)
                    change_text(SSN + " has been removed.")
                except:
                    change_text("SSN has already been removed.")
                close()
            except:
                change_text("Something went wrong")
                close()
        else:
            change_text("No name or SSN was entered.")
            close()
    #Get tuple from init_window function.
    enter_window, close, Entry_Message, SSN_Entry, Name_Entry, Phone_Entry = init_window(commit, SSN_Activated=True, Name_Activated=True)
def Search_phone():
    def commit(SSN=None, name=None, phone=None):
        registret = load_registret()
        String_of_phones = f"Search for phone '{phone}':\n"
        #Goes throgh every person in registry.
        for person in registret:
            #Will detect if there is a match between entered phone and a phone in database.
            if registret[person]["phone"][0:len(phone)] == phone:
                #If there is a match add the match to the finished string
                String_of_phones += f"---------------\nPhone: '{registret[person]['phone']}'\nSSN: {person}\nName: {registret[person]['name']}\n"
        #If the string contains something other than original assignment
        if String_of_phones != f"Search for {phone} returned:":
            #Change output text to search results.
            change_text(String_of_phones)
            close()
        else:
            change_text(f"No owners found for\nPhone: '{phone}'")
            close()
    enter_window, close, Entry_Message, SSN_Entry, Name_Entry, Phone_Entry = init_window(commit, Phone_Activated=True)
def Search_birth():
    def commit(SSN=None, name=None, phone=None):
        registret = load_registret()
        String_of_dates = f"Search for date: '{SSN}':\n"
        #Goes throgh every person in registry.
        for person in registret:
            #Will detect if there is a match between entered phone and a phone in database.
            if person[0:len(SSN)] == SSN:
                #If there is a match add the match to the finished string
                String_of_dates += f"---------------\nSSN: {person}\n Name: {registret[person]['name']}\n"
        #If the string contains something other than original assignment
        if String_of_dates != f"Search for {SSN} returned:":
            #Change output text to search results.
            change_text(String_of_dates)
            close()
        else:
            change_text(f"No owners found for\nDate: '{SSN}'")
            close()
    enter_window, close, Entry_Message, SSN_Entry, Name_Entry, Phone_Entry = init_window(commit, SSN_Activated=True, placeholder_SSN="Search (YYYYMMDD): ")

def Search_given_phone():
    def commit(SSN=None, name=None, phone=None):
        #SSN will be equal to inputted phone number.
        #It's  just easier to define it as SSN because of how the GUI works.
        registret = load_registret()
        String_of_phones = ""
        for person in registret:
            if registret[person]["phone"] == phone:
                String_of_phones += f"Owner for '{phone}'\nSSN: {person}\nName: {registret[person]['name']}\n"
        if String_of_phones != "":
            change_text(String_of_phones)
            close()
        else:
            change_text(f"No owners found for\nPhone: '{phone}'")
            close()
    enter_window, close, Entry_Message, SSN_Entry, Name_Entry, Phone_Entry = init_window(commit, Phone_Activated=True)
def Search_given_SSN():
    def commit(SSN, phone=None, name=None):
        registret = load_registret()
        String_of_Birth_Dates = f"Matching SSN with birthdate\n({SSN}):\n"
        for people in registret:
            print(people[0:8])
            if people == SSN:
                String_of_Birth_Dates += f"'SSN:{people}\nName:{registret[people]['name']}'\n"
        if String_of_Birth_Dates == f"Matching SSN with birthdate\n({SSN}):\n":
            change_text(f"No SSN found matching {SSN}")
            close()
        else:
            change_text(String_of_Birth_Dates)
            close()
    enter_window, close, Entry_Message, SSN_Entry, Name_Entry, Phone_Entry = init_window(commit, SSN_Activated=True)
def Print_all_Names():
    global load_registret
    registret = load_registret()
    Alphabetic_order_list = []
    for person in registret:
        Alphabetic_order_list.append(f"{registret[person]['name']}, {person}")
    #Sort list alphabetically
    Alphabetic_order_list.sort()
    name_string = ""
    for people in Alphabetic_order_list:
        name_string += people + "\n"
    change_text(name_string)
def Change_registry():
    selection_window.withdraw()
    new_file_name = tk.filedialog.askopenfilename(initialdir = os.getcwd()+r"\assets",
                                          title = "Select a File",
                                          filetypes = (("Reg files",
                                                        "*.reg*"),
                                                       ("all files",
                                                        "*.*")))
    if new_file_name != "":
        print(new_file_name[0:len(os.getcwd()+"/assets")])
        print(os.getcwd().replace("\\", "/")+"/assets")
        if new_file_name[0:len(os.getcwd()+"/assets")] != os.getcwd().replace("\\", "/")+"/assets":
            change_text("Registry must be inside " + os.getcwd()+"/assets")
            selection_window.deiconify()
        else:
            global registry_file
            registry_file = new_file_name
            change_text("Current working registry changed to " + new_file_name[len(os.getcwd()+"/assets")+1:])
            selection_window.deiconify()
    else:
        change_text("Registry assignment terminated.")
        selection_window.deiconify()

def option_taken():
    global scriptInit, selection_window, row_count, \
        Enter_new_person, dump_registret_file, change_text, \
        Print_all_Names, Remove_person, Search_phone, Search_birth, \
        Search_given_SSN, Search_given_phone, Change_registry
    change_text("Output")
    print(scriptInit.get())
    option = scriptInit.get()
    if option == "0":
        return_call = Enter_new_person()
        if return_call != None:
            change_text(return_call)
    elif option == "1":
        return_call = Remove_person()
        if return_call != None:
            change_text(return_call)
    elif option == "2":
        return_call = Search_phone()
        if return_call != None:
            change_text(return_call)
    elif option == "3":
        return_call = Search_birth()
        if return_call != None:
            change_text(return_call)
    elif option == "4":
        return_call = Search_given_phone()
        if return_call != None:
            change_text(return_call)
    elif option == "5":
        return_call = Search_given_SSN()
        if return_call != None:
            change_text(return_call)
    elif option == "6":
        return_call = Print_all_Names()
        if return_call != None:
            change_text(return_call)
    elif option == "7":
        return_call = Change_registry()
        if return_call != None:
            change_text(return_call)
    elif option == "8":
        outputText("Registry manager session was terminated.")
        selection_window.destroy()
        return None

scriptInit = ctk.StringVar(value="None")
row_count = 0
#Button for each option
for option in options:
    selection_window.scriptText = ctk.CTkRadioButton(selection_window,
                                         text=option,
                                         variable=scriptInit,
                                         value=options.index(option))
    selection_window.scriptText.grid(row=row_count, column=0,
                     padx=20, pady=10,
                     sticky="ew")
    row_count += 1
print(scriptInit.get())
#Small output window
selection_window.text = ctk.CTkTextbox(selection_window, height=150, state="normal", font=('Comic Sans MS', 15))
selection_window.text.grid(row=int(row_count+3), column=0,
                            columnspan=1, padx=0,
                            pady=20, sticky="ew")
def change_text(text):
    selection_window.text.configure(state="normal")
    selection_window.text.delete("0.0", "end")
    selection_window.text.insert("0.0", text)
    selection_window.text.configure(state="disabled")

change_text("Output")

selection_window_button = ctk.CTkButton(selection_window,
                                           text="Done",
                                           command=option_taken,
                                           width=30)

selection_window_button.grid(row=int(row_count+1), column=0,
                                columnspan=1, padx=0,
                                pady=20, sticky="ew")

stay_on_top()