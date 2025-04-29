import pygame
import time
import heapq
# pygame setup
width = 1280
height = 720
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
font = pygame.font.SysFont(None, 48)


delay = 300  # milisegundos entre pulsaciones
last_press = 0
count = 0

def create_m():
    mazes = []

    while True:
        # Leer la primera línea
        r_c = input().strip()
        if r_c == '0':
            break

        r_c = r_c.split()
        rows = int(r_c[0])
        columns = int(r_c[1])
        posinit_x = int(r_c[2])
        posinit_y = int(r_c[3])
        posfinal_x = int(r_c[4])
        posfinal_y = int(r_c[5])

        print("Filas:", rows, "Columnas:", columns, 
              "Posinit_x:", posinit_x, "Posinit_y:", posinit_y, 
              "Posfinal_x:", posfinal_x, "Posfinal_y:", posfinal_y)

        # Recibir matriz
        mat = []
        for _ in range(rows):
            row = input().split()
            row = [int(x) for x in row]
            mat.append(row)

        # Guardar el laberinto
        mazes.append((mat, rows, columns, posinit_x, posinit_y, posfinal_x, posfinal_y))

    return mazes



#Dibuja las celdas
def draw_rect(mat,m,n, posinit_x, posinit_y, posfinal_x, posfinal_y):
    
    # centrado
    offset_x = (width - n*cell_s) // 2
    offset_y = (height - m*cell_s) // 2
    # dibujo de las celdas
    for i in range(0,m):
        for j in range(0,n):
            cell_r = offset_x + j*cell_s
            cell_c = offset_y + i*cell_s

            rect = pygame.draw.rect(screen, "white", (cell_r, cell_c, cell_s, cell_s))
            pygame.draw.rect(screen, (0, 0, 0), rect, width=2)  # borde

            #el texto en cada celda (azul inicio, verde final)
            if(i == posinit_x and j == posinit_y):
                text = font.render(str(mat[i][j]), True, "blue")  # texto
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
            elif(i == posfinal_x and j == posfinal_y):
                text = font.render(str(mat[i][j]), True, "green")  # texto
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
            else:
                text = font.render(str(mat[i][j]), True, (0, 0, 0))  # texto
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)


#Actualiza posicion visual jugador
def player_posi(mat, n, m, posinit_x, posinit_y):
    offset_x = (width - n*cell_s + cell_s) // 2
    offset_y = (height - m*cell_s+ cell_s) // 2
    posmat_x = posinit_x
    posmat_y = posinit_y
    player_pos = pygame.Vector2(offset_x + (posinit_y)*cell_s, offset_y + (posinit_x)*cell_s) # posinit_y mueve en columnas, posinit_x mueve en filas (por eso estan intercambiados)
    return player_pos, posmat_x, posmat_y



#Hace los movimientos respecto a la matriz
def mov(mat, m, n, posx, posy):
    global last_press                   # No se por que pero no la reconoce como global sin esto pero cell_s si
    i = posx
    j = posy
    h = mat[i][j]
    #print(h)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and current_time - last_press > delay:
        if i-h < 0:
            print("Movimiento no posible")
            last_press = current_time
            return i, j
        else:
            print("Movimiento realizado: ", i-h, j)
            last_press = current_time
            countg()
            return i-h, j
        

    if keys[pygame.K_s] and current_time - last_press > delay:
        if i+h >m-1:
            print("Movimiento no posible")
            last_press = current_time
            return i, j
        else:
            print("Movimiento realizado: ", i+h, j)
            last_press = current_time
            countg()
            return i+h, j
        

    if keys[pygame.K_a] and current_time - last_press > delay:
        if j-h < 0:
            print("Movimiento no posible")
            last_press = current_time
            return i, j
        else:
            print("Movimiento realizado: ", i, j-h)
            last_press = current_time
            countg()
            return i, j-h
        

    if keys[pygame.K_d] and current_time - last_press > delay:
        if j+h >n-1:
            print("Movimiento no posible")
            last_press = current_time
            return i, j
        else:
            print("Movimiento realizado: ", i, j+h)
            last_press = current_time
            countg()
            return i, j+h
        
    return i, j
   
#Verifica estado objetivo
def goal(posactual_x, posactual_y,posfinal_x, posfinal_y):
    if(posactual_x ==  posfinal_x and posactual_y == posfinal_y):
        print("Meta alcanzada")
        return True
    return False

#Cuenta movimientos hechos a mano
def countg():
    global count
    count +=1
    print(count)
#Movimientos en pantalla
def draw_counter(screen, count):
    counter_text = font.render(f"Movimientos: {count}", True, "white")
    screen.blit(counter_text, (20, 20))  # posicion 

class Nodo:
    def __init__(self, x, y, padre=None, costo = 0):
        self.x = x
        self.y = y
        self.padre = padre
        self.hijos = []  # hijos que surgen de este nodo
        self.costo = costo

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

    def obtener_camino(self):
        camino = []
        nodo = self
        while nodo:
            camino.append((nodo.x, nodo.y))
            nodo = nodo.padre
        return camino[::-1]

