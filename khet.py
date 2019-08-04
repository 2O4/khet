import pygame
from pygame import *
import time


# ==================== INITIALISATION OF THE BOARD =======
def khetBoardIni(n, p):
    khetBoard = [0] * n
    for x in range(0, n):
        khetBoard[x] = [0] * p
    for x in range(0, n):
        for y in range(0, p):
            khetBoard[x][y] = [0] * 3
    return khetBoard


# =loading from save file=
def loadBoard(file):  # load board from file
    khetBoard = khetBoardIni(8, 10)
    map = open("saves\\" + file + ".txt", "r")
    for x in range(0, 80):
        k = map.readline()
        for y in k:
            if k[3] != "0":
                if k[3] == "n":
                    rot = "north"
                elif k[3] == "s":
                    rot = "south"
                elif k[3] == "w":
                    rot = "west"
                elif k[3] == "e":
                    rot = "east"
            else:
                rot = 0

            if k[4] != "0":
                if k[5] == "n":
                    pi = "anubis"
                elif k[5] == "p":
                    pi = "sphinx"
                elif k[5] == "c":
                    pi = "scarab"
                elif k[5] == "h":
                    pi = "pharaoh"
                elif k[5] == "y":
                    pi = "pyramid"
            else:
                pi = 0
            khetBoard[int(k[0])][int(k[1])] = [int(k[2]), rot, pi]
    return khetBoard


# = saving the board =
def saveBoard(khetBoard, file):
    map = open("saves\\" + file + ".txt", "w")
    for x in range(0, 8):
        for y in range(
            0, 10
        ):  # exemple output : 062sanubis correspond a : case [0][6], joueur 2, south, anubis
            map.write(
                str(x)
                + str(y)
                + str(khetBoard[x][y][0])[0]
                + str(khetBoard[x][y][1])[0]
                + str(khetBoard[x][y][2])
                + "\n"
            )


# ==================== INITIALISATION OF THE BOARD =======


# ==================== CONSOLE DISPLAY ===================
def display(
    khetBoard, n, p
):  # we made a console display to debug, and also to have a better view of the khetBoard
    print(" u\\v  ", sep="", end="")
    for x in range(0, p):
        if x <= 9:
            print("[  ", x, "] ", sep="", end="")
        else:
            print("[ ", x, "] ", sep="", end="")
    print()
    for x in range(0, n):
        if x <= 9:
            print("[  ", x, "] ", sep="", end="")
        else:
            print("[ ", x, "] ", sep="", end="")
        for y in range(0, p):
            print("[", end="")
            for z in range(0, 3):
                print(khetBoard[x][y][z], end="")
            print("]", end=" ")
        print()
    print("[xyz] x=player(color); y=rotation; z=type")


# ==================== CONSOLE DISPLAY ===================


# ==================== PLAYER TURN =======================
def selectionPossible(khetBoard, n, p, u, v, player):
    if 0 <= u and u <= (n - 1) and 0 <= v and v <= (p - 1):
        if khetBoard[u][v][0] == player:
            return True
    return False


# = ROTATION =
def rotationRight(rot):
    if rot == "south":
        return "west"
    elif rot == "north":
        return "east"
    elif rot == "east":
        return "south"
    elif rot == "west":
        return "north"


def rotationLeft(rot):
    if rot == "south":
        return "east"
    elif rot == "north":
        return "west"
    elif rot == "east":
        return "north"
    elif rot == "west":
        return "south"


def rotationPossible(khetBoard, n, p, u, v, rotation):
    if (
        (
            rotation == "north"
            or rotation == "south"
            or rotation == "east"
            or rotation == "west"
        )
        and khetBoard[u][v][1] != rotation
        and (
            (
                (khetBoard[u][v][1] == "north" or khetBoard[u][v][1] == "south")
                and (rotation == "east" or rotation == "west")
            )
            or (
                (khetBoard[u][v][1] == "east" or khetBoard[u][v][1] == "west")
                and (rotation == "north" or rotation == "south")
            )
        )
    ):  # and (khetBoard[u][v][2]=='sphinx' and((rotation == 'north' and u-1>=0)or(rotation == 'south' and u+1<=n-1)or(rotation == 'west' and v-1>=0)or(rotation == 'east' and v+1<=p-1)))
        if khetBoard[u][v][2] == "sphinx":
            if (
                (rotation == "north" and u - 1 >= 0)
                or (rotation == "south" and u + 1 <= n - 1)
                or (rotation == "west" and v - 1 >= 0)
                or (rotation == "east" and v + 1 <= p - 1)
            ):
                return True
            else:
                return False
        return True
    return False


def rotation(khetBoard, u, v, rotation):
    khetBoard[u][v][1] = rotation
    return khetBoard


# = MOVE =
def movementPossible(khetBoard, n, p, player, u, v, w, x):
    if ((0 <= w <= n - 1) and (0 <= x <= p - 1)) and not (
        (
            player == 1
            and (x == 0 or (w == 0 and x == p - 2) or (w == n - 1 and x == p - 2))
        )
        or (
            player == 2
            and (x == p - 1 or (w == 0 and x == 1) or (w == n - 1 and x == 1))
        )
    ):
        if (
            (
                ((w == u + 1) or (w == u) or (w == u - 1))
                and ((x == v + 1) or (x == v) or (x == v - 1))
            )
            and ((w != u) or (x != v))
            and (
                (khetBoard[w][x][0] == 0)
                or (
                    khetBoard[u][v][2] == "scarab"
                    and (
                        khetBoard[w][x][2] == "pyramid"
                        or khetBoard[w][x][2] == "anubis"
                    )
                )
            )
            and khetBoard[u][v][2] != "sphinx"
        ):
            return True
    return False


def movement(khetBoard, u, v, w, x):
    if khetBoard[u][v][2] == "scarab" and (
        khetBoard[w][x][2] == "pyramid" or khetBoard[w][x][2] == "anubis"
    ):
        khetBoard[w][x], khetBoard[u][v] = khetBoard[u][v], khetBoard[w][x]
    else:
        khetBoard[w][x], khetBoard[u][v] = khetBoard[u][v], [0, 0, 0]
    return khetBoard


# ==================== PLAYER TURN =======================


# ==================== SPHINX SHOT =======================
def sphinxShotInit(khetBoard, n, p, player):
    x, y, rot = sphinxPlace(khetBoard, n, p, player)
    lazer = [x, y, rot]
    return lazer


def sphinxPlace(khetBoard, n, p, player):
    for x in range(0, n):
        for y in range(0, p):
            if khetBoard[x][y][2] == "sphinx" and khetBoard[x][y][0] == player:
                return x, y, khetBoard[x][y][1]


