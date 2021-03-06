# -*- coding: utf-8 -*-
from Competence import *
from random import *
import time

class CompetenceAttaque(Competence):
    def __init__(self, nom, cout, description, groupe, tauxReussite, degat, degatFixe, statut):
        Competence.__init__(self,nom, cout, description, groupe, tauxReussite)
        self.__degat = degat
        self.__degatFixe = degatFixe #Faut-il prendre en compte l'attaque du perso?
        self.__statut = statut

    def activerCompetence(self, combattant, teamAllie, teamEnnemi, isIA):
        if (self.getGroupe() == 0):
            if(isIA == False):
                print("qui attaquer? (utiliser les z et q pour choisir et entrée pour selectionner)")
            rep = "0x00"
            i=0
            maxRange = len(teamEnnemi)
            if(isIA):
                i = randint(0,maxRange-1)
            else:
                while rep != "0xd": #différent de entrée
                    print(teamEnnemi[i].getNom())
                    rep = hex(ord(self.getch()))    #on récupère la touche tapé par l'utilisateur (pas besoin de faire entrée)
                    if(rep == "0x7a"):    #z
                        if(i<maxRange-1):
                            i = i+1
                        else :
                            i=0
                    if(rep == "0x73"):    #s
                        if(i>0):
                            i = i-1
                        else:
                            i = maxRange - 1
            rand = randint(0, 100) #le sort echoue?
            if rand > self.getTauxReussite():
                print("le sort echoue...")
            else: 
                if (self.__degatFixe == True):
                    degat = self.__degat
                else:
                    degat = self.__degat+combattant.getAttaque()
                teamEnnemi[i].setPV(teamEnnemi[i].getPV()-degat)
                print(teamEnnemi[i].getNom()+" perd "+str(degat)+"PV!")
                if (self.__statut != None):
                    x = randint(0, 1)
                    if (x):
                        teamEnnemi[i].ajouterStatut(self.__statut)
                        print(teamEnnemi[i].getNom() + " est maintenant " + self.__statut.getNom() + "!")
        else:   #attaque de groupe
            rand = randint(0, 100) #le sort echoue?
            if rand > self.getTauxReussite():
                print("le sort echoue...")
            else:
                for c in teamEnnemi:
                    if (self.__degatFixe == True):
                        degat = self.__degat
                    else:
                        degat = self.__degat+combattant.getAttaque()
                    c.setPV(c.getPV()-degat)
                    print(c.getNom()+" perd "+str(degat)+"PV!")
                    if (self.__statut != None):
                        x = randint(0,1)
                        if (x):
                            c.ajouterStatut(self.__statut)
                            print(c.getNom() + " est maintenant " + self.__statut.getNom() + "!")
            if(combattant.getNom()=="Boomer"):
                time.sleep(1.5)
                print("Le boomer explose dans un bain de sang immonde...")     #cas si c'est le boomer qui se fait exploser
                combattant.setPV(0)

                    
                    


