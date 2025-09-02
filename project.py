from PIL import Image
from PIL import ImageDraw
import random

#Grayscale

def load_grayscale_image(filename):
    im = Image.open(filename)
    return im.convert('L')

def load_grayscale_pixels(filename):
	if type(filename) == type('foo'):
		im = load_grayscale_image(filename)
	else:
		im = filename
	return list(im.getdata())

def load_grayscale_pixels_2d(filename):
	if type(filename) == type('foo'):
		im = load_grayscale_image(filename)
	else:
		im = filename
	w,h = im.size
	data = im.getdata()
	return [[data[y*w + x] for y in range(h)] for x in range(w)]

def new_grayscale_pixels_2d(w,h):
    return [[0 for y in range(h)] for x in range(w)]

def new_grayscale_image(w, h, pixels=None):
    im = Image.new('L', (w,h))
    if pixels is not None:
        if isinstance(pixels[0], list):
            pixels = list(zip(*pixels))
            pixels = [item for sublist in pixels for item in sublist]
        im.putdata(pixels)
    return im


#RGB

def load_rgb_image(filename):
    im = Image.open(filename)
    return im.convert('RGB')

def load_rgb_pixels_2d(filename):
    if type(filename) == type('foo'):
        im = Image.open(filename)
    else:
        im = filename
    w, h = im.size
    data = im.getdata();
    return [[data[y*w + x] for y in range(h)] for x in range(w)]

def load_rgb_pixels(filename):
    if type(filename) == type('foo'):
        im = load_rgb_image(filename)
    else:
        im = filename
    return list(im.getdata())

def new_rgb_pixels_2d(w,h):
    return [[(0,0,0) for y in range(h)] for x in range(w)]

def new_rgb_image(w, h, pixels=None):
    im = Image.new('RGB', (w,h))
    def mapInt(p):
        r,g,b = p
        return int(r), int(g), int(b)
    if pixels is not None:
        if isinstance(pixels[0], list):
            pixels = list(zip(*pixels))
            pixels = [mapInt(item) for sublist in pixels for item in sublist]
        else:
            pixels = list(map(mapInt, pixels))
        im.putdata(pixels)
    return im



#Canvas:

class Canvas:
    
    def __init__(self, img):            
        self.img = img.copy()
        self.draw = ImageDraw.Draw(self.img)
        
    def rect(self, x1,y1,x2,y2,c ,outline = None, width=0):
        self.draw.rectangle((x1,y1,x2,y2), c, outline, width)
        
    def square(self, x,y,w,c, outline=None, width=0):
        self.draw.rectangle((x,y,x+w,y+w), c, outline, width)
        
    def circle(self, x,y,r,c, outline=None):
        self.draw.ellipse((x,y,x+r,y+r),c, outline)
        
    def polygon(self, x, y, r, s, c, rot=0, outline=None, width=0):
        self.draw.regular_polygon((x,y,r),s,rot,c, outline)
        
    def show(self):
        self.img.show()
        
        
def create_canvas(img):
    return Canvas(img)

#Misc:

def pixel_average(img, x1,y1,x2,y2):
    if type(img) != type([]):
        pixels = load_rgb_pixels_2d(img)
    else:
        pixels = img
    
    sum_r, sum_g, sum_b = 0,0,0
    num_pixels = 0
    for x in range(x1,x2):
        for y in range(y1,y2):
            num_pixels += 1
            r,g,b = pixels[x][y]
            sum_r += r
            sum_g += g
            sum_b += b
    return sum_r//num_pixels, sum_g//num_pixels, sum_b//num_pixels



#Actual project

print("Welcome to the Mosaicinator")
img = load_rgb_image(input("Which image should be loaded? Please provide the exact name including the file extension and ensure that the image is in the same folder as the Python script. "))
w, h = img.size
pixels = load_rgb_pixels_2d(img)

#Define canvas
new_img = new_rgb_image(w,h)
c = Canvas(new_img)

#Color filter
color_filter = str(input("Which color filter should be applied? Enter red, green, blue or press ENTER to continue without a color filter. "))
if color_filter == "red":
    for x in range (w):
        for y in range (h):
            r,g,b = pixels[x][y]
            
            new_r = 0
            new_g = g
            new_b = b
            pixels[x][y] = (new_r,new_g,new_b)

elif color_filter == "green":
    for x in range (w):
        for y in range (h):
            r,g,b = pixels[x][y]
            
            new_r = r
            new_g = 0
            new_b = b
            pixels[x][y] = (new_r,new_g,new_b)

elif color_filter == "blue":
    for x in range (w):
        for y in range (h):
            r,g,b = pixels[x][y]
            
            new_r = r
            new_g = g
            new_b = 0
            pixels[x][y] = (new_r,new_g,new_b)

#Mosaic stone
N = int(input("How large should a mosaic stone be?"))
Z = input("Press ENTER to automatically adjust the spacing to the image resolution or enter a value to set it manually.")

if Z == "":
    M = N/3
else:
    M = int(Z)


for x in range(0,w,N):
    for y in range(0,h,N):
        r,g,b = pixels[x][y]
        c.square(x, y, N-M, (r,g,b))

new_image = new_rgb_image(w,h,pixels)
c.show()