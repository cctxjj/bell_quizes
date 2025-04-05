import threading
import time

from IPython.core.display_functions import display

import ipywidgets as widgets
import random


class Checkbutton:
    def __init__(self,
                 condition,
                 reaction_correct=None,
                 elements_to_disable=None):
        checkbutton = widgets.Button(
            description="Prüfen",
            style={"button_color": "#87CEFA"},  # Farbe setzen
            layout=widgets.Layout(
                width="120px", 
                height="40px",  
                border="none",  
                border_radius="12px",  
                font_weight="bold",  
                font_size="20px",  
                font_family="Arial",
                box_shadow="2px 2px 5px rgba(0, 0, 0, 0.2)", 
                margin="0px 0px 30px 0px"
            )
        )
        
        display(checkbutton)
        self.is_blinking = False

        def check(b):
            if condition():
                b.style.button_color = "#90EE90"
                b.disabled = True
                b.description = "Richtig!"
                if reaction_correct is not None:
                    reaction_correct()
                if elements_to_disable is not None:
                    for element in elements_to_disable:
                        element.disabled = True
            else:
                def blink_red():
                    if self.is_blinking:
                        return
                    self.is_blinking = True
                    for ignored in range(2):
                        b.style.button_color = "#FF7F7F"
                        time.sleep(0.5)
                        b.style.button_color = "#87CEFA"
                        time.sleep(0.5)
                    self.is_blinking = False

                threading.Thread(target=blink_red).start()

        checkbutton.on_click(check)
        Line()


class SimpleInput:
    def __init__(self,
                 question: str,
                 target_result: str,
                 instant_create: bool = True):
        self.question = question
        self.target_result = target_result
        if instant_create:
            self.create()

    def create(self):

        textbox = widgets.Text(value='',
                               placeholder='Hier eingeben',
                               description='Antwort: ',
                               disabled=False,
                              layout=widgets.Layout(
                                    margin="0px 0px 15px 0px"
                                ))
        instruction = widgets.HTML(value=self.question)

        display(instruction)
        display(textbox)

        def is_correct():
            return textbox.value.strip().replace(" ", '').lower() == self.target_result.strip().replace(" ", '').lower()
        Checkbutton(is_correct, None, [textbox])


class MultipleChoice:
    def __init__(self,
                 question: str,
                 correct_results: list,
                 false_results: list,
                 items_per_row: int = 2,
                 instant_create: bool = True):
        self.question = question
        self.correct_results = correct_results
        self.false_results = false_results
        self.items_per_row = items_per_row
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

        def is_correct():
            corr = True
            for checkbox, target_result in answer_buttons.items():
                if checkbox.value != target_result:
                    corr = False
                    break
            return corr
        Checkbutton(is_correct, None, answer_buttons.keys())



class SingleChoice:
    def __init__(self,
                 question: str,
                 correct_result: str,
                 false_results: list,
                 items_per_row: int = 2,
                 instant_create: bool = True):
        self.question = question
        self.correct_result = correct_result
        self.false_results = false_results
        self.items_per_row = items_per_row
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

        def is_correct():
            corr = True
            for checkbox, target_result in answer_buttons.items():
                if checkbox.value != target_result:
                    corr = False
                    break
            return corr

        Checkbutton(is_correct, None, answer_buttons.keys())


class ButtonedMultipleChoice:
    def __init__(self,
                 question: str,
                 correct_results: list,
                 false_results: list,
                 items_per_row: int = 2,
                 instant_create: bool = True):
        self.question = question
        self.correct_results = correct_results
        self.false_results = false_results
        self.items_per_row = items_per_row
        self.answers = [*correct_results, *false_results]
        random.shuffle(self.answers)
        if instant_create:
            self.create()

    def create(self):

        instruction = widgets.HTML(value=self.question)
        display(instruction)

        answer_buttons = {}
        len_buttons = f"{len(max(self.answers)) * 12 + 50}px"
        for option in self.answers:
            cb: widgets.Button = widgets.Button(
                description=option,
                style={"button_color": "#D3D3D3"},  
                layout=widgets.Layout(
                    width=len_buttons,
                    height="50px",  
                    border="none",  
                    border_radius="12px",  
                    font_weight="bold",  
                    font_size="16px",  
                    padding="10px",  
                    margin="5px"
                )
            )
            cb.selected = False
            def select(b):
                if b.selected:
                    b.layout.border = "none"
                    b.selected = False
                else:
                    b.layout.border = "4px solid #0056b3"
                    b.selected = True

            cb.on_click(select)
            answer_buttons[cb] = option in self.correct_results

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

        def is_correct():
            corr = True
            for button, target_result in answer_buttons.items():
                if button.selected != target_result:
                    corr = False
                    break
            return corr

        Checkbutton(is_correct, None, answer_buttons.keys())