def dfs(mat, m, n, inicio, objetivo):
    nodo_inicio = Nodo(inicio[0], inicio[1])
    pila = [nodo_inicio]
    visitados = set()

    while pila:
        actual = pila.pop()
        
        if (actual.x, actual.y) in visitados:
            continue
        visitados.add((actual.x, actual.y))
        print(actual.x, actual.y)
        if (actual.x, actual.y) == objetivo:
            return actual.obtener_camino()

        h = mat[actual.x][actual.y]
        movimientos = [
            (actual.x - h, actual.y),   # arriba
            (actual.x, actual.y + h),   # derecha


            (actual.x + h, actual.y),   # abajo
            (actual.x, actual.y - h)    # izquierda
            
        ]

        for x_nuevo, y_nuevo in movimientos:
            if 0 <= x_nuevo < m and 0 <= y_nuevo < n and (x_nuevo, y_nuevo) not in visitados:
                hijo = Nodo(x_nuevo, y_nuevo, actual)
                actual.agregar_hijo(hijo)
                pila.append(hijo)

    return None  # camino no encontrado

#def c_uni():
def uc(mat, m, n, inicio, objetivo):
    nodo_inicio = Nodo(inicio[0], inicio[1], costo=0)
    pila = [nodo_inicio]
    visitados = set()

    while pila:
        # Ordenar la pila por costo 
        pila.sort(key=lambda nodo: nodo.costo)
        actual = pila.pop(0)  
        
        if (actual.x, actual.y) in visitados:
            continue
        visitados.add((actual.x, actual.y))
        print(actual.x, actual.y)

        if (actual.x, actual.y) == objetivo:
            return actual.obtener_camino()

        h = mat[actual.x][actual.y]
        movimientos = [
            (actual.x, actual.y - h),    # izquierda
            (actual.x + h, actual.y),   # abajo
            
            
            (actual.x, actual.y + h),   # derecha
            (actual.x - h, actual.y),   # arriba
        ]

        for x_nuevo, y_nuevo in movimientos:
            if 0 <= x_nuevo < m and 0 <= y_nuevo < n and (x_nuevo, y_nuevo) not in visitados:
                costo = actual.costo + 1  # Suponemos un costo unitario para moverse
                hijo = Nodo(x_nuevo, y_nuevo, costo=costo, padre=actual)
                pila.append(hijo)

    return None  # Camino no encontrado


mazes = create_m()

for idx, (mat, m, n, posinit_x, posinit_y, posfinal_x, posfinal_y) in enumerate(mazes):
    print(f"Laberinto N°: {idx}")
    running = True
    cell_s_w = width // n     # Tamaño según columnas (ancho)
    cell_s_h = height // m    # Tamaño según filas (alto)
    cell_s = min(cell_s_w, cell_s_h)  # Elegir el más pequeño para que todo encaje
    player_pos, posmat_x, posmat_y = player_posi(mat, n, m, posinit_x, posinit_y)

    print("¿Con qué método quieres resolver el laberinto?")
    print("1: DFS (Búsqueda en Profundidad)")
    print("2: UC (Costo Uniforme)")
    eleccion = input("Escribe 1 o 2: ").strip()

    if eleccion == "1":
        camino = dfs(mat, m, n, (posinit_x, posinit_y), (posfinal_x, posfinal_y))
    elif eleccion == "2":
        camino = uc(mat, m, n, (posinit_x, posinit_y), (posfinal_x, posfinal_y))
    else:
        print("Elección inválida, se usará DFS por defecto.")
        camino = dfs(mat, m, n, (posinit_x, posinit_y), (posfinal_x, posfinal_y))


    if camino:
        print("Camino encontrado con opción: ", eleccion)
        print("Largo del camino: ",len(camino) - 1)
    else:
        print("No se encontró camino.")
        continue




    showing_path = True
    path_index = 0
    path_delay = 1000  # milisegundos entre pasos del camino
    last_step_time = pygame.time.get_ticks()


    while running:
        current_time = pygame.time.get_ticks()
        
        if goal(posmat_x, posmat_y, posfinal_x, posfinal_y) == True:
            running = False


        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill("blue")
    
        draw_rect(mat,m,n, posinit_x, posinit_y, posfinal_x, posfinal_y)

        draw_counter(screen, path_index)
    
    
        #Un delay mientras se muestra el camino
        
        if showing_path and camino:
            current_time = pygame.time.get_ticks()
            if current_time - last_step_time > path_delay:
                if path_index < len(camino):
                    path_index += 1
                    posmat_x, posmat_y = camino[path_index]
                    
                    last_step_time = current_time
                    
                else:
                    showing_path = False  

        posmat_x, posmat_y = mov(mat, m, n, posmat_x, posmat_y)
        
        player_pos, posmat_x, posmat_y = player_posi(mat, n, m, posmat_x, posmat_y)
        pygame.draw.circle(screen, "red", player_pos, 40, width=5)

    

    
    
        # flip() the display to put your work on screen
        pygame.display.flip()



pygame.quit()