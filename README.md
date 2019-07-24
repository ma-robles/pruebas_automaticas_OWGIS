# Pruebas automáticas en OWGIS
Scripts para realizar pruebas automáticas para los diversos OWGIS del grupo IOA usando python y Selenium

## Primeros pasos
Para obtener la copia del proyecto solo es necesario clonar el proyecto usando la instrucción:

`git clone https://github.com/grupoioa/pruebas_automaticas_OWGIS.git`

Hay que contar con chrome o firefox instalados (chrome recomendado), además de los prerrequisitos que se describen a continuación.

### Prerrequisitos

Se requieren las siguientes bibliotecas
* pandas
* Selenium 3.141.59

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

Actualmente el proyecto cuenta con el driver para usar el navegador Chrome Versión 74.0.3729.131, para usar firefox como navegador se puede consultar la documentacion de [Selenium](https://www.seleniumhq.org/docs/03_webdriver.jsp) o si la versión de Chrome es diferente a la mencionada descargue el correspondiente [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/)

## Probando

Para ejecutar la pruebas automáticas hay que entrar en carpeta /modulos y ejecutar la siguiente instrucción:

`./Automatic_test.sh`

Al momento de ejecutar la instrucción anterior se desplegara un menu para escoger a que OWGIS se le realizaran las pruebas.

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
