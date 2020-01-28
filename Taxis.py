from threading import Thread, Lock
from math import sqrt
from time import sleep
import random
from sys import argv


class Celda:
    def __init__(self):
        # Variable que almacena el taxi
        self.taxi = None
        # Lista de clientes
        self.clientes = []
        # Mutex de la celda
        self.mutex = Lock()

    def add_taxi(self, taxi):
        """Introduce el taxi pasado por argumento en la celda."""
        self.taxi = taxi

    def remove_taxi(self):
        """Elimina el taxi existente en la celda."""
        self.taxi = None

    def add_cliente(self, cliente):
        """Introduce el taxi pasado por argumento en la celda."""
        self.clientes.append(cliente)

    def pop_cliente(self):
        """Saca uno de los clientes de la celda."""
        return self.clientes.pop(0)

    def remove_cliente(self, cliente):
        """Saca de la celda al cliente pasado como argumento."""
        self.clientes.remove(cliente)

    def lock_mutex(self):
        """Bloquea el mutex de la celda."""
        self.mutex.acquire()

    def release_mutex(self):
        """Libera el mutex de la celda."""
        self.mutex.release()


class Cliente:
    def __init__(self, id_):
        # Identificador del cliente
        self.id = id_
        # No ha sido recogido por ningun taxi
        self.taken = 0
        # El cliente esta vivo
        self.vivo = 1
        # Tupla con las coordenadas de origen
        self.origen = (0, 0)
        # Tupla con las coordenadas de destino
        self.destino = (0, 0)

    def vive(self):
        """Ciclo de vida del cliente."""

        # Bloquea el mutex global
        lock.acquire()
        # Genera posiciones aleatorias de origen y destino
        self.origen = random_position()
        self.destino = random_position()
        # Si el origen y el destino son iguales, vuelve a generar el destino hasta que sean distintos
        while self.origen == self.destino:
            self.destino = random_position()
        # Se mete en la matriz
        self.entrar()
        # Pide un taxi para que le lleve a su destino
        if verbose_mode != 2:
            self.pedir_taxi()
        # Libera el mutex global
        lock.release()

        # Mientras este vivo
        while self.vivo == 1:
            # Mientras no haya sido recogido ni haya llegado a su destino
            while self.taken == 0 and self.ha_llegado() == 0:
                sleep(0.6)

                # Obtiene las coordenadas de las celdas adyacentes
                celdas_ady = get_celdas_ady(self.origen[0], self.origen[1])

                # Bloquea el mutex en las celdas adyacentes
                for (x, y) in celdas_ady:
                    matriz[x][y].lock_mutex()

                # Si no ha sido recogido por ningun taxi mientras bloqueaba los mutex
                if self.taken == 0:
                    # Sale de su celda
                    self.salir()
                    # Se calcula el siguiente movimiento de forma aleatoria
                    self.origen = random_move(celdas_ady)
                    # Se mueve a la nueva posicion
                    self.entrar()

                    # Si está en modo verbose, imprime por pantalla el estado del cliente
                    if verbose_mode == 1:
                        self.mostrar_estado()

                # Libera el mutex en las celdas adyacentes
                for (x, y) in celdas_ady:
                    matriz[x][y].release_mutex()

            # Si llega a pie al destino
            if self.ha_llegado() == 1:
                print("Soy {0} y he llegado a pie mi destino ({1}, {2}). ".format(str(self.id), str(self.destino[0]),
                                                                                  str(self.destino[1])))
                # Bloquea el mutex global
                lock.acquire()
                # Genera nuevas posiciones aleatorias de origen y destino
                self.origen = random_position()
                self.destino = random_position()
                # Si el origen y el destino son iguales, vuelve a generar el destino hasta que sean distintos
                while self.origen == self.destino:
                    self.destino = random_position()
                global num_clientes
                # Incrementa el numero de clientes
                num_clientes += 1
                self.id = "Cliente " + str(num_clientes - 1)
                # Se mete en la matriz
                self.entrar()
                if verbose_mode != 2:
                    self.pedir_taxi()
                # Libera el mutex global
                lock.release()

    def pedir_taxi(self):
        """Imprime por pantalla la posicion y destino del cliente y pide un taxi."""
        print("Soy {0} y estoy en ({1}, {2}), mi destino es ({3}, {4}). TAXIII!!!".format(str(self.id),
                                                                                          str(self.origen[0]),
                                                                                          str(self.origen[1]),
                                                                                          str(self.destino[0]),
                                                                                          str(self.destino[1])))

    def mostrar_estado(self):
        """Imprime por pantalla la posicion y destino del cliente."""
        print("Soy {0} y estoy en ({1}, {2}), mi destino es ({3}, {4}).".format(str(self.id), str(self.origen[0]),
                                                                                str(self.origen[1]),
                                                                                str(self.destino[0]),
                                                                                str(self.destino[1])))

    def ha_llegado(self):
        """Devuelve 1 si el cliente ha llegado al destino por su propio pie."""
        return 1 if (self.origen[0] == self.destino[0] and self.origen[1] == self.destino[1]) else 0

    def salir(self):
        """El cliente sale de la celda."""
        # Obtiene la lista de clientes que hay en la celda
        matriz[self.origen[0]][self.origen[1]].remove_cliente(self)

    def entrar(self):
        """El cliente entra en la celda."""
        matriz[self.origen[0]][self.origen[1]].add_cliente(self)