def lazerMovementPossible(
    khetBoard, n, p, lazer
):  # check si le lazer est toujours dans le plateau ou non, et si au prochain déplacement il sortirat du plateau ou non
    if (
        0 <= lazer[0] < n
        and 0 <= lazer[1] < p
        and (
            (lazer[2] == "north" and lazer[0] > 0)
            or (lazer[2] == "south" and lazer[0] < n - 1)
            or (lazer[2] == "west" and lazer[1] > 0)
            or (lazer[2] == "east" and lazer[1] < p - 1)
        )
    ):
        return True
    return False


def lazerMovement(khetBoard, n, p, player, lazer):
    if lazer[2] == "north":
        lazer[0] -= 1
    elif lazer[2] == "south":
        lazer[0] += 1
    elif lazer[2] == "east":
        lazer[1] += 1
    elif lazer[2] == "west":
        lazer[1] -= 1
    return lazer


def lazerHitPossible(
    khetBoard, lazer
):  # en cas d'impacte du lazer avec n'importe quel pion dans n'importe quelle orientation
    if khetBoard[lazer[0]][lazer[1]][2] != 0:
        return True
    return False


def lazerHit(
    khetBoard, player, lazer
):  # quand le lazer rentre en collision avec un pion qui ne réfléchis pas le rayon
    winner = 0
    destroy = False
    if khetBoard[lazer[0]][lazer[1]][2] == "pharaoh":  # WIN
        winner = player
    elif khetBoard[lazer[0]][lazer[1]][2] == "anubis":
        if (
            (khetBoard[lazer[0]][lazer[1]][1] == "north" and lazer[2] != "south")
            or (khetBoard[lazer[0]][lazer[1]][1] == "south" and lazer[2] != "north")
            or (khetBoard[lazer[0]][lazer[1]][1] == "east" and lazer[2] != "west")
            or (khetBoard[lazer[0]][lazer[1]][1] == "west" and lazer[2] != "east")
        ):
            khetBoard[lazer[0]][lazer[1]] = [0, 0, 0]
            destroy = True
    elif khetBoard[lazer[0]][lazer[1]][2] == "pyramid":
        khetBoard[lazer[0]][lazer[1]] = [0, 0, 0]
        destroy = True
    return khetBoard, winner, destroy


def lazerHitReflectionPossible(
    khetBoard, lazer
):
    if khetBoard[lazer[0]][lazer[1]][2] == "scarab" or (
        khetBoard[lazer[0]][lazer[1]][2] == "pyramid"
        and (
            (
                khetBoard[lazer[0]][lazer[1]][1] == "north"
                and (lazer[2] == "south" or lazer[2] == "east")
            )
            or (
                khetBoard[lazer[0]][lazer[1]][1] == "south"
                and (lazer[2] == "north" or lazer[2] == "west")
            )
            or (
                khetBoard[lazer[0]][lazer[1]][1] == "east"
                and (lazer[2] == "south" or lazer[2] == "west")
            )
            or (
                khetBoard[lazer[0]][lazer[1]][1] == "west"
                and (lazer[2] == "east" or lazer[2] == "north")
            )
        )
    ):
        return True
    return False


def lazerHitReflection(
    khetBoard, lazer
):  # If you look from the lazer dirrection, for a reflection there is only 2 ways, right or left
    if (
        lazer[2] == "west"
        and (
            (
                khetBoard[lazer[0]][lazer[1]][2] == "pyramid"
                and khetBoard[lazer[0]][lazer[1]][1] == "south"
            )
            or (
                khetBoard[lazer[0]][lazer[1]][2] == "scarab"
                and (
                    khetBoard[lazer[0]][lazer[1]][1] == "north"
                    or khetBoard[lazer[0]][lazer[1]][1] == "south"
                )
            )
        )
    ) or (
        lazer[2] == "east"
        and (
            (
                khetBoard[lazer[0]][lazer[1]][2] == "pyramid"
                and khetBoard[lazer[0]][lazer[1]][1] == "west"
            )
            or (
                khetBoard[lazer[0]][lazer[1]][2] == "scarab"
                and (
                    khetBoard[lazer[0]][lazer[1]][1] == "east"
                    or khetBoard[lazer[0]][lazer[1]][1] == "west"
                )
            )
        )
    ):
        lazer[2] = "south"
    elif (
        lazer[2] == "east"
        and (
            (
                khetBoard[lazer[0]][lazer[1]][2] == "pyramid"
                and khetBoard[lazer[0]][lazer[1]][1] == "north"
            )
            or (
                khetBoard[lazer[0]][lazer[1]][2] == "scarab"
                and (
                    khetBoard[lazer[0]][lazer[1]][1] == "north"
                    or khetBoard[lazer[0]][lazer[1]][1] == "south"
                )
            )
        )
    ) or (
        lazer[2] == "west"
        and (
            (
                khetBoard[lazer[0]][lazer[1]][2] == "pyramid"
                and khetBoard[lazer[0]][lazer[1]][1] == "east"
            )
            or (
                khetBoard[lazer[0]][lazer[1]][2] == "scarab"
                and (
                    khetBoard[lazer[0]][lazer[1]][1] == "west"
                    or khetBoard[lazer[0]][lazer[1]][1] == "east"
                )
            )
        )
    ):
        lazer[2] = "north"
    elif (
        lazer[2] == "south"
        and (
            (
                khetBoard[lazer[0]][lazer[1]][2] == "pyramid"
                and khetBoard[lazer[0]][lazer[1]][1] == "north"
            )
            or (
                khetBoard[lazer[0]][lazer[1]][2] == "scarab"
                and (
                    khetBoard[lazer[0]][lazer[1]][1] == "north"
                    or khetBoard[lazer[0]][lazer[1]][1] == "south"
                )
            )
        )
    ) or (
        lazer[2] == "north"
        and (
            (
                khetBoard[lazer[0]][lazer[1]][2] == "pyramid"
                and khetBoard[lazer[0]][lazer[1]][1] == "west"
            )
            or (
                khetBoard[lazer[0]][lazer[1]][2] == "scarab"
                and (
                    khetBoard[lazer[0]][lazer[1]][1] == "east"
                    or khetBoard[lazer[0]][lazer[1]][1] == "west"
                )
            )
        )
    ):
        lazer[2] = "west"
    elif (
        lazer[2] == "south"
        and (
            (
                khetBoard[lazer[0]][lazer[1]][2] == "pyramid"
                and khetBoard[lazer[0]][lazer[1]][1] == "east"
            )
            or (
                khetBoard[lazer[0]][lazer[1]][2] == "scarab"
                and (
                    khetBoard[lazer[0]][lazer[1]][1] == "east"
                    or khetBoard[lazer[0]][lazer[1]][1] == "west"
                )
            )
        )
    ) or (
        lazer[2] == "north"
        and (
            (
                khetBoard[lazer[0]][lazer[1]][2] == "pyramid"
                and khetBoard[lazer[0]][lazer[1]][1] == "south"
            )
            or (
                khetBoard[lazer[0]][lazer[1]][2] == "scarab"
                and (
                    khetBoard[lazer[0]][lazer[1]][1] == "north"
                    or khetBoard[lazer[0]][lazer[1]][1] == "south"
                )
            )
        )
    ):
        lazer[2] = "east"
    return lazer


