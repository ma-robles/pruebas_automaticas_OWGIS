'''
File name : Automatic_test.py
Author: Pablo Camacho Gonzalez
Python version: 3.7.3
Date last modified: 13/05/2019
'''



from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.firefox.options import Options
from goes_test import check_goes
import configparser
import sys
import pandas as df
import time
import os


def initDriver(browser):
    """
    Funcion para crear una instancia de un navegador web
    para realizar las pruebas automaticas usando Selenium

    :param browser: navegador a usar firefox o chrome (firefox no sirve la captura de logs)
    :type browser: String
    :return: driver Selenium
    """
    if browser == "firefox":
        opts = Options()
        opts.log.level = "trace"
        driver = webdriver.Firefox(options=opts)
        return driver
    elif browser == "chrome":
        d = DesiredCapabilities.CHROME
        d['loggingPrefs'] = { 'browser':'ALL'}
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome('../Data/chromedriver_linux64/chromedriver',chrome_options=options,desired_capabilities=d)
        return driver
    else:
        print("------- Navegador no compatible ---------")
        return null

def check_trans(driver,nombre):
    try:
        for xs in range(10):
            element = driver.execute_script("owgis.transparency.decreaseTransp();")
            #time.sleep(1)
        time.sleep(5)
        for xs in range(10):
            element = driver.execute_script("owgis.transparency.increaseTransp();")
            #time.sleep(1)
        print('true')
    except:
        print('false')

def check_load_streamlines(driver, nombre):
    """
    Funcion para revisar la carga de las streamlines
    solo se usa cuando se cambia de capa en los menus

    :param driver: driver de Selenium
    :type driver: driver
    :param nombre: nombre de la capa se obtiene via los menus
    :type nombre: String
    :return: (Booleno, string) True si se carga las streamlines False en otro caso,
            Si es falso se regresa la direccion de un txt con el log del error
    """
    msn = ""
    try:
        wait = WebDriverWait(driver,0)                                                                                                                                                                                                                                                                                                  #pcg
        time.sleep(5)
        element = wait.until(EC.presence_of_element_located((By.ID,"loadperc")))
    finally:
        result = check_loading(driver)
        if result:
            return (True,msn)
        else:
            msn = catch_log(driver, nombre+'_streamlines')
            return (False,msn)
        # if element.text == "Current 100 %":
        #     return (True,msn)
        # elif element.text == "":
        #     return (True,msn)
        # else:
        #     #msn = catch_log(driver, nombre+'_streamlines')
        #     return (False,msn)


def check_alert1(driver):
    """
    Funcion para cerrar un ventana de alerta
    los hace 10 veces de forma consecutiva

    :param driver: driver de Selenium
    :type driver: driver
    """
    cont = 0
    while(cont< 10):
        try:
            Alert(driver).accept()
        except:
            cont+=1


def check_total_load(driver):
    """
    Funcion para revisar que la pagina se carga de forma completa
    se usa para revisar la carga de la pagina al cambiar de capa de fondo

    :param driver: driver de Selenium
    :type driver: driver
    :return: (Booleno, string) True si se carga las streamlines False en otro caso,
            Si es falso se regresa la direccion de un txt con log del error
    """
    msn= ''
    try:
        wait = WebDriverWait(driver,0)
        #element = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"ol-unselectable")))
        element = wait.until(EC.presence_of_element_located((By.ID,"canvas-palette-horbar")))
        print(element)
        #element = driver.find_element_by_id("ol-unselectable")
        return (True, msn)
    except:
        print('Error en la revision de la capa de fondo')
        return (False, msn)


def check_alert(driver):
    """
    Funcion para cerrar un ventana de alerta

    :param driver: driver de Selenium
    :type driver: driver
    """
    try:
        #driver.get_screenshot_as_file("../Data/screenshots/error_alert.png")
        #print(EC.alert_is_present())
        Alert(driver).accept()
        #print('close')
        #driver.switch_to.alert.accept()
    except:
        #print('not close')
        pass

