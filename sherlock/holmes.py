# version 0.13, 23.07.2027 (c) Joachim Kutzera
# last changes:
#### 01.07.2024 - keep_file as parameter in holmes to keep the test file or not
#### 23.07.2024 - Fragen are bold and start with "Frage: "

import json
import os
import subprocess
import time
import sherlock.CL_canvas as CLC
from IPython.display import clear_output

#  pattern strings for sherlockholmes ( Student Code Testing tool)
possible_config_paths_sherlock =  ["code_tests.ipynb",".code_tests.ipynb"]
python_footer_nopoints = ['print("\\n".join(sherlock_antwort))']
python_footer_points =   ['print("\\n".join(sherlock_antwort)+"\\nsherlock_punkte=<"+str(sherlock_punkte)+">")']
settings_tag = "# wichtige Einstellungen"

#  pattern strings for drwatson (student quiz tool)
possible_config_paths_drwatson =  ["quiz_antworten.ipynb",".quiz_antworten.ipynb"]
frage_tag = "Frage"
richtige_antwort_tag = "Richtige Antwort"
falsche_antwort_tag = "Falsche Antwort"
multiple_tag = "multiple"
korrekt_tag = "korrekt"
falsch_tag = "falsch"

###################################################

def extract_nb_code_cells(nbpath):
    json_block = json.load(open(nbpath))
    code_blocks = {}
    for cell_index in range(len(json_block["cells"])):
        if json_block["cells"][cell_index]["cell_type"] == "code":
            if len(json_block["cells"][cell_index]["source"]) > 0:
                if json_block["cells"][cell_index]["source"][0].startswith("#"):
                    code_blocks[json_block["cells"][cell_index]["source"][0].strip()] =  json_block["cells"][cell_index]["source"]
    return(code_blocks)
        
def extract_config_element(json_cell, pattern):
    for element in json_cell:
        if element.startswith(pattern):
            return element.split('=')[1].strip('\n "')
    return("")

def load_config_nb(possible_config_paths):
    # checks:
    config_path = ""
    for item in possible_config_paths:
        if os.path.isfile(item):
            config_path = item
            break
    if config_path == "":    
        print("Sherlock-Holmes Fehler! Kann keine der Dateien " + str(possible_config_paths) + " finden!")
        return ""
    config_nb = extract_nb_code_cells(config_path)
    return(config_nb)

def display_points(points, maxpoints):
    picture_width = 50
    margin = 5
    cl_canvas = CLC.CL_pixel_canvas(maxpoints * (picture_width + margin)+margin ,picture_width + 2*margin,1, canvastype="normal", fillstyle="#404040")
    for a in range(maxpoints):
        if a < points:
            cl_canvas.draw_image_from_file((a*(picture_width + margin))+5,5,"../sherlock/star.png")
        else:
            cl_canvas.draw_image_from_file((a*(picture_width + margin))+5,5,"../sherlock/darkstar.png")
    return cl_canvas

def update_points(cl_canvas, points, maxpoints):
    picture_width = 50
    margin = 5
    for a in range(maxpoints):
        if a < points:
            cl_canvas.draw_image_from_file((a*(picture_width + margin))+5,5,"../sherlock/star.png")
        else:
            cl_canvas.draw_image_from_file((a*(picture_width + margin))+5,5,"../sherlock/darkstar.png")
    

###################################################

