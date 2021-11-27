#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 01:41:59 2020

@author: chendeb
"""

import http.client
import time
import numpy as np
import copy
import random
import sys
import math
import copy

CRED = '\33[31m'
CEND = '\033[0m'
CBLUE   = '\33[34m'

servergame="chendeb.free.fr"

nb_row = 6
nb_col = 12

def jouerWEB(idjeu,monid,tour,jeu,server=servergame):
    conn = http.client.HTTPConnection(server)
    req=conn.request("GET", "/Puissance6?status=JeJoue&idjeu="+idjeu+"&idjoueur="+monid+"&tour="+str(tour)+"&jeu="+str(jeu))
    r1 = conn.getresponse()
    return (r1.status, r1.reason)  

def getJeuAdv(idjeu,idAdv,tour,server=servergame):
    conn = http.client.HTTPConnection(server)
    req=conn.request("GET", "/Puissance6?status=GetJeuAdv&idjeu="+idjeu+"&idjoueur="+idAdv+"&tour="+str(tour))
    r1 = conn.getresponse()
    advJeu=None
    if(r1.status==200):
        temp=r1.read()
        print(temp)
        if(temp.decode('UTF-8')!='PASENCOREJOUE'):
            advJeu=int(temp)
    return advJeu  

def loopToGetJeuAdv( inetvalle,idjeu,idAdv,tour,server=servergame):
    advJeu=getJeuAdv(idjeu,idAdv,tour,server)
    while(advJeu==None):
        time.sleep(inetvalle)
        advJeu=getJeuAdv(idjeu,idAdv,tour,server)
    return advJeu

def remplirGrille(joueur, jeu):
    for i in range(nb_row-1,-1,-1):
        if(grille[i][jeu]==0):
            grille[i][jeu]=joueur
            break
            
def printGrille():
    for i in range(nb_row):
        print("|",end=' ')
        for j in range(nb_col):
            if(grille[5-i][j]==1):
                print(CBLUE+'0'+CEND,end=' ')
            elif grille[5-i][j]==2:
                print(CRED+'0'+CEND,end=' ')
            else:
                print(" ",end=' ')
            print("|",end=' ')
        print()
    print("|",end=' ')
    for i in range(nb_col):
        print("_",end=" ")
        print("|",end=' ')
    print()
    print("|",end=' ')
    for i in range(nb_col):
        print(i%10+1,end=" ")
        print("|",end=' ')
    print()
    


#############################################################
#                                                           #
#  Vous n'avez qu'a remplacer les deux methodes monjeu et   #
#      appliqueJeuAdv  selon votre IA                       #
#                                                           #
#  Bien definir un idjeu pour l'id de la partie de jeu      #
#  votre nom et celui du joueur distant                     #
#  puis bien préciser si vous commencer le jeu True,        #
#  False signifie que le joueurDistant qui commence.        #
#                                                           #
#                                                           #
#############################################################



grilleDim=12
grille=np.zeros((nb_row,nb_col))


#idjeu est un id unique, si vous abondonnez une partie, pensez à créer un nouveau idjeu
idjeu="ID1504_001_2"
idjoueurLocal="Safwan"
idjoueurDistant="Christophe"

# bien préviser si vous commencer le jeu ou c'est l'adversaire qui commence
joueurLocalquiCommence=True



# fonctions pour minimax

def jouer(grille,i,j,joueur):
    grille[i][j]=joueur


def is_valid(grille,j):
    return grille[nb_row-1][j] == 0

def next_open_row(grille, j):
    for i in range(nb_row):
        if grille[i][j]==0:
            return i
       
    

def is_end(grille, joueur):
    
    # victoire horizontale    
    for i in range(nb_col-3):
        for j in range(nb_row):
            if grille[j][i] == grille[j][i+1] == grille[j][i+2] == grille[j][i+3] == joueur:
                return True
        
    # victoire verticale   
    for i in range(nb_col):
        for j in range(nb_row-3):
            if grille[j][i] == grille[j+1][i] == grille[j+2][i] == grille[j+3][i] == joueur:
                return True      
            
    
    #victoire horizontale   
    for i in range(nb_col-3):
       for j in range(nb_row-3):
           if grille[j][i] == grille[j+1][i+1] == grille[j+2][i+2] == grille[j+3][i+3] == joueur:
               return True
                       
    for i in range(nb_col-3):
        for j in range(3, nb_row):
            if grille[j][i] == grille[j-1][i+1] == grille[j-2][i+2] == grille[j-3][i+3] == joueur:
                return True
            

def evaluation_grille(sous_grille, joueur):
    compteur_piece = 0
    compteur_vide = 0
    compteur_piece_adv = 0
    score = 0
    joueur_adv = 1
    if joueur == 1:
        joueur_adv = 2
    
    for i in range(len(sous_grille)):
        if sous_grille[i] == joueur:
            compteur_piece += 1
        elif sous_grille[i] == 0:
            compteur_vide += 1
    
    if compteur_piece == 4 :
        score+=100
    
    elif compteur_piece == 3 and compteur_vide == 1:
        score+=5
    
    elif compteur_piece == 2 and compteur_vide == 2:
        score+=2
            
    for i in range(len(sous_grille)):
        if sous_grille[i] == joueur_adv:
            compteur_piece_adv +=1
    
    if compteur_piece_adv == 3 and compteur_vide == 1:
        score-=4
        
    return score


def score_position(grille, joueur):
    score = 0
    compteur_central = 0
    
    colone_milieu = [int(i) for i in list(grille[:,nb_col//2])]
    for i in range(len(colone_milieu)):
        if colone_milieu[i] == joueur:
            compteur_central += 1
    score+=compteur_central * 3
    
    
    #score horizontal
    for i in range(nb_row):
        ligne = [int(x) for x in list(grille[i,:])]
        for j in range(nb_col-3):
            sous_grille =  ligne[j:j+4]
            score += evaluation_grille(sous_grille,joueur)
            
            
    #score vertical
    for j in range(nb_col):
        colone = [int(x) for x in list(grille[:,j])]
        for i in range(nb_row-3):
            sous_grille = colone[i:i+4]
            score += evaluation_grille(sous_grille,joueur)
            
            
    #score diagonaux
    for i in range(nb_row-3):
        for j in range(nb_col-3):
            sous_grille = [grille[i+x][j+x] for x in range(4)]
            score += evaluation_grille(sous_grille,joueur)
    
    for i in range(nb_row-3):
        for j in range(nb_col-3):
            sous_grille = [grille[i+3-x][j+x] for x in range(4)]
            score += evaluation_grille(sous_grille,joueur)            
    
    return score


def vainqueur(grille):
    return is_end(grille,1) or is_end(grille,2) or len(position_valable(grille)) == 0



def position_valable(grille):
    liste_position = []
    for j in range(nb_col):
        if is_valid(grille,j):
            liste_position.append(j)
    return liste_position
  
    
def minimax(grille,profondeur,alpha,beta,maximiser):
    
    liste_position = position_valable(grille)
    est_fini = vainqueur(grille)
    
    if profondeur == 0 or est_fini:
        if est_fini:
            if is_end(grille,2): #victoire IA
                return(None,10000000)
            elif is_end(grille,1): #victoire joueur
                return(None,-1000000)
            else: #match nul
                return(None,0)
        else: #profondeur == 0
            return(None,score_position(grille,2))
            
    if maximiser:
        value = -math.inf
        colone = random.choice(liste_position)
        for j in liste_position:
            i = next_open_row(grille,j)
            grille_copie = grille.copy()
            jouer(grille_copie,i,j,2)
            nouveau_score = minimax(grille_copie,profondeur-1,alpha, beta, False)[1]
            if nouveau_score> value:
                value = nouveau_score
                colone = j
            alpha = max(alpha, value)
            if alpha>= beta:
                break
        return colone,value
    
    else: #minimiser
        value = math.inf
        colone = random.choice(liste_position)
        for j in liste_position:
            i = next_open_row(grille,j)
            grille_copie = grille.copy()
            jouer(grille_copie,i,j,1)
            nouveau_score = minimax(grille_copie,profondeur-1,alpha, beta, True)[1]
            if nouveau_score< value:
                value = nouveau_score
                colone = j
            beta = min(beta,value)
            if alpha>= beta:
                break
        return colone,value
    


#cette methode est à remplacer par votre une fonction IA qui propose le jeu
def monjeu():
   
    meilleure_colonne = minimax(grille,3,-math.inf,math.inf,True)[0]
    print("Jeu conseillé: " + str(meilleure_colonne))                
                    
              
    return meilleure_colonne


# cette fonction est à remplacer une qui saisie le jeu de l'adversaire à votre IA
def appliqueJeuAdv(jeu):
 
    print("jeu de l'adversair est ", jeu)





def jeu_offline(tour_joueur):
    
    while True:
        
        printGrille()
        fini = vainqueur(grille)
        
        if fini:
            if is_end(grille,1):
                print("Victoire Joueur")
            elif is_end(grille,2):
                print("Victoire IA")
            else:
                print("Match nul")
            return
            
        if tour_joueur == 1:
            
            j = int(input("Veuillez saisir une colonne : "))
            if is_valid(grille,j):
                i = next_open_row(grille,j)
                jouer(grille,i,j,1)
                tour_joueur = 2
            
        else:
            
            j = minimax(grille,3,-math.inf,math.inf,True)[0]
            i = next_open_row(grille,j)
            jouer(grille,i,j,2)
            tour_joueur = 1
            
            
            
def jeu_online():
    
    if(joueurLocalquiCommence):
        joueurLocal=2
        joueurDistant=1
    else:
        joueurLocal=1
        joueurDistant=2
        
        
    tour=0
    while(True):
        
        
        if(joueurLocalquiCommence):
            jeu=monjeu()
            jouerWEB(idjeu,idjoueurLocal,tour,jeu)
            remplirGrille(joueurLocal,jeu)
            printGrille()
            jeuAdv=loopToGetJeuAdv( 10,idjeu,idjoueurDistant,tour)
            #c'est ce jeu qu'on doit transmettre à notre IA
            appliqueJeuAdv(jeuAdv)
            remplirGrille(joueurDistant,jeuAdv)
            printGrille()
        else:
            jeuAdv=loopToGetJeuAdv(10,idjeu,idjoueurDistant,tour)
            #c'est ce jeu qu'on doit transmettre à notre IA
            appliqueJeuAdv(jeuAdv)
            remplirGrille(joueurDistant,jeuAdv)
            printGrille()
            jeu=monjeu()
            jouerWEB(idjeu,idjoueurLocal,tour,jeu)
            remplirGrille(joueurLocal,jeu)
            printGrille()
            
        tour+=1        

    
if __name__ == "__main__":
    tour_joueur = 1
    jeu_offline(tour_joueur)
