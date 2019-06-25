from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.firefox.options import Options
import pandas as df
import time


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
        if "error" in entry['message']:
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



def check_load(driver):
    repet = 0
    try:
        loader = driver.find_element_by_class_name("loader")
        display = loader.value_of_css_property("display")
        if display == 'none':
            return True
        else:
            while display == 'none':
                time.sleep(3)
                loader = driver.find_element_by_class_name("loader")
                display = loader.value_of_css_property("display")
                if display != 'none':
                    return True
                else:
                    if repet == 10:
                        catch_log(driver,'GOES')
                        return False
                    else:
                        repet += 1
            return True
    except:
        print("ERROR EN LA CARGA DE LAS IMAGENES")


def animation(driver):
    driver.execute_script("stop('goesAnimation')")
    button_play = driver.find_element_by_id("goesAnimationbtn_stop")
    display = button_play.value_of_css_property("display")
    time.sleep(5)
    if display == 'none':
        try:
            for xs in range(5):
                driver.execute_script("go2image('goesAnimation',goesAnimation.currImg + 1)")
                time.sleep(1)
            for xs in range(5):
                driver.execute_script("go2image('goesAnimation',goesAnimation.currImg - 1)")
                time.sleep(1)
            time.sleep(5)
            driver.execute_script("go2image('goesAnimation',0)")
            time.sleep(5)
            driver.execute_script("go2image('goesAnimation',goesAnimation.totImgs-1)")
            time.sleep(5)
            driver.execute_script("play('goesAnimation')")
            time.sleep(5)
            for xs in range(7):
                driver.execute_script("change_speed('goesAnimation',1)")
            time.sleep(5)
            for xs in range(7):
                driver.execute_script("change_speed('goesAnimation',-1)")
            return True
        except:
            print("Error en los botones de animacion")
            catch_log(driver, 'GOES')
            return False
    else:
        catch_log(driver, 'GOES')
        return False



def month_str(month):
    if month == 1:
        return ('January','Jan')
    elif month == 2:
        return ('February', 'Feb')
    elif month == 3:
        return ('March','Mar')
    elif month == 4:
        return ('April', 'Apr')
    elif month == 5:
        return ('May','May')
    elif month == 6:
        return ('June', 'Jun')
    elif month == 7:
        return ('July', 'Jul')
    elif month == 8:
        return ('August', 'Aug')
    elif month == 9:
        return ('September','Sep')
    elif month == 10:
        return ('October', 'Oct')
    elif month == 11:
        return ('November', 'Nov')
    elif month ==12:
        return ('December', 'Dec')
    else:
        print('null')

def calendar(driver):
    day = time.strftime("%d")
    month = time.strftime("%m")
    year = time.strftime("%Y")
    try:
        if int(month) == 1 and int(day) < 4:
            start_date = driver.find_elements_by_class_name("fa-calendar")
            start_date[0].click()
            month_st = month_str(int(month))
            driver.find_element_by_xpath("//*[contains(text(), '"+month_st[0]+"')]").click()
            driver.find_element_by_xpath("//*[contains(text(), '"+year+"')]").click()
            driver.find_element_by_xpath("//*[contains(text(), 'Dec')]").click()
            driver.find_element_by_xpath("//*[contains(text(), '28')]").click()
        elif int(day)  < 4:
            start_date = driver.find_elements_by_class_name("fa-calendar")
            start_date[0].click()
            month_st = month_str(int(month))
            driver.find_element_by_xpath("//*[contains(text(), '"+month_st[0]+"')]").click()
            month_st = month_str(int(month)-1)
            driver.find_element_by_xpath("//*[contains(text(), '"+month_st[1]+"')]").click()
            driver.find_element_by_xpath("//*[contains(text(), '28')]").click()
        else:
            start_date = driver.find_elements_by_class_name("fa-calendar")
            start_date[0].click()
            time.sleep(3)
            dayC = str(int(day)-3)
            word = driver.find_element_by_xpath("//*[contains(text(), '"+dayC+"')]")
            word.click()
        time.sleep(3)
        # start_date[1].click()
        # calendar = driver.find_elements_by_class_name("dropdown-menu")
        # print(calendar[0].text)
        # word = driver.find_element_by_xpath("//*[contains(text(), '23')]")
        # word.click()
        driver.execute_script("updateAnimation();")
        return check_load(driver)
    except:
        print('Error en las fechas del calendario')


def check_goes(dir):
    name_test = ['Carga de imagen','Botones de animacion', 'Calendario']
    result_test = []
    driver = initDriver("chrome")
    driver.get(dir)
    try:
        load = check_load(driver)
        result_test.append(load)
        time.sleep(2)
        animation1 = animation(driver)
        result_test.append(animation1)
        time.sleep(2)
        calendar1 = calendar(driver)
        result_test.append(calendar1)
        time.sleep(2)
        driver.close()
        test = df.DataFrame(name_test, columns=['Pruebas'])
        result =  df.DataFrame(result_test, columns=['Resultados'])
        report = df.concat([test,result], axis=1)
        print(report)
        report.to_csv("../Data/report_GOES.csv", encoding='utf-8',index=False)
    except:
        print('Error en la revision de la pagina de GOES : ' + dir)
