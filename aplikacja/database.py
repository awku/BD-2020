import psycopg2
import json 

class DataBase():
    def __init__(self):
        """inicjalizacja i łączenie się z bazą danych"""
        database="wtshrchu"
        username="wtshrchu"
        password="UyNLvApGg4xA-K09gJFArm8841DF25jw"
        hostname="dumbo.db.elephantsql.com"
        port="5432"
        self.conn = psycopg2.connect(database=database, user=username, password=password, host=hostname, port=port)

    def close_database(self):
        """zamknięcie połączenia z bazą"""
        self.conn.close()

    def handle_errors(self, err):
        """cofnięcie operacji w przypadku błędu z triggera i przyjaźniejsze dla użytkownika wyświetlanie komunikatu"""
        errormessage = str(err.pgerror).split("CONTEXT")
        self.conn.rollback()
        return errormessage[0]
    
    def handle_general_errors(self, err):
        """cofnięcie operacji w przypadku błędu i przyjaźniejsze dla użytkownika wyświetlanie komunikatu"""
        errormessage = str(err.pgerror).split("LINE")
        self.conn.rollback()
        return errormessage[0]

    def update_reservations(self):
        """aktualizacja rezerwacji"""
        cur = self.conn.cursor()
        try:
            cur.execute("""SELECT * FROM aktualizuj_rezerwacje()""")
            self.conn.commit()
            message = (True, 'Pomyslnie zaktualizowano statusy rezerwacji')
        except psycopg2.errors.RaiseException as err:
            print(err)
            message = (False, self.handle_errors(err))
        except Exception as err:
            print(err)
            message = (False, self.handle_general_errors(err))
        cur.close()
        return message

    def get_statistics(self):
        """odczyt ogólnych statystyk hoteli w bazie"""
        cur = self.conn.cursor()
        data = {}

        cur.execute("SELECT min_cena, max_cena FROM min_max_cena;")
        result = cur.fetchone()
        data.setdefault("min_cena", result[0])
        data.setdefault("max_cena", result[1])

        cur.execute("SELECT l_hoteli FROM liczba_hoteli;")
        result = cur.fetchone()
        data.setdefault("liczba_hoteli", result[0])

        cur.execute("SELECT l_pokoi FROM liczba_pokoi;")
        result = cur.fetchone()
        data.setdefault("liczba_pokoi", result[0])

        cur.close()
        return data

    def get_hotel_statistics(self, id_hotel):
        """odczyt statystyk dla hotelu z danym id_hotel"""
        cur = self.conn.cursor()
        data = {}

        cur.execute("SELECT min_cena, max_cena FROM min_max_cena_na_hotel WHERE id_hotel=%s;", (id_hotel,))
        result = cur.fetchone()
        data.setdefault("min_cena", result[0])
        data.setdefault("max_cena", result[1])

        cur.execute("SELECT l_pokoi FROM liczba_pokoi_na_hotel WHERE id_hotel=%s;", (id_hotel,))
        result = cur.fetchone()
        data.setdefault("liczba_pokoi", result[0])

        cur.close()
        return data

    def get_guest(self, id_gosc):
        """odczyt informacji o danym gościu"""
        cur = self.conn.cursor()
        cur.execute("SELECT email, imie, nazwisko, telefon FROM Gosc WHERE id_gosc=%s;", (id_gosc,))
        result = cur.fetchone()
        data = {'email':result[0], 
                'imie':result[1],
                'nazwisko':result[2], 
                'telefon':result[3]}
        cur.close()
        return data

    def get_employee(self, id_pracownik):
        """odczyt informacji o danym pracowniku"""
        cur = self.conn.cursor()
        cur.execute("SELECT email, imie, nazwisko FROM Pracownik WHERE id_pracownik=%s;", (id_pracownik,))
        result = cur.fetchone()
        data = {'email':result[0], 
                'imie':result[1],
                'nazwisko':result[2]}
        cur.close()
        return data

    def get_attractions(self):
        """odczyt wszystkich możliwych atrakcji z bazy danych"""
        cur = self.conn.cursor()
        cur.execute("SELECT id_atrakcje, opis FROM Atrakcje;")
        result = cur.fetchall()
        data = [(x[0], x[1]) for x in result]
        cur.close()
        return data

    def get_status(self):
        """odczyt wszystkich możliwych statusów rezerwacji z bazy danych"""
        cur = self.conn.cursor()
        cur.execute("SELECT id_status, opis FROM Status;")
        result = cur.fetchall()
        data = [(x[0], x[1]) for x in result]
        cur.close()
        return data

    def get_equipments(self):
        """odczyt wszystkich możliwych wyposażeń pokoju z bazy danych"""
        cur = self.conn.cursor()
        cur.execute("SELECT id_wyposazenie, opis FROM Wyposazenie;")
        result = cur.fetchall()
        data = [(x[0], x[1]) for x in result]
        cur.close()
        return data

    def get_hotel_attractions(self, id_hotel):
        """odczyt atrakcji danego hotelu"""
        cur = self.conn.cursor()
        cur.execute("SELECT opis, otwarcie, zamkniecie, cena_godzina FROM atrakcje_hotelu WHERE id_hotel=%s;", (id_hotel,))
        result = cur.fetchall()
        data = [(x[0], x[1], x[2], x[3]) for x in result]
        cur.close()
        return data

    def get_hotels(self):
        """odczyt wszystkich hoteli wraz z ich sieciami z bazy danych"""
        cur = self.conn.cursor()
        cur.execute("SELECT nazwa_sieci, id_hotel, nazwa, adres, email, telefon, kategoria FROM hotele_sieci;")
        result = cur.fetchall()
        data = {}
        for x in result:
            data.setdefault(x[0], [])
            data[x[0]].append({'id_hotel': x[1], 'nazwa':x[2], 'adres':x[3], 'email':x[4], 'telefon':x[5], 'kategoria': x[6]})
        cur.close()
        return data

    def get_filtered_hotels(self, args):
        """odczyt wszystkich hoteli wraz z ich sieciami z bazy danych przefiltrowane przez dostępność atrakcji"""
        cur = self.conn.cursor()
        cur.execute("SELECT nazwa_sieci, id_hotel, nazwa, adres, email, telefon, kategoria FROM filtruj_atrakcje %s;", (args,))
        result = cur.fetchall()
        data = {}
        for x in result:
            data.setdefault(x[0], [])
            data[x[0]].append({'id_hotel': x[1], 'nazwa':x[2], 'adres':x[3], 'email':x[4], 'telefon':x[5], 'kategoria': x[6]})
        self.conn.commit()
        cur.close()
        return data

    def get_filtered_rooms(self, data):
        """odczyt wszystkich pokoji z danego hotelu przefiltrowane przez dostępność pokoi"""
        cur = self.conn.cursor()
        cur.execute("""SELECT numer, id_pokoj, nazwa, opis_typu, dla_palaczy, typ_wezlu_higsan, pietro, liczba_miejsc, 
            opis_pokoju, cena, okres_poczatek, okres_koniec FROM filtruj_pokoje(%s,%s,%s);""", (data['data_start'],data['data_end'], data['id_hotel']))
        result = cur.fetchall()
        data = {}
        for x in result:
            data.setdefault(x[0], [])
            data[x[0]].append({'numer': x[0], 'id_pokoj':x[1], 'nazwa':x[2], 'opis_typu':x[3], 'dla_palaczy':x[4],
            'typ_wezlu_higsan':x[5], 'pietro':x[6], 'liczba_miejsc':x[7], 'opis_pokoju':x[8], 'cena':x[9], 'okres_poczatek':x[10],
            'okres_koniec':x[11]})
        cur.close()
        return data

    def get_room_availability(self, id_pokoj):
        """odczyt wolnych terminów pokoju"""
        cur = self.conn.cursor()
        cur.execute("SELECT data_poczatku, data_konca FROM terminy_pokoju WHERE id_pokoj=%s;", (id_pokoj,))
        result = cur.fetchall()
        data = []
        for x in result:
            data.append({'data_poczatku': x[0], 'data_konca':x[1]})
        cur.close()
        return data

    def get_calculated_price(self, data):
        """odczyt wyliczonej przez bazę kwoty za dany pobyt"""
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM wylicz_cene(%s, %s, %s);", (data['data_poczatku'], data['data_konca'], data['id_pokoj']))
        result = cur.fetchone()[0]
        cur.close()
        return result

    def get_guest_reservations(self, id_gosc):
        """odczyt wszystkich rezerwacji złożonych przez danego gościa"""
        cur = self.conn.cursor()
        cur.execute("""SELECT id_rezerwacja, id_pokoj, data_poczatku, data_konca, data_rezerwacji, opis 
                FROM rezerwacje_goscia WHERE id_gosc=%s AND r=1;""", (id_gosc,))
        result = cur.fetchall()
        data = {}
        for x in result:
            data.setdefault(x[0], {'id_pokoj':x[1], 'data_poczatku':x[2], 'data_konca':x[3], 'data_rezerwacji':x[4], 'opis':x[5]})
        cur.close()
        return data

    def get_hotel_reservations(self, id_hotel):
        """odczyt wszystkich rezerwacji złożonych w danym hotelu"""
        cur = self.conn.cursor()
        cur.execute("""SELECT id_rezerwacja, id_pokoj, data_poczatku, data_konca, data_rezerwacji, opis, id_gosc, email
                FROM rezerwacje_hotelu WHERE id_hotel=%s AND r=1;""", (id_hotel,))
        result = cur.fetchall()
        data = {}
        for x in result:
            data.setdefault(x[0], {'id_pokoj':x[1], 'data_poczatku':x[2], 'data_konca':x[3], 'data_rezerwacji':x[4], 'opis':x[5], 'id_gosc':x[6], 'email':x[7]})
        cur.close()
        return data

    def get_filtered_hotel_reservations(self, id_hotel, email):
        """odczyt wszystkich rezerwacji złożonych w danym hotelu przez gościa o danym adresie email"""
        cur = self.conn.cursor()
        cur.execute("""SELECT id_rezerwacja, id_pokoj, data_poczatku, data_konca, data_rezerwacji, opis, id_gosc, email
                FROM rezerwacje_hotelu WHERE id_hotel=%s AND LOWER(email)=LOWER(%s) AND r=1;""", (id_hotel,email))
        result = cur.fetchall()
        data = {}
        for x in result:
            data.setdefault(x[0], {'id_pokoj':x[1], 'data_poczatku':x[2], 'data_konca':x[3], 'data_rezerwacji':x[4],'opis':x[5], 'id_gosc':x[6], 'email':x[7]})
        cur.close()
        return data

    def get_rooms(self, id_hotel):
        """odczyt wszystkich pokoi z danego hotelu"""
        cur = self.conn.cursor()
        cur.execute("""SELECT numer, id_pokoj, nazwa, opis_typu, dla_palaczy, typ_wezlu_higsan, pietro, liczba_miejsc, 
            opis_pokoju, cena, okres_poczatek, okres_koniec FROM pokoje_hotelu WHERE id_hotel=%s;""", (id_hotel,))
        result = cur.fetchall()
        data = {}
        for x in result:
            data.setdefault(x[0], [])
            data[x[0]].append({'numer': x[0], 'id_pokoj':x[1], 'nazwa':x[2], 'opis_typu':x[3], 'dla_palaczy':x[4],
            'typ_wezlu_higsan':x[5], 'pietro':x[6], 'liczba_miejsc':x[7], 'opis_pokoju':x[8], 'cena':x[9], 'okres_poczatek':x[10],
            'okres_koniec':x[11]})
        cur.close()
        return data

    def get_chains(self):
        """odczyt wszystkich sieci w bazie"""
        cur = self.conn.cursor()
        cur.execute("SELECT id_siec, nazwa FROM Siec;")
        result = cur.fetchall()
        data = {}
        for x in result:
            data.setdefault(x[0],{'nazwa': x[1]})
        cur.close()
        return data
    
    def get_types(self, id_hotel):
        """odczyt typów pokoju"""
        cur = self.conn.cursor()
        cur.execute("SELECT id_typ, nazwa, opis_pokoju, dla_palaczy, typ_wezlu_higsan, ilosc, opis_wyposazenia FROM typy_pokojow WHERE id_hotel=%s;", (id_hotel,))
        result = cur.fetchall()
        data = {}
        for x in result:
            data.setdefault(x[0], {'id_typ': x[0], 'nazwa' : x[1], 'opis_pokoju' : x[2], 'dla_palaczy' : x[3],
            'typ_wezlu_higsan' : x[4], 'wyposazenie':[]})
            data[x[0]]['wyposazenie'].append({'ilosc': x[5], 'opis_wyposazenia' : x[6]})
        cur.close()
        return data

    def get_room_equipments(self, id_pokoj):
        """odczyt wyposażenia danego pokoju"""
        cur = self.conn.cursor()
        cur.execute("SELECT ilosc, opis FROM wyposazenie_pokoju WHERE id_pokoj=%s;", (id_pokoj,))
        result = cur.fetchall()
        data = []
        for x in result:
            data.append({'ilosc': x[0], 'opis' : x[1]})
        cur.close()
        return data

    def add_guest(self, data):
        """rejestracja gościa w bazie"""
        cur = self.conn.cursor()
        try:
            cur.execute("INSERT INTO Gosc ( email, haslo, imie, nazwisko, telefon ) VALUES (%s, crypt(%s, gen_salt('bf')), %s, %s, %s);",
                    (data['email'], data['haslo'], data['imie'], data['nazwisko'], data['telefon']))
            message = (True,"Pomyslnie zarejestrowano")
            self.conn.commit()
        except psycopg2.errors.RaiseException as err:
            print(err)
            message = (False, self.handle_errors(err))
        except Exception as err:
            print(err)
            message = (False, self.handle_general_errors(err))
        cur.close()
        return message

    def update_guest(self, data, id_gosc):
        """edycja danych gościa o danym id_gosc"""
        cur = self.conn.cursor()
        try:
            if data['email']:
                cur.execute("UPDATE Gosc SET email = %s WHERE id_gosc = %s", (data['email'], id_gosc))
                self.conn.commit()
            if data['haslo']:
                cur.execute("UPDATE Gosc SET haslo = crypt(%s, gen_salt('bf')) WHERE id_gosc = %s", (data['haslo'], id_gosc))
                self.conn.commit()
            if data['imie']:
                cur.execute("UPDATE Gosc SET imie = %s WHERE id_gosc = %s", (data['imie'], id_gosc))
                self.conn.commit()
            if data['nazwisko']:
                cur.execute("UPDATE Gosc SET nazwisko = %s WHERE id_gosc = %s", (data['nazwisko'], id_gosc))
                self.conn.commit()
            if data['telefon']:
                cur.execute("UPDATE Gosc SET telefon = %s WHERE id_gosc = %s", (data['telefon'], id_gosc))
                self.conn.commit()
            message = (True,"Pomyslnie edytowano dane")
        except psycopg2.errors.RaiseException as err:
            print(err)
            message = (False, self.handle_errors(err))
        except Exception as err:
            print(err)
            message = (False, self.handle_general_errors(err))
        cur.close()
        return message

    def add_employee(self, data):
        """rejestracja pracownika"""
        cur = self.conn.cursor()
        try:
            cur.execute("""INSERT INTO Pracownik ( id_hotel, email, haslo, imie, nazwisko) 
                    VALUES (%s, %s, crypt(%s, gen_salt('bf')), %s, %s);""", 
                    (data['id_hotel'], data['email'], data['haslo'], data['imie'], data['nazwisko']))
            message = (True,"Pomyslnie dodano pracownika")
            self.conn.commit()
        except psycopg2.errors.RaiseException as err:
            print(err)
            message = (False, self.handle_errors(err))
        except Exception as err:
            print(err)
            message = (False, self.handle_general_errors(err))
        cur.close()
        return message

    def update_employee(self, data, id_pracownik):
        """edycja danych pracownika o danym id_pracownik"""
        cur = self.conn.cursor()
        try:
            if data['email']:
                cur.execute("UPDATE Pracownik SET email = %s WHERE id_pracownik = %s", (data['email'], id_pracownik))
                self.conn.commit()
            if data['haslo']:
                cur.execute("UPDATE Pracownik SET haslo = crypt(%s, gen_salt('bf')) WHERE id_pracownik = %s", (data['haslo'], id_pracownik))
                self.conn.commit()
            if data['imie']:
                cur.execute("UPDATE Pracownik SET imie = %s WHERE id_pracownik = %s", (data['imie'], id_pracownik))
                self.conn.commit()
            if data['nazwisko']:
                cur.execute("UPDATE Pracownik SET nazwisko = %s WHERE id_pracownik = %s", (data['nazwisko'], id_pracownik))
                self.conn.commit()
            message = (True,"Pomyslnie edytowano dane")
        except psycopg2.errors.RaiseException as err:
            print(err)
            message = (False, self.handle_errors(err))
        except Exception as err:
            print(err)
            message = (False, self.handle_general_errors(err))
        cur.close()
        return message

    def login_user(self, data):
        """sprawdzanie poprawności logowania użytkownika"""
        cur = self.conn.cursor()
        cur.execute("SELECT id_gosc FROM Gosc WHERE email=%s AND haslo = crypt(%s, haslo);", (data['email'], data['haslo']))
        result = cur.fetchone()
        if result:
            cur.close()
            return (True, False, result[0])
        else:
            cur.execute("SELECT id_hotel, id_pracownik FROM Pracownik WHERE email=%s AND haslo = crypt(%s, haslo);", (data['email'], data['haslo']))
            result = cur.fetchone()
            if result:
                cur.close()
                return (True, True, result[0], result[1])
        cur.close()
        return (False, False)

    def logout(self):
        """wylogowanie użytkownika, czyli usunięcie obecnego user_id z bazy"""
        cur = self.conn.cursor()
        cur.execute("SET public.user_id TO DEFAULT;")
        self.conn.commit()
        cur.close()

    def add_guest_reservation(self, data):
        """dodawanie rezerwacji przez gościa"""
        cur = self.conn.cursor()
        cur.execute("SET public.user_id = %s", (data['id_gosc'],))
        try:
            cur.execute("""INSERT INTO Rezerwacja (id_pokoj, data_poczatku, data_konca, data_rezerwacji) 
                VALUES (%s, %s, %s, CURRENT_DATE);""", (data['id_pokoj'],data['data_poczatku'], data['data_konca']))
            message = (True, "Pomyslnie zlozono rezerwacje")
            self.conn.commit()
        except psycopg2.errors.RaiseException as err:
            print(err)
            message = (False, self.handle_errors(err))
        except Exception as err:
            print(err)
            message = (False, self.handle_general_errors(err))
        cur.close()
        return message

    def cancel_guest_reservation(self, data):
        """anulowanie danej rezerwacji przez gościa"""
        cur = self.conn.cursor()
        try:
            cur.execute("SELECT * FROM anuluj_rezerwacje(%s);", (data,))
            message = (True, "Pomyslnie anulowano rezerwacje")
            self.conn.commit()
        except psycopg2.errors.RaiseException as err:
            print(err)
            message = (False, self.handle_errors(err))
        except Exception as err:
            print(err)
            message = (False, self.handle_general_errors(err))
        cur.close()
        return message

    def pay_guest_reservation(self, data):
        """zapłacanie za daną rezerwacje przez gościa"""
        cur = self.conn.cursor()
        try:
            cur.execute("INSERT INTO Status_rezerwacji (id_rezerwacja, data_zmiany_stanu, id_status) VALUES (%s, CURRENT_DATE, 2);", (data,))
            message = (True, "Pomyslnie zaplacono za rezerwacje")
            self.conn.commit()
        except psycopg2.errors.RaiseException as err:
            print(err)
            message = (False, self.handle_errors(err))
        except Exception as err:
            print(err)
            message = (False, self.handle_general_errors(err))
        cur.close()
        return message

    def change_guest_reservation(self, data):
        """zmiana statusu danej rezerwacji przez pracownika"""
        cur = self.conn.cursor()
        try:
            cur.execute("INSERT INTO Status_rezerwacji (id_rezerwacja, data_zmiany_stanu, id_status) VALUES (%s, CURRENT_DATE, %s);", 
                (data['id_rezerwacja'],data['id_status']))
            message = (True, "Pomyslnie zmieniono status rezerwacji")
            self.conn.commit()
        except psycopg2.errors.RaiseException as err:
            print(err)
            message = (False, self.handle_errors(err))
        except Exception as err:
            print(err)
            message = (False, self.handle_general_errors(err))
        cur.close()
        return message

    def add_chain(self, data):
        """dodawanie sieci do bazy"""
        cur = self.conn.cursor()
        try:
            cur.execute("INSERT INTO Siec (nazwa) VALUES (%s);", (data['nazwa'],))
            message = (True, "Pomyslnie dodano siec")
            self.conn.commit()
        except psycopg2.errors.RaiseException as err:
            print(err)
            message = (False, self.handle_errors(err))
        except Exception as err:
            print(err)
            message = (False, self.handle_general_errors(err))
        cur.close()
        return message
    
    def add_hotel(self, data):
        """dodawanie hotelu do bazy"""
        cur = self.conn.cursor()
        try:
            cur.execute("INSERT INTO Hotel (id_siec, nazwa, telefon, email, kategoria, adres) VALUES (%s, %s, %s, %s, %s, %s);",
                (data['id_siec'], data['nazwa'],data['telefon'], data['email'],data['kategoria'], data['adres']))
            message = (True, "Pomyslnie dodano hotel")
            self.conn.commit()
        except psycopg2.errors.RaiseException as err:
            print(err)
            message = (False, self.handle_errors(err))
        except Exception as err:
            print(err)
            message = (False, self.handle_general_errors(err))
        cur.close()
        return message

    def add_attraction(self, data):
        """dodawanie atrakcji do bazy"""
        cur = self.conn.cursor()
        try:
            cur.execute("INSERT INTO Atrakcje (opis) VALUES (%s);", (data['opis'],))
            message = (True, "Pomyslnie dodano atrakcje")
            self.conn.commit()
        except psycopg2.errors.RaiseException as err:
            print(err)
            message = (False, self.handle_errors(err))
        except Exception as err:
            print(err)
            message = (False, self.handle_general_errors(err))
        cur.close()
        return message

    def add_equipment(self, data):
        """dodawanie wyposażenia do bazy"""
        cur = self.conn.cursor()
        try:
            cur.execute("INSERT INTO Wyposazenie (opis) VALUES (%s);", (data['opis'],))
            message = (True, "Pomyslnie dodano wyposazenie")
            self.conn.commit()
        except psycopg2.errors.RaiseException as err:
            print(err)
            message = (False, self.handle_errors(err))
        except Exception as err:
            print(err)
            message = (False, self.handle_general_errors(err))
        cur.close()
        return message

    def add_equipment_to_type(self, data):
        """przypisywanie wyposażenia do danego typu pokoju"""
        cur = self.conn.cursor()
        try:
            cur.execute("INSERT INTO typ_wyp (id_typ, id_wyposazenie, ilosc) VALUES (%s,%s,%s);",
                (data['id_typ'],data['id_wyposazenie'],data['ilosc']))
            message = (True, "Pomyslnie dodano wyposazenie do typu")
            self.conn.commit()
        except psycopg2.errors.RaiseException as err:
            print(err)
            message = (False, self.handle_errors(err))
        except Exception as err:
            print(err)
            message = (False, self.handle_general_errors(err))
        cur.close()
        return message 

    def add_price_to_type(self, data):
        """dodawanie ceny do danego typu pokoju"""
        cur = self.conn.cursor()
        try:
            cur.execute("INSERT INTO Cena_dzien (id_typ, cena, okres_poczatek, okres_koniec) VALUES (%s,%s,%s,%s);",
                (data['id_typ'],data['cena'],data['okres_poczatek'],data['okres_koniec']))
            message = (True, "Pomyslnie dodano cene do typu")
            self.conn.commit()
        except psycopg2.errors.RaiseException as err:
            print(err)
            message = (False, self.handle_errors(err))
        except Exception as err:
            print(err)
            message = (False, self.handle_general_errors(err))
        cur.close()
        return message 

    def add_attraction_to_hotel(self, data):
        """przypisywanie atrakcji do danego hotelu"""
        cur = self.conn.cursor()
        try:
            cur.execute("INSERT INTO hot_atr (id_hotel, id_atrakcje, otwarcie, zamkniecie, cena_godzina) VALUES (%s,%s,%s,%s,%s);",
                (data['id_hotel'],data['id_atrakcje'],data['otwarcie'],data['zamkniecie'],data['cena_godzina']))
            message = (True, "Pomyslnie dodano atrakcje do hotelu")
            self.conn.commit()
        except psycopg2.errors.RaiseException as err:
            print(err)
            message = (False, self.handle_errors(err))
        except Exception as err:
            print(err)
            message = (False, self.handle_general_errors(err))
        cur.close()
        return message 

    def add_room(self, data):
        """dodawanie pokoju dla danego typu"""
        cur = self.conn.cursor()
        try:
            cur.execute("INSERT INTO Pokoj (id_typ, pietro, numer, liczba_miejsc, opis) VALUES (%s,%s,%s,%s,%s);", 
                (data['id_typ'],data['pietro'],data['numer'],data['liczba_miejsc'],data['opis']))
            message = (True, "Pomyslnie dodano pokoj")
            self.conn.commit()
        except psycopg2.errors.RaiseException as err:
            print(err)
            message = (False, self.handle_errors(err))
        except Exception as err:
            print(err)
            message = (False, self.handle_general_errors(err))
        cur.close()
        return message

    def add_type(self, data):
        """dodawanie typu pokoju dla danego hotelu"""
        cur = self.conn.cursor()
        try:
            cur.execute("INSERT INTO Typ_pokoju (id_hotel, nazwa, opis, dla_palaczy, typ_wezlu_higsan) VALUES (%s, %s,%s,%s,%s);", 
                (data['id_hotel'], data['nazwa'],data['opis'],data['dla_palaczy'],data['typ_wezlu_higsan']))
            message = (True, "Pomyslnie dodano typ pokoju")
            self.conn.commit()
        except psycopg2.errors.RaiseException as err:
            print(err)
            message = (False, self.handle_errors(err))
        except Exception as err:
            print(err)
            message = (False, self.handle_general_errors(err))
        cur.close()
        return message

    def input_from_file(self, filename, table):
        """pomocnicza funkcja wstawiająca dane z pliku json"""
        f = open(filename, encoding="utf-8") 
        file_input = json.load(f)
        f.close()
        cur = self.conn.cursor()
        for i in range(len(file_input)):
            key = file_input[i].keys()
            keys = ', '.join(key)
            vals = ['%s' for i in range(len(key))]
            vals = ', '.join(vals)
            SQL = f"INSERT INTO {table} ( {keys} ) VALUES ( {vals} );"
            data = tuple([value for key, value in file_input[i].items()])
            print(SQL, data)
            cur.execute(SQL, data)
            self.conn.commit()
        cur.close()
