import copy

class Node():
    def __init__(self, val,suiv,prec) -> None:
        self.val = val
        self.suiv = suiv
        self.prec = prec

class Possibilite():
    def __init__(self,x : int, y : int,possibilite:list,NbPossibilite : int) -> None:
        self.x = x
        self.y = y
        self.possibilite = possibilite
        self.NbPossibilite = NbPossibilite

    def isFinish(self) -> bool :
        return self.x == None and self.y == None and self.possibilite == None


class choix():
    def __init__(self, poss : Possibilite,choix : int) -> None:
        self.poss = poss
        self.choix = choix

def initialiserGrille(nomFichier : str) -> list:
    fichier = open(nomFichier)
    Grille = []
    for ligne in fichier:
        L = [ int(nb) for nb in ligne.split(',')]
        Grille.append(L)
    fichier.close()
    return Grille

def defPossibilite(numligne : int,index : int,Grille : list) -> list:
    L = list(range(1, 10))
    for i in Grille[numligne]:
        if i in L:
            L.remove(i)
    for j in range(len(Grille)):
        if Grille[j][index] in L:
            L.remove(Grille[j][index])
    y = numligne
    x = index
    while x%3!=0:
        x = x-1
    while y%3 != 0:
        y = y-1

    for i in range(3):
        for j in range(3):
            if Grille[y+i][x+j] in L:
                L.remove(Grille[y+i][x+j])
    
    return L

def initPossibilite(Grille : list) -> list:
    L = []
    for numligne, ligne in enumerate(Grille):
        for index, nombre in enumerate(ligne):
            if nombre == 0:
                poss = defPossibilite(numligne,index,Grille)
                nb = len(poss)
                L.append(Possibilite(index,numligne,poss,nb))
    L.append(Possibilite(None,None,None,999999))
    return L

def sortPoss(LPossibilite : list) -> list:
    L = LPossibilite.sort(key= lambda Possibilite : Possibilite.NbPossibilite)

    return L

def check(y : int, x : int, val : int,Grille : list) -> bool :
    for i in Grille[y]:
        if i == val:
            return False
    for j in range(len(Grille)):
        if Grille[j][x] == val :
            return False
    while x%3!=0:
        x = x-1
    while y%3 != 0:
        y = y-1

    for i in range(3):
        for j in range(3):
            if Grille[y+i][x+j] == val:
                return False

    return True

def solve(Grille : list, LPossibilite : list) -> list:
    L = copy.deepcopy(Grille)
    i = 0
    choixStart = choix(LPossibilite.pop(0),0)
    N = Node(choixStart,None,None)
    
    while not(N.val.poss.isFinish()):
        """Point a ameliorer, la derniére possibilite"""
        if N.val.choix < len(N.val.poss.possibilite):
            if check(N.val.poss.y,N.val.poss.x,N.val.poss.possibilite[N.val.choix],L):
                L[N.val.poss.y][N.val.poss.x] = N.val.poss.possibilite[N.val.choix]
                N.val.choix = N.val.choix + 1
                NvC = choix(LPossibilite.pop(0),0)
                NvN = Node(NvC,None,N)
                NvN.prec = N
                N.suiv = NvN
                N = NvN
            else:
                N.val.choix = N.val.choix + 1
        else:
            L[N.val.poss.y][N.val.poss.x] = 0
            LPossibilite.insert(0,N.val.poss)
            if(N.prec != None):
                N = N.prec
                N.suiv = None
            else:
                return
        
    return L

def output(Grille : list, FileName : str) :
    fichier = open(FileName,"w")

    for ligne in Grille:
        for colone in ligne :
            fichier.write("" + str(colone) + ",")
        fichier.write("\n")
        
    fichier.close()

Grille = initialiserGrille("input.txt")
LPossibilite = initPossibilite(Grille)
sortPoss(LPossibilite)
Solved = solve(Grille,LPossibilite)
output(Solved,"output.txt")