def change_layer(driver, idMenu, nameLayer):
    """
    Funcion para cambiar la capa usando los menus

    :param driver: driver de Selenium
    :type driver: driver
    :param idMenu: id del menu
    :type idMenu: String
    :param nameLayer: nombre de la capa a la que se cambiara
    :type nameLayer: String
    :return: True si se cambio de capa False en otro caso
    """
    try:
        layer_menu = Select(driver.find_element_by_id(idMenu))
        layer_menu.select_by_value(nameLayer)
        return True
    except:
        return False

def change3d(driver,nombre):
    """
    Funcion para cambiar a la version 3D y revisar la carga de streamlines
    y tomar un screenshots

    :param driver: driver Selenium
    :type driver: driver
    :param nombre: nombre de la capa
    :type nombre: String
    :return: direccion del screenshot
    """
    if not os.path.exists('../Data/screenshots/'):
            os.makedirs('../Data/screenshots/')
    try:
        driver.execute_script( "updateAnimationStatus('none');")
    except:
        return "Error en la capa: " + nombre
    time.sleep(5)
    dir = "../Data/screenshots/"+nombre+'.png'
    element = driver.execute_script("owgis.cesium.toogleCesium();")
    result = check_loading(driver)
    driver.execute_script("animatePositionMap(2.0,[-10602433.379006794, 2546668.0769200223]);")
    time.sleep(30)
    driver.get_screenshot_as_file(dir)
    element = driver.execute_script("owgis.cesium.toogleCesium();")
    driver.execute_script("animatePositionMap(2.0,[-10602433.379006794, 2546668.0769200223]);")
    time.sleep(5)
    return dir

def changeBackLayer(driver):
    for xs in backLayers:
        time.sleep(5)
        change_layer(driver,'backLayersDropDown',xs)
        print(xs)
        time.sleep(5)
    driver.close()


def change_bavklayers(driver):
    """
    Funcion para cambiar a todas las capas de fondo

    :param driver: drive de Selenium
    :type driver: driver
    :return: DataFrame
    """
    print("Revisando capas de fondo...")
    status = []
    name = []
    #driver.get(dir)
    #backLayers = ['googler','osm','bingr','binga','bingh']
    backLayers = ['googler','osm','bingr','binga','bingh','wms']
    for xs in backLayers:
        time.sleep(5)
        change_layer(driver,'backLayersDropDown',xs)
        result = check_total_load(driver)
        #print(xs)
        #print(result[0])
        status.append(result[0])
        name.append(xs)
        time.sleep(5)
    try:
        driver.close()
        dataNombre = df.DataFrame(name, columns=['Nombre'])
        satus_Back = df.DataFrame(status, columns=['Estatus Backlayers'])
        report = df.concat([dataNombre,satus_Back],axis=1)
        print(report)
    except:
        print("Proceso terminado")
        dataNombre = df.DataFrame(name, columns=['Nombre'])
        satus_Back = df.DataFrame(status, columns=['Estatus Backlayers'])
        report = df.concat([dataNombre,satus_Back],axis=1)
        print(report)




def check_loading(driver):
    """
    Funcion para revisar la descarga de las imagenes y streamlines

    :param driver: driver Selenium
    :type drive: driver
    :return: True si se terminan de cargar las streamlines False en otro caso
    """
    try:
        check_alert1(driver)
        time.sleep(2)
        check_alert1(driver)
        load = driver.find_element_by_id('loadperc')
        #print("porcentaje: "+load.text)
        repet = 0
        if load.text == "":
            return True
        else:
            #print("revision porcentaje")
            split_load = load.text.split(" ")
            if len(split_load) == 3:
                percents = int(split_load[1])
            else:
                percents = int(split_load[0])
            igual = percents
            while percents < 100:
                check_alert(driver)
                time.sleep(5)
                load=driver.find_element_by_id('loadperc')
                #print(load.text)
                if load.text == "":
                    return True
                else:
                    split_load = load.text.split(" ")
                    if len(split_load) == 3:
                        percents = int(split_load[1])
                    else:
                        percents = int(split_load[0])
                if igual == percents:
                    if repet == 10:
                        return False
                    else:
                        repet += 1
                else:
                    igual = percents
            return True
    except:
        return True


