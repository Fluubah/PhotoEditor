from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from PIL import Image, ImageDraw
import random

from kivy.uix.widget import Widget


class PhotoEditorApp(App):
    pass


class MouseTouch(Widget):

    button = ObjectProperty(None)

    def on_touch_down(self, touch):
        print("Button Down")
        coords=touch.pos
        print(f"x coordinate: {str(int(coords[0]))}")
        print(f"y coordinate: {str(int(coords[1]))}")
        self.button.background_color, self.button.color, self.button.text = "white", "black", "pressed"

    def on_touch_move(self, touch):
        pass

    def on_touch_up(self, touch):
        print("Button Up")
        coords = touch.pos
        print(f"x coordinate: {str(int(coords[0]))}")
        print(f"y coordinate: {str(int(coords[1]))}")
        self.button.background_color = "black"
        self.button.color = "white"
        self.button.text = "Press Me"


class Display(Screen):

    def load_image(self):
        self.ids.image.source = self.ids.img_name.text

    def display_image(self):
        return

    def invert(self, image):
        img = Image.open(image)
        pixels = img.load()
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                red = 255 - pixels[x, y][0]
                green = 255 - pixels[x, y][1]
                blue = 255 - pixels[x, y][2]
                pixels[x, y] = (red, green, blue)
        img.save(self.ids.image.source + "_inverted.png")
        self.ids.image.source = self.ids.image.source+"_inverted.png"

    def sepia(self, image):
        img = Image.open(image)
        pixels = img.load()
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                red = pixels[x, y][0]
                green = pixels[x, y][1]
                blue = pixels[x, y][2]
                red = int(red*.393 + green*0.769 + blue * 0.189)
                green = int(red*.349 + green*0.686 + blue * 0.168)
                blue = int(red*.272 + green*0.534 + blue * 0.131)
                pixels[x, y] = (red, green, blue)
        img.save(image+"_sepia.png")
        self.ids.image.source = self.ids.image.source+"_sepia.png"

    def black_and_white(self, image):
        img = Image.open(image)
        pixels = img.load()
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                red = pixels[x, y][0]
                green = pixels[x, y][1]
                blue = pixels[x, y][2]
                pixels[x, y] = (red, red, red)
        img.save(image + "_bw.png")
        self.ids.image.source = image+"_bw.png"

    def pointillism(self, image):
        img = Image.open(image)
        pixels = img.load()
        canvas = Image.new("RGB", (img.size[0], img.size[1]), "white")
        for i in range(10000):
            x = random.randint(0, img.size[0] - 1)
            y = random.randint(0, img.size[1] - 1)

            size = random.randint(10, 20)
            circle = [(x, y), (x + size, y + size)]
            draw = ImageDraw.Draw(canvas)

            draw.ellipse(circle, fill=(pixels[x, y][0], pixels[x, y][1], pixels[x, y][2]))

            del draw
        canvas.save(f"{image}_pointillism.png")
        self.ids.image.source = image+"_pointillism.png"

    def line_drawing(self, image):

        img = Image.open(image)
        pixels = img.load()
        difference = 0

        for y in range(img.size[1]):
            for x in range(img.size[0]):
                for i in range(-1, 2):
                    if 1 < x < img.size[0] - 1 and 1 < y < img.size[1] - 1:

                        difference += (pixels[x, y][0] - pixels[x + i, y][0])
                        difference += (pixels[x, y][1] - pixels[x + i, y][1])
                        difference += (pixels[x, y][2] - pixels[x + i, y][2])
                        difference += (pixels[x, y][0] - pixels[x, y + 1][0])
                        difference += (pixels[x, y][1] - pixels[x + i, y + 1][1])
                        difference += (pixels[x, y][2] - pixels[x + i, y + 1][2])

                        if difference > 400:
                            # black
                            pixels[x, y] = (0, 0, 0)

                        else:
                            # white
                            pixels[x, y] = (255, 255, 255)
                            difference = 0
                    else:
                        pixels[x, y] = (255, 255, 255)
        img.save(f"{image}_line.png")
        self.ids.image.source = (self.ids.image.source+"_line.png")


PhotoEditorApp().run()
