# Pruebas automáticas en OWGIS
Scripts para realizar pruebas automáticas para los diversos OWGIS del grupo IOA usando python y Selenium

## Primeros pasos
Para obtener la copia del proyecto solo es necesario clonar el proyecto usando la instrucción:

`git clone`

Hay que contar con chrome o firefox instalados (chrome recomendado), además de los prerrequisitos que se describen a continuación.

### Prerrequisitos

Se requieren las siguientes bibliotecas
* pandas
* Selenium

Se recomienda instalar todas las bibliotecas mediante [conda](https://conda.io).

Para crear un ambiente se usa la instrucción:

`conda create --nombreAmbiente`

Ya creado el ambiente se puede cambiar a él usando la instrucción:

`conda activate nombreAmbiente`

dentro del ambiente se instalan la bibliotecas correspondientes.

### pandas:
`conda install -c anaconda pandas`

### Selenium:
`conda install -c anaconda selenium`

Actualmente el proyecto cuenta con el driver para usar el navegador chrome, para usar firefox como navegador se puede consultar la documentacion de [Selenium](https://www.seleniumhq.org/docs/03_webdriver.jsp).

## Probando

Antes de ejecutar las pruebas dentro del archivo /modulos/Automatic_test.sh hay que modificar la linea 3, si se tiene un ambiente en anaconda hay que modificar el nombre del ambiente.
Ejemplo:

`source ~/anaconda3/envs/tensorflow/bin/activate nombreAmbiente`

Si no se tiene ambiente, basta con comentar la linea.

Para ejecutar la pruebas automáticas hay que entrar en carpeta /modulos y ejecutar la siguiente instrucción:

`./Automatic_test.sh`

Esta instrucción por default ejecuta el script para todos los OWGIS que se tienen implementados, si se desea realizar para uno en específico basta con editar el archivo, dentro del archivo se encuentra las instrucciones para que pueda ser modificado.

Como resultado de la ejecución del script se generan dentro de la carpeta /Data tres tipos de archivos:

    * Archivos .csv que contiene el resultado de las pruebas para cada OWGIS
    * Archivos .txt que contiene en caso de error el log producido por el navegador
    * Archivos .png screenshot de la versión 3d

## Deployment

Se cuenta con un archivo de configuración dentro de la carpeta /modulos de nombre test.conf, en dicho archivo se puede modificar la dirección de los OWGIS a los cuales se les está realizando la pruebas.

## Construido con

* [Python](https://www.python.org/)
* [Selenium](https://www.seleniumhq.org/)

## Autores
* **Pablo Camacho Gonzalez** -[GitHub](https://github.com/Pablocg0)