def check_animation(driver):
    """
    Funcion para revisar la carga de las imagenes y streamlines cuando
    se manda a realizar una animacion

    :param driver: driver Selenium
    :type driver: driver
    :return: (Booleno, string) True si se carga las streamlines False en otro caso,
            Si es falso se regresa la direccion de un txt con log del error
    """
    try:
        element = driver.execute_script("owgis.ncwms.animation.dispAnimation();")
        check_alert1(driver)
        time.sleep(2)
        check_alert1(driver)
        load = driver.find_element_by_id('loadperc')
        #print("porcentaje: "+load.text)
        repet = 0
        if load.text == "":
            driver.execute_script( "updateAnimationStatus('none');")
            return True
        else:
            #print("revision porcentaje")
            split_load = load.text.split(" ")
            if len(split_load) == 3:
                percents = int(split_load[1])
            else:
                percents = int(split_load[0])
            igual = percents
            while percents < 100:
                check_alert(driver)
                time.sleep(5)
                load=driver.find_element_by_id('loadperc')
                #print(load.text)
                if load.text == "":
                    driver.execute_script( "updateAnimationStatus('none');")
                    return True
                else:
                    split_load = load.text.split(" ")
                    if len(split_load) == 3:
                        percents = int(split_load[1])
                    else:
                        percents = int(split_load[0])
                if igual == percents:
                    if repet == 10:
                        driver.execute_script( "updateAnimationStatus('none');")
                        return False
                    else:
                        repet += 1
                else:
                    igual = percents
            driver.execute_script( "updateAnimationStatus('none');")
            return True
    except:
        return True



def catch_log(driver, nombre):
    """
    Funcion para guardar los logs que ocurren en ciertas pruebas
    Esta funcion solo sirve en chrome

    :param driver: driver Selenium
    :type driver: driver
    :param nombre: nombre de la capa
    :type nombre: String

    :return: String con el nombre del txt con el log
    """
    msn = ""
    msn1 = ""
    msn2 = ""
    saveFile = "../Data/logs/" + nombre + '.txt'
    if not os.path.exists('../Data/logs/'):
            os.makedirs('../Data/logs/')
    for entry in driver.get_log('browser'):
        if "Not possible to read JSON data for" in entry['message']:
            msn += entry['message'] + '\n'
        elif "error" in entry['message']:
            msn1 += entry['message'] + '\n'
        elif entry['level'] == 'SEVERE':
            msn2 += entry['message'] + '\n'
        else:
            pass
    if (msn == "") and (msn1 == "") and (msn2 == ""):
        return ''
    else:
        arch = open(saveFile,'w')
        arch.write(msn)
        arch.write(msn1)
        arch.write(msn2)
        arch.close()
        return saveFile

def month_to_int(month):
    """
    Funcion para cambiar de un mes String a su version Int

    :param month: mes
    :type month: String
    :return: int
    """
    if month == "January" or month == "enero":
        return 1
    elif month == "February" or month == "febrero":
        return 2
    elif month == "March" or month == "marzo":
        return 3
    elif month == "April" or month == "abril":
        return 4
    elif month == "May" or month == "mayo":
        return 5
    elif month == "June" or  month == "junio":
        return 6
    elif month == "July" or month == "julio":
        return 7
    elif month == "August" or month == "agosto":
        return 8
    elif month == "September" or month == "septiembre":
        return 9
    elif month == "October" or month == "octubre":
        return 10
    elif month == "November" or month == "noviembre":
        return 11
    elif month == "December" or month == "diciembre":
        return 12
    else:

        #print('null')
        return null



