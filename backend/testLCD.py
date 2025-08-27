from helpers.klasseLCD import LCD
from helpers.klasseip import IP_lezen
import time

mijn_LCD = LCD(0x38, 21, 20)

mijn_LCD.init_LCD()



# mijn_LCD.set_cursor_display(cursorOn=False,blinkCursor=False)
mijn_ip_lijst = IP_lezen().ip_uitlezen()
print(f"Mijn ip lijst: {mijn_ip_lijst}")
mijn_LCD.cursor_ga_naar(pagina=2, lijn=1)
mijn_LCD.write_message(mijn_ip_lijst[0])
mijn_LCD.cursor_ga_naar(2, 2)
mijn_LCD.write_message(mijn_ip_lijst[1])
# mijn_LCD.cursorHome_0x00()





# mijn_LCD.display_zichtbaar_maken(2)
# for i in range(16):
#     mijn_LCD.display_shift(1, False)
#     time.sleep(1)
mijn_LCD.display_zichtbaar_maken(2)
referentie_tijd_ip = time.time()
ip_getoond = False
while (True and (ip_getoond == False)):
    if ((time.time() - referentie_tijd_ip) >= 5):
        referentie_tijd_ip = time.time()
        mijn_LCD.display_zichtbaar_maken(1)
        ip_getoond = True





