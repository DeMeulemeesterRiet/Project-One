import threading
import time
import datetime  
from datetime import datetime
from datetime import timedelta
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from helpers.klassehc_sr04 import HC_SR04
from helpers.klasseOneWireTemp import TempOneWire
from helpers.klasseRotaryEncoder import Rotary
from helpers.klasserfid import RFID
from helpers.klasseip import IP_lezen
from helpers.klasseLCD import LCD
from helpers.klasseknop import Button
from helpers.klasseMatrix import Matrix
from helpers.klasseTafels import Tafels
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from subprocess import call


# TODO: GPIO
from RPi import GPIO
GPIO.setmode(GPIO.BCM)
chip_select = 18
GPIO.setup(chip_select, GPIO.OUT)
GPIO.output(chip_select, GPIO.HIGH)


bestandsnaam = '/sys/bus/w1/devices/28-01813c00007d/w1_slave' # nodig voor de one-wire temperatuursensor
adres_PCF = 0x38 # Nodig voor LCD

waarde_rotor = 0
antwoord_plaats = 0

huidige_leerlingid = None
ip_nog_tonen = False
gekozen_tafel = None
huidig_oefensessieid = None

mijn_rotor = None

lengte_lijst_aantal_tafels = None
lijst_tafels_matrix = None
lijst_antwoorden = None
lijst_getal2 = None
lijst_huidige_plaats = None
# huidige_oefening = None
# huidig_antwoord_correct = None
# huidig_getal2 = None


app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUWILLNEVERKNOW'
app.config['JWT_SECRET_KEY'] = 'VERRYSECRET'  
jwt = JWTManager(app)

# ping interval forces rapid B2F communication
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent', ping_interval=0.5)
CORS(app)


def setup_hulpklasses():
    mijn_LCD.init_LCD()
    mijn_matrix.setup()
    mijn_matrix.uit()
    # mijn_knop1.on_press(lees_knop)
    mijn_knop2.on_press(lees_knop)
    print("Setup hulpklasse gedaan")

def lees_knop(pin):
    global ip_nog_tonen
    print(threading.current_thread())
    if mijn_knop2.pressed:
        print(f"**** button pressed {pin} ****")
        referentie_tijd_knop = time.time()
        ip_nog_tonen = True
        status_ip_zichtbaar_maken()
        while True:
            if ((time.time() - referentie_tijd_knop) >= 5):
                referentie_tijd_knop = time.time()
                if mijn_knop2.pressed:
                    print("****Pi afsluiten******")
                    shutdownbutton()
                    # mijn_LCD.clearLCD()
                    # mijn_LCD.write_message("Tot ziens!")
                    # time.sleep(2)
                    # mijn_LCD.set_cursor_display(displayOn=False)
                    # mijn_LCD.clearLCD()
                    # mijn_matrix.uit()
                    # GPIO.cleanup()
                    # call("sudo shutdown -h now", shell=True)
            break
        # t4 = threading.Thread(target=status_ip_zichtbaar_maken, daemon=True)
        # t4.start()
        # # print(threading.active_count())
        # # print(threading.enumerate())
        # # print(f"thread in functie 'lees knop': {threading.current_thread()}")
        # t4.join(timeout=10.0)
        
    elif mijn_knop1.pressed:
        print(f"**** button pressed {pin} ****")

        