def checkCalendar(driver, nombre):
    """
    Funcion para revisar la fecha en el calendario

    :param driver: driver Selenium
    :type driver: driver
    :param nombre: nombre de la capa
    :type nombre: String
    :return: (Booleno, string) True si las fechas son correctas False en otro caso,
            Si es falso se regresa la direccion de un txt con log del error
    """
    msn = ""
    correct = True
    #time.sleep(5)
    day = time.strftime("%d")
    month = time.strftime("%m")
    year = time.strftime("%Y")
    try:
        cal = driver.find_elements_by_class_name("ui-datepicker-today")
        month_des = driver.find_elements_by_class_name("ui-datepicker-month")
    except:
        print('Problemas en la revision de los calendarios')
        return (False,msn)

    if len(month_des)==0:
        return (True,msn)
    month_cal_fin = month_to_int(month_des[1].text)
    #print(month_cal_fin)
    month_cal_init = month_to_int(month_des[0].text)
    select_fin = driver.find_elements_by_class_name("ui-state-active")
    currents = driver.find_elements(By.XPATH,"//*[@data-handler=\'selectDay\']")
    for xs in cal:
        slect = xs.get_attribute("data-handler")
        if (xs.text.zfill(2) == day) and (slect== 'selectDay') and ((int(select_fin[1].text)>int(xs.text)) or (int(month_cal_fin) > int(month))):
            #print("True")
            correct=True
        else:
            msn = catch_log(driver, nombre+"_calendar")
            correct =False
    return (correct,msn)


def create_report(infoName,streamlines, calendar,messenger, animation,v3d):
    """
    Funcion para crear un DataFrame que contien el resultado de las pruebas

    :param infoName: lista con los nombre de las capas
    :type infoName: list
    :param streamlines: lista con los resultado de la carga de las stremalines
    :type streamlines: list
    :param calendar: lista con los resultado de revisar la fecha de los calendarios
    :type calendar: list
    :param messenger: lista de los nombres de los archivos logs
    :type messenger: list
    :param animation: lista de los resultados de revisar la carga de las animaciones
    :type animation: list
    :param v3d: lista de los resultado de cambiar a la version 3D
    :type v3d: list
    :return: DataFrame con todos los resultados de las pruebas
    """
    dataNombre = df.DataFrame(infoName, columns=['Nombre'])
    strem = df.DataFrame(streamlines, columns=['Estatus Streamlines'])
    calendar = df.DataFrame(calendar, columns=['Estatus Calendarios'])
    messenger =  df.DataFrame(messenger, columns=['LOG'])
    animations = df.DataFrame(animation, columns=["Estatus animacion"])
    ver_3d =  df.DataFrame(v3d, columns=["Estatus 3D"])
    report = df.concat([dataNombre,strem,calendar,animations,ver_3d,messenger],axis=1)
    heatmap = df.concat([strem,calendar,animations],axis=1)
    # plt.figure(figsize=(12.2,8.4))
    # plt.title("Reporte de pruebas");
    # plt.pcolor(heatmap)
    # plt.xticks(fontsize=8)
    # plt.savefig("../Data/reporte.png")
    # plt.show()
    # plt.clf()
    # plt.close()
    #report = df.DataFrame([name,streamlines,calendar],columns=['Nombre','Estatus Streamlines', 'Estatus Calendario'])
    return report

def check_oleaje(dir,driver, opt):
    """
    Funcion para revisar el OWGIS de oleaje

    :param dir: direccion del OWGIS de oleaje
    :type dir: String
    :param driver: driver de Selenium
    :type drive: driver
    """
    menuLevel1= ['Pom','Gom','Wo']
    menuLevel2 = ['Altura','Periodo']
    nombres = []
    calendars = []
    streamlines = []
    messenger = []
    animations = []
    a_3ds = []
    print(dir)
    print("--------Test Oleaje--------")
    try:
        driver.get(dir)
    except:
        print("La pagina proporcionada no existe o no esta disponible")
        return null
    #driver.execute_script("animatePositionMap(2.0,[-10602433.379006794, 2546668.0769200223]);")
    for xs in menuLevel1 :
        change_layer(driver,'dropDownLevels1',xs)
        for ys in menuLevel2:
            nombre = xs+"-"+ys
            print(nombre)
            change_layer(driver, 'dropDownLevels2',ys)
            streamline = check_load_streamlines(driver,nombre)
            calendar = checkCalendar(driver,nombre)
            rev = check_animation(driver)
            try:
                a3d = change3d(driver,nombre)
            except:
                a_3ds.append('Error en la version 3d')
            a_3ds.append(a3d)
            animations.append(rev)
            nombres.append(nombre)
            calendars.append(calendar[0])
            streamlines.append(streamline[0])
            messenger.append(calendar[1]+" "+streamline[1])
    time.sleep(2)
    df_oleaje = create_report(nombres,streamlines,calendars,messenger,animations,a_3ds)
    if opt == 1 :
        df_oleaje.to_csv("../Data/report_oleaje.csv", encoding='utf-8',index=False)
        change_bavklayers(driver)
    else:
        df_oleaje.to_csv("../Data/report_oleaje_cen.csv", encoding='utf-8',index=False)
    time.sleep(5)
    try:
        driver.close()
        print(df_oleaje)
    except:
        print(df_oleaje)
        print("Proceso terminado")


