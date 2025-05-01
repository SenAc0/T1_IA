import pygame
import time
import heapq

width = 1280
height = 720
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
font = pygame.font.SysFont(None, 48)


delay = 300  # milisegundos
last_press = 0
count = 0



class Nodo:
    def __init__(self, x, y, padre=None, costo = 0):
        self.x = x
        self.y = y
        self.padre = padre
        self.hijos = []  
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
## FUNCIONES PARA RECIBIR Y PROCESAR LABERINTOS 
## FUNCIONES PARA RECIBIR Y PROCESAR LABERINTOS
## FUNCIONES PARA RECIBIR Y PROCESAR LABERINTOS 


# funcion laberintos desde un txt
def create_m_from_file(filename):
    mazes = []
    
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    index = 0
    while index < len(lines):
        r_c = lines[index].strip()
        index += 1

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

        mat = []
        for _ in range(rows):
            row = list(map(int, lines[index].strip().split()))
            mat.append(row)
            index += 1
        
        mazes.append((mat, rows, columns, posinit_x, posinit_y, posfinal_x, posfinal_y))

    return mazes

# funcion laberinto desde la consola
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



## FUNCIONES DE DIBUJADO EN PYGAME
## FUNCIONES DE DIBUJADO EN PYGAME
## FUNCIONES DE DIBUJADO EN PYGAME

# funcion que hace las casillas con su numero correspondiente
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


# funcion que dibuja el contador
def draw_counter(screen, count):
    counter_text = font.render(f"Movimientos: {count}", True, "white")
    screen.blit(counter_text, (20, 20))  # posicion 

# funcion que dibuja los botones
def draw_button(rect, text, color):
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, "white", rect, 3)
    label = font.render(text, True, "white")
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