# ==================== SPHINX SHOT =======================


# ==================== MAIN ==============================
def Khet():
    khetWindow, khetBoard, n, p = guiMainMenu()
    khetWindow, winner = guiKhetGameplay(khetWindow, khetBoard, n, p)
    guiEndMenu(khetWindow, winner)


def main():
    Khet()


# ==================== MAIN ==============================


# ==================== GUI MENU ==========================
def guiMainMenu():
    pygame.init()
    khetWindow = pygame.display.set_mode((1600, 900), 0, 32)
    width, height = pygame.display.get_surface().get_size()
    maplist = ["classic", "imhotep", "dynasty", "custom"]
    mapnb = 0
    n = 8
    p = 10
    poseditor = False
    guiMenuInit(khetWindow, width, height, maplist, mapnb)
    clock = pygame.time.Clock()
    while True:
        pygame.display.update()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if (
                        (width / 2) - 150 < pos[0] < (width / 2) - 150 + 300
                        and (height / 2) + 150 < pos[1] < (height / 2) + 150 + 100
                    ):  # Click on "play"
                        khetBoard = loadBoard(maplist[mapnb])
                        return khetWindow, khetBoard, n, p
                    if (
                        (width / 2) + 170 < pos[0] < (width / 2) + 270
                        and (height / 2) + 150 < pos[1] < (height / 2) + 250
                    ):  # Click on the board
                        khetBoard = loadBoard(maplist[mapnb])
                        guiKhetEditor(
                            khetBoard, n, p, khetWindow, marge, tilesize, height, width
                        )
                    if (
                        (width / 2) - 150 < pos[0] < (width / 2) - 150 + 420
                        and (height / 2) + 60 < pos[1] < (height / 2) + 130
                    ):  # Click on button to chqnge ;qp
                        mapnb = guiMenuChangeMap(
                            khetWindow, mapnb, maplist, width, height, pos
                        )
                    if (
                        40 < pos[0] < 160 and 40 < pos[1] < 80
                    ):  # Click on rules
                        guiMenuRules(khetWindow, width, height)
                        guiMenuInit(khetWindow, width, height, maplist, mapnb)
            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                guiMenuEffectButton(
                    khetWindow, pos, width, height
                )  # Hover effect on button


def guiMenuInit(khetWindow, width, height, maplist, mapnb):
    khetWindow.fill((30, 30, 30))
    buttoncolor = (51, 51, 51)
    textcolor = (25, 25, 25)
    guiMenuButton(
        khetWindow,
        True,
        ((width / 2) - 150, (height / 2) + 150),
        (300, 100),
        buttoncolor,
        True,
        textcolor,
        "PLAY",
        ((width / 2) - 95, (height / 2) + 150),
        65,
    )  # Button 'play'
    guiMenuButton(
        khetWindow,
        True,
        ((width / 2) + 170, (height / 2) + 150),
        (100, 100),
        buttoncolor,
        True,
        textcolor,
        "E",
        ((width / 2) + 195, (height / 2) + 150),
        65,
    )  # Button 'e' (edit)
    guiMenuButton(
        khetWindow,
        True,
        (40, 40),
        (100, 40),
        buttoncolor,
        True,
        textcolor,
        "RULES",
        (44, 42),
        25,
    )  # Button 'rules'

    guiMenuButton(
        khetWindow,
        True,
        ((width / 2) - 150, (height / 2) + 60),
        (65, 70),
        (60, 60, 60),
        True,
        (30, 30, 30),
        "<",
        ((width / 2) - 132, (height / 2) + 62),
        45,
    )  # Button '<'
    guiMenuButton(
        khetWindow,
        True,
        ((width / 2) + 205, (height / 2) + 60),
        (65, 70),
        (60, 60, 60),
        True,
        (30, 30, 30),
        ">",
        ((width / 2) + 223, (height / 2) + 62),
        45,
    )  # Button '>'

    guiMenuButton(
        khetWindow,
        True,
        ((width / 2) - 85, (height / 2) + 60),
        (290, 70),
        (51, 51, 51),
        True,
        (25, 25, 25),
        maplist[mapnb],
        ((width / 2) - 60, (height / 2) + 60),
        45,
    )  # shoz map name
    guiMenuChangeMapPreview(khetWindow, maplist[mapnb], width, height)


def guiMenuButton(
    khetWindow,
    button=True,
    buttonPos=0,
    buttonsize=0,
    buttoncolor=(51, 51, 51),
    textB=False,
    textcolor=(25, 25, 25),
    text="",
    textPos=0,
    textsize=65,
):
    if button:
        khetWindow.fill(buttoncolor, pygame.Rect((buttonPos, buttonsize)))
    if textB:
        pygame.font.init()
        arialfont = pygame.font.SysFont("Arial Black", textsize)
        khetWindow.blit(arialfont.render(text, False, textcolor), textPos)


def guiMenuChangeMap(khetWindow, mapnb, maplist, width, height, pos):
    if (
        (width / 2) - 150 < pos[0] < (width / 2) - 150 + 65
        and (height / 2) + 60 < pos[1] < (height / 2) + 130
    ):  # "<"
        if mapnb - 1 < 0:
            mapnb = len(maplist) - 1
        else:
            mapnb -= 1
    elif (
        (width / 2) + 205 < pos[0] < (width / 2) + 205 + 65
        and (height / 2) + 60 < pos[1] < (height / 2) + 130
    ):  # ">"
        if mapnb + 2 > len(maplist):
            mapnb = 0
        else:
            mapnb += 1
    guiMenuButton(
        khetWindow,
        True,
        ((width / 2) - 85, (height / 2) + 60),
        (290, 70),
        (51, 51, 51),
        True,
        (25, 25, 25),
        maplist[mapnb],
        ((width / 2) - 60, (height / 2) + 60),
        45,
    )
    guiMenuChangeMapPreview(khetWindow, maplist[mapnb], width, height)
    return mapnb


