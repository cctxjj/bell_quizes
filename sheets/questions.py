from IPython.core.display_functions import display

from sheets import lib
from ipycanvas import Canvas
import ipywidgets as wd
import matplotlib.pyplot as plt

class PG:

    def __init__(self):
        self.canvas = None

    def text_1(self):
        # Text angepasst von Wikipedia 
        return lib.DropdownText("Eine Pixelgrafik ist eine Form der Beschreibung eines Bildes in Form von computerlesbaren Daten. Pixelgrafiken bestehen aus einer {ausgedehnten/rasterförmigen/kreisartigen/rasterförmigen} Anordnung sogenannter {Pixel/Vektoren/Bilder/Pixel}, denen jeweils eine {Größe/Farbe/Höhe/Farbe} zugeordnet ist. Daher nennt man die Pixelgrafik auch {Vektorgrafik/Rastergrafik/Bildpunkttechnik/Rastergrafik}. Die Hauptmerkmale einer {Vektorgrafik/Rastergrafik/Bildpunkttechnik/Rastergrafik} sind entsprechend die Bildgröße, umgangssprachlich auch Bildauflösung genannt, sowie die {Farbhöhe/Farbtiefe/Farbintensität/Farbtiefe}.")

    def text_2(self):
        return lib.DropdownText("RLE steht für {right-lenght-enclosure/run-length encoding/short-lenght-code/run-length encoding}, auf deutsch {Lauflängenkodierung/Längenlaufkodierung/Kodierungsalgrithmus/Lauflängenkodierung}.")

    def question_1(self):
        return lib.ButtonedMultipleChoice("Eingesetzt wird die Pixelgrafik vorwiegend zur Darstellung von", ["komplexen Bildern", "Fotos"], ["simplen Formen", "Vektorgrafiken"], 2)

    def question_2(self):
        return lib.ButtonedSingleChoice("Woraus besteht eine Rastergrafik?", "Bildpunkte", ["3D-Modelle", "mathematische Formeln", "Vektoren"], 2)

    def question_3(self):
        return lib.ButtonedMultipleChoice("Was wird bei einem Bild von einem roten Rechteck in der Pixelgrafik gespeichert?", ["alle Pixel", "Maße des Bildes"], ["Seitenlängen", "relevante Bildpunkte"], 2)

    def question_3(self):
        return lib.ButtonedMultipleChoice("Welche Farben werden im RGB-Farbmodell verwendet?", ["rot", "grün", "blau"], ["grau", "magenta", "gelb"], 3)

    def question_4(self):
        return lib.ButtonedMultipleChoice("Was bedeutet eine Farbtiefe von 24 Bit?", ["16,7 Mio. Farben", "24 Bit pro Pixel Speicherplatz"], ["24 Farben", "Nur Schwarz-Weiß"], 2)

    def question_5(self):
        return lib.ButtonedMultipleChoice("Welches Dateiformat gehört zur Pixelgrafik?", [".bmp", ".jpg", ".png"], [".svg"], 2)

    def question_6(self):
        return lib.ButtonedSingleChoice("Wie wird der String 'AABBACCC' nach RLE komprimiert?", "2A2B1A3C", ["2A2BA4C", "3A2B3C", "8ABC"], 2)

    def question_7(self):
        return lib.SimpleInput("Wie wird der String 'GGBBBRR' nach RLE komprimiert?", "2G3B2R")

    def question_8(self):
        return lib.ButtonedMultipleChoice("Welche Aussagen über den Code stimmen?", ["'letzter_buchstabe' speicherz den letzten Buchstaben, um ihn mit dem Nächsten zu vergleichen.", "'ergebnis' speichert den komprimierten String"], ["Die for-Schleife beginnt mit dem ersten Zeichen der Eingabe", "'zähler' hat stets den Wert 1"], 1)

    def question_9(self):
        return lib.ButtonedSingleChoice("Warum wird am Ende das Ergebnis noch einmal außerhalb der Schleife angepasst? (ergebnis = str(zähler) + letzter_buchstabe) ", "Damit der letzte Buchstabe und seine Anzahl nicht verloren gehen", ["Da der Zähler sonst stets 1 wäre", "Damit die Schleife korrekt weiterläuft", "Um sicherzustellen, dass das Ergebnis kein leerer String ist"], 1)

    def order_1(self):
        return lib.OrderTask("Sortiere die einzelnen Schritte im Bresenham-Algorithmus", ["Startpunkt und Endpunkt (x und y) sind gegeben", "Betrachtung des Pixels rechts vom aktuellen Bildpunkt (Ausgangspunkt)", "Fehlererrechnung - Abweichung von der Ideallinie wird ermittelt", "Fallunterscheidung in Abhängigkeit vom Fehler, Verschiebung nach oben falls nötig", "Pixel wird ausgemalt"])

    def stelle_dar(self, pixel_x, pixel_y, color="black"):
        # function used to display bresenham algorithm
        if self.canvas is None:
            self.canvas = Canvas(width=210, height=210)
            display(self.canvas)
        self.canvas.fill_sytle = color
        self.canvas.fill_rect(pixel_x*10, 190-pixel_y*10, 10, 10)
        