# funcion que utiliza draw_button para obligar al jugador a elegir antes de empezar
def select_algorithm():
    selecting = True
    dfs_rect = pygame.Rect(width//2 - 250, height//2 - 50, 200, 100)
    uc_rect = pygame.Rect(width//2 + 50, height//2 - 50, 200, 100)

    while selecting:
        screen.fill("black")
        draw_button(dfs_rect, "DFS", (70, 130, 180))
        draw_button(uc_rect, "UC", (34, 139, 34))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if dfs_rect.collidepoint(event.pos):
                    return "dfs"
                elif uc_rect.collidepoint(event.pos):
                    return "uc"

        pygame.display.flip()
        clock.tick(60)

# funcion para dibujar las casillas exploradas (simplemente cambio de color a gris las visitadas, igual que draw_rect en todo lo demas)
def draw_rect_visits(mat, m, n, posinit_x, posinit_y, posfinal_x, posfinal_y, explorados, explorados_index):
    offset_x = (width - n * cell_s) // 2
    offset_y = (height - m * cell_s) // 2

    for i in range(m):
        for j in range(n):
            cell_r = offset_x + j * cell_s
            cell_c = offset_y + i * cell_s
            cell_color = "white"

            # 
            if (i, j) in explorados[:explorados_index]:
                cell_color = (200, 200, 200)  # gris claro para explorados

            rect = pygame.draw.rect(screen, cell_color, (cell_r, cell_c, cell_s, cell_s))
            pygame.draw.rect(screen, (0, 0, 0), rect, width=2)  # borde

            
            if (i == posinit_x and j == posinit_y):
                text = font.render(str(mat[i][j]), True, "blue")
            elif (i == posfinal_x and j == posfinal_y):
                text = font.render(str(mat[i][j]), True, "green")
            else:
                text = font.render(str(mat[i][j]), True, (0, 0, 0))

            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)






##FUNCION DE MOVIMIENTOS Y VERIFICACIONES (RESPECTO A MATRIZ QUE REPRESENTA A LABERINTO)
##FUNCION DE MOVIMIENTOS Y VERIFICACIONES (RESPECTO A MATRIZ QUE REPRESENTA A LABERINTO)
##FUNCION DE MOVIMIENTOS Y VERIFICACIONES (RESPECTO A MATRIZ QUE REPRESENTA A LABERINTO)

# Actualiza posicion visual jugador respecto matriz
def player_posi(mat, n, m, posinit_x, posinit_y):
    offset_x = (width - n*cell_s + cell_s) // 2
    offset_y = (height - m*cell_s+ cell_s) // 2
    posmat_x = posinit_x
    posmat_y = posinit_y
    player_pos = pygame.Vector2(offset_x + (posinit_y)*cell_s, offset_y + (posinit_x)*cell_s) # posinit_y mueve en columnas, posinit_x mueve en filas (por eso estan intercambiados)
    return player_pos, posmat_x, posmat_y



# Hace los movimientos respecto a la matriz (son movimientos del jugador)
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
   
# Verifica estado objetivo
def goal(posactual_x, posactual_y,posfinal_x, posfinal_y):
    if(posactual_x ==  posfinal_x and posactual_y == posfinal_y):
        print("Meta alcanzada")
        return True
    return False

# Cuenta movimientos hechos a mano
def countg():
    global count
    count +=1
    print(count)














## METODOS DE BUSQUEDA
## METODOS DE BUSQUEDA
## METODOS DE BUSQUEDA

# dfs
def dfs(mat, m, n, inicio, objetivo):
    nodo_inicio = Nodo(inicio[0], inicio[1])
    pila = [nodo_inicio]
    visitados = set()
    explorados = []
    while pila:
        actual = pila.pop()
        
        if (actual.x, actual.y) in visitados:
            continue
        visitados.add((actual.x, actual.y))
        explorados.append((actual.x, actual.y))
        #print(actual.x, actual.y)
        if (actual.x, actual.y) == objetivo:
            return explorados, actual.obtener_camino()

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

    return  explorados, None  # camino no encontrado

# uc
def uc(mat, m, n, inicio, objetivo):
    nodo_inicio = Nodo(inicio[0], inicio[1], costo=0)
    pila = [nodo_inicio]
    visitados = set()
    explorados = []
    while pila:
        # Ordenar la pila por costo 
        pila.sort(key=lambda nodo: nodo.costo)
        actual = pila.pop(0)  
        
        if (actual.x, actual.y) in visitados:
            continue
        visitados.add((actual.x, actual.y))
        explorados.append((actual.x, actual.y))
        #print(actual.x, actual.y)

        if (actual.x, actual.y) == objetivo:
            return explorados, actual.obtener_camino()

        h = mat[actual.x][actual.y]
        movimientos = [
            (actual.x, actual.y - h),    # izquierda
            (actual.x + h, actual.y),   # abajo
            
            
            (actual.x, actual.y + h),   # derecha
            (actual.x - h, actual.y),   # arriba
        ]

        for x_nuevo, y_nuevo in movimientos:
            if 0 <= x_nuevo < m and 0 <= y_nuevo < n and (x_nuevo, y_nuevo) not in visitados:
                costo = actual.costo + 1  # un costo unitario para moverse
                hijo = Nodo(x_nuevo, y_nuevo, costo=costo, padre=actual)
                pila.append(hijo)

    return explorados, None  # Camino no encontrado











#Comentar o descomentar dependiendo cual se quiera usar
mazes = create_m_from_file("test_mapas.txt")    #por archivo texto
#mazes = create_m()                             #por terminal

for idx, (mat, m, n, posinit_x, posinit_y, posfinal_x, posfinal_y) in enumerate(mazes):
    print(f"Laberinto N°: {idx}")
    camino = []
    running = True
    cell_s_w = width // n     # Tamaño segun columnas (ancho)
    cell_s_h = height // m    # Tamaño segun filas (alto)
    cell_s = min(cell_s_w, cell_s_h)  # Elegir el más pequeño para que todo encaje
    player_pos, posmat_x, posmat_y = player_posi(mat, n, m, posinit_x, posinit_y)

    

    draw_rect(mat,m,n, posinit_x, posinit_y, posfinal_x, posfinal_y)

    algoritmo = select_algorithm()
    if algoritmo == "dfs":
        explorados, camino = dfs(mat, m, n, (posinit_x, posinit_y), (posfinal_x, posfinal_y))
    elif algoritmo == "uc":
        explorados, camino = uc(mat, m, n, (posinit_x, posinit_y), (posfinal_x, posfinal_y))
    else:
        continue    

    if camino is None:
        print("No se encontró camino.")
        texto = font.render("No se encontró camino, en 2 segundos puedes continuar", True, (255, 255, 255))
        texto_rect = texto.get_rect(center=(width // 2, height // 2 + 100))
        screen.blit(texto, texto_rect)
        pygame.display.flip()
        pygame.time.delay(2000)
        continue
     
    if camino!= None:
        print("Camino encontrado con opción: ", algoritmo)
        print("Largo del camino: ",len(camino) - 1)
        
        
    


    showing_path = True
    path_index = 0
    path_delay = 1000  # milisegundos entre pasos del camino


    explorados_index = 0
    delay_exploracion = 100  # en milisegundos
    last_step_time = pygame.time.get_ticks()
    mostrando_exploracion = False  # para saber si ya pasamos a mostrar el camino

    while running:
        current_time = pygame.time.get_ticks()
        
        
        if goal(posmat_x, posmat_y, posfinal_x, posfinal_y) == True:
            running = False


        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill("blue")
    
        draw_rect(mat,m,n, posinit_x, posinit_y, posfinal_x, posfinal_y)

        draw_counter(screen, path_index)

        #Un delay mientras se muestra la exploracion

        current_time = pygame.time.get_ticks()
        if not mostrando_exploracion and current_time - last_step_time > delay_exploracion:
            if explorados_index < len(explorados):
                explorados_index += 1
                last_step_time = current_time
            else:
                mostrando_exploracion = True  # termina la fase de exploración, inicia camino
                last_step_time = current_time
                path_index = 0
        draw_rect_visits(mat, m, n, posinit_x, posinit_y, posfinal_x, posfinal_y, explorados, explorados_index)

        #Un delay mientras se muestra el camino
        
        if showing_path and camino and mostrando_exploracion:
            current_time = pygame.time.get_ticks()
            if current_time - last_step_time > path_delay:
                if path_index < len(camino):
                    path_index += 1
                    posmat_x, posmat_y = camino[path_index]
                    
                    last_step_time = current_time
                    
                else:
                    showing_path = False  

        #posmat_x, posmat_y = mov(mat, m, n, posmat_x, posmat_y) #descomentar si se quiere mover al jugador de forma manual (lo dejo comentado por defecto para que no afecte a la busqueda)
        
        player_pos, posmat_x, posmat_y = player_posi(mat, n, m, posmat_x, posmat_y)
        pygame.draw.circle(screen, "red", player_pos, 40, width=5)

    
    
        
        pygame.display.flip()



pygame.quit()