class Taxi:
    def __init__(self, id_):
        self.id = id_
        self.busy = 0
        self.origen = (0, 0)
        self.destino = (0, 0)
        self.cliente = None
        self.num_clientes = 0

    def empieza_servicio(self):
        """Ciclo de vida del taxi. """

        # Genera una posicion aleatoria de origen
        origen = random_position()
        # Bloquea el mutex global
        lock.acquire()
        # Vuelve a generar la posicion de origen mientras en la generada haya ya un taxi
        while hay_taxi(origen):
            origen = random_position()
        # Toma como origen una posicion vacia
        self.origen = origen
        # Se mete en dicha posicion
        self.add_taxi()
        # Libera el mutex global
        lock.release()

        global game_end
        # Mientras no se haya terminado el juego
        while game_end == 0:

            # Obtiene las posiciones de las celdas adyacentes disponibles
            pos_coord = self.get_pos_coord()
            # Bloquea el mutex de dichas celdas adyacentes
            for (x, y) in pos_coord:
                matriz[x][y].lock_mutex()
            # Si hay un cliente en su celda, lo recoge
            if self.hay_cliente():
                self.coger_cliente()
            # Libera los mutex
            for (x, y) in pos_coord:
                matriz[x][y].release_mutex()

            # Mientras esta libre y el juego no ha terminado
            while self.busy == 0 and game_end == 0:
                sleep(0.1)
                # Obtiene las posiciones de las celdas adyacentes disponibles
                pos_coord = self.get_pos_coord()
                # Bloquea el mutex de dichas celdas adyacentes
                for (x, y) in pos_coord:
                    matriz[x][y].lock_mutex()
                # Obtiene las coordenadas de uno de los clientes adyacentes, (-1, -1) si no hay
                adj_client = is_adjacent_client(pos_coord)
                # Si hay algun cliente en las adyacentes, toma la posicion de este para moverse a su celda
                if adj_client != (-1, -1):
                    new_x = adj_client[0]
                    new_y = adj_client[1]
                # Si no, se dirige a una al azar de las disponibles
                else:
                    new = random.choice(pos_coord)
                    new_x = new[0]
                    new_y = new[1]
                # Sale de la celda
                self.remove_taxi()
                # Guarda la posicion de la celda a la que se va a mover
                self.origen = (new_x, new_y)
                # Se mete en la celda
                self.add_taxi()

                # Si hay un cliente en la celda, lo recoge
                if self.hay_cliente():
                    self.coger_cliente()
                else:
                    if verbose_mode == 1:
                        self.mostrar_estado()
                # Libera los mutex
                for (x, y) in pos_coord:
                    matriz[x][y].release_mutex()

            # Mientras esta ocupado
            while self.busy == 1 and game_end == 0:
                sleep(0.1)
                # Mientras no haya llegado al origen
                while self.origen[0] != self.destino[0] or self.origen[1] != self.destino[1] and game_end == 0:
                    # Obtiene las posiciones de las celdas adyacentes disponibles
                    next_coord = self.get_pos_coord()
                    # Bloquea el mutex de dichas celdas adyacentes
                    for (x, y) in next_coord:
                        matriz[x][y].lock_mutex()
                    # Ordenamos las coordenadas por cercania al destino
                    next_move = sorted(next_coord, key=self.euclidean_distance)[0]
                    # Sale de la celda
                    self.remove_taxi()
                    # Guarda la posicion de la celda a la que se va a mover
                    self.origen = (next_move[0], next_move[1])
                    # Se mete en la celda
                    self.add_taxi()

                    if verbose_mode == 1:
                        self.mostrar_estado_trayecto()
                    # Libera los mutex
                    for (x, y) in next_coord:
                        matriz[x][y].release_mutex()

                # Si llega al destino
                if self.origen[0] == self.destino[0] and self.origen[1] == self.destino[1]:
                    # Vuelve a estar libre
                    self.busy = 0
                    # Se suma un cliente al contador
                    self.num_clientes += 1
                    lock.acquire()
                    # Muestra por pantalla que ha dejado al taxi y el numero de carreras que lleva realizadas
                    out = "Soy " + str(self.id) + " y dejo a " + str(self.cliente.id) + " en (" + str(self.origen[0]) \
                          + ", " + str(self.origen[1]) + "), he realizado "
                    if self.num_clientes != 1:
                        out += str(self.num_clientes) + " carreras. "
                    else:
                        out += " 1 carrera."
                    # No lleva ningun cliente
                    self.cliente = None
                    print(out)

                    # Si ha conseguido 10 clientes
                    if self.num_clientes == 10:
                        # Informa de que ha ganado
                        print("SE ACABÓ EL JUEGO. EL GANADOR ES {0}. ".format(str(self.id)))
                        # Se acaba el juego
                        game_end = 1
                    # Si ha dejado a un cliente pero aún no ha ganado, crea uno nuevo
                    else:
                        crear_cliente()
                    lock.release()

    def euclidean_distance(self, celda):
        """Devuelve la distancia euclidea entre el destino y la celda pasada como argumento."""
        return sqrt((self.destino[0] - celda[0]) ** 2 + (self.destino[1] - celda[1]) ** 2)

    def hay_cliente(self):
        """Devuelve 1 si hay un cliente en la celda del taxi, 0 en caso contrario."""
        return 1 if len(matriz[self.origen[0]][self.origen[1]].clientes) > 0 else 0

    def saludar(self):
        """Imprime por pantalla su identificador y su posicion."""
        print("Soy " + str(self.id) + " y estoy en (" + str(self.origen[0]) + ", " + str(self.origen[1]) + "). ")

    def add_taxi(self):
        """Se mete en su nueva celda."""
        matriz[self.origen[0]][self.origen[1]].add_taxi(self)

    def remove_taxi(self):
        """Sale de su celda."""
        matriz[self.origen[0]][self.origen[1]].remove_taxi()

    def remove_cliente(self):
        """Saca un cliente de su celda."""
        return matriz[self.origen[0]][self.origen[1]].pop_cliente()

    def get_pos_coord(self):
        """Devuelve las celdas adyacentes a las que sea posible moverse."""
        # Obtiene todas las celdas adyacentes
        celdas_ady = get_celdas_ady(self.origen[0], self.origen[1])
        ret = []
        # Guarda en la lista aquellas que no tienen un taxi y la celda actual
        for (x, y) in celdas_ady:
            if matriz[x][y].taxi is None or matriz[x][y].taxi == self:
                ret.append((x, y))
        return ret

    def coger_cliente(self):
        """Recoge a un cliente de su celda, sacando a este de su celda y marcandolo como no vivo. El taxi pasa a estar
        ocupado y toma como destino el destino del cliente. Imprime por pantalla que ha recogido al cliente."""
        # Esta ocupado
        self.busy = 1
        # Saca al cliente de la celda
        cl = self.remove_cliente()
        # El cliente ha sido recogido
        cl.taken = 1
        # El cliente deja de estar vivo
        cl.vivo = 0
        # Guarda al cliente
        self.cliente = cl
        # Adquiere el destino del cliente
        self.destino = (cl.destino[0], cl.destino[1])
        # Informa por pantalla
        print("Soy {0} y cogí a {5} en ({1}, {2}), le llevo a ({3}, {4})".format(str(self.id), str(self.origen[0]),
                                                                                 str(self.origen[1]),
                                                                                 str(self.destino[0]),
                                                                                 str(self.destino[1]), str(cl.id)))

    def mostrar_estado_trayecto(self):
        """Imprime por pantalla la posicion del taxi y su destino."""
        print("Soy {0} y estoy en ({1}, {2}), llevo a {5} a ({3}, {4})"
              .format(str(self.id), str(self.origen[0]), str(self.origen[1]), str(self.destino[0]),
                      str(self.destino[1]), str(self.cliente.id)))

    def mostrar_estado(self):
        """Imprime por pantalla la posicion del taxi."""
        print("Soy {0} y estoy en ({1}, {2}).".format(str(self.id), str(self.origen[0]), str(self.origen[1])))


