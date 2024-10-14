# myChatProtocol [ Proyecto de Telematica ]

Indice
- Introduccion
- Desarrollo
- Aspectos Logrados y no Logrados
- Conclusiones
- Referencias


## Introduccion
En este documento estaremos describiendo los aspectos del proyecto de Telematica. Asi mismo como su desarrollo y su implementacion. El proyecto tiene como objetivo desarrollar una aplicacion de chat utilizando el modelo cliente/servidor. Donde la aplicacion debe ser capaz de gestionar mensajes en tiempo real y trabajar con concurrencia, permitiendo la comunicacion de varios clientes al mismo tiempo.


## 2. Desarrollo
### 2.1  Arquitectura
El sistema esta basado en una arquitectura cliente/servidor, en la cual:
- Las multiples conexiones de clientes son manejadas por un servidor central.
- Los clientes se conectan al servidor para enviar y recibir mensajes.
- Se utilizan sockets TCP para la comunicacion en red.

### 2.2. Protocolo de comunicacion 
Se diseno un protocolo de comunicacion personalizado (MyChatProtocol) para estandarizar la comunicacion entre el cliente y sel servidor. Este protocolo cuenta con caracteristicas basicas y mensajes para:
- Conexion y desconexion de usuarios
- Envio de mensajes privados y mensajes broadcast
- Visualizacion y actualizacion de usuarios conectados
- Manejo de errores basico

### 2.3. Implementacion del servidor
Se desarrollo un servidor capaz de manejar multiples conexiones utilizado threading (hilos). El servidor es responsable de:
- Aceptar nuevas conexiones de clientes
- Procesar los mensajes que llegan
- Distribuir los mensajes a los destinatarios (clientes) apropiados
- Mantener una lista de usuarios conectados
- Verificar que no se repitan nombres de usuario

### 2.4. Implementacion del cliente
Se creo un cliente con una interfaz basica de consola que permite a los usuarios:
- Conectarse al servidor
- Enviar mensajes privados a otros usuarios
- Enviar mensajes de broadcast a todos los usuarios
- Ver la lista de usuarios conectados
- Desconectarse del servidor


## 3. Aspectos logrados y no logrados
### 3.1. Aspectos logrados
- Implementacion de un protocolo de comunicacion personalizado
- Desarrollo de un servidor capaz de manejar conexiones recurrentes
- Creacion de un cliente funcional con interfaz de uso
- Implementacion de mensajes broadcast y mensajes privados entre usuarios
- Manejo basico  de errores y desconexiones inesperadas
- Actualizacion en tiempo real de la lista de usuarios conectados

### 3.1. Aspectos no logrados (o pendientes)
- Interfaz grafica de usuario para el cliente
- Implementacion de salas de chat (Crear y unirse a salas de Chat_
- Persistencia de mensajes e historial de chat
- Metodos de encriptacion de mensajes para mejorar la seguridad de la comunicacion
- Optimizacion para conexiones masivas

## 4. Conclusiones

El desarrollo de este proyecto ha proporcionado conocimiento valioso durante su transcurso. Siendo un excelente ejercicio para aproximarse al desarrollo de aplicaciones de Red. Algunos temas clave que se reforzaron durante el desarrollo fueron:
- Manejo de threading de clientes
- Programacion de Sockets en python
- Manejo de concurrencia mediante threads
- Diseno de arquitectura cliente/servidor
- Diseno de protocolos de comunicacion TCP

## 5. Referencias
1. Python Socket Programming Documentation [https://docs.python.org/3/library/socket.html](https://docs.python.org/3/library/socket.html)
2. Threading in Python https://docs.python.org/es/3.8/library/threading.html
3. Beej's Guide to Network Programming [https://beej.us/guide/bgnet/](https://beej.us/guide/bgnet/)
4.  Socket Programming in Python (Guide)https://realpython.com/python-sockets/
