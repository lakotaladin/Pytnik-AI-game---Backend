from rest_framework.decorators import api_view
from django.http import JsonResponse
import json
import heapq
from collections import deque
import math

@api_view(['POST'])
def Projekat1(request):
    data = json.loads(request.body) #u data se nalazi sve sto je poslato sa fronta
    tiles = data['tiles'] #tiles je matrica sa 0,1,2,3,4,5
    playerx = data['playerx'] 
    playery = data['playery'] 
    player_type = data['player_type'] #tip igraca
    gold_positions = data['gold_positions'] #pozicije zlatnika
    width = 11 
    height = 11 
    g = Graph(height, width) #pravimo objekat klase Graph

    start = (playerx, playery)

    matrix = g.make_matrix(height, width, tiles) #ovo je matrica sa 0,1,2,3,4,5
    matrixCost = g.make_matrixCost(matrix) #ovo je matrica cena

    if player_type == 'Aki': #ako je Aki
        path = g.aki_search(start, matrixCost, gold_positions) #pozivamo funkciju za Aki
    elif player_type == 'Jocke':
       path = g.jocke_search(start, matrixCost, gold_positions)
    elif player_type == 'Micko':
        path = g.micko_search(start, matrixCost, gold_positions) 
    elif player_type == 'Uki':
        path = g.uki_search(start, matrixCost, gold_positions)
    else:
        path = []

    return JsonResponse({'path': path}) #vracamo putanju
  