def guiMenuEffectButton(khetWindow, pos, width, height):
    flyovercolor = (69, 69, 69)
    defaultcolor = (51, 51, 51)
    textcolor = (25, 25, 25)
    pos = pygame.mouse.get_pos()
    if (
        (width / 2) + 170 < pos[0] < (width / 2) + 270
        and (height / 2) + 150 < pos[1] < (height / 2) + 250
    ):  # Button 'edit'
        guiMenuButton(
            khetWindow,
            True,
            ((width / 2) + 290, (height / 2) + 170),
            (170, 60),
            flyovercolor,
            True,
            defaultcolor,
            "editor",
            ((width / 2) + 300, (height / 2) + 165),
            45,
        )
        guiMenuButton(
            khetWindow,
            True,
            ((width / 2) + 170, (height / 2) + 150),
            (100, 100),
            flyovercolor,
            True,
            textcolor,
            "E",
            ((width / 2) + 195, (height / 2) + 150),
            65,
        )
    else:
        guiMenuButton(
            khetWindow,
            True,
            ((width / 2) + 270, (height / 2) + 170),
            (190, 60),
            (30, 30, 30),
            False,
        )
        guiMenuButton(
            khetWindow,
            True,
            ((width / 2) + 170, (height / 2) + 150),
            (100, 100),
            defaultcolor,
            True,
            textcolor,
            "E",
            ((width / 2) + 195, (height / 2) + 150),
            65,
        )
    if (
        (width / 2) - 150 < pos[0] < (width / 2) - 150 + 300
        and (height / 2) + 150 < pos[1] < (height / 2) + 150 + 100
    ):  # Button 'play'
        guiMenuButton(
            khetWindow,
            True,
            ((width / 2) - 150, (height / 2) + 150),
            (300, 100),
            flyovercolor,
            True,
            textcolor,
            "PLAY",
            ((width / 2) - 95, (height / 2) + 150),
            65,
        )
    else:
        guiMenuButton(
            khetWindow,
            True,
            ((width / 2) - 150, (height / 2) + 150),
            (300, 100),
            (51, 51, 51),
            True,
            textcolor,
            "PLAY",
            ((width / 2) - 95, (height / 2) + 150),
            65,
        )
    if (
        (width / 2) - 150 < pos[0] < (width / 2) - 150 + 65
        and (height / 2) + 60 < pos[1] < (height / 2) + 130
    ):  # "<"
        guiMenuButton(
            khetWindow,
            True,
            ((width / 2) - 150, (height / 2) + 60),
            (65, 70),
            (79, 79, 79),
            True,
            (30, 30, 30),
            "<",
            ((width / 2) - 132, (height / 2) + 62),
            45,
        )
    else:
        guiMenuButton(
            khetWindow,
            True,
            ((width / 2) - 150, (height / 2) + 60),
            (65, 70),
            (60, 60, 60),
            True,
            (30, 30, 30),
            "<",
            ((width / 2) - 132, (height / 2) + 62),
            45,
        )
    if (
        (width / 2) + 205 < pos[0] < (width / 2) + 205 + 65
        and (height / 2) + 60 < pos[1] < (height / 2) + 130
    ):  # ">"
        guiMenuButton(
            khetWindow,
            True,
            ((width / 2) + 205, (height / 2) + 60),
            (65, 70),
            (79, 79, 79),
            True,
            (30, 30, 30),
            ">",
            ((width / 2) + 223, (height / 2) + 62),
            45,
        )
    else:
        guiMenuButton(
            khetWindow,
            True,
            ((width / 2) + 205, (height / 2) + 60),
            (65, 70),
            (60, 60, 60),
            True,
            (30, 30, 30),
            ">",
            ((width / 2) + 223, (height / 2) + 62),
            45,
        )
    if 40 < pos[0] < 160 and 40 < pos[1] < 80:  # Button 'règles'
        guiMenuButton(
            khetWindow,
            True,
            (40, 40),
            (100, 40),
            flyovercolor,
            True,
            textcolor,
            "RULES",
            (44, 42),
            25,
        )
    else:
        guiMenuButton(
            khetWindow,
            True,
            (40, 40),
            (100, 40),
            defaultcolor,
            True,
            textcolor,
            "RULES",
            (44, 42),
            25,
        )


def guiMenuChangeMapPreview(khetWindow, board, width, height):  # TODO map preview image
    khetWindow.blit(
        pygame.transform.scale(
            pygame.image.load("ressources\preview\\" + board + ".png"), (600, 410)
        ),
        (int((width / 2) - 240), int((height / 2) - 380)),
    )


def guiMenuRules(khetWindow, width, height):
    page = 0
    khetWindow.blit(
        pygame.transform.scale(
            pygame.image.load("ressources\\rules\page0.png"),
            (int((width) - 300), int((height) - 100)),
        ),
        (150, 50),
    )
    clock = pygame.time.Clock()
    while True:
        pygame.display.update()
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if (
                        40 < pos[0] < 160 and 40 < pos[1] < 80
                    ):  # Click sur le bouton de règles
                        return None
                    else:
                        page = (page + 1) % 6
                        khetWindow.blit(
                            pygame.transform.scale(
                                pygame.image.load(
                                    "ressources\\rules\page" + str(page) + ".png"
                                ),
                                (int((width) - 300), int((height) - 100)),
                            ),
                            (150, 50),
                        )
                elif event.button == 3:
                    page = (page - 1) % 6
                    khetWindow.blit(
                        pygame.transform.scale(
                            pygame.image.load(
                                "ressources\\rules\page" + str(page) + ".png"
                            ),
                            (int((width) - 300), int((height) - 100)),
                        ),
                        (150, 50),
                    )


# ==================== GUI MENU ==========================


# ==================== GUI END MENU ======================
def guiEndMenu(khetWindow, winner):
    width, height = pygame.display.get_surface().get_size()
    guiEndMenuInit(khetWindow, width, height, winner)
    # khetWindow.fill((30, 30, 30))
    clock = pygame.time.Clock()
    while True:
        pygame.display.update()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (
                    event.button == 1
                ):
                    pos = pygame.mouse.get_pos()
                    if (
                        (width / 2) - 150 < pos[0] < (width / 2) - 150 + 300
                        and (height / 2) + 150 < pos[1] < (height / 2) + 150 + 100
                    ):  # click sur le bouton "menu"
                        Khet()
            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                if (width / 2) - 150 < pos[0] < (width / 2) - 150 + 300 and (
                    height / 2
                ) + 150 < pos[1] < (height / 2) + 150 + 100:
                    guiMenuButton(
                        khetWindow,
                        True,
                        ((width / 2) - 150, (height / 2) + 150),
                        (300, 100),
                        (69, 69, 69),
                        True,
                        (25, 25, 25),
                        "MENU",
                        ((width / 2) - 110, (height / 2) + 150),
                        65,
                    )
                else:
                    guiMenuButton(
                        khetWindow,
                        True,
                        ((width / 2) - 150, (height / 2) + 150),
                        (300, 100),
                        (51, 51, 51),
                        True,
                        (25, 25, 25),
                        "MENU",
                        ((width / 2) - 110, (height / 2) + 150),
                        65,
                    )