class VG:
    def __init__(self):
        self.canvas = None
        self.ax = None
        self.fig = None

    def text_1(self):
        # Text angepasst von Wikipedia 
        return lib.DropdownText("Eine Vektorgrafik ist eine Computergrafik, die aus simplen grafischen Elementen wie Linien, Kreisen, Polygonen oder allgemeinen {Kanten/Kasten/Kurven/Kurven} zusammengesetzt ist. Meist sind mit Vektorgrafiken Darstellungen gemeint, deren Körper sich zweidimensional in der Ebene beschreiben lassen, ähnlich wie bei einem {Graphen/Vektor/Bild/Vektor} in der analytischen Geometrie. Entscheiden ist, dass nicht {Objekte und Attribute/einzelne Bildpunkte/einzelne Bildpunkte}, sondern {Objekte und Attribute/einzelne Bildpunkte/Objekte und Attribute} gespeichert werden.")

    def question_1(self):
        return lib.ButtonedSingleChoice("Die Vektorgrafik ist ", "objektorientiert", ["veraltet", "bildpunktorientiert", "auflösungsbedacht"], 2)

    def question_2(self):
        return lib.ButtonedMultipleChoice("Was wird bei einem Bild von einem roten Rechteck in der Vektorgrafik gespeichert?", ["Seitenlängen", "Farbe"], ["Flächeninhalt", "zugehörige Pixel"], 2)

    def question_3(self):
        return lib.ButtonedSingleChoice("Was ist eine Besonderheit der Vektorgrafik?", "skalierbar ohne Qualitätsverlust", ["ideal für Fotos", "besteht aus Bildpunkten", "hoher Speicherplatzbedarf"], 2)
    
    def question_4(self):
        return lib.ButtonedMultipleChoice("Welches Dateiformat gehört zur Vektorgrafik?", [".svg"], [".bmp", ".jpg", ".png"], 2)
    
    def print_rect(self, breite, hoehe, x, y, farbe="#Ff0000"):
        # function to display a rectangle according to given attributes
        if self.canvas is None:
            self.canvas = Canvas(width=800, height=400)
        self.canvas.clear()
        display(self.canvas)
        try:
            self.canvas.fill_style = farbe
        except Exception:
            pass
        self.canvas.fill_rect(x=x, y=self.canvas.height-(y + hoehe), width=breite, height=hoehe)

    def adjustable_rect(self):
        wd.interact(self.print_rect, breite=(0, 400, 20), höhe=(0, 200, 20), x=(0, 400, 20), y=(0, 200, 20))

    def stelle_punkte_dar(self, points, step, color="blue"):
        dspl = True
        if self.ax is None:
            dspl = False
            self.fig, self.ax = plt.subplots()
            self.ax.set_xlabel('x-Achse')
            self.ax.set_ylabel('y-Achse')
            
        x, y = zip(*points)
        # plotting points
        self.ax.set_title(f'Visualisierung der {step}-Punkte (mit Matplotlib)')
        self.ax.scatter(x, y, color=color, label='Punkte')
        self.ax.plot(x, y, color=color, label='Punkte')
        if dspl:
            display(self.fig)

    def stelle_kurve_dar(self, starting_points, points, color_1="blue", color_2="green"):
        fig, ax = plt.subplots()
        x, y = zip(*points)
        x_s, y_s = zip(*starting_points)

        ax.scatter(x, y, color=color_1)
        ax.scatter(x_s, y_s, color=color_2)
        ax.plot(x_s, y_s, color=color_2)

        ax.set_xlabel('x-Achse')
        ax.set_ylabel('y-Achse')

        ax.set_title('Punkt-Darstellung mit Matplotlib')
        
        

    def teiler_punkte(self, points, t):
        new_points_x = []
        if not 0 < t < 1:
            t = 0.5
            print("t größer 1 bzw. kleiner 0 --> t auf 0.5 angepasst")
        for i in range(len(points) - 1):
            new_point = (1 - t) * points[i][0] + t * points[i + 1][0]
            new_points_x.append(new_point)
        new_points_y = []
        for i in range(len(points) - 1):
            new_point = (1 - t) * points[i][1] + t * points[i + 1][1]
            new_points_y.append(new_point)
        return list(zip(new_points_x, new_points_y))

    def errechne_kurvenpunkt(self, points, t):
        points_x, points_y = [p[0] for p in points], [p[1] for p in points]
        return self.de_casteljau(points_x, t), self.de_casteljau(points_y, t)
        
    def de_casteljau(self, control_points, t):
        # function calculating one point on the curve according to t, recursive
        if not 0 < t < 1:
            raise
        if len(list(control_points)) == 1:
            return control_points[0]
        else:
            new_points = []
            for i in range(len(control_points) - 1):
                new_point = control_points[i] + t*(control_points[i+1]-control_points[i])
                new_points.append(new_point)
        return self.de_casteljau(new_points, t)
        
                

class Rechteck:
    def __init__(self, breite, hoehe, x, y, farbe):
        self.breite = breite
        self.hoehe = hoehe
        self.x = x
        self.y = y
        self.farbe = farbe
        self.canvas = None

    def anzeigen(self):
        if self.canvas is None:
            self.canvas = Canvas(width=max(self.breite+self.x, 100), height=max(self.hoehe+self.y, 100))
            display(self.canvas)
        self.canvas.fill_style = self.farbe
        self.canvas.fill_rect(x=self.x, y=self.canvas.height-(self.y+self.hoehe), width=self.breite, height=self.hoehe)
        



    

        