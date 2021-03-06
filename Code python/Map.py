from random import choice, randrange as rand
from Salle import *
import sys, termios, tty, os, time	#for getch()
from random import *
from SalleEntree import *
from SalleSortie import *
from SallePiege import *
from SalleBuffet import *
from SalleCuisine import *
from SalleGardeManger import *
from SalleLevier import *
from SalleCachee import *

class Map:
    def __init__(self):
        self.__tailleX = 0
        self.__tailleY = 0
        self.__positionX = 0
        self.__positionY = 0
        self.__salleEntree = 0
        self.__levierActive = False
        
    def getPositionX(self):
        return self.__positionX

    def getPositionY(self):
        return self.__positionY


    def genererMap(self, tailleX, tailleY):
        self.__tailleX = tailleX
        self.__tailleY = tailleY

        ##
        # Dimensions du labyrinthe
        self.width = self.__tailleX
        self.height = self.__tailleY

        ##
        # Constantes servant à décrire les directions des passages
        self.N, self.S, self.E, self.W = 1, 2, 4, 8
        self.IN = 0x10
        self.FRONTIER = 0x20
        self.OPPOSITE = {self.E: self.W, self.W: self.E, self.S: self.N, self.N: self.S}

        ##
        # Structures de données
        self.__grid = [([0] * self.width) for _ in range(self.height)]
        self.__salles = [([0] * self.width) for _ in range(self.height)]
        self.frontier = set()
        ##
        # Exécution du script
        from sys import argv

        if len(argv) == 3:
            self.width, self.height = map(int, argv[1:])
            self.__grid = [[0] * self.width for _ in range(self.height)]
            self.__salles = [([0] * self.width) for _ in range(self.height)]

        self.creerSalle()

        self.mark(rand(self.width), rand(self.height))
        while self.frontier:
            ##SalleCachee
            # Choix d'un voisin à la frontière
            x, y = choice(list(self.frontier))
            self.frontier.remove((x, y))
            nx, ny = choice(list(self.neighbors(x, y)))

            ##
            # Création d'un passage
            dir = self.direction(x, y, nx, ny)
            self.__grid[y][x] |= dir
            self.__grid[ny][nx] |= self.OPPOSITE[dir]

            self.mark(x, y)

            ## DEBUG :
            #print("frontier =", self.frontier)
            #print("(%d, %d) -> (%d, %d)" % (x, y, nx, ny))
            #self.display_maze()
            #input("Appuyez sur Entree pour continuer")

            #self.display_maze()
        #print("générer map")
        self.createSalleEvent()
        self.creationFrontiereSalle()
        ##
        # Méthodes utilitaires

    def creerSalle(self):
        for x in range(self.width):
            for y in range(self.height):
                self.__salles[x][y] = Salle(False,x,y)


    def add_frontier(self, x, y):
        if (x >= 0 and y >= 0 and y < len(self.__grid) and x < len(self.__grid[y]) and self.__grid[y][x] == 0):
            self.__grid[y][x] |= self.FRONTIER
            self.frontier.add((x, y))

    def mark(self, x, y):
        self.__grid[y][x] |= self.IN
        self.add_frontier(x - 1, y)
        self.add_frontier(x + 1, y)
        self.add_frontier(x, y - 1)
        self.add_frontier(x, y + 1)

    def neighbors(self, x, y):
        if x > 0 and (self.__grid[y][x - 1] & self.IN):
            yield (x - 1, y)
        if x + 1 < len(self.__grid[y]) and (self.__grid[y][x + 1] & self.IN):
            yield (x + 1, y)
        if y > 0 and (self.__grid[y - 1][x] & self.IN):
            yield (x, y - 1)
        if y + 1 < len(self.__grid) and (self.__grid[y + 1][x] & self.IN):
            yield (x, y + 1)

    def direction(self, fx, fy, tx, ty):
        return {(fx < tx): self.E,
                (fx > tx):self. W,
                (fy < ty): self.S,
                (fy > ty): self.N}[True]

    def is_empty(self, cell):
        return cell == 0 or cell == self.FRONTIER

    def creationFrontiereSalle(self):
        for y, row in enumerate(self.__grid):
            for x, cell in enumerate(row):
                if (cell & self.E):
                    self.__salles[x][y].setSalleDoite(self.__salles[x+1][y])
                    #print("on peut aller a doite de : "+str(x) + " " + str(y))
                if (cell & self.N):
                    self.__salles[x][y].setSalleHaut(self.__salles[x][y - 1])
                    #print("on peut aller en haut de : " + str(x) + " " + str(y))
                if (cell & self.S):
                    self.__salles[x][y].setSalleBas(self.__salles[x][y + 1])
                    #print("on peut aller en bas de : " + str(x) + " " + str(y))
                if (cell & self.W):
                    self.__salles[x][y].setSalleGauche(self.__salles[x-1][y])
                    #print("on peut aller a gauche de : " + str(x) + " " + str(y))

    def display_maze(self):
        print("Vous etes en "+str(self.__positionX)+":"+str(self.__positionY))
        sys.stdout.write("  ")
        for i in range(self.__tailleX):
            sys.stdout.write(" "+str(i))
        print()
        print('   ' + '_' * (len(self.__grid[0]) * 2 - 1))
        for y, row in enumerate(self.__grid):
            line = str(y)+" |"
            for x, cell in enumerate(row):
                # Dessin du mur ou du passage Sud
                if self.is_empty(cell) and y + 1 < len(self.__grid) and self.is_empty(self.__grid[y + 1][x]):
                    line += ' '
                else:
                    line += ' ' if cell & self.S else '_'

                # Dessin du mur ou du passage Est
                if self.is_empty(cell) and x + 1 < len(row) and self.is_empty(row[x + 1]):
                    if y + 1 < len(self.__grid) and (self.is_empty(self.__grid[y + 1][x]) or
                                              self.is_empty(self.__grid[y + 1][x + 1])):
                        line += ' '
                    else:
                        line += '_'
                elif cell & self.E:
                    line += ' ' if (cell | row[x + 1]) &self. S else '_'
                else:
                    line += '|'
            print(line)

    def createSalleEvent(self):
        fichier_debug = open("debug.txt", "w")
        x = randint(0, self.__tailleX-1)
        y = randint(0, self.__tailleY-1)
        self.__salles[x][y] = SalleEntree(0,x,y, self.__salles[x][y].getSalleDroite(), self.__salles[x][y].getSalleGauche(), self.__salles[x][y].getSalleHaut(), self.__salles[x][y].getSalleBas())    #et bim une salle entrée
        self.__positionX = x
        self.__positionY = y
        self.__salleEntree = self.__salles[x][y]
        fichier_debug.write("entrée : "+str(self.__salleEntree.getX())+" "+str(self.__salleEntree.getY())+"\n")
        ok = False
        while ok == False:  #on va essayer de mettre la sortie à plus d'une case d'écart de l'entrée
            x = randint(0, self.__tailleX-1)
            y = randint(0, self.__tailleY-1)
            if(abs(self.__salleEntree.getX()-x)>1 and abs(self.__salleEntree.getY()-y)>1):
                self.__salles[x][y] = SalleSortie(0,x,y,self, self.__salles[x][y].getSalleDroite(), self.__salles[x][y].getSalleGauche(), self.__salles[x][y].getSalleHaut(), self.__salles[x][y].getSalleBas())
                ok = True
                fichier_debug.write("sortie : "+str(x)+" "+str(y)+"\n")
        ok = False
        while ok == False:  #on va placer la salle piege, de preference sur une salle vide
            x = randint(0, self.__tailleX-1)
            y = randint(0, self.__tailleY-1)
            if(self.recupererSalle(x,y).getSalleVide()):
                self.__salles[x][y] = SallePiege(0,x,y, self.__salles[x][y].getSalleDroite(), self.__salles[x][y].getSalleGauche(), self.__salles[x][y].getSalleHaut(), self.__salles[x][y].getSalleBas())
                ok = True
                fichier_debug.write("salle piege : "+str(x)+" "+str(y)+"\n")
        ok = False
        while ok == False:  #on va placer la salle buffet, de preference sur une salle vide
            x = randint(0, self.__tailleX-1)
            y = randint(0, self.__tailleY-1)
            if(self.recupererSalle(x,y).getSalleVide()):
                self.__salles[x][y] = SalleBuffet(0,x,y, self.__salles[x][y].getSalleDroite(), self.__salles[x][y].getSalleGauche(), self.__salles[x][y].getSalleHaut(), self.__salles[x][y].getSalleBas())
                ok = True
                fichier_debug.write("salle buffet : "+str(x)+" "+str(y)+"\n")
        ok = False
        while ok == False:  #on va placer la salle cuisine, de preference sur une salle vide
            x = randint(0, self.__tailleX-1)
            y = randint(0, self.__tailleY-1)
            if(self.recupererSalle(x,y).getSalleVide()):
                self.__salles[x][y] = SalleCuisine(0,x,y, self.__salles[x][y].getSalleDroite(), self.__salles[x][y].getSalleGauche(), self.__salles[x][y].getSalleHaut(), self.__salles[x][y].getSalleBas())
                ok = True
                fichier_debug.write("salle cuisine : "+str(x)+" "+str(y)+"\n")
        ok = False
        while ok == False:  #on va placer le garde à manger, de preference sur une salle vide
            x = randint(0, self.__tailleX-1)
            y = randint(0, self.__tailleY-1)
            if(self.recupererSalle(x,y).getSalleVide()):
                self.__salles[x][y] = SalleGardeManger(0,x,y, self.__salles[x][y].getSalleDroite(), self.__salles[x][y].getSalleGauche(), self.__salles[x][y].getSalleHaut(), self.__salles[x][y].getSalleBas())
                ok = True
                fichier_debug.write("garde manger : "+str(x)+" "+str(y)+"\n")
        ok = False
        while ok == False:  #on va placer la salle levier, de preference sur une salle vide
            x = randint(0, self.__tailleX-1)
            y = randint(0, self.__tailleY-1)
            if(self.recupererSalle(x,y).getSalleVide()):
                self.__salles[x][y] = SalleLevier(0,self, x,y, self.__salles[x][y].getSalleDroite(), self.__salles[x][y].getSalleGauche(), self.__salles[x][y].getSalleHaut(), self.__salles[x][y].getSalleBas())
                ok = True
                fichier_debug.write("salle levier : "+str(x)+" "+str(y)+"\n")
        ok = False
        while ok == False:  #on va placer la salle cachée, de preference sur une salle vide
            x = randint(0, self.__tailleX-1)
            y = randint(0, self.__tailleY-1)
            if(self.recupererSalle(x,y).getSalleVide()):
                self.__salles[x][y] = SalleCache(0,self,x,y, self.__salles[x][y].getSalleDroite(), self.__salles[x][y].getSalleGauche(), self.__salles[x][y].getSalleHaut(), self.__salles[x][y].getSalleBas())
                ok = True
                fichier_debug.write("salle cachée : "+str(x)+" "+str(y)+"\n")
        fichier_debug.close()
    
    def recupererSalle(self, x, y):
        return self.__salles[x][y]

    def recupererSalleActuelle(self):
        return self.__salles[self.getPositionX()][self.getPositionY()]

    def seDeplacer(self, saisie):
        haut = 0
        bas = 0
        droite = 0
        gauche = 0
        if (self.__salles[self.__positionX][self.__positionY].getSalleHaut()!= None):
            haut=1
        if (self.__salles[self.__positionX][self.__positionY].getSalleDroite()!= None):
            droite=1
        if (self.__salles[self.__positionX][self.__positionY].getSalleGauche()!= None):
            gauche=1
        if (self.__salles[self.__positionX][self.__positionY].getSalleBas()!= None):
            bas=1

        if(saisie not in ('z','q','s','d')): #z,q,s,d
            return False
        if((saisie == 'z') and haut):
            self.__positionY-=1
            return True
        elif ((saisie == 's') and bas):
            self.__positionY += 1
            return True
        elif ((saisie == 'q') and gauche):
            self.__positionX -= 1
            return True
        elif ((saisie == 'd') and droite):
            self.__positionX += 1
            return True
        else :
            print("Impossible d'aller par là...")
            return False
            
    def declancherEvent(self):
        return self.__salles[self.__positionX][self.__positionY].declancherEvenement()
    
    def setLevierActive(self, levierActiver):
        self.__levierActive = levierActiver

    def getLevierActive(self):
        return self.__levierActive 
    
    def getch(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
     
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