class Graph(object):
    def __init__(self, height, width): #inicijalizujemo objekat
        self.visitedS = [] #poseceni cvorovi
        self.height = height #visina 
        self.width = width  #sirina
   
    def get_moves(self, position): #funkcija za poteze
        (x, y) = position #x i y su pozicije
        moves = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]  # Dodajemo horizontalne i vertikalne poteze
        # Proveravamo da li su potezi unutar granica matrice
        moves = [(x, y) for (x, y) in moves if 0 <= x < self.height and 0 <= y < self.width] #ako su unutar granica matrice
        return moves #vracamo poteze

    def make_matrix(self, height, width, tiles): #funkcija za pravljenje matrice
        matrix = []
        for i in range(height):
            matrix.append(tiles[i * width:i * width + width])
        return matrix

    def make_matrixCost(self, matrix): #svaki put da se redefinise matrica cena
        height = len(matrix)
        width = len(matrix[0]) if height > 0 else 0
        matrixCost = [[0 for _ in range(width)] for _ in range(height)]
        for i in range(height):
            for j in range(width):
               if(matrix[i][j] == 0 ):
                    matrixCost[i][j] = 1
               if(matrix[i][j] == 1 ):
                    matrixCost[i][j] = 4
               if(matrix[i][j] == 2 ):
                    matrixCost[i][j] = 2
               if(matrix[i][j] == 3 ):
                    matrixCost[i][j] = 3
               if(matrix[i][j] == 4 ):
                    matrixCost[i][j] = 6
               if(matrix[i][j] == 5 ):
                    matrixCost[i][j] = 5
                # Dodajte ostale uslove ovde
        return matrixCost

    def reconstruct_path(self, came_from, start, end):  # Rekonstruišemo put od starta do zlatnika
        path = []
        current = end
        while current != start:
            path.append(current)
            current = came_from[current]
        path.reverse()  # Rekonstruisani put je u obrnutom redosledu
        return path

    

    def aki_search(self, start, matrixCost, gold_positions): #dubina
        paths = [] 
        gold_positions = [(pos, i) for i, pos in enumerate(gold_positions)] 

        for _ in range(len(gold_positions)):  
            heap = [(0, start)]  
            visited = set([tuple(start)]) 
            came_from = {tuple(start): None} 

            while heap: # Dok god heap nije prazan
                # Izaberemo poziciju sa najmanjom cenom puta iz heapa
                cost, position = heapq.heappop(heap)

                if list(position) in [pos for pos, _ in gold_positions]:
                    path = self.reconstruct_path(came_from, start, position)  # Rekonstruišemo put od starta do zlatnika 
                    if paths: # Ako smo već pronašli neki zlatnik
                        paths[-1].extend(path)  # Dodajemo putanju do zlatnika na poslednju putanju u listi
                    else: # Ako nismo pronašli nijedan zlatnik
                        paths.append(path)  #dodajemo trenutnu putanju u listu
                    gold_positions.remove((list(position), [i for pos, i in gold_positions if pos == list(position)][0])) 
                    
                    start = position 
                    break

                    heap = [(0, start)]
                    visited = set([tuple(start)])
                    came_from = {tuple(start): None}

                    break

                moves = self.get_moves(position)
                for move in moves: 
                    if tuple(move) not in visited and matrixCost[move[0]][move[1]] != 0:
                         # Ako nova pozicija nije posećena i ima neki trošak (različit od nule), dodajemo je u heap za dalju obradu

                        # Dodajemo novu poziciju u heap sa ažuriranom cenom puta
                        heapq.heappush(heap, (cost + matrixCost[move[0]][move[1]], move)) 
                        visited.add(tuple(move))
                        came_from[tuple(move)] = position 

        return paths    
    




    

    from collections import deque

    def BFS(self, start, matrixCost, gold_positions): #po sirini pretraga
        visited = set() 
        queue = deque([(start, 0, [])]) 

        while queue: # Dok god red nije prazan
            (x, y), cost, path = queue.popleft() # Uzimamo prvu poziciju iz reda (pozicija, cena puta, putanja) (izvršavanje)
            if (x, y) not in visited: # Ako pozicija nije posećena
                visited.add((x, y)) 
                path = path + [(x, y)]  # Dodajemo trenutnu poziciju u putanju

                if [x, y] in gold_positions:  # Ako smo pronašli zlatnik
                    return path, (x, y)  # Vraćamo putanju do zlatnika i poziciju zlatnika



                for move in self.get_moves((x, y)): 
                    if move not in visited: 
                        new_cost = cost + matrixCost[move[0]][move[1]]
                        queue.append((move, new_cost, path)) # Dodajemo novu poziciju u red za dalju obradu ali dodajemo na kraj reda

        return None, None 

    def jocke_search(self, start, matrixCost, gold_positions): 
        paths_to_gold = [] 
        while gold_positions: 
            path_to_gold, last_position = self.BFS(start, matrixCost, gold_positions) 
            #Koristi se BFS za pronalaženje putanjje do najblizeg zlatnika path_to_gold je pronađena putanja, a last_position je poslednja pozicija na toj putanji, koja sadrži zlatnik.
            if path_to_gold:  # Ako smo pronašli putanju do zlatnika
                paths_to_gold.append(path_to_gold) # Dodajemo putanju do zlatnika u listu svih putanja
                gold_positions.remove(list(last_position))  
                start = last_position  
        return paths_to_gold 
    




    # uki
    
    def get_moves(self, position):
        x, y = position
        moves = []

        possible_moves = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

        for move in possible_moves:
            if 0 <= move[0] < self.height and 0 <= move[1] < self.width:
                moves.append(move)

        return moves
    
 

    import math

    

    def get_heuristic(self, current_position, position, remaining_gold_positions): # Manhattan heuristika
        if not remaining_gold_positions:    # Ako nema preostalih ciljnih položaja, vraćamo 0
            return 0

        # Računa Manhattan udaljenost do svakog preostalog ciljnog položaja
        distances = [abs(position[0] - pos[0]) + abs(position[1] - pos[1]) for pos in remaining_gold_positions] 

        # Vraća minimalnu udaljenost kao heuristiku
        min_distance = min(distances)

        return min_distance


    def reconstruct_path2(self, came_from, start, end): # Rekonstruišemo put od starta do zlatnika
        path = []
        current = end # Trenutna pozicija je poslednja pozicija
        while current != start: 
            path.append(list(current)) # Dodajemo trenutnu poziciju u putanju
            current = came_from[tuple(current)]
        path.append(start)  
        path.reverse() # Rekonstruisani put je u obrnutom redosledu
        return path 


    def micko_search(self, start, matrix_cost, gold_positions):
        paths = [] # Inicijalizujemo praznu listu za cuvanje pronadjenih puteva
        gold_positions = [(pos, i) for i, pos in enumerate(gold_positions)] # Dodajemo indeks zlatnika u listu zlatnika
        gold_positions.sort(key=lambda x: (x[1], -x[0][0], -x[0][1]))

        while gold_positions:
            heap = [(0, 0, 0, start)]  # Dodajemo broj sakupljenih zlatnika u heap
            visited = set([tuple(start)])
            came_from = {tuple(start): None}

            while heap:
                # Izaberemo poziciju sa najmanjom cenom puta, najvećim brojem sakupljenih zlatnika,
                # i najmanjom vrednošću identifikacione oznake
                cost, neg_gold_count, id_value, position = heapq.heappop(heap)

                heuristic_value = self.get_heuristic(start, position, [pos for pos, _ in gold_positions]) 
                # Računamo heuristiku za trenutnu poziciju

                if list(position) in [pos for pos, _ in gold_positions]:
                    path = self.reconstruct_path2(came_from, start, position)
                    if paths:
                        paths[-1].extend(path[1:])  # Dodajemo putanju do zlatnika na poslednju putanju
                    else:
                        paths.append(path)
                    current_gold_position = next(i for i, pos in enumerate(gold_positions) if pos[0] == list(position))
                    gold_positions.pop(current_gold_position)
                    start = position  # Ažuriramo početnu poziciju
                    visited.add(tuple(position))  # Mark the gold position as visited
                    break

                moves = self.get_moves(position)
                for move in moves:
                    if tuple(move) not in visited and matrix_cost[move[0]][move[1]] != 0:
                        # Dodajemo novu poziciju u heap sa ažuriranim brojem sakupljenih zlatnika
                        # i vrednošću identifikacione oznake
                        heapq.heappush(heap, (cost + matrix_cost[move[0]][move[1]], -neg_gold_count-1, -heuristic_value, move))
                        visited.add(tuple(move)) # Mark the gold position as visited
                        came_from[tuple(move)] = position

        return paths

