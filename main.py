# -*- coding: UTF-8 -*-

# Pygame-Modul importieren.
import pygame
import random

# Überprüfen, ob die optionalen Text- und Sound-Module geladen werden konnten.
if not pygame.font: print('Fehler pygame.font Modul konnte nicht geladen werden!')
if not pygame.mixer: print('Fehler pygame.mixer Modul konnte nicht geladen werden!')

# Hilfsfunktion, um ein Bild zu laden:
def load_image(myImage, colorkey=None):
    # Pygame das Bild laden lassen.
    image = pygame.image.load(myImage)

    # Das Pixelformat der Surface an den Bildschirm (genauer: die screen-Surface) anpassen.
    # Dabei die passende Funktion verwenden, je nach dem, ob wir ein Bild mit Alpha-Kanal haben oder nicht.
    if image.get_alpha() is None:
        image = image.convert()
    else:
        image = image.convert_alpha()

    # Colorkey des Bildes setzen, falls nicht None.
    # Bei -1 den Pixel im Bild an Position (0, 0) als Colorkey verwenden.
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)

    return image

def main():
    # Initialisieren aller Pygame-Module und
    # Fenster erstellen (wir bekommen eine Surface, die den Bildschirm repräsentiert).
    pygame.init()
    screen = pygame.display.set_mode((800, 700))

    # Titel des Fensters setzen, Mauszeiger nicht verstecken und Tastendrücke wiederholt senden.
    pygame.display.set_caption("Das grosse HAW-Spiel")
    pygame.mouse.set_visible(1)
    pygame.key.set_repeat(1, 30)

    image = load_image("Fabi.jpeg")
    screen.blit(image, (40,-287))
    # Clock-Objekt erstellen, das wir benötigen, um die Framerate zu begrenzen.
    clock = pygame.time.Clock()

    # Die Schleife, und damit unser Spiel, läuft solange running == True.
    running = True
    while running:
        # Framerate auf 30 Frames pro Sekunde beschränken.
        # Pygame wartet, falls das Programm schneller läuft.
        clock.tick(30)

        # screen-Surface mit Schwarz (RGB = 0, 0, 0) füllen.
        #screen.fill((0, 255, 0))

        # Alle aufgelaufenen Events holen und abarbeiten.
        for event in pygame.event.get():
            # Spiel beenden, wenn wir ein QUIT-Event finden.
            if event.type == pygame.QUIT:
                running = False

            # Wir interessieren uns auch für "Taste gedrückt"-Events.
            if event.type == pygame.KEYDOWN:
                # Wenn Escape gedrückt wird, posten wir ein QUIT-Event in Pygames Event-Warteschlange.
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

            # Inhalt von screen anzeigen.
            pygame.display.flip()


# Überprüfen, ob dieses Modul als Programm läuft und nicht in einem anderen Modul importiert wird.
if __name__ == '__main__':
    # Unsere Main-Funktion aufrufen.
    main()

# Speichert die Daten eines Tile-Typs:
class TileType(object):
    # Im Konstruktor speichern wir den Namen
    # und erstellen das Rect (den Bereich) dieses Typs auf der Tileset-Grafik.
    def __init__(self, name, start_x, start_y, width, height):
        self.name = name
        self.rect = pygame.rect.Rect(start_x, start_y, width, height)

# Verwaltet die Tileset Grafik und eine Liste mit Tile-Typen.
class Tileset(object):
    # Im Konstruktor laden wir die Grafik
    # und erstellen ein leeres Dictionary für die Tile-Typen.
    def __init__(self, image, colorkey, tile_width, tile_height):
        self.image = Utils.load_image(image, colorkey)
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.tile_types = dict()

    # Neuen Tile-Typ hinzufügen.
    def add_tile(self, name, start_x, start_y):
        self.tile_types[name] = TileType.TileType(name, start_x, start_y, self.tile_width, self.tile_height)

    # Versuchen, einen Tile-Type über seinen Name in der Liste zu finden.
    # Falls der Name nicht existiert, geben wir None zurück.
    def get_tile(self, name):
        try:
            return self.tile_types[name]
        except KeyError:
            return

# Die Tilemap Klasse verwaltet die Tile-Daten, die das Aussehen der Karte beschreiben.
class Tilemap(object):
    def __init__(self):
        # Wir erstellen ein neues Tileset.
        # Hier im Tutorial fügen wir manuell vier Tile-Typen hinzu.
        self.tileset = Tileset.Tileset("tileset.png", (255, 0, 255), 32, 32)
        self.tileset.add_tile("grass", 0, 0)
        self.tileset.add_tile("mud", 32, 0)
        self.tileset.add_tile("water", 64, 0)
        self.tileset.add_tile("block", 0, 32)

        # Festlegen der Startposition der Kamera. Hier (0, 0).
        self.camera_x = 0
        self.camera_y = 0

        # Die Größe der Maps in Tiles.
        self.width = 30
        self.height = 25

        # Erstellen einer leeren Liste für die Tile Daten.
        self.tiles = list()

        # Manuelles Befüllen der Tile-Liste:
        # Jedes Feld bekommt ein zufälliges Tile zugewiesen.
        for i in range(0, self.height):
            self.tiles.append(list())
            for j in range(0, self.width):
                x = random.randint(0, 4)
                if x == 0:
                    self.tiles[i].append("grass")
                elif x == 1:
                    self.tiles[i].append("water")
                elif x == 2:
                    self.tiles[i].append("mud")
                else:
                    self.tiles[i].append("block")


    # Hier rendern wir den sichtbaren Teil der Karte.
    def render(self, screen):
        # Zeilenweise durch die Tiles durchgehen.
        for y in range(0, int(screen.get_height() / self.tileset.tile_height) + 1):
            # Die Kamera Position mit einbeziehen.
            ty = y + self.camera_y
            if ty >= self.height or ty < 0:
                continue
            # Die aktuelle Zeile zum einfacheren Zugriff speichern.
            line = self.tiles[ty]
            # Und jetzt spaltenweise die Tiles rendern.
            for x in range(0, int(screen.get_width() / self.tileset.tile_width) + 1):
                # Auch hier müssen wir die Kamera beachten.
                tx = x + self.camera_x
                if tx >= self.width or tx < 0:
                    continue
                # Wir versuchen, die Daten des Tiles zu bekommen.
                tilename = line[tx]
                tile = self.tileset.get_tile(tilename)
                # Falls das nicht fehlschlägt können wir das Tile auf die screen-Surface blitten.
                if tile is not None:
                    screen.blit(self.tileset.image, (x * self.tileset.tile_width, y * self.tileset.tile_height), tile.rect)


    # Tastendrücke verarbeiten:
    def handle_input(self, key):
        # Pfeiltaste links oder rechts erhöht bzw. verringert die x-Position der Kamera.
        if key == pygame.K_LEFT:
            self.camera_x += 1
        if key == pygame.K_RIGHT:
            self.camera_x -= 1

        # Und das gleiche nochmal für die y-Position.
        if key == pygame.K_UP:
            self.camera_y += 1
        if key == pygame.K_DOWN:
            self.camera_y -= 1








