# El juego del taxista

![taxi](https://user-images.githubusercontent.com/48054735/123552650-5ad63580-d777-11eb-9663-3cb45dad8428.jpg)

## 1. Objetivo

Implementación de *El juego del taxista* mediante *multithreading* en Python. En este juego, los taxis compiten por conseguir clientes a los que llevar a su destino. El primer taxista que recoja y lleve a su destino a 10 clientes gana el juego.

## 2. Restricciones

El juego tiene las siguientes restricciones:

-   Se debe representar el entorno mediante una matriz de 50 x 50 que contenga a los clientes y los taxis.

-   El número de clientes y taxis debe ser configurable al comenzar el juego. El número de taxis y clientes será siempre constante.

-   Los taxis y clientes se crean en posiciones aleatorias al comenzar el juego.

-   Solo puede haber un taxi en cada celda, los clientes sí pueden solaparse.

-   Los clientes van andando, por lo que deben ser mucho más lentos que los taxistas en sus movimientos.

-   Cada vez que un cliente llegue a su destino, ya sea llevado por un taxi o por su propio pie, este debe desaparecer del entorno y que sea creado uno nuevo en una posición aleatoria.

-   Un taxi no puede llevar más de un cliente cada vez.

-   Los movimientos permitidos son a las celdas adyacentes (también se puede mover en diagonal) incluida la casilla actual, respetando las restricciones anteriores.

-   Se debe mostrar por pantalla cuando un cliente solicita un taxi, el movimiento del cliente y cuando un taxi recoge y deja a un cliente, identificando siempre al cliente y al taxi.

-   Se deben utilizar procesos o hilos para simular los taxis y clientes.

-   El acceso al entorno de juego por parte de los participantes debe ser en exclusión mutua.

## 3. Ejecución

Ejecutar el siguiente mandato en la terminal:

<code>>$ python taxis.py [args]</code>
donde los argumentos son opcionales y son los siguientes:

-   <code>–verbose</code> o <code>-v</code>: Se muestran por pantalla todos los sucesos.

-   <code>–simple</code> o <code>-s</code>: Se muestra por pantalla únicamente cuando un taxi recoge un cliente y le deja en su destino.

Solo se puede ejecutar con uno de estos argumentos. Si se ejecuta sin argumentos, además de imprimir los sucesos que se muestran en <code>–simple</code>, se muestran las posiciones de los clientes creados.

## 4. Implementación y decisiones de diseño

Véase el documento *practica4.pdf*.