def guiEndMenuInit(khetWindow, width, height, winner):
    s = pygame.Surface((width, height))  # |
    s.set_alpha(180)
    s.fill((25, 25, 25))
    khetWindow.blit(s, (0, 0))
    # Button 'menu'
    if winner == 1:
        winnern = "winner: silver"
    else:
        winnern = "winner: red"
    guiMenuButton(
        khetWindow,
        True,
        ((width / 2) - 150, (height / 2) + 150),
        (300, 100),
        (51, 51, 51),
        True,
        (25, 25, 25),
        "MENU",
        ((width / 2) - 110, (height / 2) + 150),
        65,
    )
    guiMenuButton(
        khetWindow,
        False,
        0,
        0,
        0,
        True,
        (200, 200, 200),
        winnern,
        ((width / 2) - 250, (height / 2) - 50),
        65,
    )


# ==================== GUI END MENU ======================


# ==================== GUI GAME ==========================
def guiKhetGameplay(khetWindow, khetBoard, n, p):
    winner = 0
    player = 1
    selected = 0
    u, v, w, x = 0, 0, 0, 0
    clock = pygame.time.Clock()
    khetWindow, guiKhetBoard, tilesize, marge, height, width = guiInitKhet(
        khetWindow, n, p
    )
    guiDrawGrid(n, p, khetWindow, tilesize, marge, height, width, player)
    guiUpdateTile(khetBoard, n, p, khetWindow, tilesize, marge, height, width)
    while winner == 0:
        pygame.display.update()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                khetBoard, guiKhetBoard, u, v = guiUpdateTurn(
                    khetBoard, n, p, player, u, v, w, x, khetWindow,
                    marge, tilesize, width, height, event, guiKhetBoard,
                )
                if (guiKhetBoard == "mooved" or guiKhetBoard == "rot"):
                    khetBoard, player, guiKhetBoard, winner = guiEndTurn(
                        khetBoard, n, p, player, khetWindow,
                        tilesize, marge, height, width,
                    )
    return khetWindow, winner


def guiUpdateTurn(
    khetBoard,
    n,
    p,
    player,
    u,
    v,
    w,
    x,
    khetWindow,
    marge,
    tilesize,
    width,
    height,
    event,
    guiKhetBoard,
):
    if event.button == 1:
        rotLocal = ""
        pos = pygame.mouse.get_pos()
        y = int((pos[1] - marge) / tilesize)  # ligne
        z = int((pos[0] - (marge + width / 6.4)) / tilesize)  # colonne
        if (0 < ((pos[1] - marge) / tilesize) < n) and (
            0 < ((pos[0] - (marge + width / 6.4)) / tilesize) < p
        ):  # if (click est dans le plateau)
            if guiKhetBoard == "":  # if (aucun pion séléctionné) do (sélection de pion)
                if selectionPossible(khetBoard, n, p, y, z, player):
                    u, v = y, z
                    guiKhetBoard = "selected"
                    guiPossibleMoove(khetBoard, n, p, player, u, v, marge, width, tilesize, khetWindow)
                    guiPossibleRotation(khetBoard, n, p, u, v, khetWindow, tilesize)
            elif guiKhetBoard == "selected":
                if movementPossible(khetBoard, n, p, player, u, v, y, z):
                    w, x = y, z
                    khetBoard = movement(khetBoard, u, v, w, x)
                    guiMoovedUpdatePos(khetBoard, n, p, player, u, v, khetWindow, tilesize, marge, height, width)
                    guiUpdateRotation(khetWindow, tilesize, (20, 20, 20))
                    guiKhetBoard = "mooved"
                    # player = player%2
                else:  # déselectionner en clickant sur une cases sur laquelle le joueur ne peut pas se déplacer
                    if selectionPossible(
                        khetBoard, n, p, y, z, player
                    ):  # changement de sélection de pion
                        guiMoovedUpdatePos(khetBoard, n, p, player, u, v, khetWindow, tilesize, marge, height, width)
                        u, v = y, z
                        guiPossibleRotation(khetBoard, n, p, u, v, khetWindow, tilesize)
                        guiKhetBoard = "selected"
                        guiPossibleMoove(khetBoard, n, p, player, u, v, marge, width, tilesize, khetWindow)
                    else:  # le pion clické n'est pas sélectionnable
                        guiMoovedUpdatePos(khetBoard, n, p, player, u, v, khetWindow, tilesize, marge, height, width)
                        guiUpdateRotation(khetWindow, tilesize, (20, 20, 20))
                        guiKhetBoard = ""
                        u, v = 0, 0
        else:  # elif (click est sur le bouton de rotation)
            if guiKhetBoard == "selected":
                if (
                    45 < pos[0] < 45 + tilesize - 4
                    and 700 < pos[1] < 700 + tilesize - 4
                ):  # bouton de rotation sens inverse des aiguilles d'une montre
                    rotLocal = rotationLeft(khetBoard[u][v][1])
                if (
                    60 + tilesize < pos[0] < 60 + (tilesize * 2) - 4
                    and 700 < pos[1] < 700 + tilesize - 4
                ):  # bouton de rotation sens des aiguilles d'une montre
                    rotLocal = rotationRight(khetBoard[u][v][1])
                if rotLocal != "":
                    if rotationPossible(khetBoard, n, p, u, v, rotLocal):
                        khetBoard = rotation(khetBoard, u, v, rotLocal)
                        guiMoovedUpdatePos(khetBoard, n, p, player, u, v, khetWindow, tilesize, marge, height, width)
                        guiKhetBoard = "rot"
    elif event.button == 3:
        guiMoovedUpdatePos(
            khetBoard, n, p, player, u, v, khetWindow, tilesize, marge, height, width
        )
        guiUpdateRotation(khetWindow, tilesize, (20, 20, 20))
        guiKhetBoard = ""
        u, v = 0, 0
    return khetBoard, guiKhetBoard, u, v