def sherlockholmes(id_string):

    def run_test(uebung_nb,config_nb,id_string):
        sherlock_antwort = ""
        sherlock_punkte = 0
    
        if not id_string in config_nb.keys():
            print("Sherlock-Holmes Fehler! Ich kann die Prüfung für diese Zeile nicht finden.")
            return("","","")
        if not id_string in uebung_nb.keys():
            print("Sherlock-Holmes Fehler! Ich kann die zu prüfende Zeile nicht finden.")
            return("","","")
    
        # which message in case of cannot run code?
        cannot_run_code = "Dein Code erzeugt eine Fehlermeldung. Bitte die Codezelle ausführen und auf die Fehlermeldung schauen."
        cannot_run = extract_config_element(config_nb[settings_tag], "cannot_run_code")
        if not cannot_run == "":
            cannot_run_code = cannot_run
        # should I keep the test file instead of deleting it?
        keep_file = extract_config_element(config_nb[settings_tag], "keep_file")
        
        # finding out max-reachable points
        sherlock_max = extract_config_element(config_nb[id_string], "sherlock_max_punkte")
        sherlock_max_punkte = 0
        if not sherlock_max == "":
            sherlock_max_punkte = int(sherlock_max)
            
        if sherlock_max_punkte == 0:
            footer = python_footer_nopoints
        else:
            footer = python_footer_points
        
        python_out = uebung_nb[id_string] + ["\n"] + \
                     config_nb[id_string] + ["\n"] + footer
        
        # creating and running the file
        python_file = open("temp.py","w")
        python_file.write("".join(python_out))
        python_file.close()
        pipe = subprocess.Popen( 'python temp.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
        res = pipe.communicate()
        if not keep_file == "ja":
            os.popen('rm temp.py')
    
        # checking result
        if not pipe.returncode == 0:
            result = cannot_run_code
            sherlock_punkte = 0
        else:
            lres = list(res)
            result = "".join([item.decode("UTF-8") for item in lres])
            # extracting the points
            if "sherlock_punkte=<" in result:
                sherlock_punkte = int(result.split("sherlock_punkte=<")[1].split(">")[0])
                result = result.replace("sherlock_punkte=<"+str(sherlock_punkte)+">", "")
        return result, sherlock_punkte, sherlock_max_punkte
    ###
    
    config_nb = load_config_nb(possible_config_paths_sherlock)
    if len(config_nb) == 0:
        return("")
        
    if settings_tag in config_nb:
        nbpath = extract_config_element(config_nb[settings_tag], "nbpath")
        graphic_points = extract_config_element(config_nb[settings_tag], "graphic_points")
    else:
        print('Sherlock-Holmes Fehler! Ich kann die Zelle mit ' + settings_tag + ' nicht finden!')
        return("")
    if not os.path.isfile(nbpath):
        print("Sherlock-Holmes Fehler! Kann die Übungsdatei unter " + nbpath + " nicht finden!")
        return("")

    # loading exercise-nb
    uebung_nb = extract_nb_code_cells(nbpath)

    print("Analysiere..")    

    sherlock_antwort,sherlock_punkte, sherlock_max_punkte = run_test(
        uebung_nb, 
        config_nb,
        id_string,
    )
    if sherlock_antwort == "": # there was a error within run_test
        return ""
        
    clear_output()
    if sherlock_max_punkte > 0:
        if graphic_points == "ja":
            canvas = display_points(sherlock_punkte,sherlock_max_punkte)
        else:
            print("Deine Punktzahl: ", sherlock_punkte, "von", sherlock_max_punkte,".")
    print(sherlock_antwort) 

###################################################

def drwatson(id_string):

    def run_quiz():
        cl_canvas = display_points(0, max_points)
        def make_func(no):
            def onclick(_):
                if button_selected[no] == 0:
                    if not multiple == "ja":
                        for a in range(len(button_selected)):
                            button_selected[a] = 0
                            buttons[a].style.button_color = 'skyblue'
                    button_selected[no] = 1
                    buttons[no].style.button_color = 'lightgreen'
                else:
                    button_selected[no] = 0
                    buttons[no].style.button_color = 'skyblue'
                if sum(button_selected) == 0:
                    submitbutton.disabled = True
                else:
                    submitbutton.disabled = False
            return onclick
        
        def checkanswers(_):
            submitbutton.layout.display = "none"
            for a in range(len(button_labels)): 
                buttons[a].disabled = True
            answer_correct = True
            points = 0
            for a in range(len(button_labels)): 
                if (button_selected[a] == 1 and correct_or_wrong[a] == "R") or \
                   (button_selected[a] == 0 and correct_or_wrong[a] == "F"):
                   if correct_or_wrong[a] == "R":
                       points = points + 1
                else:
                    answer_correct = False
            if answer_correct:
                ausgabe_feld.value = correct_answer
            else:
                ausgabe_feld.value = false_answer
                show_correct_answers_button.layout.display = "block"
            update_points(cl_canvas, points, max_points)
            
        def showcorrectanswers(_):
            for a in range(len(correct_or_wrong)):
                if correct_or_wrong[a] == "R":
                    buttons[a].style.button_color = 'lightgreen'
                else:
                    buttons[a].style.button_color = 'skyblue'
        
        frage_feld = CLC.widgets.HTML('<b> Frage: ' + frage + '</b>')
        CLC.display(frage_feld)
        button_funcs = []
        
        for a in range(len(button_labels)):
            button_funcs.append(make_func(a))

        # checking whether all labels are shorter than 10 chars. if so, equalize length to 10 for better button look
        lens = [len(button_labels[a]) for a in range(len(button_labels))]
        if max(lens) < 10:
            button_labels_out = []
            for a in range(len(button_labels)):
                spaces = (10 - lens[a]) / 2
                # WARNING: Here, I used the unicode-braille-space-blank char instead of a normal char!! ((U+2800))
                button_labels_out.append("⠀" * (round(spaces)) +    # spaces before label
                                         button_labels[a] +         # label
                                         "⠀" * (round(spaces)) +    # spaces after label
                                         round(2*(spaces % 2)) * ' '# in case of only 9 chars add one more space
									   )
        else:
           button_labels_out = button_labels 
                
        buttons = CLC.CL_make_buttons(button_labels_out,button_funcs, return_buttons=True,auto_button_width = True)  
        for a in range(len(button_labels)):
            buttons[a].style.button_color = 'skyblue'

        if multiple == "ja":    
            ausgabe_feld = CLC.widgets.Label("Wähle eine oder mehrere Antworten aus.")
        else:
            ausgabe_feld = CLC.widgets.Label("Bitte wähle eine Antwort aus.")
        CLC.display(ausgabe_feld)
        
        submitbutton = CLC.CL_make_buttons(["Antworten Prüfen"], [checkanswers], 
                              return_buttons=True)[0]
        submitbutton.style.button_color = "lightgray"
        submitbutton.disabled = True   

        show_correct_answers_button = CLC.CL_make_buttons(["Lösung zeigen"], [showcorrectanswers], 
                                      return_buttons=True)[0]
        show_correct_answers_button.style.button_color = "lightgray"
        show_correct_answers_button.layout.display = "none"

    
    config_nb = load_config_nb(possible_config_paths_drwatson)
    if len(config_nb) == 0:
        return("")

    if not id_string in config_nb.keys():
        print("Dr_watson Fehler! Ich kann das Quiz zur angegebenen ID nicht finden.")
        return("")

    frage = ""
    button_labels = []
    correct_or_wrong = []
    nb_cell = config_nb[id_string]
    max_points = 0
    for line in nb_cell:
        if line.startswith(frage_tag):
            frage = line[(len(frage_tag)+1):].strip()
        if line.startswith(korrekt_tag):
            correct_answer = line[(len(korrekt_tag)+1):].strip()
        if line.startswith(falsch_tag):
            false_answer = line[(len(falsch_tag)+1):].strip()
        if line.startswith(multiple_tag):
            multiple = line[(len(multiple_tag)+1):].strip()
        if line.startswith(richtige_antwort_tag):
            button_labels.append(line[(len(richtige_antwort_tag)+1):].strip())
            correct_or_wrong.append("R")
            max_points = max_points + 1
        if line.startswith(falsche_antwort_tag):
            button_labels.append(line[(len(falsche_antwort_tag)+1):].strip())
            correct_or_wrong.append("F")
            
    button_selected = [0] * len(button_labels)  
    if frage == "":
        print("Dr-watson Fehler! Das Quiz hat keine Frage.")
        return("")
    if len(button_labels) == 0:
        print("Dr-watson Fehler! Das Quiz hat keine Antworten.")
        return("")
    if "R" not  in correct_or_wrong:
        print("Dr-watson Fehler! Das Quiz hat keine richtige Antwort.")
        return("")
    if "F" not  in correct_or_wrong:
        print("Dr-watson Fehler! Das Quiz hat keine falsche Antwort.")
        return("")
        
    run_quiz()
