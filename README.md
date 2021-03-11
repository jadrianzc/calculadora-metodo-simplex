<h2 align="center">
  CALCULADORA DE MÉTODO SIMPLEX Y PERT
</h2>

## 📄 Resumen

<p align="justify">
  Programa que permite realizar ejercicios de programación lineal de maximización implementando el método simplex. Además, permite planificar proyectos en los que hace falta coordinar un gran número de actividades, gracias a la implementación de la metodología Pert.
  
  Desarrollado usando PyQt5, que es un binding de la librería Qt para el lenguaje de programación Python.
</p>

## 📜 Uso del Programa
<h3>Simplex</h3>
<p align="justify">
  Tiene una intefaz sencilla, en la cual se deben ingresar la cantidad de variables y de restricciones que emplea el problema, 
  esto permite generar las el espacio para que el usuario ingrese su función objetivo y las diferentes restricciones. El software valida 
  que estos valores sean ya sea enteros o decimales, de lo contrario, si se ubica un caracter o se deja vacío, mostrará un mensaje de error.
  Una vez validado, se podrá generar la primer tabla y mostrar la función objetiva y restricciones con sus respectivas variables de holgura.
  Se pueden ir generando tablas tanto el ejercicio las permita, así mismo por cada tabla hay un botón que calcula su pivote, variable de entrada y de salida.
  Se puede retroceder de tabla, y al finalizar se mostrará el resultado y se habilitará el botón de imprimir.
</p>

<h3>Pert</h3>
<p align="justify">
  Una interfaz sencilla, debe ingresar la cantidad de actividades que se van a realizar, se desplegará una tabla, la cual se debe llenar con la descripción de las actividades, sus predecesores, y los respectivos tiempos optimistas, normal y pesimista. Además, tendrá las opciones de escoger los días que no va a laborar y un calendario para elegir la fecha de inicio del las actividades.
  Una vez ingrese los datos correctamente, se mostrará una nueva tabla con los resultados finales, donde se observan las fechas de inicio y final, la ruta crítica de actividades y un resumen del ejercio. Se activará el botón de guardar el cual permite generar un reporte de la tabla.
</p>

### 🔨 Ejecutable del programa

[Calculadora Simplex-Pert.exe](https://github.com/jadrianzc/calculadora-metodo-simplex/releases/download/v.1.0/Calculadora.Simplex-Pert.exe)
