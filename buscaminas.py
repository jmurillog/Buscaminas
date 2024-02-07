# JUEGO BUSCA MINAS
# El juego planta un numero de bombas x en un plano (matriz)
# Cada celda que no es bomba tiene que poner cuantas bombas tiene al rededor
# Si no hay bombas al rededor poner 0

from random import randint


class Logic:
    def contar_bombas(self, plano, dimension):
        for i, row in enumerate(plano):
            for j, value in enumerate(row):
                num = 0
                if value != "B" and i > 0 and j > 0 and i < (len(row) - 1) and j < (len(row) - 1):
                    for b in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1), (1, 1), (-1, -1)]:
                        if plano[i + b[0]][j + b[1]] == "B":
                            num += 1
                    plano[i][j] = str(num)
        return plano[1:dimension]

    def crear_plano_bombas(self, dimension):
        plano = [[0 for _ in range(dimension + 1)] for _ in range(dimension + 1)]
        bombas = []
        porcentaje = int(dimension * dimension * 0.1)
        while len(bombas) < porcentaje:
            bomb = (randint(1, dimension - 1)), (randint(1, dimension - 1))
            if bomb not in bombas:
                bombas.append(bomb)
        for bomba in bombas:
            plano[bomba[0]][bomba[1]] = "B"
        nuevo = self.contar_bombas(plano, dimension)
        plano_final = [i[1:dimension] for i in nuevo]
        return (plano_final, porcentaje)

    def plano_oculto(self, dimension):
        return [["x" for _ in range(dimension - 1)] for _ in range(dimension - 1)]

    def hacer_plano_oculto(self, oculto, plano, descubiertas):
        for casilla in descubiertas:
            oculto[casilla[0]][casilla[1]] = plano[casilla[0]][casilla[1]]
        return oculto

    def descubrir_ceros(self, descubiertas, row, col, plano, dimension):
        descubiertas.append((row, col))
        if plano[row][col] == "0":
            por_ver = [(row, col)]
            while por_ver:
                casilla = por_ver.pop(0)
                for i in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1), (1, 1), (-1, -1)]:
                    if -1 < casilla[0] + i[0] < (dimension - 1) and -1 < casilla[1] + i[1] < (dimension - 1):
                        if plano[casilla[0] + i[0]][casilla[1] + i[1]] == "0":
                            if (casilla[0] + i[0], casilla[1] + i[1]) not in descubiertas:
                                por_ver.append((casilla[0] + i[0], casilla[1] + i[1]))
                                descubiertas.append((casilla[0] + i[0], casilla[1] + i[1]))
                        else:
                            if (casilla[0] + i[0], casilla[1] + i[1]) not in descubiertas:
                                descubiertas.append((casilla[0] + i[0], casilla[1] + i[1]))

    def ganado(self, descubiertas, dimension, n_bombas):
        return len(descubiertas) == ((dimension - 1) * (dimension - 1) - n_bombas)


class Imprimir:
    def imp_dimension(self):
        return int(input("Que tamaño deseas: ")) + 1

    def imp_row_col(self):
        row = int(input("Elige fila: ")) - 1
        col = int(input("Elige columna: ")) - 1
        return (row, col)

    def imp_plano(self, plano):
        columnas = "   "
        for i in range(len(plano)):
            if i < 10:
                espacio = "    "
            elif i < 100:
                espacio = "   "
            else:
                espacio = "  "
            columnas += f"{espacio}{i+1}"
        print(columnas)
        for i, row in enumerate(plano):
            print(i + 1, "\t", row, i + 1)
        print(columnas)

    def imp_repetida(self):
        print("Ya habías seleccionado esta casilla antes!")

    def imp_fin(self):
        print("El juego ha terminado!")

    def imp_bombas(self, n_bombas):
        print(f"Hay {n_bombas} bombas")

    def imp_otra(self):
        return input("Quieres jugar otra vez? (y/n): ").lower()

    def imp_ganado(self):
        print("Has ganado!!!")

def main():
    Brain = Logic()
    Log = Imprimir()

    dimension = Log.imp_dimension()
    plano, n_bombas = Brain.crear_plano_bombas(dimension)
    oculto = Brain.plano_oculto(dimension)
    descubiertas = []

    otra = True
    game = True
    Log.imp_bombas(n_bombas)
    Log.imp_plano(oculto)
    while otra:
        while game:
            row, col = Log.imp_row_col()
            if plano[row][col] == "B":
                oculto[row][col] = "BOMBA"
                game = False
            elif (row, col) in descubiertas:
                Log.imp_repetida()
            else:
                Brain.descubrir_ceros(descubiertas, row, col, plano, dimension)
                oculto = Brain.hacer_plano_oculto(oculto, plano, descubiertas)
                if Brain.ganado(descubiertas, dimension, n_bombas):
                    Log.imp_ganado()
                    game = False
            Log.imp_bombas(n_bombas)
            Log.imp_plano(oculto)
        if Log.imp_otra() == "n":
            otra = False
    Log.imp_fin()


main()