def is_adjacent_client(pos_coord):
    """Devuelve las coordenadas de un cliente, si es que hay uno en las coordenadas adyacentes, o (-1, -1) en caso
    contrario."""
    for (x, y) in pos_coord:
        if len(matriz[x][y].clientes) > 0:
            return x, y
    return -1, -1


def random_move(moves):
    """Devuelve una celda aleatoria de las pasadas como parametro."""
    return moves[random.randint(0, len(moves) - 1)]


def crear_cliente():
    """Crea un nuevo cliente."""
    # Incrementa el numero de cliente para crear el identificador
    global num_clientes
    num_clientes += 1
    id_ = "Cliente " + str(num_clientes - 1)
    Thread(target=constructor_cliente, args=(id_,)).start()


def hay_taxi(coord):
    """Devuelve 1 si hay un taxi en la posicion dada, 0 en caso contrario."""
    return 1 if matriz[coord[0]][coord[1]].taxi is not None else 0


def get_adj_coord(coord):
    """Devuelve las posiciones adyacentes en el eje dado."""
    # Si no esta en los bordes
    if coord != 0 and coord != len(matriz) - 1:
        # Tiene 3 posibles movimientos
        return [coord - 1, coord, coord + 1]
    # Si esta a la izquierda
    elif coord == 0:
        # Tiene 2 posibles movimientos
        return [coord, coord + 1]
    # Si esta a la derecha
    else:
        # Tiene 2 posibles movimientos
        return [coord - 1, coord]


