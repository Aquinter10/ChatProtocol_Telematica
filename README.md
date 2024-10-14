# myChatProtocol [ Proyecto de Telemática ]

Indice
- Introducción
- Desarrollo
- Aspectos Logrados y no Logrados
- Conclusiones
- Referencias


## Introducción
En este documento estaremos describiendo los aspectos del proyecto de Telemática. Así mismo como su desarrollo y su implementación. El proyecto tiene como objetivo desarrollar una aplicación de chat utilizando el modelo cliente/servidor. Donde la aplicación debe ser capaz de gestionar mensajes en tiempo real y trabajar con concurrencia, permitiendo la comunicación de varios clientes al mismo tiempo.


## 2. Desarrollo
### 2.1  Arquitectura
El sistema esta basado en una arquitectura cliente/servidor, en la cual:
- Las multiples conexiones de clientes son manejadas por un servidor central.
- Los clientes se conectan al servidor para enviar y recibir mensajes.
- Se utilizan sockets TCP para la comunicación en red.

### 2.2. Protocolo de comunicación 
Se diseño un protocolo de comunicación personalizado (MyChatProtocol) para estandarizar la comunicación entre el cliente y el servidor. Este protocolo cuenta con características básicas y mensajes para:
- Conexión y desconexion de usuarios
- Envió de mensajes privados y mensajes broadcast
- Visualización y actualización de usuarios conectados
- Manejo de errores básico

### 2.3. Implementación del servidor
Se desarrollo un servidor capaz de manejar multiples conexiones utilizado threading (hilos). El servidor es responsable de:
- Aceptar nuevas conexiones de clientes
- Procesar los mensajes que llegan
- Distribuir los mensajes a los destinatarios (clientes) apropiados
- Mantener una lista de usuarios conectados
- Verificar que no se repitan nombres de usuario

### 2.4. Implementación del cliente
Se creo un cliente con una interfaz básica de consola que permite a los usuarios:
- Conectarse al servidor
- Enviar mensajes privados a otros usuarios
- Enviar mensajes de broadcast a todos los usuarios
- Ver la lista de usuarios conectados
- Desconectarse del servidor


## 3. Especificación del Protocolo myChatProtocol
### 3.1 Conceptos basicos
#### 3.1.1 Codificación de los mensajes
Todos los mensajes se codifican utilizando UTF-8.
#### 3.1.2 Tamaño maximo de mensaje 
El tamano maximo de un mensaje es de 1024 Bytes.

#### 3.1.3 Esctructura del mensaje:
Los mensajes tienen la siguiente estructura:

``COMANDO|PARÁMETRO1|PARÁMETRO2|...|PARAMETROn``

- El primer campo siempre es el Comando.
- Los campos estan separados por el caracter `|` (Pipe).
- El numero de parametros depende del comando en particular.

### 3.2 Comandos del protocolo

#### 3.2.1. CONNECT

Usado por el cliente para conectarse al servidor.

Formato: `CONNECT|username`

Ejemplo: `CONNECT|Alice`

#### 3.2.2. CONNECT_ACK

Respuesta del servidor a una solicitud de conexión.

Formato: `CONNECT_ACK|status`

Ejemplo: `CONNECT_ACK|OK` o `CONNECT_ACK|FAIL`

#### 3.2.3. DISCONNECT

Usado por el cliente para desconectarse del servidor.

Formato: `DISCONNECT`

#### 3.2.4. MESSAGE

Usado para enviar un mensaje privado a un usuario específico.

Formato: `MESSAGE|recipient|content`

Ejemplo: `MESSAGE|Bob|Hola, ¿cómo estás?`

#### 3.2.5. BROADCAST

Usado para enviar un mensaje a todos los usuarios conectados.

Formato: `BROADCAST|content`

Ejemplo: `BROADCAST|Hola a todos`

#### 3.2.6. USER_LIST

Enviado por el servidor para actualizar la lista de usuarios conectados.

Formato: `USER_LIST|user1,user2,user3,...`

Ejemplo: `USER_LIST|Alice,Bob,Charlie`

#### 3.2.7. ERROR

Usado para notificar errores.

Formato: `ERROR|error_code|error_message`

Ejemplo: `ERROR|404|Usuario no encontrado`


### 3.3. Flujo de comunicación
#### 3.3.1. Conexión
```flow
    Cliente -->|CONNECT| Servidor
    Servidor -->|CONNECT_ACK|OK| Cliente
    Servidor -->|CONNECT_ACK|FAIL| Cliente
    Servidor -->|USER_LIST|user1,user2,...| Cliente

```

1.  Cliente envía: `CONNECT|username`
2.  Servidor responde: `CONNECT_ACK|OK` o `CONNECT_ACK|FAIL`
3.  Si la conexión es exitosa, el servidor envía: `USER_LIST|user1,user2,...`

#### 3.3.2. Envío de Mensaje Privado

1.  Cliente envía: `MESSAGE|recipient|content`
2.  Servidor reenvía al destinatario: `MESSAGE|sender|content`

#### 3.3.3. Envío de Broadcast

1.  Cliente envía: `BROADCAST|content`
2.  Servidor reenvía a todos los clientes: `BROADCAST|sender|content`

#### 3.3.4. Desconexión

1.  Cliente envía: `DISCONNECT`
2.  Servidor cierra la conexión y envía una `USER_LIST` actualizada a los demás clientes



## 4. Aspectos logrados y no logrados
### 4.1. Aspectos logrados
- Implementación de un protocolo de comunicación personalizado
- Desarrollo de un servidor capaz de manejar conexiones recurrentes
- Creación de un cliente funcional con interfaz de uso
- Implementación de mensajes broadcast y mensajes privados entre usuarios
- Manejo básico  de errores y desconexiones inesperadas
- Actualización en tiempo real de la lista de usuarios conectados

### 4.2. Aspectos no logrados (o pendientes)
- Interfaz grafica de usuario para el cliente
- Implementación de salas de chat (Crear y unirse a salas de Chat_
- Persistencia de mensajes e historial de chat
- Métodos de encriptado de mensajes para mejorar la seguridad de la comunicación
- Optimización para conexiones masivas

## 5. Conclusiones

El desarrollo de este proyecto ha proporcionado conocimiento valioso durante su transcurso. Siendo un excelente ejercicio para aproximarse al desarrollo de aplicaciones de Red. Algunos temas clave que se reforzaron durante el desarrollo fueron:
- Manejo de threading de clientes
- Programación de Sockets en python
- Manejo de concurrencia mediante threads
- Diseño de arquitectura cliente/servidor
- Diseño de protocolos de comunicación TCP/IP

## 6. Referencias
1. Python Socket Programming Documentation [https://docs.python.org/3/library/socket.html](https://docs.python.org/3/library/socket.html)
2. Threading in Python https://docs.python.org/es/3.8/library/threading.html
3. Beej's Guide to Network Programming [https://beej.us/guide/bgnet/](https://beej.us/guide/bgnet/)
4.  Socket Programming in Python (Guide)https://realpython.com/python-sockets/
