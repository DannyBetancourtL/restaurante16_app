# UNIVERSIDAD ESTATAL AMAZONICA

Carrera de Tecnologias de la Informacion
Programacion Orientada a Objetos

Profesor: Mgs. Luis Antonio Llerena Ocaña
Alumno: Danny Henry Betancourt Luzon

USUARIOS DEL SISTEMA
Danny Betancourt  Administrador
USUARIO: 1101234567 contraseña 1234
Carlos Perez rol Empleado
USUARIO: 1107654321, contraseña 1234
Maria Jaramillo rol Cliente
USUARIO:1123456789, contraseña 1234, 
---

# Sistema de Restaurante - restaurante_app

## De que se trata esta entrega

Esta semana se siguio trabajando sobre el mismo proyecto de siempre, sin
reconstruir nada. Se conserva el login, el menu lateral, la gestion de
productos, el registro de ventas y la identidad visual con el logo de
fondo. Lo que cambio fue la seccion Usuarios: antes se manejaba con un
formulario y botones sueltos (Registrar, Cargar, Actualizar, Eliminar,
Limpiar), y ahora pasa a responder tambien a eventos directos sobre la
tabla y el teclado, ademas de incorporar un rol para cada persona.

La idea de esta semana era justamente esa: ver la diferencia entre un
boton con command= y un evento capturado con bind(), y como ambos
terminan llamando a los mismos metodos del servicio sin repetir logica.

## Roles

Se agrego el atributo rol al modelo Usuario, con tres valores posibles:
Administrador, Empleado y Cliente.

Solo quien tiene el rol Administrador ve la opcion Usuarios en el menu
lateral y puede entrar a esa gestion. Un Empleado o un Cliente ven
Productos y Ventas igual que siempre, pero no tienen acceso a la
administracion de usuarios.

Desde el formulario de Usuarios no se pueden crear cuentas nuevas con
rol Administrador, para evitar que cualquiera se de permisos de
administrador por accidente. Tampoco se permite que la cuenta con la que
se inicio sesion se cambie su propio rol, ni que se elimine a si misma
mientras esta conectada. Estas tres reglas se revisan en
RestauranteServicio, no en la interfaz.

## Lo que cambio en la gestion de usuarios

La tabla de usuarios ahora responde directamente al hacer clic en una
fila: no hace falta escribir el identificador ni presionar un boton
Cargar, los datos de esa persona aparecen solos en el formulario. El
boton Cargar que existia antes ya no hace falta y se quito.

Tambien se puede presionar Enter desde cualquier campo del formulario
para registrar, y Escape para limpiar todo y quitar la seleccion de la
tabla. El selector de rol avisa cuando cambia de opcion.

Los botones Registrar, Actualizar, Eliminar y Limpiar se mantienen
como estaban, usando command=.

## Eventos que se usaron y donde

<<TreeviewSelect>>: se asocia a la tabla de usuarios con bind(). Cuando
se selecciona una fila, se toma el identificador de esa fila, se busca
el usuario completo con RestauranteServicio y se llenan los campos del
formulario. La tabla nunca guarda la contraseña, asi que ese dato se
obtiene siempre desde el servicio, no desde lo que se ve en pantalla.

<Return>: se asocia a cada campo del formulario. Al presionarlo se
llama al mismo metodo que usa el boton Registrar, no se repite la
logica en otro lado.

<Escape>: se asocia tambien a los campos del formulario. Llama al mismo
metodo que usa el boton Limpiar.

<<ComboboxSelected>>: se asocia al selector de rol. Cuando cambia de
valor, se muestra un mensaje simple confirmando el rol elegido.

## Como quedo el flujo

Se selecciona una fila en la tabla, eso dispara el evento
<<TreeviewSelect>>, bind() ejecuta el callback correspondiente, ese
callback le pide el usuario a RestauranteServicio usando el
identificador de la fila, y el resultado se muestra llenando el
formulario. Para guardar un cambio, se presiona Actualizar (o Enter),
eso llama al servicio, el servicio valida las reglas, guarda en
usuarios.json, y la tabla se vuelve a dibujar con la informacion
actualizada.

