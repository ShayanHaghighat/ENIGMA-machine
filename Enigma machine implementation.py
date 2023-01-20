""""
Shayan Akbari Haghighat
ENIGMA MAachine implementation with python
Winter 2023
"""
import pygame
#setiing up the game
pygame.init()
pygame.font.init()
pygame.display.set_caption("Enigma simulator")
BOLD = pygame.font.SysFont("FreeMono", 15, bold=True)
MONO = pygame.font.SysFont("FreeMono", 15)

#Globlal vars
WIDTH = 1200
HEIGHT = 675
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT), pygame.RESIZABLE)
MARGINS = {"top":100, "bottom":100, "left":50, "right":50}
GAP = 50
INPUT = ""
OUTPUT = ""
PATH = []

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class Keyboard:

    def forward(self, letter):
        signal = alphabet.find(letter)
        return signal

    def backward(self, signal):
        letter = alphabet[signal]
        return letter

    def draw(self, screen, x, y, w, h, font):
        #The rectangle
        r = pygame.Rect(x,y,w,h)
        pygame.draw.rect(screen, "white", r, width=2, border_radius=15)
        #The letters
        for i in range(26):
            letter = alphabet[i]
            letter = font.render(letter, True, "grey")
            text_box = letter.get_rect(center = (x+w/2,y+(i+1)*h/27))
            screen.blit(letter, text_box)


class Plugboard:

    def __init__(self, pairs):

        self.right = alphabet
        self.left = alphabet

        for pair in pairs:
            swapping = pair[0]
            swapped = pair[1]
            pos_swapping = self.left.find(swapping)
            pos_swapped = self.left.find(swapped)
            self.left = self.left[:pos_swapping] + swapped + self.left[pos_swapping+1:]
            self.left = self.left[:pos_swapped] + swapping + self.left[pos_swapped+1:]

    def forward(self, signal):
        letter = self.right[signal]
        signal = self.left.find(letter)
        return signal

    def backward(self, signal):
        letter = self.left[signal]
        signal = self.right.find(letter)
        return signal

    def draw(self, screen, x, y, w, h, font):
        #The rectangle
        r = pygame.Rect(x,y,w,h)
        pygame.draw.rect(screen, "white", r, width=2, border_radius=15)
        #The letters
        for i in range(26):
            #left side
            letter = self.left[i]
            letter = font.render(letter, True, "grey")
            text_box = letter.get_rect(center = (x+w/4,y+(i+1)*h/27))
            screen.blit(letter, text_box)
            #right side
            letter = self.right[i]
            letter = font.render(letter, True, "grey")
            text_box = letter.get_rect(center=(x+w*3/4,y+(i+1)*h/27))
            screen.blit(letter, text_box)



class Rotor:

    def __init__(self, wiring, notch):
        self.left = alphabet
        self.right = wiring
        self.notch = notch

    def forward(self, signal):
        letter = self.right[signal]
        signal = self.left.find(letter)
        return signal

    def backward(self, signal):
        letter = self.left[signal]
        signal = self.right.find(letter)
        return signal

    def show(self):
        print(self.left)
        print(self.right)
        print("")

    def rotate(self, n=1, forward=True):
        for i in range(n):
            if forward:
                self.left = self.left[1:] + self.left[0]
                self.right = self.right[1:] + self.right[0]
            else:
                self.left = self.left[25] + self.left[:25]
                self.right = self.right[25] + self.right[:25]

    def set_ring(self, n):
        n_notch = alphabet.find(self.notch)
        self.notch = alphabet[(n_notch - n + 1)%26]

    def rotate_to(self, letter):
        n = alphabet.find(letter)
        self.rotate(n)

    def draw(self, screen, x, y, w, h, font):
        #The rectangle
        r = pygame.Rect(x,y,w,h)
        pygame.draw.rect(screen, "white", r, width=2, border_radius=15)
        #The letters
        for i in range(26):
            #left side
            letter = self.left[i]
            letter = font.render(letter, True, "grey")
            text_box = letter.get_rect(center = (x+w/4,y+(i+1)*h/27))
            # Highlight the top letter
            if i == 0:
                pygame.draw.rect(screen, "teal", text_box, border_radius=5)
            #Highlight turn over notch
            if self.left[i] == self.notch:
                letter = font.render(self.notch, True, "#333333")
                pygame.draw.rect(screen, "white", text_box, border_radius=5)
            screen.blit(letter, text_box)
            #right side
            letter = self.right[i]
            letter = font.render(letter, True, "grey")
            text_box = letter.get_rect(center=(x+w*3/4,y+(i+1)*h/27))
            screen.blit(letter, text_box)



I = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q")
II = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E")
III = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V")
IV = Rotor("ESOVPZJAYQUIRHXLNFTGKDCMWB", "J")
V = Rotor("VZBRGITYUPSDNHLXAWMJQOFECK", "Z")

class Reflector:

    def __init__(self, wiring):
        self.left = alphabet
        self.right = wiring

    def reflect(self, signal):
        letter = self.right[signal]
        signal = self.left.find(letter)
        return signal

    def draw(self, screen, x, y, w, h, font):
        # The rectangle
        r = pygame.Rect(x, y, w, h)
        pygame.draw.rect(screen, "white", r, width=2, border_radius=15)
        # The letters
        for i in range(26):
            # left side
            letter = self.left[i]
            letter = font.render(letter, True, "grey")
            text_box = letter.get_rect(center=(x + w / 4, y + (i + 1) * h / 27))
            screen.blit(letter, text_box)
            # right side
            letter = self.right[i]
            letter = font.render(letter, True, "grey")
            text_box = letter.get_rect(center=(x + w * 3 / 4, y + (i + 1) * h / 27))
            screen.blit(letter, text_box)


class Enigma:

    def __init__(self, ref, ro1, ro2, ro3, pb, kb):
        self. ref = ref
        self.ro1 = ro1
        self.ro2 = ro2
        self.ro3 = ro3
        self.pb = pb
        self.kb = kb

    def set_rings(self, rings):
        self.ro1.set_ring(rings[0])
        self.ro2.set_ring(rings[1])
        self.ro3.set_ring(rings[2])

    def set_key(self, key):
        self.ro1.rotate_to(key[0])
        self.ro2.rotate_to(key[1])
        self.ro3.rotate_to(key[2])

    def cipher(self, letter):
        if self.ro2.left[0] == self.ro2.notch and self.ro3.left[0] == self.ro3.notch:
            self.ro1.rotate()
            self.ro2.rotate()
            self.ro3.rotate()
        elif self.ro2.left[0] == self.ro2.notch: #Double step annomally
            self.ro1.rotate()
            self.ro2.rotate()
            self.ro3.rotate()
        elif self.ro3.left[0] == self.ro3.notch:
            self.ro2.rotate()
            self.ro3.rotate()

        path = []
        signal = self.kb.forward(letter)
        path = [signal, signal]
        signal = self.pb.forward(signal)
        path.append(signal)
        path.append(signal)
        signal = self.ro3.forward(signal)
        path.append(signal)
        path.append(signal)
        signal = self.ro2.forward(signal)
        path.append(signal)
        path.append(signal)
        signal = self.ro1.forward(signal)
        path.append(signal)
        path.append(signal)
        signal = self.ref.reflect(signal)
        path.append(signal)
        path.append(signal)
        path.append(signal)
        signal = self.ro1.backward(signal)
        path.append(signal)
        path.append(signal)
        signal = self.ro2.backward(signal)
        path.append(signal)
        path.append(signal)
        signal = self.ro3.backward(signal)
        path.append(signal)
        path.append(signal)
        signal = self.pb.backward(signal)
        path.append(signal)
        path.append(signal)
        letter = self.kb.backward(signal)

        return path,letter