class ButtonedSingleChoice:
    def __init__(self,
                 question: str,
                 correct_result: str,
                 false_results: list,
                 items_per_row: int = 2,
                 instant_create: bool = True):
        self.question = question
        self.correct_result = correct_result
        self.false_results = false_results
        self.items_per_row = items_per_row
        self.answers = [correct_result, *false_results]
        random.shuffle(self.answers)
        if instant_create:
            self.create()

    def create(self):

        instruction = widgets.HTML(value=self.question)
        display(instruction)

        answer_buttons = {}
        len_buttons = f"{len(max(self.answers)) * 12 + 50}px"
        for option in self.answers:
            cb: widgets.Button = widgets.Button(
                description=option,
                style={"button_color": "#D3D3D3"},  
                layout=widgets.Layout(
                    width=len_buttons,
                    height="50px",  
                    border="none",  
                    border_radius="12px",  
                    font_weight="bold",  
                    font_size="16px",  
                    padding="10px",  
                    margin="5px"
                )
            )
            cb.selected = False
            def select(b):
                if b.selected:
                    b.layout.border = "#D3D3D3"
                    b.selected = False
                else:
                    for button_to_correct in answer_buttons.keys():
                        b.layout.border = "#D3D3D3"
                        button_to_correct.selected = False
                    b.layout.border = "4px solid #0056b3"
                    b.selected = True

            cb.on_click(select)
            answer_buttons[cb] = option == self.correct_result

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

        def is_correct():
            corr = True
            for button, target_result in answer_buttons.items():
                if button.selected != target_result:
                    corr = False
                    break
            return corr

        Checkbutton(is_correct, None, answer_buttons.keys())


class Hint:
    def __init__(self,
                 content: str,
                 name: str = "Hinweis",
                 color="grey",
                 color_revealed="olive",
                 instant_create: bool = True):
        self.content = content
        self.name = name
        self.color = color
        self.color_revealed = color_revealed
        if instant_create:
            self.create()

    def create(self):
        hint_button = widgets.Button(description=self.name)
        hint_button.style.button_color = self.color
        hint_text: widgets.HTML = widgets.HTML(value="")

        def on_click(b):
            hint_text.value = self.content
            b.style.button_color = self.color_revealed
            b.disabled = True

        hint_button.on_click(on_click)
        display(widgets.HBox([hint_button, hint_text]))


# Todo: Maybe remove unnecessary return f funcs for on_button_click
# Todo: Add design, colors, visual difference between options
class OrderTask:
    def __init__(self,
                 question: str,
                 items: list,
                 color: str = "aqua",
                 width: str = "300px",
                 instant_create: bool = True):
        self.items = list(set(items))
        self.question = question
        self.width = width
        self.color = color
        self.correct_order = items

        random.shuffle(self.items)

        if instant_create:
            self.create()

    def create(self):

        instruction = widgets.HTML(value=self.question)
        display(instruction)

        boxes = []
        box_text_rel = {}
        button_text_rel = {}
        for element in self.items:
            button_up: widgets.Button = widgets.Button(description="↑",
                                                            style={"button_color": "#D3D3D3"},  
                                                            layout=widgets.Layout(
                                                                width="60px",
                                                                height="25px",  
                                                                border="none",  
                                                                border_radius="12px",  
                                                                font_weight="bold",  
                                                                font_size="25px"
                                                            ))
            button_down = widgets.Button(description="↓",
                                        style={"button_color": "#D3D3D3"},  
                                        layout=widgets.Layout(
                                        width="60px",
                                        height="25px",  
                                        border="none",  
                                        border_radius="12px",  
                                        font_weight="bold",  
                                        font_size="25px"
                                        ))

            def up(b):
                for index, item in enumerate(boxes):
                    if box_text_rel[item] == button_text_rel[b]:
                        if index == 0:
                            break
                        else:
                            temp = boxes[index - 1]
                            boxes[index] = temp
                            boxes[index - 1] = item
                            main_container.children = boxes
                        break

            def down(b):
                for index, item in enumerate(boxes):
                    if box_text_rel[item] == button_text_rel[b]:
                        if index >= len(boxes) - 1:
                            break
                        else:
                            temp = boxes[index + 1]
                            boxes[index] = temp
                            boxes[index + 1] = item
                            main_container.children = boxes
                        break

            button_up.on_click(up)
            button_down.on_click(down)

            button_text_rel[button_up] = element
            button_text_rel[button_down] = element

            button_container = widgets.VBox([button_up, button_down])

            text: widgets.HTML = widgets.HTML(
                                            f"""
                                            <div style="
                                                display: flex;
                                                justify-content: center;
                                                align-items: center;
                                                width: 100%;
                                                padding: 10px;
                                                background-color: #f4f4f4;
                                                border-radius: 8px;
                                                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
                                                font-family: 'Arial', sans-serif;
                                                font-size: 14px;
                                                color: #333;
                                                margin-bottom: 15px;
                                            ">
                                                <strong>{element}</strong>
                                            </div>
                                            """
                                        )
            text.actual_value = element
            main_box: widgets.HBox = widgets.HBox([text, button_container])
            box_text_rel[main_box] = element
            boxes.append(main_box)

        main_container = widgets.VBox(boxes)
        display(main_container)

        def is_correct():
            corr = True
            for i in range(len(self.correct_order)):
                if self.correct_order[i] != boxes[i].children[0].actual_value:
                    corr = False
                    break
            return corr
        Checkbutton(is_correct, None, button_text_rel.keys())



