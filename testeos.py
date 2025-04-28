import keyboard

def create_m():
    r_c = input()
    r_c = r_c.split()
    rows = int(r_c[0])
    columns = int(r_c[1])
    print(rows, columns)

    mat = []

    for i in range(rows):
        row = input().split()
        row = [int(x) for x in row] 
        mat.append(row)
    return mat, rows, columns


def show_m(mat):
    print("-------------")
    print("Matriz:")
    for fila in mat:
        for elemento in fila:
            print(elemento, end=' ')
        print()
    print("-------------")

def mov(mat, m, n, posx, posy,  x):
    i = posx
    j = posy
    h = mat[i][j]
    print(h)


    #CORREGIR LOGICA

    if x == "a":
        if j-h < 0:
            print("Movimiento no posible")
            return i, j
        else:
            print("Movimiento realizado")
            return i, j-h
    
    if x == "d":
        if j+h >n-1:
            print("Movimiento no posible")
            return i, j
        else:
            print("Movimiento realizado")
            return i, j+h
    if x == "w":
        if i-h < 0:
            print("Movimiento no posible")
            return i, j
        else:
            print("Movimiento realizado")
            return i-h, j
    if x == "s":
        if i+h >m-1:
            print("Movimiento no posible")
            return i, j
        else:
            print("Movimiento realizado")
            return i+h, j


mat, m, n = create_m()
posx = 0
posy = 0
print("Estas en: ", posx, posy)
while True:
    show_m(mat)
    x = input("Ingrese movimiento\n")
    x = str(x)
    posx, posy = mov(mat, m, n, posx, posy, x)
    print("Estas en: ", posx, posy)