A = Reflector("EJMZALYXVBWFCRQUONTSPIKHGD")
B = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
C = Reflector("FVPJIAOYEDRZXWGCTKUQSBNMHL")

def draw(enigma, path, screen, width, height, margins, gap, font):
    h = height - margins["top"] - margins["bottom"]
    w = (width - margins["left"] - margins["right"] - 5 * gap) / 6
    #drawing path

    y = [margins["top"] + (signal + 1)* h /27 for signal in path]
    x = [width-margins["right"] - w/2]
    for i in [4,3,2,1,0]:  #Forward path
        x.append(margins["left"]+i*(w+gap)+3*w/4)
        x.append(margins["left"] + i * (w + gap) + w*1/4)
    x.append(margins["left"] + w *3/4)

    for i in [1,2,3,4]: #Backward path
        x.append(margins["left"]+i*(w+gap)+w/4)
        x.append(margins["left"] + i * (w + gap) + w*3/4)
    x.append(width - margins["right"] - w / 2)  # Lampboard


    if len(path) > 0:
        for i in range(1, 21):
            if i < 10:
                color = "#43aa8b"
            elif i < 12:
                color = "#f9c74f"
            else:
                color = "#e63946"
            start = (x[i-1], y[i-1])
            end = (x[i], y[i])
            pygame.draw.line(screen, color, start, end, width=5)
    # Drawing the machine
    x = margins["left"]
    y = margins["top"]

    for component in [enigma.ref, enigma.ro1, enigma.ro2, enigma.ro3, enigma.pb, enigma.kb]:
        component.draw(SCREEN, x, y, w, h, BOLD)
        x += w + gap

    #add names
    names = ["Reflector", "Left", "Middle", "Right",  "Plugboard", "Key/Lamp"]
    for i in range(6):
        x = margins["left"] + w/2 + i*(w+gap)
        title = font.render(names[i], True, "white")
        text_box = title.get_rect(center = (x, margins["top"]*0.8))
        screen.blit(title, text_box)


#Enigma settings
KB = Keyboard()
PB = Plugboard(["AR", "GK", "OX"])
ENIGMA= Enigma(A,III,II,I,PB,KB)
ENIGMA.set_key("BOQ")
ENIGMA.set_rings((1,1,1))

message = "TEST"
cipher_text = ""
for letter in message:
    cipher_text = cipher_text + ENIGMA.cipher(letter)[1]

animating=True

while animating:
    #Background
    SCREEN.fill("#333333")
    #text input
    text = BOLD.render(INPUT, True, "white")
    text_box = text.get_rect(center = (WIDTH/2,MARGINS["top"]/2 - 15))
    SCREEN.blit(text, text_box)
    # text output
    text = BOLD.render(OUTPUT, True, "grey")
    text_box = text.get_rect(center=(WIDTH / 2, MARGINS["top"] / 2 + 5 ))
    SCREEN.blit(text, text_box)
    #Info
    text = BOLD.render("Shayan A. Haghighat", True, "#9FB6CD")
    text_box = text.get_rect(center=(1100, 660))
    SCREEN.blit(text, text_box)
    text = BOLD.render("ENIGMA Machine simulator", True, "#9FB6CD")
    text_box = text.get_rect(center=(120, 660))
    SCREEN.blit(text, text_box)

    #drawing enigma
    draw(ENIGMA, PATH, SCREEN, WIDTH, HEIGHT, MARGINS, GAP, BOLD)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            animating = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                INPUT = INPUT + " "
                OUTPUT = OUTPUT + " "
            else:
                key = event.unicode
                if key in "abcdefghijklmnopqrstuvwxyz":
                    letter = key.upper()
                    INPUT = INPUT + letter
                    PATH, ciphered = ENIGMA.cipher(letter)
                    OUTPUT = OUTPUT + ciphered