class DropdownText:
    def __init__(self,
                 text: str,
                 instant_create: bool = True):
        # Syntax: options in {}, seperated by /; last option is processed as correct result
        self.text = text

        if instant_create:
            self.create()

    def create(self):
        processed_text = []
        is_multiple_choice = []
        cur = ""
        for letter in self.text:
            if letter == "{" or letter == "}":
                if cur != "":
                    processed_text.append(cur)
                    if letter == "}":
                        is_multiple_choice.append(True)
                    else:
                        is_multiple_choice.append(False)
                cur = ""
            else:
                cur = cur + letter
        if cur != "":
            processed_text.append(cur)
            is_multiple_choice.append(False)

        elements = []
        choice_elements = {}

        for index in range(len(processed_text)):
            if is_multiple_choice[index]:
                dropdown: widgets.Dropdown = widgets.Dropdown(options=["_"*len(max(processed_text[index].split("/"))), *processed_text[index].split("/")[0:-1]], value="_"*len(max(processed_text[index].split("/"))), layout=widgets.Layout(width="auto"))
                elements.append(dropdown)
                choice_elements[dropdown] = processed_text[index].split("/")[-1]
            else:
                text = processed_text[index]
                wdgt = widgets.HTML(text)
                elements.append(wdgt)
        final_hbox = widgets.HBox(elements, layout=widgets.Layout(flex_flow="wrap"))
        display(final_hbox)

        def is_correct():
            corr = True
            for element in choice_elements.keys():
                if element.value != choice_elements[element]:
                    corr = False
                    break
            return corr
        Checkbutton(is_correct, None, list(choice_elements.keys()))



class AnswerboxText:
    def __init__(self,
                 text: str,
                 instant_create: bool = True):
        # Syntax: text with correct answer in {}
        self.text = text

        if instant_create:
            self.create()

    def create(self):
        processed_text = []
        is_textbox = []
        cur = ""
        for letter in self.text:
            if letter == "{" or letter == "}":
                if cur != "":
                    processed_text.append(cur)
                    if letter == "}":
                        is_textbox.append(True)
                    else:
                        is_textbox.append(False)
                cur = ""
            else:
                cur = cur + letter
        if cur != "":
            processed_text.append(cur)
            is_textbox.append(False)

        elements = []
        textbox_elements = {}

        for index in range(len(processed_text)):
            if is_textbox[index]:
                textbox: widgets.Text = widgets.Text(placeholder="", layout=widgets.Layout(width=str(30 + 10*len(processed_text[index]))+"px"))
                elements.append(textbox)
                textbox_elements[textbox] = processed_text[index]
            else:
                text = processed_text[index]
                wdgt = widgets.HTML(text)
                elements.append(wdgt)
        final_hbox = widgets.HBox(elements, layout=widgets.Layout(flex_flow="wrap"))
        display(final_hbox)

        def is_correct():
            corr = True
            for element in textbox_elements.keys():
                if element.value != textbox_elements[element]:
                    corr = False
                    break
            return corr
        Checkbutton(is_correct, None, textbox_elements.keys())

class Line():
    def __init__(self):
        line = widgets.HTML("<hr style='border:1px solid #ccc; margin:10px 0;'>")
        display(line)