def guiEndTurn(khetBoard, n, p, player, khetWindow, tilesize, marge, height, width):
    guiUpdateRotation(khetWindow, tilesize, (20, 20, 20))
    winner = 0
    lazer = sphinxShotInit(khetBoard, n, p, player)
    while lazerMovementPossible(khetBoard, n, p, lazer) == True:
        lazer = lazerMovement(khetBoard, n, p, player, lazer)
        if lazerHitPossible(khetBoard, lazer) == True:
            if lazerHitReflectionPossible(khetBoard, lazer) == True:
                guiDrawLazerCornerIn(
                    khetBoard, lazer, khetWindow, tilesize, marge, height, width
                )
                lazer = lazerHitReflection(khetBoard, lazer)
                guiDrawLazerCornerOut(
                    khetBoard, lazer, khetWindow, tilesize, marge, height, width
                )
            else:
                e = khetBoard[lazer[0]][lazer[1]]
                khetBoard, winner, destroy = lazerHit(khetBoard, player, lazer)
                if destroy:
                    guiEffectPawnDestroy(
                        khetBoard, khetWindow, tilesize, marge, height, width, lazer, e
                    )
                break
        else:
            guiDrawLazerLine(
                khetBoard, lazer, khetWindow, tilesize, marge, height, width
            )
        pygame.display.update()
        time.sleep(0.08)
    time.sleep(0.04)
    player = (player % 2) + 1
    guiDrawGrid(n, p, khetWindow, tilesize, marge, height, width, player)
    guiUpdateTile(khetBoard, n, p, khetWindow, tilesize, marge, height, width)
    guiKhetBoard = ""
    return khetBoard, player, guiKhetBoard, winner


def guiInitKhet(khetWindow, n, p):
    khetWindow.fill((30, 30, 30))
    width, height = pygame.display.get_surface().get_size()
    tilesize = width / 16
    marge = width / 32
    guiKhetBoard = ""
    # background
    guiUpdateBackground(khetWindow)
    return khetWindow, guiKhetBoard, tilesize, marge, height, width


def guiUpdateBackground(khetWindow):
    bg = pygame.image.load("ressources/board.png")
    khetWindow.blit(bg, (0, 0))


def guiDrawGrid(n, p, khetWindow, tilesize, marge, height, width, player):
    khetWindow.fill(
        (2, 2, 2),
        pygame.Rect(
            ((marge / 2) - (marge * 0.12), (marge) - (marge * 0.12)),
            (
                (width / 6.4) + ((marge * 0.12) * 2),
                (tilesize * n) + ((marge * 0.12) * 2),
            ),
        ),
    )
    khetWindow.fill(
        (2, 2, 2),
        pygame.Rect(
            (
                (width - ((width / 6.4) + marge / 2)) - (marge * 0.12),
                marge - (marge * 0.12),
            ),
            (
                (width / 6.4) + ((marge * 0.12) * 2),
                (tilesize * n) + ((marge * 0.12) * 2),
            ),
        ),
    )

    khetWindow.fill(
        (38, 38, 38),
        pygame.Rect(
            ((marge / 2) - (marge * 0.12) + 7, (marge) - (marge * 0.12) + 7),
            (
                (width / 6.4) - 14 + ((marge * 0.12) * 2),
                (tilesize * n) - 14 + ((marge * 0.12) * 2),
            ),
        ),
    )
    khetWindow.fill(
        (38, 38, 38),
        pygame.Rect(
            (
                (width - ((width / 6.4) + marge / 2)) - (marge * 0.12) + 7,
                marge - (marge * 0.12) + 7,
            ),
            (
                (width / 6.4) - 14 + ((marge * 0.12) * 2),
                (tilesize * n) - 14 + ((marge * 0.12) * 2),
            ),
        ),
    )

    guiUpdateRotation(khetWindow, tilesize, (20, 20, 20))

    guiUpdatePlayer(n, p, khetWindow, width, height, marge, tilesize, player)

    # couleur de fond du plateau
    khetWindow.fill(
        (2, 2, 2),
        pygame.Rect(
            (marge - (marge * 0.12) + width / 6.4, marge - (marge * 0.12)),
            (tilesize * p + ((marge * 0.12) * 2), tilesize * n + ((marge * 0.12) * 2)),
        ),
    )  # couleur de fond

    for x in range(0, n):  # place les carrés gris qui délimitent les cases
        for y in range(0, p):
            khetWindow.fill(
                (20, 20, 20),
                pygame.Rect(
                    (tilesize * y + marge + 2 + width / 6.4, tilesize * x + marge + 2),
                    (tilesize - 4, tilesize - 4),
                ),
            )  # création des cases (grise)


def guiUpdatePlayer(
    n, p, khetWindow, width, height, marge, tilesize, player
):  # TODO image joueur
    if player == 1:
        khetWindow.fill(
            (38, 51, 51),
            pygame.Rect(
                ((marge / 2) - (marge * 0.12) + 17, (marge) - (marge * 0.12) + 17),
                (
                    (width / 6.4) - 14 + ((marge * 0.12) * 2) - 20,
                    (tilesize * (n / 2)) - 34 + ((marge * 0.12) * 2),
                ),
            ),
        )
    else:
        khetWindow.fill(
            (128, 51, 51),
            pygame.Rect(
                ((marge / 2) - (marge * 0.12) + 17, (marge) - (marge * 0.12) + 17),
                (
                    (width / 6.4) - 14 + ((marge * 0.12) * 2) - 20,
                    (tilesize * (n / 2)) - 34 + ((marge * 0.12) * 2),
                ),
            ),
        )
    khetWindow.blit(
        pygame.transform.scale(
            pygame.image.load("ressources/image_player/player" + str(player) + ".png"),
            (
                int((width / 6.4) - 14 + ((marge * 0.12) * 2) - 26),
                int((tilesize * (n / 2)) - 40 + ((marge * 0.12) * 2)),
            ),
        ),
        ((marge / 2) - (marge * 0.12) + 20, (marge) - (marge * 0.12) + 20),
    )


def guiUpdateRotation(khetWindow, tilesize, color=(20, 20, 20), right=True, left=True):
    if right:
        khetWindow.fill(
            color,
            pygame.Rect(
                (int(60 + tilesize) - 5, 695),
                (int(tilesize - 4) + 10, int(tilesize - 4) + 10),
            ),
        )
        khetWindow.blit(
            pygame.transform.scale(
                pygame.image.load("ressources/rotation_right.png"),
                (int(tilesize - 4), int(tilesize - 4)),
            ),
            (int(60 + tilesize), 700),
        )
    if left:
        khetWindow.fill(
            color,
            pygame.Rect((40, 695), (int(tilesize - 4) + 10, int(tilesize - 4) + 10)),
        )
        khetWindow.blit(
            pygame.transform.scale(
                pygame.image.load("ressources/rotation_left.png"),
                (int(tilesize - 4), int(tilesize - 4)),
            ),
            (45, 700),
        )