#za svakog sledbenika poslednjeg cvora na uklonjenoj putanji formira se po jedna nova parcijalna putanja 
    def uki_search(self, start, matrix_cost, gold_positions):
        paths = [] 
        gold_positions = [(pos, i) for i, pos in enumerate(gold_positions)] 
        gold_positions.sort(key=lambda x: (x[1], -x[0][0], -x[0][1])) 
        visited = set()
        came_from = {}  # Inicijalizujemo rečnik odakle smo došli

        while gold_positions: 
            stack = [(0, 0, 0, start)] 
            heapq.heapify(stack) # Heapify stack

            while stack: # Dok god stack nije prazan
                cost, collected_gold, id_value, position = heapq.heappop(stack) #najmanja cena

                if list(position) in [pos for pos, _ in gold_positions]: 
                    path = self.reconstruct_path2(came_from, start, position) 
                    if paths: 
                        paths[-1].extend(path) 
                    else: # Ako nismo pronašli nijedan zlatnik
                        paths.append(path) # Dodajemo trenutnu putanju u listu
                    current_gold_position = next(i for i, pos in enumerate(gold_positions) if pos[0] == list(position)) # Pronalazimo poziciju zlatnika u listi zlatnika
                    gold_positions.pop(current_gold_position)  
                    start = position 
                    came_from = {start: None} # Resetujemo rečnik odakle smo došli
                    visited = {start} 
                    break 

                moves = self.get_moves(position) 
                for move in moves: # Za svaki potez
                    if tuple(move) not in visited and matrix_cost[move[0]][move[1]] != 0: # Ako nova pozicija nije posećena 
                        heapq.heappush(stack, (cost + matrix_cost[move[0]][move[1]], -collected_gold-1, -id_value, move)) 
                        # Dodajemo novu poziciju u heap sa ažuriranim brojem sakupljenih zlatnika i vrednošću identifikacione oznake
                        visited.add(tuple(move)) 
                        came_from[tuple(move)] = position 

            paths = [path for path in paths if path] # Uklanjamo prazne putanje
            paths.sort(key=lambda x: (len(x), -x[-1][1] if len(x[-1]) > 1 else 0, x[-1][2] if len(x[-1]) > 2 else 0)) 

        return paths