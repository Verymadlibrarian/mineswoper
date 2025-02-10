from random import randint
import fltk, fltk_addons
fltk_addons.init(fltk)
import pprint
from sys import setrecursionlimit
setrecursionlimit(10**6)

EMPTY = "#d8dee9"
BOMB = "#bf616a"
UNKOWN = "#4c566a"
ALONE = "#81a1c1"

def bombes(nbcases, nbbombes):
    """
    Renvoie la liste des coordonnées aléatoires des bombes.
    """
    boumz = []
    for i in range(nbbombes):
        x = randint(0, nbcases - 1)
        y = randint(0, nbcases - 1)
        boumz.append((y, x))

    return boumz


def grille(nbcases, coord_bombes):
    """
    Crée la grille vide représentant les valeurs des différentes cases.
    -2 --> Case inconnue
    -1 --> Case bombe
    0 --> Case vide connue
    x --> Case adjacente à x bombes
    """
    boumz = [[-2 for i in range(nbcases)] for j in range(nbcases)]

    for i in range(len(coord_bombes)):
        boumz[coord_bombes[i][0]][coord_bombes[i][1]] = -1

    return boumz

def get_clicked_case(obj,mode):
            print("obj : ", obj)
            print("----")
            if obj != None :
                if type(obj) == int:
                    tags = list(fltk_addons.recuperer_tags(obj))    
                else:
                    tags = list(fltk_addons.recuperer_tags(obj[1]))
                print("tags : ", tags)
                print("----")
                if "current" in tags:
                    tags.remove("current")
                    if mode == "right":
                        return (tags[1],tags[2])
                    else:
                        if tags[0] == "-1": #Si c'est une bombe
                            print("boum")
                            return (-1,0,0)
                        
                        return tags
                    # if tags[0] == "-1" and mode == "left":
                    #     print("boum")
                    #     return (-1,tags[1],tags[2])
                    # elif tags == "-2":
                    #     print("prut")
                    #     return -2,0
                    # else:
                    #     if len(tags) >= 3:
                    #         tags.pop(-1)
                    #     bomb,y,x = int(tags[0]), int(tags[1]), int(tags[2])
                    #     print("Retour des xy : ", y,x)
                    #     print("----\n")
                    #     return (y,x)
            return (3,0)