def guiPossibleRotation(khetBoard, n, p, u, v, khetWindow, tilesize):
    if khetBoard[u][v][2] == "sphinx":
        right, left = False, False
        for x in range(0, 4):
            if (
                (
                    khetBoard[u][v][1] == "north"
                    and rotationPossible(khetBoard, n, p, u, v, "east")
                )
                or (
                    khetBoard[u][v][1] == "east"
                    and rotationPossible(khetBoard, n, p, u, v, "south")
                )
                or (
                    khetBoard[u][v][1] == "south"
                    and rotationPossible(khetBoard, n, p, u, v, "west")
                )
                or (
                    khetBoard[u][v][1] == "west"
                    and rotationPossible(khetBoard, n, p, u, v, "north")
                )
            ):  # rotationPossible(khetBoard,n,p,u,v,rotation)
                right = True
            if (
                (
                    khetBoard[u][v][1] == "north"
                    and rotationPossible(khetBoard, n, p, u, v, "west")
                )
                or (
                    khetBoard[u][v][1] == "east"
                    and rotationPossible(khetBoard, n, p, u, v, "north")
                )
                or (
                    khetBoard[u][v][1] == "south"
                    and rotationPossible(khetBoard, n, p, u, v, "east")
                )
                or (
                    khetBoard[u][v][1] == "west"
                    and rotationPossible(khetBoard, n, p, u, v, "south")
                )
            ):  # rotationPossible(khetBoard,n,p,u,v,rotation)
                left = True
    else:
        right, left = True, True
    guiUpdateRotation(khetWindow, tilesize, (255, 214, 51), right, left)
    guiUpdateRotation(khetWindow, tilesize, (20, 20, 20), not (right), not (left))


def guiUpdateTile(
    khetBoard, n, p, khetWindow, tilesize, marge, height, width
):
    for x in range(0, n):
        for y in range(0, p):
            guiDrawTile(khetBoard, khetWindow, tilesize, marge, height, width, x, y)


def guiDrawTile(
    khetBoard, khetWindow, tilesize, marge, height, width, x, y
):
    if khetBoard[x][y][1] == "north":  # Rotation des images
        rot = 0
    elif khetBoard[x][y][1] == "east":
        rot = 270
    elif khetBoard[x][y][1] == "south":
        rot = 180
    else:
        rot = 90

    # couleur de base du plateau de jeu
    khetWindow.fill(
        (25, 25, 25),
        pygame.Rect(
            (tilesize * y + marge + 2 + width / 6.4, tilesize * x + marge + 2),
            (tilesize - 4, tilesize - 4),
        ),
    )

    imagesize = (
        96,
        96,
    )  # 96x96 pour une résolution de 1600x900 et 116x116 pour du HD 1920x1080, nous avons opté pour du 1600x900 afin que la fenêtre rentre sur l'écran sans mode plein ecran
    listpawn = ["sphinx", "pharaoh", "scarab", "anubis", "pyramid"]
    listcolor = ["silver", "red"]
    for i in range(1, 3):
        for j in listpawn:
            if khetBoard[x][y][0] == i and khetBoard[x][y][2] == j:
                khetWindow.blit(
                    pygame.transform.rotate(
                        pygame.transform.scale(
                            pygame.image.load(
                                "ressources/Image_piece/"
                                + j
                                + "_"
                                + listcolor[i - 1]
                                + ".png"
                            ),
                            imagesize,
                        ),
                        rot,
                    ),
                    (tilesize * y + marge + 2 + width / 6.4, tilesize * x + marge + 2),
                )  # charge, tourne, redimensionne et affiche l'images du pion a la cas "[x][y]"

    # affichage des cases blocké
    n = len(khetBoard)
    p = len(khetBoard[0])
    if khetBoard[x][y][0] == 0:
        if y == 0 or (x == 0 and y == p - 2) or (x == n - 1 and y == p - 2):  # player 1
            khetWindow.fill(
                (69, 0, 0),
                pygame.Rect(
                    (tilesize * y + marge + 2 + width / 6.4, tilesize * x + marge + 2),
                    (tilesize - 4, tilesize - 4),
                ),
            )
            # khetWindow.blit(pygame.transform.scale(pygame.image.load("ressources/Image_piece/special_red.png"), imagesize), (tilesize * y + marge + 2 + width / 6.4,tilesize * x + marge + 2))  # charge, tourne, redimensionne et affiche l'image des cases interdites a la case "[x][y]"
        if y == p - 1 or (x == 0 and y == 1) or (x == n - 1 and y == 1):  # player 2
            khetWindow.fill(
                (51, 51, 51),
                pygame.Rect(
                    (tilesize * y + marge + 2 + width / 6.4, tilesize * x + marge + 2),
                    (tilesize - 4, tilesize - 4),
                ),
            )
            # khetWindow.blit(pygame.transform.scale(pygame.image.load("ressources/Image_piece/special_silver.png"), imagesize), (tilesize * y + marge + 2 + width / 6.4,tilesize * x + marge + 2))  # charge, tourne, redimensionne et affiche l'image des cases interdites a la case "[x][y]"


def guiPossibleMoove(
    khetBoard, n, p, player, u, v, marge, width, tilesize, khetWindow
):  # met en evidence les cases sur lesquelles le joueur peut faire déplacer son pion sélectionné
    for x in range(-1, 2):
        for y in range(-1, 2):
            if movementPossible(khetBoard, n, p, player, u, v, u + x, v + y):
                if player == 1:
                    colorSquare = (80, 80, 80)
                    colorTrans = (200, 200, 200)
                else:
                    colorSquare = (240, 20, 20)
                    colorTrans = (200, 80, 80)
                # filtre semi-transparent
                s = pygame.Surface((tilesize - 4, tilesize - 4))
                s.set_alpha(40)
                s.fill(colorTrans)
                khetWindow.blit(
                    s,
                    (
                        tilesize * (v + y) + marge + 2 + width / 6.4,
                        tilesize * (u + x) + marge + 2,
                    ),
                )
                # contour rouge
                k = int(
                    ((tilesize - 4) * 0.95) + 1
                )  # k correspond a 19/20 de la taille d'une case qui est (tilesize -4) le problème est que pygame ne prend que des valeurs entière pour l'affichage, or ((tilesize - 4) * 0.95) = 91.1999... et ((tilesize - 4)/20)*19 = 91.2, nous avons donc arrondi a 92 (pour la résolution 1600x900) (arrondi : le +1 a la fin et la mise en entier avec int())
                khetWindow.fill(
                    colorSquare,
                    pygame.Rect(
                        (
                            tilesize * (v + y) + marge + 2 + width / 6.4,
                            tilesize * (u + x) + marge + 2,
                        ),
                        ((tilesize - 4) / 20, tilesize - 4),
                    ),
                )
                khetWindow.fill(
                    colorSquare,
                    pygame.Rect(
                        (
                            tilesize * (v + y) + marge + 2 + width / 6.4,
                            tilesize * (u + x) + marge + 2,
                        ),
                        (tilesize - 4, (tilesize - 4) / 20),
                    ),
                )
                khetWindow.fill(
                    colorSquare,
                    pygame.Rect(
                        (
                            tilesize * (v + y) + marge + 2 + width / 6.4 + k,
                            tilesize * (u + x) + marge + 2,
                        ),
                        ((tilesize - 4) / 20, tilesize - 4),
                    ),
                )
                khetWindow.fill(
                    colorSquare,
                    pygame.Rect(
                        (
                            tilesize * (v + y) + marge + 2 + width / 6.4,
                            tilesize * (u + x) + marge + 2 + k,
                        ),
                        (tilesize - 4, (tilesize - 4) / 20),
                    ),
                )