def check_tormenta(dir,driver, opt):
    menuLevel1=['Dom1','Dom2']
    menuLevel2=['ele']
    nombres = []
    calendars = []
    streamlines = []
    messenger = []
    animations = []
    a_3ds = []
    print(dir)
    print("--------Test Marea y Tormenta--------")
    try:
        driver.get(dir)
    except:
        print("La pagina proporcionada no existe o no esta disponible")
        return null
    driver.execute_script("animatePositionMap(2.0,[-10602433.379006794, 2546668.0769200223]);")
    for xs in menuLevel1 :
        nombre = xs+"-"+menuLevel2[0]
        change_layer(driver,'dropDownLevels1',xs)
        print(nombre)
        streamline = check_load_streamlines(driver,nombre)
        calendar = checkCalendar(driver,nombre)
        check_trans(driver,nombre)
        rev = check_animation(driver)
        a3d = change3d(driver,nombre)
        a_3ds.append(a3d)
        animations.append(rev)
        nombres.append(nombre)
        calendars.append(calendar[0])
        streamlines.append(streamline[0])
        messenger.append(calendar[1]+" "+streamline[1])
    time.sleep(2)
    df_oleaje = create_report(nombres,streamlines,calendars,messenger,animations,a_3ds)
    if opt == 1:
        df_oleaje.to_csv("../Data/report_tormenta.csv", encoding='utf-8',index=False)
        change_bavklayers(driver)
    else:
        df_oleaje.to_csv("../Data/report_tormenta_cen.csv", encoding='utf-8',index=False)
    time.sleep(5)
    try:
        driver.close()
        print(df_oleaje)
    except:
        print(df_oleaje)
        print("Proceso terminado")



def check_calidadAire(dir,driver):
    menuLevel1=['Dom1']
    menuLevel2=['o3','Temp2','VtoSup10','PBLH','co','PM10','so2','nox','VarViento']
    nombres = []
    calendars = []
    streamlines = []
    messenger = []
    animations = []
    a_3ds = []
    print(dir)
    print("--------Test Calidad del aire--------")
    try:
        driver.get(dir)
    except:
        print("La pagina proporcionada no existe o no esta disponible")
        return null
    driver.execute_script("animatePositionMap(2.0,[-10602433.379006794, 2546668.0769200223]);")
    for xs in menuLevel2 :
        nombre = menuLevel1[0]+"-"+xs
        change_layer(driver,'dropDownLevels2',xs)
        print(nombre)
        streamline = check_load_streamlines(driver,nombre)
        calendar = checkCalendar(driver,nombre)
        rev = check_animation(driver)
        a3d = change3d(driver,nombre)
        a_3ds.append(a3d)
        animations.append(rev)
        nombres.append(nombre)
        calendars.append(calendar[0])
        streamlines.append(streamline[0])
        messenger.append(calendar[1]+" "+streamline[1])
    time.sleep(2)
    df_oleaje = create_report(nombres,streamlines,calendars,messenger,animations,a_3ds)
    df_oleaje.to_csv("../Data/report_calidadAire.csv", encoding='utf-8',index=False)
    change_bavklayers(driver)
    time.sleep(5)
    try:
        driver.close()
        print(df_oleaje)
    except:
        print(df_oleaje)
        print("Proceso terminado")