def huidige_datumtijd():
    timestamp=(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
    return timestamp

from datetime import datetime

def convert_datetime(obj):
    """Convert a datetime object to an ISO 8601 string."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj

def convert_datetimes(data):
    """Recursively convert all datetime objects in a data structure."""
    if isinstance(data, dict):
        return {k: convert_datetimes(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_datetimes(item) for item in data]
    else:
        return convert_datetime(data)

def callback_print(waarde, richting):
    global waarde_rotor
    waarde_rotor = waarde
    # print(f"{waarde}, Richting: {richting}")
    # print(f"thread in functie 'callback print' van rotor: {threading.current_thread()}") # callback thread

# region IP
def status_ip_instellen():
    # mijn_LCD.set_cursor_display(cursorOn=False,blinkCursor=False)
    mijn_ip_lijst = IP_lezen().ip_uitlezen() # ['192.168.168.169', '172.30.248.176']
    print(f"Mijn ip lijst: {mijn_ip_lijst}")
    mijn_LCD.pagina_legen(2)
    mijn_LCD.cursor_ga_naar(pagina=2 , lijn=1)
    mijn_LCD.write_message(mijn_ip_lijst[0])
    # mijn_LCD.cursor_ga_naar(pagina=2,lijn=2)
    # mijn_LCD.write_message(mijn_ip_lijst[1])
    # mijn_LCD.cursorHome_0x00()
    print(f"thread in functie 'status ip instellen': {threading.current_thread()}")
    
# def status_ip_zichtbaar_maken():
#     mijn_LCD.display_zichtbaar_maken(2)
#     print(f"thread in functie 'status ip zichtbaar maken': {threading.current_thread()}")
#     status_ip_instellen()
#     referentie_tijd_ip = time.time()
#     ip_getoond = False
#     while (True and (ip_getoond == False)):
#         if ((time.time() - referentie_tijd_ip) >= 5):
#             referentie_tijd_ip = time.time()
#             mijn_LCD.display_zichtbaar_maken(1)
#             ip_getoond = True
#             print("einde ip zichtbaar maken")
           
def status_ip_zichtbaar_maken():
    print(f"thread in functie 'status ip zichtbaar maken': {threading.current_thread()}")
    status_ip_instellen()
    mijn_LCD.display_zichtbaar_maken(2)
    time.sleep(5)
    mijn_LCD.display_zichtbaar_maken(1)
    print("einde ip zichtbaar maken")

# endregion IP

#region Threads

# START een thread op. Belangrijk!!! Debugging moet UIT staan op start van de server, anders start de thread dubbel op
# werk enkel met de packages gevent en gevent-websocket.  
# def all_out():
#     # wait 10s with sleep sintead of threading.Timer, so we can use daemon
#     time.sleep(10)
#     referentie_tijd = time.time()
#     huidige_temperatuur = mijn_temp.lees_temperatuur()
#     mijn_HC_SR04.afstand_uitlezen()
#     while True:
#         if ((time.time() - referentie_tijd) >= 60):
#             referentie_tijd = time.time()
#             print('*** We zetten alles uit **')
#             # huidige_temperatuur = mijn_temp.lees_temperatuur()
#             # print(huidige_temperatuur)
#             new_logging(1) # 1 want tempsensor id is 1
#             mijn_HC_SR04.afstand_uitlezen()
             
# def test_rotor():
#     global waarde_rotor
#     # print(f"thread in functie 'test_rotor': {threading.current_thread()}")
#     rotor_vorig = waarde_rotor
#     referentie_tijd_1 = time.time()
#     referentie_tijd_2 = time.time()
#     while True:
#         if ((time.time() - referentie_tijd_1) >= 2):
#             referentie_tijd_1 = time.time()
#             if waarde_rotor != rotor_vorig:
#                 rotor_vorig = waarde_rotor
#                 print(f'er is aan gedraaid {waarde_rotor}')
#                 mijn_matrix.antwoord_wijzigen(5)
#                 # print(f"thread in functie 'test rotor 'er is aan gedraaid'': {threading.current_thread()}")
#         if ((time.time() - referentie_tijd_2) >= 10):
#             referentie_tijd_2 = time.time()
#             print('*** We zetten alles uit **')
#             huidige_temperatuur = mijn_temp.lees_temperatuur()
#             print(huidige_temperatuur)
#             # new_logging(1) # 1 want tempsensor id is 1
#             mijn_HC_SR04.afstand_uitlezen()
            
def test_rotor():
    global waarde_rotor
    # print(f"thread in functie 'test_rotor': {threading.current_thread()}")
    rotor_vorig = waarde_rotor
    referentie_tijd_1 = time.time()
    while True:
        if ((time.time() - referentie_tijd_1) >= 2):
            referentie_tijd_1 = time.time()
            if waarde_rotor != rotor_vorig:
                rotor_vorig = waarde_rotor
                print(f'er is aan gedraaid {waarde_rotor}')
                mijn_matrix.matrix_instellen(antwoord=str(abs(waarde_rotor)))
                # print(f"thread in functie 'test rotor 'er is aan gedraaid'': {threading.current_thread()}")

def sensor_uitlezen():
    # print(f"thread in functie 'test_rotor': {threading.current_thread()}")
    referentie_tijd_2 = time.time()
    while True:
        if ((time.time() - referentie_tijd_2) >= 60):
            referentie_tijd_2 = time.time()
            print('*** Temperatuur **')
            mijn_temp.lees_temperatuur()
            new_logging(1) # 1 want tempsensor id is 1

def afsluiten():
    global ip_nog_tonen
    print(threading.active_count())
    print(threading.enumerate())
    print("Afsluiten is klaar")
    # if button presses start timer?
    # mijn_knop2.on_press(status_ip_zichtbaar_maken)
    # print(f"thread in functie 'afsluiten': {threading.current_thread()}")
    # mijn_knop1.on_press(lees_knop)
    # while True:
    #     if (ip_nog_tonen == True):
    #         print(f"thread in functie 'afsluiten' in while: {threading.current_thread()}")
    #         ip_nog_tonen = False

def persoon_dichtbij():
    mijn_HC_SR04 = HC_SR04(16, 12)
    mijn_LCD.clearLCD()
    mijn_LCD.write_message("Welkom!")

    # time.sleep(2)
    # print("einde sleep 10s persoon dichtbij")
    referentie_tijd_3 = time.time()
    while True:
        if ((time.time() - referentie_tijd_3) >= 3):
            referentie_tijd_3 = time.time()
            print('*** Kijen of er iemand voor staat ***')
            afstand = mijn_HC_SR04.afstand_uitlezen()
            if (afstand <= 30):
                start_thread_badgen()
                break

def detected_badge():
    global huidige_leerlingid
    mijn_rfid = RFID(bus=0, device=1, pin_rst=17, pin_mode=GPIO.BCM, pin_irq=13, pin_ce=1)
    print("Welkom\nWachten op badge...")
    mijn_LCD.clearLCD()
    mijn_LCD.write_message("Welkom")
    mijn_LCD.cursor_ga_naar(lijn=2)
    mijn_LCD.write_message("Wachten op badge")
    leerling_gekend = False
    while leerling_gekend == False:
        mijn_rfid.wait_for_tag()
        uid = mijn_rfid.read_id(as_number = True)
        if uid is not None:
            print(f'UID: {uid:X}  {uid}')
            data = DataRepository.read_leerling_by_rfidcode(uid)
            print(data) # None of vb {'leerlingid': 1, 'naam': 'Cédric'}
            if data is None:
                print("Ongeldige badge")
                mijn_LCD.pagina_legen(1)
                mijn_LCD.cursorHome_0x00()
                mijn_LCD.write_message("Ongekende badge")
                time.sleep(5)
                # tijd_kort = time.time()
                # while (time.time() - tijd_kort < 5):
                #     # print("wachten")
                #     pass
                mijn_LCD.pagina_legen(1)
                mijn_LCD.cursorHome_0x00()
                mijn_LCD.write_message("Welkom!")
                mijn_LCD.cursor_ga_naar(lijn=2)
                mijn_LCD.write_message("Wachten op badge")
                return detected_badge()
            else:
                leerling_gekend = True
                huidige_leerlingid = data['leerlingid']
                print(f"Welkom terug {data['naam']} met badgeid: {uid}")
                mijn_LCD.pagina_legen(1)
                mijn_LCD.cursorHome_0x00()
                mijn_LCD.write_message("Welkom terug")
                mijn_LCD.cursor_ga_naar(lijn=2)
                mijn_LCD.write_message(f"{data['naam']}!")
    # print(threading.active_count())
    # print(threading.enumerate())
    mijn_rfid.cleanup()
    return start_thread_keuze_tafel()

# def keuze_tafel():
#     global gekozen_tafel
#     # print(f"thread in functie 'BOVENAAN tafel kiezen 'er is aan gedraaid'': {threading.current_thread()}")
#     global waarde_rotor
#     waarde_rotor = 0
#     rotor_vorig = waarde_rotor
#     lijst_tafels = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6','T7', 'T8','T9', 'T10','T11', 'T12']
#     mijn_matrix.matrix_instellen_kiezen(lijst_tafels[0])
#     # print(f"thread in functie 'test_rotor': {threading.current_thread()}")
#     referentie_tijd_1 = time.time()
#     # print(threading.active_count())
#     # print(threading.enumerate())
#     while True and (gekozen_tafel == None):
#         if ((time.time() - referentie_tijd_1) >= 1):
#             referentie_tijd_1 = time.time()
#             if waarde_rotor != rotor_vorig:
#                 rotor_vorig = waarde_rotor
#                 print(f'er is aan gedraaid {waarde_rotor}')
#                 antwoord_plaats = ((abs(waarde_rotor))%(len(lijst_tafels)))
#                 antwoord = lijst_tafels[antwoord_plaats]
               
#                 mijn_matrix.matrix_instellen_kiezen(antwoord)

#                 # print(f"thread in functie 'tafel kiezen 'er is aan gedraaid'': {threading.current_thread()}")
#                 # print(threading.active_count())
#                 # print(threading.enumerate())
#         if mijn_knop1.pressed == True:
#             gekozen_tafel = (antwoord_plaats+1)
#             print(f"*********oefenen starten***** met tafel {gekozen_tafel}**********")
#             nieuwe_oefensessie()
#             oefenen()

def keuze_tafel():
    # print(f"thread in functie 'BOVENAAN tafel kiezen 'er is aan gedraaid'': {threading.current_thread()}")
    global gekozen_tafel
    global waarde_rotor
    global antwoord_plaats
    global mijn_rotor
    mijn_rotor = Rotary(clk=19,dt=26,knop_aan = False, callback= callback_keuze_tafel)
    mijn_knop1.on_press(callback_OK_keuze_tafel)
    time.sleep(1)
    lijst_tafels = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6','T7', 'T8','T9', 'T10','T11', 'T12']
    mijn_matrix.matrix_instellen_kiezen(lijst_tafels[0])
    # print(f"thread in functie 'test_rotor': {threading.current_thread()}")
    # referentie_tijd_1 = time.time()
    # # print(threading.active_count())
    # # print(threading.enumerate())
    # while True and (gekozen_tafel == None):
    #             # print(f"thread in functie 'tafel kiezen 'er is aan gedraaid'': {threading.current_thread()}")
    #             # print(threading.active_count())
    #             # print(threading.enumerate())
    #     if ((time.time() - referentie_tijd_1) >= 2):
    #         referentie_tijd_1 = time.time()
    #         if mijn_knop1.pressed == True:
    #             gekozen_tafel = (antwoord_plaats+1)
    #             print(f"*********oefenen starten***** met tafel {gekozen_tafel}**********")
    #             mijn_rotor.close_rotor()
    #             nieuwe_oefensessie()
    #             oefenen()

def callback_keuze_tafel(waarde, richting):
    print(threading.active_count())
    print(threading.enumerate())
    global waarde_rotor
    global antwoord_plaats
    lijst_tafels = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6','T7', 'T8','T9', 'T10','T11', 'T12']
    if waarde_rotor != waarde:
        waarde_rotor = waarde
        print(f'er is aan gedraaid {waarde_rotor}, Richting: {richting}")')
        antwoord_plaats = ((abs(waarde_rotor))%(len(lijst_tafels)))
        antwoord = lijst_tafels[antwoord_plaats]
        mijn_matrix.matrix_instellen_kiezen(antwoord)

def callback_OK_keuze_tafel(pin):
    global antwoord_plaats
    global mijn_rotor
    global gekozen_tafel
    print(GPIO.input(23))
    if mijn_knop1.pressed:
        gekozen_tafel = (antwoord_plaats+1)
        print(f"*********oefenen starten***** met tafel {gekozen_tafel}**********")
        try:
            mijn_rotor.close_rotor()
            print("rotor afsluiten")
        except:
            print("rotor niet kunnen afsluiten")
        try:
            mijn_knop1.remove_event()
            print("knop 1 event afzetten")
        except:
            print("knop 1 event niet kunnen afzetten")
        nieuwe_oefensessie()
        return oefenen()


def oefenen():
    global gekozen_tafel
    global lengte_lijst_aantal_tafels
    global lijst_tafels_matrix
    global lijst_antwoorden
    global lijst_getal2
    global lijst_huidige_plaats
    # global huidige_oefening
    # global huidig_antwoord_correct
    # global huidig_getal2
    data = Tafels(gekozen_tafel).genereer_tafels()
    lijst_tafels_matrix = data[0]
    print(lijst_tafels_matrix)
    lijst_antwoorden = data[1]
    lijst_getal2 = data[2]
    lijst_huidige_plaats = 0
    lengte_lijst_aantal_tafels = len(lijst_tafels_matrix)
    return volgende_oefening()

    # for i in range(len(lijst_tafels_matrix)):
    #     oefening_antwoord_keuze(lijst_tafels_matrix[i], lijst_antwoorden[i], lijst_getal2[i])
    #     time.sleep(2)

def volgende_oefening():
    global lengte_lijst_aantal_tafels
    global lijst_tafels_matrix
    global lijst_antwoorden
    global lijst_getal2
    global lijst_huidige_plaats
    if lijst_huidige_plaats == lengte_lijst_aantal_tafels:
        print("volledige oefensessie afgewerkt")
        mijn_LCD.clearLCD()
        mijn_LCD.write_message('Hoera!')
        mijn_LCD.cursor_ga_naar(1,2)
        mijn_LCD.write_message('Je bent klaar')
        mijn_matrix.smiley_happy_instellen(2)
        time.sleep(2)
        mijn_LCD.clearLCD()
        mijn_LCD.write_message('Ga verder')
        mijn_LCD.cursor_ga_naar(1,2)
        mijn_LCD.write_message('of sluit af')
        time.sleep(2)
        return start_thread_keuze_tafel()
    else:
        lcd_huidige_oefening()
        oefening_antwoord_keuze(lijst_tafels_matrix[lijst_huidige_plaats], lijst_antwoorden[lijst_huidige_plaats], lijst_getal2[lijst_huidige_plaats])
    


# def oefening_antwoord_keuze(oefening, antwoord, getal2):
#     global waarde_rotor
#     waarde_rotor = 0
#     rotor_vorig = waarde_rotor
#     referentie_tijd_1 = time.time()
#     gekozen_antwoord = None
#     correctheid = None
#     mijn_matrix.matrix_instellen(oefening, str(waarde_rotor))
#     time.sleep(2)
#     # print(threading.active_count())
#     # print(threading.enumerate())
#     while True and (gekozen_antwoord == None):
#         if ((time.time() - referentie_tijd_1) >= 2):
#             referentie_tijd_1 = time.time()
#             if waarde_rotor != rotor_vorig:
#                 rotor_vorig = waarde_rotor
#                 print(f'er is aan gedraaid {waarde_rotor}')             
#                 mijn_matrix.matrix_instellen(antwoord=str(abs(waarde_rotor)))

#                 # print(f"thread in functie 'tafel kiezen 'er is aan gedraaid'': {threading.current_thread()}")
#                 # print(threading.active_count())
#                 # print(threading.enumerate())
#         if mijn_knop1.pressed == True:
#             gekozen_antwoord = abs(waarde_rotor)
#             print(f"*********antwoord oefening***** met antwoord {gekozen_antwoord}**********")
#             waarde_rotor = 0
#             rotor_vorig = 0
            
#     if (str(gekozen_antwoord) == str(antwoord)):
#         print('Correct')
#         mijn_matrix.smiley_happy_instellen(2)
#         nieuw_ingeoefend(getal2, 1, gekozen_antwoord)
#         time.sleep(1)
#     else:
#         print(f'Jammer, het antwoord is {antwoord}')
#         nieuw_ingeoefend(getal2, 0, gekozen_antwoord)
#         time.sleep(1)

def oefening_antwoord_keuze(oefening, antwoord, getal2):
    global waarde_rotor
    global mijn_rotor
    waarde_rotor = 0
    mijn_matrix.matrix_instellen(oefening, str(abs(waarde_rotor)))
    mijn_rotor = Rotary(clk=19,dt=26,knop_aan = False, callback= callback_keuze_antwoord)
    mijn_knop1.on_press(callback_OK_keuze_antwoord)

    # referentie_tijd_1 = time.time()
    # gekozen_antwoord = None
    # correctheid = None
   
    time.sleep(1)
    # while True and (gekozen_antwoord == None):
    #     if ((time.time() - referentie_tijd_1) >= 2):
    #         referentie_tijd_1 = time.time()
    #         if waarde_rotor != rotor_vorig:
    #             rotor_vorig = waarde_rotor
    #             print(f'er is aan gedraaid {waarde_rotor}')             
    #             mijn_matrix.matrix_instellen(antwoord=str(abs(waarde_rotor)))

    #             # print(f"thread in functie 'tafel kiezen 'er is aan gedraaid'': {threading.current_thread()}")
    #             # print(threading.active_count())
    #             # print(threading.enumerate())
    #     if mijn_knop1.pressed == True:
    #         gekozen_antwoord = abs(waarde_rotor)
    #         print(f"*********antwoord oefening***** met antwoord {gekozen_antwoord}**********")
    #         waarde_rotor = 0
    #         rotor_vorig = 0
            
    # if (str(gekozen_antwoord) == str(antwoord)):
    #     print('Correct')
    #     mijn_matrix.smiley_happy_instellen(2)
    #     nieuw_ingeoefend(getal2, 1, gekozen_antwoord)
    #     time.sleep(1)
    # else:
    #     print(f'Jammer, het antwoord is {antwoord}')
    #     nieuw_ingeoefend(getal2, 0, gekozen_antwoord)
    #     time.sleep(1)


def callback_keuze_antwoord(waarde, richting):
    # print(threading.active_count())
    # print(threading.enumerate())
    global waarde_rotor
    if abs(waarde_rotor) != waarde:
        waarde_rotor = waarde
        print(f'er is aan gedraaid {waarde_rotor}')             
        mijn_matrix.matrix_instellen(antwoord=str(abs(waarde_rotor)))

def callback_OK_keuze_antwoord(pin):
    global mijn_rotor
    global gekozen_tafel
    global waarde_rotor
    print(GPIO.input(23))
    if mijn_knop1.pressed:
        print(f"*********antwoord oefening***** met antwoord {waarde_rotor}**********")
        try:
            mijn_rotor.close_rotor()
            print("rotor afsluiten")
        except:
            print("rotor niet kunnen afsluiten")
        try:
            mijn_knop1.remove_event()
            print("knop 1 event afzetten")
        except:
            print("knop 1 event niet kunnen afzetten")
        antwoord_nagaan()

def antwoord_nagaan():
    global waarde_rotor
    global lijst_huidige_plaats
    if (str(abs(waarde_rotor)) == str(lijst_antwoorden[lijst_huidige_plaats])):
        print('Correct')
        mijn_matrix.smiley_happy_instellen(2)
        nieuw_ingeoefend(lijst_getal2[lijst_huidige_plaats], 1, abs(waarde_rotor))
        lijst_huidige_plaats += 1
        time.sleep(1)
    else:
        mijn_matrix.smiley_sad_instellen()
        print(f'Jammer, het antwoord is {lijst_antwoorden[lijst_huidige_plaats]}')
        nieuw_ingeoefend(lijst_getal2[lijst_huidige_plaats], 0, abs(waarde_rotor))
        time.sleep(1)
        mijn_matrix.matrix_instellen(lijst_tafels_matrix[lijst_huidige_plaats], lijst_antwoorden[lijst_huidige_plaats])
        lijst_huidige_plaats += 1
        time.sleep(3)
    return volgende_oefening()


def lcd_huidige_oefening():
    # global lijst_huidige_plaats
    # global lengte_lijst_aantal_tafels
    mijn_LCD.clearLCD() 
    mijn_LCD.write_message(f"Oefening {lijst_huidige_plaats+1}/{lengte_lijst_aantal_tafels}")

def start_thread():
    start_thread_persoon_dichtbij()
    start_thread_sensoren()
    
    print(threading.active_count())
    print(threading.enumerate())
    print("thread started")

def start_thread_rotor():
    t_rotor = threading.Thread(target=test_rotor, daemon=True)
    t_rotor.start()
    print(threading.active_count())
    print(threading.enumerate())
    print("thread rotor started")

# def start_thread_kiezen_rotor():
#     t_kiezen_rotor = threading.Thread(target=keuzen_rotor, daemon=True)
#     t_kiezen_rotor.start()
#     print(threading.active_count())
#     print(threading.enumerate())
#     print("thread t_kiezen_rotor started")

def start_thread_afsluiten():
    t_afsluiten = threading.Thread(target=afsluiten, daemon=True)
    t_afsluiten.start()
    print(threading.active_count())
    print(threading.enumerate())
    print("thread afsluiten started")

def start_thread_sensoren():
    t_sensoren = threading.Thread(target=sensor_uitlezen, daemon=True)
    t_sensoren.start()
    print(threading.active_count())
    print(threading.enumerate())
    print("thread sensoren started")

def start_thread_badgen():
    t_badgen = threading.Thread(target=detected_badge, daemon=True)
    t_badgen.start()
    print(threading.active_count())
    print(threading.enumerate())
    print("thread badgen started")

def start_thread_persoon_dichtbij():
    t_persoon_dichtbij = threading.Thread(target=persoon_dichtbij, daemon=True)
    t_persoon_dichtbij.start()
    print(threading.active_count())
    print(threading.enumerate())
    print("thread persoon_dichtbij started")

def start_thread_keuze_tafel():
    t_persoon_dichtbij = threading.Thread(target=keuze_tafel, daemon=True)
    t_persoon_dichtbij.start()
    print(threading.active_count())
    print(threading.enumerate())
    print("thread keuze tafel started")
    # print(f"thread in functie 'qtart keuzen'': {threading.current_thread()}")


#endregion Threads

#region API ENDPOINTS
# API ENDPOINTS

endpoint = '/projectOne/RietDeMeulemeester'
# endpoint = '/api/v1'


@app.route('/')
def hallo():
    # return "Server is running, er zijn momenteel geen API endpoints beschikbaar."
    return  jsonify(info='Please go to the endpoint ' + endpoint)



@app.route(endpoint + '/historiek/', methods=['GET'])
def historiekje():
    if request.method == 'GET':
        data = DataRepository.read_records_sensor_by_id(1)
        return jsonify(records=data), 200
    # if request.method == 'POST':
    #     data = 

@app.route(endpoint + '/home/', methods=['GET'])
@jwt_required()
def inloggen():
    current_user = get_jwt_identity()
    # print(current_user)
    if request.method == 'GET':
        data = DataRepository.read_leerling_by_id(current_user)
        return jsonify(info=data), 200

@app.route(endpoint + '/home/oefensessies/', methods=['GET'])
@jwt_required()
def oefensessiesLeerling():
    current_user = get_jwt_identity()
    # print(current_user)
    if request.method == 'GET':
        data = DataRepository.read_oefensessies_by_leerlingid(current_user)
        return jsonify(records=data), 200

@app.route(endpoint + '/home/oefensessie/<oefensessieid>/', methods=['GET'])
@jwt_required()
def oefensessie_by_id(oefensessieid):
    current_user = get_jwt_identity()
    # print(current_user)
    if request.method == 'GET':
        data = DataRepository.read_oefensessie_by_oefensessieid(oefensessieid)
        return jsonify(records=data), 200

@app.route(endpoint + '/home/oefeningen/<oefensessie>/', methods=['GET'])
@jwt_required()
def oefeningenOefensessie(oefensessie):
    current_user = get_jwt_identity()
    # print(current_user)
    if request.method == 'GET':
        data = DataRepository.read_alle_ingeoefend_by_oefensessieid(oefensessie)
        return jsonify(records=data), 200

@app.route(endpoint + '/home/oefensessies/aantal/', methods=['GET'])
@jwt_required()
def aantaloefensessiesLeerling():
    current_user = get_jwt_identity()
    # print(current_user)
    if request.method == 'GET':
        data = DataRepository.read_aantal_oefensessie_by_id(current_user)
        return jsonify(aantal=data), 200



@app.route(endpoint + '/home/oefeningen/aantal/', methods=['GET'])
@jwt_required()
def aantaloefeningenLeerling():
    current_user = get_jwt_identity()
    # print(current_user)
    if request.method == 'GET':
        data = DataRepository.read_aantal_oefeningen_by_id(current_user)
        return jsonify(aantal=data), 200
# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route(endpoint + '/login/', methods=['POST'])
def login():
    if request.method == 'POST':
        gegevens = DataRepository.json_or_formdata(request)

        print(gegevens)
        username = gegevens['username']
        password = gegevens['password']

        if not username:
            return jsonify(message= "Missing username parameter"), 449
        if not password:
            return jsonify(message= "Missing password parameter"), 449
        data = DataRepository.read_leerling(username, password)
        if data is not None:
            print("inloggen gelukt")
            print("correct")
            leerling_id = data['leerlingid']
            expires = timedelta(minutes=30)
            access_token = create_access_token(identity=leerling_id, expires_delta=expires)

            print(access_token)
            return jsonify(message="This is a public endpoint to generate a token", access_token=access_token), 200
        else:
            return jsonify(message="Username and/or password are incorrect"), 401



# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route(endpoint + '/protected/', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    # print(current_user)
    return jsonify(message="This is a protected endpoint: ", logged_in_as=current_user), 200


# @app.route(endpoint + '/public/', methods=['GET'])
# def public():
#     return jsonify(message="This is a public endpoint"), 200


#endregion API ENDPOINTS

#region SOCKET IO
# SOCKET IO
@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    # # Send to the client!
    # vraag de status op van de lampen uit de DB
    #status = DataRepository.read_status_lampen()
    # socketio.emit('B2F_status_lampen', {'lampen': status})
    # Beter is het om enkel naar de client te sturen die de verbinding heeft gemaakt.
    #emit('B2F_status_lampen', {'lampen': status}, broadcast=False)

# @socketio.on('F2B_switch_light')
# def switch_light(data):
#     print('licht gaat aan/uit', data)
#     lamp_id = data['lamp_id']
#     new_status = data['new_status']
#     # spreek de hardware aan
#     # stel de status in op de DB
#     res = DataRepository.update_status_lamp(lamp_id, new_status)
#     print(res)
#     # vraag de (nieuwe) status op van de lamp
#     data = DataRepository.read_status_lamp_by_id(lamp_id)
#     socketio.emit('B2F_verandering_lamp',  {'lamp': data})
#     # Indien het om de lamp van de TV kamer gaat, dan moeten we ook de hardware aansturen.
#     if lamp_id == '3':
#         print(f"TV kamer moet switchen naar {new_status} !")
#         # Do something

@socketio.on('F2B_new_logging')
def new_logging(msg):
    # print(msg)  # vb 1 of 2 (gebruikerid)
    huidige_temperatuur = mijn_temp.lees_temperatuur()
    # print(huidige_temperatuur)
    idnummer = DataRepository.create_device_record(msg, huidige_datumtijd(), huidige_temperatuur)
    if idnummer is not None:
        socketio.emit('B2F_new_logging')

        
@socketio.on('F2B_zijn_home')
def home(msg):
    emit('B2F_toon_info', msg)


@socketio.on('F2B_shutdown')
def shutdownbutton(msg=None):
    print('shutdown ontvangen')
    mijn_LCD.clearLCD()
    mijn_LCD.write_message("Tot ziens!")
    time.sleep(2)
    mijn_LCD.set_cursor_display(displayOn=False)
    mijn_LCD.clearLCD()
    mijn_matrix.uit()
    mijn_matrix.close()
    GPIO.cleanup()
    call("sudo shutdown -h now", shell=True)

# @socketio.on('B2F_gebruiker_nodig')
# def home(token):
#     verify_jwt_in_request()
#     current_user = get_jwt_identity()
#     print(current_user)
#endregion SOCKET IO

def nieuwe_oefensessie():
    global huidig_oefensessieid
    startmoment = huidige_datumtijd()
    idoefensessie = DataRepository.create_oefensessie(huidige_leerlingid,startmoment, None)
    if idoefensessie is not None:
        huidig_oefensessieid = idoefensessie
        socketio.emit('B2F_new_oefensessie')

def nieuw_ingeoefend(getal2, correct, antwoord):
    tafelid_tafel = DataRepository.read_tafelid(gekozen_tafel)
    # print(tafelid_tafel)
    registratiemoment = huidige_datumtijd()
    idoefening = DataRepository.create_ingeoefend(huidig_oefensessieid, tafelid_tafel['tafelid'], gekozen_tafel, getal2, antwoord, correct, registratiemoment)
    if idoefening is not None:
        print('** registreren oegening gelukt **')
        socketio.emit('B2F_new_oefening')
    else:
        print('-- toevoegen oef niet gelukt--')

    


#region MAIN        
     
if __name__ == '__main__':
    try:
        GPIO.setmode(GPIO.BCM)
        # GPIO.setup(chip_select, GPIO.OUT)
        # GPIO.output(chip_select, GPIO.HIGH)
        mijn_ip_lijst = IP_lezen().ip_uitlezen() # ['192.168.168.169', '172.30.248.176']
        print(f"Mijn ip lijst: {mijn_ip_lijst}")
        mijn_LCD = LCD(0x38,21,20, cursor=False, blinkCursor=False)
        # status_ip_zichtbaar_instellen()
        # mijn_HC_SR04 = HC_SR04(16, 12)
        # mijn_rotor = Rotary(clk=19,dt=26,knop_aan = False, callback= callback_print)
        # mijn_rfid = RFID(bus=0, device=1, pin_rst=17, pin_mode=GPIO.BCM, pin_irq=13, pin_ce=1)
        mijn_temp = TempOneWire(bestandsnaam)
        mijn_knop1 = Button(pin=23)  # OK knop
        mijn_knop2 = Button(pin=24)  # IP knop en afsluiten
        mijn_matrix = Matrix()
        setup_hulpklasses()
        # detected_badge() # Moet als eerste gebeuren. 
    
        start_thread()
        print("**** Starting APP ****")
        socketio.run(app, debug=False, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print('KeyboardInterrupt exception is caught')
    finally:
        print(threading.active_count())
        print(threading.enumerate())
        mijn_LCD.clearLCD()
        mijn_LCD.write_message("Tot ziens!")
        time.sleep(2)
        mijn_LCD.set_cursor_display(displayOn=False)
        mijn_LCD.clearLCD()
        # mijn_rfid.cleanup()
        mijn_LCD.closesLCD()
        mijn_matrix.uit()
        mijn_matrix.close()
        # mijn_rotor.close_rotor()
        GPIO.cleanup()
        print("finished")

#endregion MAIN   