def get_celdas_ady(x, y):
    """Devuelve una lista de tuplas con las celdas adyacentes a las coordenadas dadas."""
    return [(a, b) for a in get_adj_coord(x) for b in get_adj_coord(y)]


def random_position():
    """Devuelve una tupla con una posicion aleatoria del entorno."""
    return random.randint(0, len(matriz) - 1), random.randint(0, len(matriz) - 1)


def constructor_cliente(id_):
    """Crea un cliente con el id pasado por parametro y le da vida"""
    c_ = Cliente(id_)
    c_.vive()


def constructor_taxi(id_):
    """Crea un taxi con el id pasado por parametro y lo pone a trabajar"""
    t_ = Taxi(id_)
    t_.empieza_servicio()


if __name__ == '__main__':

    # Crea el mutex
    lock = Lock()
    # Dimensión de la matriz
    m = 50
    # Inicializa la matriz
    matriz = [[Celda() for x in range(m)] for y in range(m)]
    # Variable que controla el fin del juego
    game_end = 0
    # Lista que contiene los taxis
    lista_taxis = []
    # Lista que contiene los clientes
    lista_clientes = []

    # Modo verbose, que permite ver por pantalla cualquier cosa que suceda en el entorno
    verbose_mode = 0
    # Se activa si ejecutamos el programa con un argumento especifico
    if len(argv) > 1:
        if argv[1] == "--verbose" or argv[1] == "-v":
            verbose_mode = 1
        elif argv[1] == "--simple" or argv[1] == "-s":
            verbose_mode = 2

    print("\n###### EL JUEGO DEL TAXISTA ######\n")
    # Pide el número de taxis por pantalla
    num_taxis = input('¿Cuántos taxis quieres que haya? \n')
    # Mientras no se introduzca un dígito
    while not num_taxis.isdigit():
        # se informa del error
        print("El caracter introducido no es un número entero positivo, vuelve a intentarlo. ")
        # y se vuelve a pedir
        num_taxis = input('¿Cuántos taxis quieres que haya? \n')
    num_taxis = int(num_taxis)
    # Pide el numero de clientes por pantalla
    num_clientes = input('¿Cuántos clientes quieres que haya? \n')
    while not num_clientes.isdigit():
        print("El caracter introducido no es un número entero positivo, vuelve a intentarlo. ")
        num_clientes = input('¿Cuántos clientes quieres que haya? \n')
    num_clientes = int(num_clientes)
    print()

    # Crea los procesos Cliente
    for c in range(num_clientes):
        id_c = "Cliente " + str(c)
        # Crea el hilo con el cliente
        lista_clientes.append(Thread(target=constructor_cliente, args=(id_c,)))

    # Crea los procesos Taxi
    for t in range(num_taxis):
        id_t = "Taxi " + str(t)
        # Crea el hilo con el taxi
        lista_taxis.append(Thread(target=constructor_taxi, args=(id_t,)))

    for clien in lista_clientes:
        # Declaramos los hilos como daemon
        clien.daemon = True
        # y les damos vida
        clien.start()

    for tax in lista_taxis:
        # Declaramos los hilos como daemon
        tax.daemon = True
        # y les damos vida
        tax.start()

    # El programa sigue vivo mientras no se cambie el valor de la variable
    while game_end == 0:
        pass