def check_meteo(dir,driver, op):
    """
    Funcion para revisar el OWGIS de meteorologia

    :param dir: direccion del OWGIS de meteorologia
    :type dir: String
    :param driver: driver de Selenium
    :type drive: driver
    """
    menuLevel1 = ['Dom1','Dom2']
    menuLevel2 = ['Temp2','Prec','Viento','relh','nubesIR','vape','alerta']
    menuPreci = ['PrecHor','PrecTot','Prec3h','Prec6h']
    menuViento = ['VtoSup10','VientoToti']
    menuAlerta = ['Temp2','Temp21','Viento','VientoTot','Prec','PrecT']
    nombres = []
    calendars = []
    streamlines = []
    messenger = []
    animations = []
    a_3ds = []
    print(dir)
    print("--------Test Meteorologico--------")
    try:
        driver.get(dir)
    except:
        print("La pagina proporcionada no existe o no esta disponible")
        return null
    for xs in menuLevel1:
        change_layer(driver,'dropDownLevels1',xs)
        for ys in menuLevel2:
            change_layer(driver,'dropDownLevels2',ys)
            if ys == 'Prec':
                for zs in menuPreci:
                    change_layer(driver,'dropDownLevels3',zs)
                    nombre = xs+"-"+ys+'-'+zs
                    print(nombre)
                    try:
                        streamline = check_load_streamlines(driver, nombre)
                    except:
                        streamline = (False,"")
                    calendar = checkCalendar(driver, nombre)
                    rev = check_animation(driver)
                    a3d = change3d(driver,nombre)
                    a_3ds.append(a3d)
                    animations.append(rev)
                    nombres.append(nombre)
                    calendars.append(calendar[0])
                    streamlines.append(streamline[0])
                    messenger.append(calendar[1]+" "+streamline[1])
            elif ys == 'Viento':
                for zs in menuViento:
                    change_layer(driver,'dropDownLevels3',zs)
                    nombre = xs+"-"+ys+'-'+zs
                    print(nombre)
                    streamline = check_load_streamlines(driver, nombre)
                    calendar = checkCalendar(driver, nombre)
                    rev = check_animation(driver)
                    a3d = change3d(driver,nombre)
                    a_3ds.append(a3d)
                    animations.append(rev)
                    nombres.append(nombre)
                    calendars.append(calendar[0])
                    streamlines.append(streamline[0])
                    messenger.append(calendar[1]+" "+streamline[1])
            elif ys == 'alerta':
                for zs in menuAlerta:
                    r = change_layer(driver,'dropDownLevels3',zs)
                    if r:
                        nombre = xs+"-"+ys+'-'+zs
                        print(nombre)
                        streamline = check_load_streamlines(driver, nombre)
                        calendar = checkCalendar(driver, nombre)
                        rev = check_animation(driver)
                        a3d = change3d(driver,nombre)
                        a_3ds.append(a3d)
                        animations.append(rev)
                        nombres.append(nombre)
                        calendars.append(calendar[0])
                        streamlines.append(streamline[0])
                        messenger.append(calendar[1]+" "+streamline[1])
                    else:
                        pass
            else:
                nombre = xs+"-"+ys
                print(nombre)
                streamline = check_load_streamlines(driver, nombre)
                calendar = checkCalendar(driver, nombre)
                rev = check_animation(driver)
                a3d = change3d(driver,nombre)
                a_3ds.append(a3d)
                animations.append(rev)
                nombres.append(nombre)
                calendars.append(calendar[0])
                streamlines.append(streamline[0])
                messenger.append(calendar[1]+" "+streamline[1])
    time.sleep(5)
    df_meteo = create_report(nombres,streamlines,calendars,messenger,animations,a_3ds)
    if op == 1:
        df_meteo.to_csv("../Data/report_meteo.csv", encoding='utf-8',index=False)
    elif op == 0:
        df_meteo.to_csv("../Data/report_meteo_cenapred.csv", encoding='utf-8',index=False)
    change_bavklayers(driver)
    time.sleep(5)
    try:
        driver.close()
        print(df_meteo)
    except:
        print(df_meteo)
        print("Proceso terminado")



