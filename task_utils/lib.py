import time
from token import AMPEREQUAL

import notebook
from Demos.desktopmanager import hicon
from IPython.core.display_functions import display

from ipywidgets import interact
import ipywidgets as widgets
import ipycanvas as canvas
import random

from scripts.regsetup import description


class SimpleInput:
    def __init__(self,
                 question: str,
                 target_result: str,
                 hints: list = None,
                 instant_create: bool = True):
        self.question = question
        self.hints = hints
        self.target_result = target_result
        if instant_create:
            self.create()

    def create(self):

        textbox = widgets.Text(value = '',
                               placeholder='Hier eingeben',
                               description='Antwort: ',
                               disabled=False)
        instruction = widgets.HTML(value=self.question)
        checkbutton = widgets.Button(description='Prüfen', disabled=False)
        checkbutton.style.button_color = 'grey'
        display(instruction)
        display(textbox)

        display(checkbutton)
        def check(b):
            if textbox.value.strip().replace(" ", '').lower() == self.target_result.strip().replace(" ", '').lower():
                b.style.button_color = 'green'
                b.disabled = True
                textbox.disabled = True
                b.description = "Richtig!"
                if self.hints is not None:
                    for h in self.hints:
                        h.disable()
            else:
                for ignored in range(2):
                    b.style.button_color = 'red'
                    time.sleep(0.5)
                    b.style.button_color = 'grey'
                    time.sleep(0.5)

        checkbutton.on_click(check)

    def add_hint(self, hint):
        if self.hints is not None:
            self.hints.append(hint)
        else:
            self.hints = [hint]



class MultipleChoice:
    def __init__(self,
                 question: str,
                 correct_results: list,
                 false_results: list,
                 items_per_row: int = 2,
                 hints: list = None,
                 instant_create: bool = True):
        self.question = question
        self.correct_results = correct_results
        self.false_results = false_results
        self.items_per_row = items_per_row
        self.hints = hints
        self.answers = [*correct_results, *false_results]
        random.shuffle(self.answers)
        if instant_create:
            self.create()

    def create(self):

        instruction = widgets.HTML(value=self.question)
        display(instruction)

        answer_buttons = {}
        for option in self.answers:
            cb: widgets.Checkbox = widgets.Checkbox()
            cb.description = option
            answer_buttons[cb] = option in self.correct_results

        layout_answers =  []
        for i in range(0, len(list(answer_buttons.keys())), self.items_per_row):
            answers_in_line = []
            for x in range(self.items_per_row):
                try:
                    answers_in_line.append(list(answer_buttons.keys())[i+x])
                except IndexError:
                    break
            layout_answers.append(widgets.HBox(answers_in_line))
        container = widgets.VBox(layout_answers)
        display(container)

        checkbutton: widgets.Button = widgets.Button(description='Prüfen', )
        checkbutton.style.button_color = 'grey'

        display(checkbutton)
        def check(b):
            corr = True
            for checkbox, target_result in answer_buttons.items():
                if not checkbox.value == target_result:
                    corr = False
                    break
            if corr:
                b.style.button_color = 'green'
                b.disabled = True
                b.description = "Richtig!"
                for checkbox in answer_buttons.keys():
                    checkbox.disabled = True
                if self.hints is not None:
                    for h in self.hints:
                        h.disable()
            else:
                for ignored in range(2):
                    b.style.button_color = 'red'
                    time.sleep(0.5)
                    b.style.button_color = 'grey'
                    time.sleep(0.5)
            return check
        checkbutton.on_click(check)

    def add_hint(self, hint):
        if self.hints is not None:
            self.hints.append(hint)
        else:
            self.hints = [hint]


class SingleChoice:
    def __init__(self,
                question: str,
                correct_result: str,
                false_results: list,
                items_per_row: int = 2,
                hints: list = None,
                instant_create: bool = True):
        self.question = question
        self.correct_result = correct_result
        self.false_results = false_results
        self.items_per_row = items_per_row
        self.hints = hints
        self.answers = [correct_result, *false_results]
        random.shuffle(self.answers)
        if instant_create:
            self.create()

    def create(self):

        instruction = widgets.HTML(value=self.question)
        display(instruction)



        answer_buttons = {}
        for option in self.answers:
            cb: widgets.Checkbox = widgets.Checkbox()
            cb.description = option
            answer_buttons[cb] = option == self.correct_result

        def on_checkbox_tick(info):
            if not info["new"]:
                return
            for checkbox in list(answer_buttons.keys()):
                if checkbox.description != info["owner"].description:
                    checkbox.value = False

        for button in answer_buttons.keys():
            button.observe(on_checkbox_tick, 'value')

        layout_answers = []
        for i in range(0, len(list(answer_buttons.keys())), self.items_per_row):
            answers_in_line = []
            for x in range(self.items_per_row):
                try:
                    answers_in_line.append(list(answer_buttons.keys())[i + x])
                except IndexError:
                    break
            layout_answers.append(widgets.HBox(answers_in_line))
        container = widgets.VBox(layout_answers)
        display(container)

        checkbutton: widgets.Button = widgets.Button(description='Prüfen', )
        checkbutton.style.button_color = 'grey'

        display(checkbutton)

        def check(b):
            corr = True
            for checkbox, target_result in answer_buttons.items():
                if not checkbox.value == target_result:
                    corr = False
                    break
            if corr:
                b.style.button_color = 'green'
                b.disabled = True
                b.description = "Richtig!"
                for checkbox in answer_buttons.keys():
                    checkbox.disabled = True
                if self.hints is not None:
                    for h in self.hints:
                        h.disable()
            else:
                for ignored in range(2):
                    b.style.button_color = 'red'
                    time.sleep(0.5)
                    b.style.button_color = 'grey'
                    time.sleep(0.5)
            return check

        checkbutton.on_click(check)

    def add_hint(self, hint):
        if self.hints is not None:
            self.hints.append(hint)
        else:
            self.hints = [hint]
# Todo: add option to add hints

class SingeChoiceButtoned:
    pass
    # TODO

class Hint:
    def __init__(self,
                 content: str,
                 name: str = "Hinweis",
                 color = "grey",
                 color_revealed = "olive",
                 instant_create: bool = True):
        self.content = content
        self.name = name
        self.color = color
        self.color_revealed = color_revealed
        if instant_create:
            self.create()

    def create(self):
        self.hint_button = widgets.Button(description=self.name)
        self.hint_button.style.button_color = self.color
        hint_text: widgets.HTML = widgets.HTML(value="")


        def on_click(b):
            if hint_text.value != "":
                b.style.button_color = self.color
                hint_text.value = ""
            else:
                hint_text.value = self.content
                b.style.button_color = self.color_revealed

        self.hint_button.on_click(on_click)
        display(widgets.HBox([self.hint_button, hint_text]))

    def disable(self):
        self.hint_button.disabled = True