def mainloop():
    global width, height, nbcases, nbbombes
    nbcases = 25
    nbbombes = 50
    width = 1600
    height = 900
    boumz = bombes(nbcases, nbbombes)
    grid = grille(nbcases, boumz)

    fltk.cree_fenetre(width, height, redimension=True)
    b_side, h_padding, v_padding = mainframe(width, height, grid)

    ev = None
    end = False
    while not end:
        fltk.mise_a_jour()
        ev = fltk.donne_ev()
        if ev is None: 
            continue
        elif ev[0] =="Quitte":
            fltk.ferme_fenetre()
            break
        
        elif ev[0] =="Redimension":
            b_side, h_padding, v_padding = mainframe(fltk.largeur_fenetre(),fltk.hauteur_fenetre(),grid)
        
        elif ev[0] == "ClicDroit":
            obj = fltk_addons.objet_survole()
            x,y = get_clicked_case(obj,"right")

            fltk.rectangle(h_padding+y*b_side//nbcases, v_padding+x*b_side//nbcases, h_padding+(y+1)*b_side//nbcases, v_padding+(x+1)*b_side//nbcases, remplissage="#bf616a", tag="-1")
        
        elif ev[0] == "ClicGauche":
            obj = fltk_addons.objet_survole()
            click = get_clicked_case(obj,"left")

            if click == (-1,0,0): #Si c'est une bombe
                fltk.ferme_fenetre()
                break
            else:
                case, y, x = int(click[0]), int(click[1]), int(click[2])
                fltk.efface(obj)
                val = compte_bombes(y, x, grid)
                grid[y][x] = val
                #Si la case n'est pas bombée, on lance une vérification récursive
                if val == 0: 
                    no_more_zeros(y, x, grid, b_side, h_padding, v_padding)
                    mainframe(width, height, grid)
                if val > 0:
                    fltk.rectangle(h_padding+x*b_side//nbcases, v_padding+y*b_side//nbcases, h_padding+(x+1)*b_side//nbcases, v_padding+(y+1)*b_side//nbcases, couleur="black", remplissage=EMPTY)
                #if val == 0:
                #    fltk.rectangle(h_padding+x*b_side//nbcases, v_padding+y*b_side//nbcases, h_padding+(x+1)*b_side//nbcases, v_padding+(y+1)*b_side//nbcases, couleur="black", remplissage=ALONE)
                if val != 0:
                    fltk.texte(h_padding+(x+1/2)*b_side//nbcases, v_padding+(y+1/2)*b_side//nbcases, chaine=str(val), taille=int(b_side/nbcases/2),ancrage="center")
                
                
def compte_bombes(y, x, grid):
    """
    Renvoie le nombre de bombes adjacentes à la place d'un pion selon sa coordonnée x et y dans la liste
    """
    val = 0
    dx, dy, = [0], [0]

    if y != 0:
        dy.append(-1)
    if y != nbcases-1:
        dy.append(1)
    if x != 0:
        dx.append(-1)
    if x != nbcases-1:
        dx.append(1)

    for x_ in dx:
        for y_ in dy:
            if grid[y+ y_][x + x_] == -1:
                val += 1

    return val

def mainframe(width, height, grid):
    fltk.efface_tout()
    if width >= height:
        b_side = 0.9*height
        h_padding = (width - b_side)/2
        v_padding = (height - b_side)/2
    else:
        b_side = 0.9*width
        h_padding = (width - b_side)/2
        v_padding = (height - b_side)/2
    fltk.rectangle(0, 0, width, height, couleur=UNKOWN, remplissage="#d8dee9")
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            case = grid[i][j]
            if case == -1 :    
                #fltk.rectangle(h_padding+j*b_side//nbcases, v_padding+i*b_side//nbcases, h_padding+(j+1)*b_side//nbcases, v_padding+(i+1)*b_side//nbcases, remplissage="#bf616a", tag=[case,i,j])
                fltk.rectangle(h_padding+j*b_side//nbcases, v_padding+i*b_side//nbcases, h_padding+(j+1)*b_side//nbcases, v_padding+(i+1)*b_side//nbcases, remplissage=UNKOWN, tag=[case, i, j])
            if case == -2:
                fltk.rectangle(h_padding+j*b_side//nbcases, v_padding+i*b_side//nbcases, h_padding+(j+1)*b_side//nbcases, v_padding+(i+1)*b_side//nbcases, remplissage=UNKOWN, tag=[case, i, j])
            if case == 0:
                fltk.rectangle(h_padding+j*b_side//nbcases, v_padding+i*b_side//nbcases, h_padding+(j+1)*b_side//nbcases, v_padding+(i+1)*b_side//nbcases, couleur="black", remplissage=ALONE, tag=[case, i, j])
                #fltk.texte(h_padding+(j+1/2)*b_side//nbcases, v_padding+(i+1/2)*b_side//nbcases, chaine=str(case), ancrage="center")
            if case >= 1:
                fltk.rectangle(h_padding+j*b_side//nbcases, v_padding+i*b_side//nbcases, h_padding+(j+1)*b_side//nbcases, v_padding+(i+1)*b_side//nbcases, couleur="black", remplissage=EMPTY, tag=[case, i, j])
                fltk.texte(h_padding+(j+1/2)*b_side//nbcases, v_padding+(i+1/2)*b_side//nbcases, chaine=str(case), taille=int(b_side/nbcases/2),ancrage="center", tag=[case, i, j])

    return b_side, h_padding, v_padding

def no_more_zeros(y, x, grid, b_side, h_padding, v_padding):
    grid[y][x] = 0
    fltk.rectangle(h_padding+x*b_side//nbcases, v_padding+y*b_side//nbcases, h_padding+(x+1)*b_side//nbcases, v_padding+(y+1)*b_side//nbcases, couleur="black", remplissage=ALONE)
    dx, dy, = [0], [0]

    if y != 0:
        dy.append(-1)
    if y != nbcases-1:
        dy.append(1)
    if x != 0:
        dx.append(-1)
    if x != nbcases-1:
        dx.append(1)

    for x_ in dx:
        for y_ in dy:
            nb_boumz = compte_bombes(y+ y_,x + x_,grid)
            
            if (nb_boumz == 0) and grid[y+y_][x+x_] == -2:
                no_more_zeros(y+ y_,x + x_,grid,b_side,h_padding,v_padding)

            elif (nb_boumz >= 0) and grid[y+y_][x+x_] == -2:
                grid[y+ y_][x + x_] = nb_boumz



mainloop()