def check_global(dir,driver):
    """
    Funcion para revisar el OWGIS global

    :param dir: direccion del OWGIS global
    :type dir: String
    :param driver: driver de Selenium
    :type drive: driver
    """
    menuLevel1=['hycom','gfs']
    menuLevel2=['cur','ts','sal','ssh']
    menuLevel2_gfs = ['wind','ts','hum','prec','vor','pres','geo','plan','conv','suri','ozone','tic','sun']
    menuLevel3_gfs = ['surf','abvgrnd','isobar','grnd','msl']
    nombres = []
    calendars = []
    streamlines = []
    messenger = []
    animation = []
    a_3ds = []
    print(dir)
    print("--------Test "+menuLevel1[0]+"--------")
    try:
        driver.get(dir)
    except:
        print("La pagina proporcionada no existe o no esta disponible")
        return null
    for xs in menuLevel2:
        change_layer(driver,'dropDownLevels2',xs)
        nombre = menuLevel1[0]+"-"+xs
        print(nombre)
        streamline = check_load_streamlines(driver, nombre)
        calendar = checkCalendar(driver, nombre)
        rev = check_animation(driver)
        a3d = change3d(driver,nombre)
        a_3ds.append(a3d)
        animation.append(rev)
        nombres.append(nombre)
        calendars.append(calendar[0])
        streamlines.append(streamline[0])
        messenger.append(calendar[1]+" "+streamline[1])
        #print(menuLevel1[0]+"-"+xs+" /"+ str(result[1]))
        #change3d(driver,menuLevel1[0],xs)
    time.sleep(5)
    print("--------Test "+menuLevel1[1]+"--------")
    change_layer(driver,'dropDownLevels1',menuLevel1[1])
    for xs in menuLevel2_gfs:
        change_layer(driver,'dropDownLevels2',xs)
        nombre = menuLevel1[1]+"-"+xs
        print(nombre)
        streamline= check_load_streamlines(driver, nombre)
        calendar = checkCalendar(driver, nombre)
        rev = check_animation(driver)
        a3d = change3d(driver,nombre)
        a_3ds.append(a3d)
        animation.append(rev)
        nombres.append(nombre)
        calendars.append(calendar[0])
        streamlines.append(streamline[0])
        messenger.append(calendar[1]+" "+streamline[1])
        #print(menuLevel1[1]+"-"+xs+" /"+ str(result[1]))
        for ys in menuLevel3_gfs:
            r = change_layer(driver,'dropDownLevels3',ys)
            if r :
                nombre = menuLevel1[1]+"-"+xs+"-"+ys
                print(nombre)
                stremaline = check_load_streamlines(driver, nombre)
                calendar = checkCalendar(driver, nombre)
                rev = check_animation(driver)
                a3d = change3d(driver,nombre)
                a_3ds.append(a3d)
                animation.append(rev)
                nombres.append(nombre)
                calendars.append(calendar[0])
                streamlines.append(stremaline[0])
                messenger.append(calendar[1]+" "+streamline[1])
                #print(menuLevel1[1]+"-"+xs+"-"+ys+" /"+ str(result_2[1]))
            else:
                pass
    print("----------------------------------")
    time.sleep(2)
    df_global = create_report(nombres,streamlines,calendars,messenger,animation,a_3ds)
    df_global.to_csv("../Data/report_global.csv", encoding='utf-8',index=False)
    change_bavklayers(driver)
    time.sleep(5)
    try:
        driver.close()
        print(df_global)
    except:
        print(df_global)
        print("Proceso terminado")

def menu():
    print("---------------------------------------------------------------------------------------------------------")
    print(" ")
    print("                         SISTEMA DE PRUEBAS PARA OWGIS")
    print(" ")
    print("     + Espere a que el sistema realice las pruebas.")
    print("     + Al terminal se imprime el resultado de las pruebas realizadas.")
    print("     + True si la prueba se cumplio.")
    print("     + False si la prueba no se cumplio.")
    print("     + Se puede revisar el log de errores en el archivo que se describe en la columna LOG")
    print("     + El reporte tambien se puede consultar en el archivo report_nombreOwgis.csv en la carpeta /Data")
    print(" ")
    print("                  TIEMPO ESTIMADO DE LAS PRUEBAS: 25 A 50 MINUTOS")
    print("---------------------------------------------------------------------------------------------------------")
    print("")
    print("       Escoja la pagina donde se ejecutaran las pruebas:")
    print("")
    print("     1. OWGIS Global")
    print("     2. OWGIS meteorologia")
    print("     3. OWGIS Oleaje")
    print("     4. OWGIS Marea y Tormenta")
    print("     5. OWGIS Calidad del aire")
    print("     6. OWGIS meteorologia cenapred")
    print("     7. OWGIS Oleaje cenapred")
    print("     8. OWGIS Marea y Tormenta cenapred")
    print("     9. GOES")
    print("     10. Todas las anteriores")
    print("     0. Salir")
    print("")
    opcion= input("     >> ")
    return opcion


