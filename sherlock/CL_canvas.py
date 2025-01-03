# version 0.12, 01.07.2027 (c) Joachim Kutzera
# last changes:
#### 01.07.2024 - automatic or default button width settable

from IPython.display import display
from threading import Thread
from time import sleep
from ipycanvas import RoughCanvas, Canvas, hold_canvas
import ipywidgets as widgets
import time

def CL_make_buttons(labels, functions, return_buttons = False, auto_button_width=False):
    buttons = []
    buttonfuncs = []
    if auto_button_width:
        layout = widgets.Layout(width='auto') 
    else:
        layout = widgets.Layout() 
    for lindex in range(len(labels)):
        buttons.append(widgets.Button(description=labels[lindex], layout = layout))
        buttons[lindex].on_click(functions[lindex])
    display(widgets.HBox(buttons))
    if return_buttons:
        return buttons

class CL_pixel_canvas:
    def __init__(self, width, height, pixelsize,fillstyle = "#F0F0C0", strokestyle = "white", canvastype = "rough"):
        self.width = width
        self.height = height
        self.pixelsize = pixelsize   
        self.fillstyle = fillstyle
        self.strokestyle = strokestyle
        self.canvastype = canvastype
        if canvastype == "rough":
            self.canvas = RoughCanvas(width=self.width * pixelsize, height=self.height * pixelsize)
        elif canvastype == "normal":
            self.canvas = Canvas(width=self.width * pixelsize, height=self.height * pixelsize)
        self.canvas.fill_style = self.fillstyle
        self.canvas.stroke_style = self.strokestyle
        self.canvas.fill_rect(0, 0, self.canvas.width, self.canvas.height)
        display(self.canvas) 
        
    def drawpixels(self, pos_Xs, pos_Ys, pixelcolor, draw_background = True):
        posXs = [x * self.pixelsize for x in pos_Xs]
        posYs = [y * self.pixelsize for y in pos_Ys]
        with hold_canvas():
            if draw_background:
                self.canvas.clear()
            self.canvas.fill_style = self.fillstyle
            self.canvas.stroke_style = self.strokestyle
            if draw_background:
                self.canvas.fill_rect(0, 0, self.canvas.width, self.canvas.height)
            self.canvas.fill_style =  pixelcolor 
            self.canvas.stroke_style = pixelcolor
            self.canvas.fill_rects(posXs, posYs, self.pixelsize)
            self.canvas.stroke_rects(posXs , posYs , self.pixelsize)

    def draw_image_from_file(self,posx, posy, file):
        img = widgets.Image.from_file(file)
        self.canvas.draw_image(img, posx, posy)

    
class CL_runfunc(Thread):
    def __init__(self, myfunc, myparams):
        self.myfunc = myfunc
        self.myparams = myparams
        super(CL_runfunc, self).__init__()

    def run(self):
        self.myfunc(*self.myparams)        