def guiMoovedUpdatePos(
    khetBoard, n, p, player, u, v, khetWindow, tilesize, marge, height, width
):  # Enlève les cases des déplacement possible
    for x in range(-1, 2):
        for y in range(-1, 2):
            if (
                0 <= u + x < n and 0 <= v + y < p
            ):  # pour ne pas avoir sortir du tableau et donc pour ne pas afficher de cases en dehord des bordures
                guiDrawTile(
                    khetBoard, khetWindow, tilesize, marge, height, width, u + x, v + y
                )


def guiDrawLazer(
    khetWindow, xo, yo, xs, ys
):  # xo=point x d'origine, yo=point y d'origine, xs=taile (size) sur l'axe x, ys=taile (size) sur l'axe y
    guiLazer = pygame.Rect((xo, yo), (xs, ys))
    lazerColor = (255, 0, 0)
    khetWindow.fill(lazerColor, guiLazer)


def guiDrawLazerLine(
    khetBoard, lazer, khetWindow, tilesize, marge, height, width
):  # Dessine le laser lorsqu'il ne rencontre aucun obstacles
    if lazer[2] == "north" or lazer[2] == "south":  # lazer verticale
        guiDrawLazer(
            khetWindow,
            tilesize * lazer[1] + marge + width / 6.4 + 0.45 * tilesize,
            tilesize * lazer[0] + marge,
            tilesize / 10,
            tilesize,
        )
    if lazer[2] == "east" or lazer[2] == "west":  # lazer horizontal
        guiDrawLazer(
            khetWindow,
            tilesize * lazer[1] + marge + width / 6.4,
            tilesize * lazer[0] + marge + 0.45 * tilesize,
            tilesize,
            tilesize / 10,
        )


def guiDrawLazerCornerIn(
    khetBoard, lazer, khetWindow, tilesize, marge, height, width
):  # Dessine la portion entrante de l'angle du laser lors de la réflection
    if lazer[2] == "north":
        guiDrawLazer(
            khetWindow,
            tilesize * lazer[1] + marge + width / 6.4 + 0.45 * tilesize,
            tilesize * lazer[0] + marge + tilesize / 2,
            tilesize / 10,
            tilesize / 2,
        )
    if lazer[2] == "south":
        guiDrawLazer(
            khetWindow,
            tilesize * lazer[1] + marge + width / 6.4 + 0.45 * tilesize,
            tilesize * lazer[0] + marge,
            tilesize / 10,
            tilesize / 2,
        )
    if lazer[2] == "east":
        guiDrawLazer(
            khetWindow,
            tilesize * lazer[1] + marge + width / 6.4,
            tilesize * lazer[0] + marge + 0.45 * tilesize,
            tilesize / 2,
            tilesize / 10,
        )
    if lazer[2] == "west":
        guiDrawLazer(
            khetWindow,
            tilesize * lazer[1] + marge + width / 6.4 + tilesize / 2,
            tilesize * lazer[0] + marge + 0.45 * tilesize,
            tilesize / 2,
            tilesize / 10,
        )


def guiDrawLazerCornerOut(
    khetBoard, lazer, khetWindow, tilesize, marge, height, width
):  # Dessine la portion sortante de l'angle du laser lors de la réflection
    if lazer[2] == "north":
        guiDrawLazer(
            khetWindow,
            tilesize * lazer[1] + marge + width / 6.4 + 0.45 * tilesize,
            tilesize * lazer[0] + marge,
            tilesize / 10,
            tilesize / 2,
        )
    if lazer[2] == "south":
        guiDrawLazer(
            khetWindow,
            tilesize * lazer[1] + marge + width / 6.4 + 0.45 * tilesize,
            tilesize * lazer[0] + marge + tilesize / 2,
            tilesize / 10,
            tilesize / 2,
        )
    if lazer[2] == "east":
        guiDrawLazer(
            khetWindow,
            tilesize * lazer[1] + marge + width / 6.4 + tilesize / 2,
            tilesize * lazer[0] + marge + 0.45 * tilesize,
            tilesize / 2,
            tilesize / 10,
        )
    if lazer[2] == "west":
        guiDrawLazer(
            khetWindow,
            tilesize * lazer[1] + marge + width / 6.4,
            tilesize * lazer[0] + marge + 0.45 * tilesize,
            tilesize / 2,
            tilesize / 10,
        )


# ==================== GUI GAME ==========================


# ==================== GUI EFECT =========================
def guiEffectPawnDestroy(
    khetBoard, khetWindow, tilesize, marge, height, width, lazer, e
):
    x = lazer[0]
    y = lazer[1]
    timeClock = 0.1
    for a in range(0, 4):
        guiDrawTile(khetBoard, khetWindow, tilesize, marge, height, width, x, y)
        khetBoard[lazer[0]][lazer[1]] = e
        time.sleep(timeClock)
        pygame.display.update()
        guiDrawTile(khetBoard, khetWindow, tilesize, marge, height, width, x, y)
        khetBoard[lazer[0]][lazer[1]] = [0, 0, 0]
        time.sleep(timeClock)
        pygame.display.update()


# ==================== GUI EFECT =========================


# ==================== GUI EDITOR =========================
def guiKhetEditor(
    khetBoard, n, p, khetWindow, marge, tilesize, height, width
):
    clock = pygame.time.Clock()
    while True:
        pygame.display.update()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    guiEditorClick(n, p, pos, marge, tilesize, height, width)


def guiEditorClick(n, p, pos, marge, tilesize, height, width):
    if (0 < ((pos[1] - marge) / tilesize) < n) and (
        0 < ((pos[0] - (marge + width / 6.4)) / tilesize) < p
    ):
        print()


def guiEditorInit():
    pass


# ==================== GUI EDITOR =========================


main()