def main():
    page = menu()
    ##system.out()
    #page = int(sys.argv[1])
    config = configparser.ConfigParser()
    config.read("../modulos/test.conf")
    dir_global = config.get("test","global")
    dir_met = config.get("test","meteo")
    dir_olea = config.get("test","oleaje")
    dir_tormenta = config.get("test","tormenta")
    dir_calidad = config.get("test","aire")
    dir_met_cen = config.get("test","meteo_cen")
    dir_olea_cen = config.get("test","oleaje_cen")
    dir_tormenta_cen = config.get("test","tormenta_cen")
    goes = config.get("test","goes")
    if page == '1':
        driver = initDriver("chrome")
        try:
            check_global(dir_global,driver)
        except:
            print('Error en el navegador revisando la pagina: ' + dir_global)
    elif page == '2':
        driver = initDriver("chrome")
        try:
            check_meteo(dir_met,driver,1)
        except:
            print('Error en el navegador revisando la pagina: ' + dir_met)
    elif page == '3':
        driver = initDriver("chrome")
        try:
            check_oleaje(dir_olea,driver,1)
        except:
            print('Error en el navegador revisando la pagina: ' + dir_olea)
    elif page == '4':
        driver = initDriver("chrome")
        try:
            check_tormenta(dir_tormenta,driver,1)
        except:
            print('Error en el navegador revisando la pagina: ' + dir_tormenta)
    elif page == '5':
        driver = initDriver("chrome")
        try:
            check_calidadAire(dir_calidad,driver)
        except:
            print('Error en el navegador revisando la pagina: ' + dir_calidad)
    elif page == '6':
        driver = initDriver("chrome")
        try:
            check_meteo(dir_met_cen,driver,0)
        except:
            print('Error en el navegador revisando la pagina: ' + dir_met_cen)
    elif page == '7':
        driver = initDriver("chrome")
        try:
            check_oleaje(dir_olea_cen,driver, 0)
        except:
            print('Error en el navegador revisando la pagina: ' + dir_olea_cen)
    elif page == '8':
        driver = initDriver("chrome")
        try:
            check_tormenta(dir_tormenta_cen,driver, 0)
        except:
            print('Error en el navegador revisando la pagina: ' + dir_tormenta_cen)
    elif page == '9':
        try:
            check_goes(goes)
        except:
            print('Error en el navegador revisando la pagina: ' + dir_tormenta_cen)
    elif page == '10':
        try:
            driver = initDriver("chrome")
            check_global(dir_global,driver)
            time.sleep(10)
            driver = initDriver("chrome")
            check_meteo(dir_met,driver,1)
            time.sleep(10)
            driver = initDriver("chrome")
            check_oleaje(dir_olea,driver,1)
            time.sleep(10)
            driver = initDriver("chrome")
            check_tormenta(dir_tormenta,driver,1)
            time.sleep(10)
            driver = initDriver("chrome")
            check_calidadAire(dir_calidad,driver)
            time.sleep(10)
            driver = initDriver("chrome")
            check_meteo(dir_met_cen,driver,0)
            time.sleep(10)
            driver = initDriver("chrome")
            check_oleaje(dir_olea_cen,driver, 0)
            time.sleep(10)
            driver = initDriver("chrome")
            check_tormenta(dir_tormenta_cen,driver, 0)
            time.sleep(10)
            check_goes(goes)
        except:
            print('Error en el navegador revisando la paginas')
    else:
        if page == '0':
            return 0
        else:
            print("Opcion incorrecta")
            main()


if __name__ == "__main__":
    opt =1
    while opt != 0:
        opt = main()
