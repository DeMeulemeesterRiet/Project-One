from datetime import datetime, timedelta
# import datetime
from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.method != 'GET' and request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    # Tafels
    @staticmethod
    def read_tafelid(tafel):
        sql = "SELECT tafelid FROM tafels WHERE getal = %s"
        params = [tafel]
        return Database.get_one_row(sql,params)

    # Device + historiek
    @staticmethod
    def create_device_record(deviceid,datumtijd,waarde):
        sql = "INSERT INTO projectoneriet.historiek (deviceid, datumtijd, waarde) VALUES (%s,%s,%s)"
        params = [deviceid,datumtijd,waarde]
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def read_records_sensor_by_id(deviceid):
        sql = "SELECT datumtijd, waarde from historiek WHERE deviceid = %s"
        params = [deviceid]
        return Database.get_rows(sql,params)
    
    @staticmethod
    def read_sensor_by_id(deviceid):
        sql = "SELECT * from device WHERE deviceid = %s"
        params = [deviceid]
        return Database.get_one_row(sql,params)
    

    # Leerlingen
    @staticmethod
    def read_leerlingen():
        sql = "SELECT * FROM leerlingen"
        return Database.get_rows(sql)        
    @staticmethod
    def read_leerling(naam, wachtwoord):
        sql = "SELECT leerlingid, naam FROM leerlingen WHERE naam = %s AND  wachtwoord = %s;"
        params = [naam, wachtwoord]
        return Database.get_one_row(sql,params)  
    @staticmethod
    def read_leerling_by_rfidcode(badgecode):
        sql = "SELECT leerlingid, naam FROM leerlingen WHERE rfidcode = %s"
        params = [badgecode]
        return Database.get_one_row(sql,params) 
    @staticmethod
    def read_leerling_by_id(id):
        sql = "SELECT leerlingid, naam FROM leerlingen WHERE leerlingid = %s"
        params = [id]
        return Database.get_one_row(sql,params) 

    # Oefensessie
    @staticmethod
    def create_oefensessie(leerlingid, startmoment, eindmoment):
        sql = "INSERT INTO oefensessie (leerlingid, startmoment, eindmoment) VALUES (%s,%s,%s)"
        params = [leerlingid, startmoment, eindmoment]
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def read_oefensessie_by_id(oefensessieid):
        sql = "SELECT * from oefensessie WHERE oefensessieid = %s"
        params = [oefensessieid]
        return Database.get_one_row(sql,params)
     
    @staticmethod
    def read_oefensessies_by_leerlingid(leerlingid):
        sql = "SELECT o.oefensessieid, TO_CHAR(o.startmoment, 'DD/MM/YYYY') AS startdatum, TO_CHAR(o.startmoment, 'HH24:MI') AS startuur, i.getal1, COUNT(*) AS totaal_aantal_oefeningen, SUM(CASE WHEN i.correct = 1 THEN 1 ELSE 0 END) AS aantal_correct FROM   oefensessie o JOIN ingeoefend i ON o.oefensessieid = i.oefensessieid WHERE  o.leerlingid = %s GROUP BY  o.oefensessieid, o.startmoment, i.getal1 ORDER BY  o.startmoment DESC;"
        params = [leerlingid]
        records = Database.get_rows(sql,params)
        return records


    @staticmethod
    def read_oefensessie_by_oefensessieid(oefensessieid):
        sql = " SELECT o.oefensessieid, TO_CHAR(o.startmoment, 'DD/MM/YYYY') AS startdatum, TO_CHAR(o.startmoment, 'HH24:MI') AS startuur, i.getal1, COUNT(*) AS totaal_aantal_oefeningen, SUM(CASE WHEN i.correct = 1 THEN 1 ELSE 0 END) AS aantal_correct FROM  oefensessie o JOIN  ingeoefend i ON o.oefensessieid = i.oefensessieid  WHERE o.oefensessieid = %s  GROUP BY  o.oefensessieid, o.startmoment, i.getal1 ORDER BY o.startmoment"
        params = [oefensessieid]
        records = Database.get_rows(sql,params)
        return records

    @staticmethod
    def read_aantal_oefensessie_by_id(leerlingid):
        sql = "SELECT  COUNT(DISTINCT o.oefensessieid) AS totaal_aantal_oefensessies FROM oefensessie o WHERE o.leerlingid = %s AND EXISTS ( SELECT 1 FROM ingeoefend i WHERE i.oefensessieid = o.oefensessieid );"
        params = [leerlingid]
        return Database.get_one_row(sql,params)

    # Ingeoefend
    @staticmethod
    def create_ingeoefend(oefensessieid, tafelid, getal1, getal2, antwoord, correct, registratiemoment):
        sql = "INSERT INTO ingeoefend (oefensessieid, tafelid, getal1, getal2, antwoord, correct, registratiemoment) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        params = [oefensessieid, tafelid, getal1, getal2, antwoord, correct, registratiemoment]
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def read_alle_ingeoefend_by_oefensessieid(oefensessieid):
        sql = "SELECT * from ingeoefend WHERE oefensessieid = %s"
        params = [oefensessieid]
        return Database.get_rows(sql,params)
    
    @staticmethod
    def read_alle_ingeoefend_by_oefensessieid_foutief(oefensessieid):
        sql = "SELECT * from ingeoefend WHERE oefensessieid = %s and correct = 0"
        params = [oefensessieid]
        return Database.get_rows(sql,params)
    
    @staticmethod
    def read_alle_ingeoefend_by_oefensessieid_juist(oefensessieid):
        sql = "SELECT * from ingeoefend WHERE oefensessieid = %s and correct = 1"
        params = [oefensessieid]
        return Database.get_rows(sql,params)

    @staticmethod
    def read_alle_ingeoefend_by_leerlingid(leerlingid):
        sql = "SELECT ingeoefend.* FROM ingeoefend JOIN oefensessie ON ingeoefend.oefensessieid = oefensessie.oefensessieid WHERE oefensessie.leerlingid = %s"
        params = [leerlingid]
        return Database.get_rows(sql,params)

    @staticmethod
    def read_alle_ingeoefend_by_leerlingid_juist(leerlingid):
        sql = "SELECT ingeoefend.* FROM ingeoefend JOIN oefensessie ON ingeoefend.oefensessieid = oefensessie.oefensessieid WHERE oefensessie.leerlingid = %s AND ingeoefend.correct = 1"
        params = [leerlingid]
        return Database.get_rows(sql,params)

    @staticmethod
    def read_alle_ingeoefend_by_leerlingid_fout(leerlingid):
        sql = "SELECT ingeoefend.* FROM ingeoefend JOIN oefensessie ON ingeoefend.oefensessieid = oefensessie.oefensessieid WHERE oefensessie.leerlingid = %s AND ingeoefend.correct = 0"
        params = [leerlingid]
        return Database.get_rows(sql,params)
    
    @staticmethod
    def read_aantal_oefeningen_by_id(leerlingid):
        sql = "SELECT COUNT(*) AS totaal_aantal_oefeningen FROM ingeoefend i JOIN oefensessie o ON i.oefensessieid = o.oefensessieid WHERE o.leerlingid = %s  AND EXISTS (SELECT 1 FROM ingeoefend WHERE oefensessieid = o.oefensessieid);"
        params = [leerlingid]
        return Database.get_one_row(sql,params)

    # tafels
    @staticmethod
    def read_tafel_by_getal(getal):
        sql = "SELECT * from tafels WHERE getal = %s"
        params = [getal]
        return Database.get_one_row(sql,params)
    
    @staticmethod
    def read_tafel_by_moeilijkheidsgraad(getal_moeilijkheidsgraad):
        sql = "SELECT * from tafels WHERE moeilijkheidsgraad = %s"
        params = [getal_moeilijkheidsgraad]
        return Database.get_one_row(sql,params)