## Estilo visual

La pantalla de acceso se rehizo como una tarjeta blanca centrada, con el
logo arriba, el nombre del sistema, los campos de identificacion y
contraseña con una linea debajo en vez de un recuadro completo, y un
boton celeste de ancho completo para iniciar sesion. El resto de la
aplicacion (encabezado, menu lateral, formularios, tablas) se paso a
una paleta de colores pastel en tonos verde agua y crema, en vez de los
colores oscuros que tenia antes. Los iconos del menu y el logo siguen
siendo los mismos archivos de la carpeta assets que ya se usaban.

## Estructura del proyecto

```
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── fondo_marca_agua.py
│   ├── login_view.py
│   └── main_view.py
├── assets/
│   ├── icons/
│   │   ├── productos.png
│   │   ├── usuarios.png
│   │   ├── ventas.png
│   │   └── salir.png
│   ├── icono_sabor_lojano.ico
│   ├── logo_sabor_lojano.jpg
│   └── marca_agua_sabor_lojano.png
├── main.py
└── README.md
```

## Usuarios y contraseñas para ingresar al sistema

identificacion 1101234567, contraseña 1234, Danny Betancourt, rol
Administrador

identificacion 1107654321, contraseña 1234, Carlos Perez, rol Empleado

identificacion 1123456789, contraseña 1234, Maria Jaramillo, rol Cliente

Con el usuario de Danny se puede entrar a Usuarios. Con los otros dos
no aparece esa opcion en el menu.

## Correccion del acceso

Hubo un problema que impedia iniciar sesion aunque la contraseña fuera
correcta. Pasaba porque el modelo de usuario empezo a pedir el campo
rol, y si un registro guardado antes no lo tenia, el sistema lo
descartaba al cargar en vez de dejarlo entrar, asi que la persona nunca
aparecia como valida y el login siempre terminaba en "credenciales
incorrectas". Ahora, si un usuario guardado no trae el rol, se le
asigna Cliente por defecto en lugar de descartarlo, para que el acceso
no se rompa. Si alguno de los usuarios deberia ser Administrador,
conviene revisar que su registro en usuarios.json tenga
"rol": "Administrador" escrito de forma explicita.

## Productos cargados

Humitas, categoria Comida, precio 1.50, stock 15

Jugo de tomate, categoria Bebida, precio 1.50, stock 20

Repe Lojano, categoria Comida, precio 1.25, stock 30

## Como se ejecuta

Se necesita Python con Tkinter y con la libreria Pillow instalada
(pip install pillow), porque de ahi se cargan el logo, la marca de agua
y los iconos del menu.

Desde la carpeta restaurante_app se corre:

python3 main.py

Se entra con cualquiera de los usuarios de la tabla de arriba.

## Pruebas que se hicieron

Se entro como Danny (Administrador) y se confirmo que la opcion
Usuarios aparece en el menu y se puede usar sin errores.

Se selecciono una fila en la tabla de usuarios y se confirmo que el
formulario se llenara solo con los datos de esa persona.

Se presiono Escape y se confirmo que el formulario quedara vacio y la
seleccion de la tabla se quitara.

Se registro un usuario nuevo con rol Cliente presionando Enter desde el
formulario, en vez de hacer clic en el boton, y se confirmo que se
guardara igual.

Se cambio el rol en el selector y se vio el mensaje de confirmacion del
cambio.

Se intento registrar un usuario con rol Administrador desde el
formulario y el sistema lo rechazo.

Se intento cambiar el propio rol de la cuenta conectada y el sistema lo
rechazo.

Se intento eliminar la cuenta con la que se habia iniciado sesion y el
sistema lo rechazo.

Se elimino un usuario distinto al propio y se confirmo que desaparecia
de la tabla, con su confirmacion previa.

Se cerro sesion y se entro como Carlos (Empleado) y como Maria
(Cliente), confirmando en ambos casos que la opcion Usuarios no
aparece en el menu, pero Productos y Ventas siguen funcionando igual.

Se cerro el programa y se volvio a abrir, confirmando que los usuarios
y sus roles se mantuvieran guardados en usuarios.json.
