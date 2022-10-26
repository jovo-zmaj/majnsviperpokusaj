import pygame, sys
import os
from random import randint

pygame.init()
pygame.display.set_caption('mine glupe')

BELA = (255, 255, 255)

FPS = 30


class Mine:
    matb = []  #bombe i br
    matv = []  #vidljivost
    matp = []  #za pipanje
    vel = []  #vel x y
    brb = 0
    velsl = 0  # velicina slicice
    DUGME = [pygame.image.load(os.path.join('slicice', 'dugme2.png'))]
    EKRAN = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    velE = []  # velicina ekrana
    BOMBE = []
    BOMBA = pygame.image.load(os.path.join('slicice', 'bomba.png'))
    brv = 0  #broj vidljivih
    bru = 0  #broj ukupno

    def praviMat(self):
        self.matb = []
        self.matv = []
        self.matp = []

        for i in range(self.vel[0]):
            a = []
            for j in range(self.vel[1]):
                a.append(0)
            self.matv.append(a)

        for i in range(self.vel[0] + 2):
            a = []
            for j in range(self.vel[1] + 2):
                a.append(0)
            self.matb.append(a)

        for i in range(self.vel[0]):
            a = []
            for j in range(self.vel[1]):
                a.append(
                    pygame.Rect(i * self.velsl, j * self.velsl, self.velsl,
                                self.velsl))
            self.matp.append(a)

    def bombiraj(self):
        bombe = self.brb
        while bombe > 0:
            x = randint(1, self.vel[0])
            y = randint(1, self.vel[1])
            if self.matb[x][y] < 69:
                self.matb[x][y] = 69
                bombe -= 1

        for i in range(1, self.vel[0] + 1):
            for j in range(1, self.vel[1] + 1):
                if (self.matb[i][j] > 68):
                    self.matb[i - 1][j - 1] += 1
                    self.matb[i - 1][j] += 1
                    self.matb[i - 1][j + 1] += 1
                    self.matb[i][j - 1] += 1
                    self.matb[i + 1][j - 1] += 1
                    self.matb[i][j + 1] += 1
                    self.matb[i + 1][j + 1] += 1
                    self.matb[i + 1][j] += 1

    def crtaj(self):
        for i in range(self.vel[0]):
            for j in range(self.vel[1]):
                if self.matv[i][j] == 0:
                    self.EKRAN.blit(self.DUGME[0],
                                    (i * self.velsl, j * self.velsl))
                elif self.matv[i][j] == 2:
                    self.EKRAN.blit(self.DUGME[1],
                                    (i * self.velsl, j * self.velsl))
                else:
                    if self.matb[i + 1][j + 1] < 69:
                        self.EKRAN.blit(self.BOMBE[self.matb[i + 1][j + 1]],
                                        (i * self.velsl, j * self.velsl))

        pygame.display.update()

    def pravidugmad(self):
        self.BOMBE.append(
            pygame.transform.scale(
                pygame.image.load(os.path.join('slicice',
                                               'dugme_prazno3.png')),
                (self.velsl, self.velsl)))

        for i in range(1, 8):
            self.BOMBE.append(
                pygame.transform.scale(
                    pygame.image.load(
                        os.path.join('slicice',
                                     str(i) + str(i) + str(i) + '.png')),
                    (self.velsl, self.velsl)))

    def rekurzijaNule(self, i, j):
        if i < 1 or j < 1 or i > self.vel[0] or j > self.vel[1] or self.matv[
                i - 1][j - 1] == 1 or self.matb[i][j] > 69:
            return

        self.matv[i - 1][j - 1] = 1
        self.brv += 1
        if self.matb[i][j] == 0:
            self.rekurzijaNule(i - 1, j)
            self.rekurzijaNule(i + 1, j)
            self.rekurzijaNule(i, j - 1)
            self.rekurzijaNule(i, j + 1)

            self.rekurzijaNule(i - 1, j - 1)
            self.rekurzijaNule(i + 1, j + 1)
            self.rekurzijaNule(i + 1, j - 1)
            self.rekurzijaNule(i - 1, j + 1)

    def razmisljaj(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i in range(self.vel[0]):
                    for j in range(self.vel[1]):
                        if self.matp[i][j].collidepoint(
                                pos) and event.button == 1:
                            if self.matb[i + 1][
                                    j + 1] > 68 and self.matv[i][j] != 2:
                                self.kraj()
                            else:
                                if self.matv[i][j] != 2:
                                    if self.matb[i + 1][j + 1] == 0:
                                        self.rekurzijaNule(i + 1, j + 1)
                                    else:
                                        self.matv[i][j] = 1
                                        self.brv += 1
                        elif self.matp[i][j].collidepoint(
                                pos) and event.button == 3:
                            if self.matv[i][j] == 0:
                                self.matv[i][j] = 2
                            elif self.matv[i][j] == 2:
                                self.matv[i][j] = 0

        if self.brv >= self.bru - self.brb:
            self.kraj()

    def kraj(self):
        for i in range(self.vel[0]):
            for j in range(self.vel[1]):
                if self.matb[i + 1][j + 1] > 68:
                    self.EKRAN.blit(self.BOMBA,
                                    (i * self.velsl, j * self.velsl))
        pygame.display.update()

        vozi = True
        while vozi:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    vozi = False

        self.brv = 0

        self.praviMat()
        self.bombiraj()
        self.pravidugmad()

        self.brz = 0

    def __init__(self, x, y, proc, velsl):
        self.vel.append(x)  #x
        self.vel.append(y)  #y
        self.brb = x * y / 100 * proc

        self.velsl = velsl

        self.DUGME[0] = pygame.transform.scale(self.DUGME[0],
                                               (self.velsl, self.velsl))

        self.DUGME.append(
            pygame.transform.scale(
                pygame.image.load(os.path.join('slicice', 'zastava2.png')),
                (self.velsl, self.velsl)))

        self.velE.append(self.velsl * self.vel[0])  #x ek
        self.velE.append(self.velsl * self.vel[1])  #y ek

        self.EKRAN = pygame.display.set_mode((self.velE[0], self.velE[1]))

        self.BOMBA = pygame.transform.scale(self.BOMBA,
                                            (self.velsl, self.velsl))

        self.brv = 0
        self.bru = x * y

        self.praviMat()

        self.bombiraj()

        self.pravidugmad()


def main():
    mine = Mine(10, 8, 8, 25)

    clock = pygame.time.Clock()

    while True:
        clock.tick(FPS)
        mine.razmisljaj()
        mine.crtaj()


main()
pygame.quit()
sys.exit()
