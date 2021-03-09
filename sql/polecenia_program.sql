-- aktualizacja rezerwacji
-- funkcja: update_reservations
SELECT * FROM aktualizuj_rezerwacje();

-- odczyt ogólnych statystyk hoteli w bazie
-- funkcja: get_statistics
SELECT min_cena, max_cena FROM min_max_cena;
SELECT l_hoteli FROM liczba_hoteli;
SELECT l_pokoi FROM liczba_pokoi;

-- odczyt statystyk dla hotelu z danym id_hotel
-- funkcja: get_hotel_statistics
SELECT min_cena, max_cena FROM min_max_cena_na_hotel WHERE id_hotel=%s;
SELECT l_pokoi FROM liczba_pokoi_na_hotel WHERE id_hotel=%s;

-- odczyt informacji o danym gościu
-- funkcja: get_guest
SELECT email, imie, nazwisko, telefon FROM Gosc WHERE id_gosc=%s;

-- odczyt informacji o danym pracowniku
-- funkcja: get_employee
SELECT email, imie, nazwisko FROM Pracownik WHERE id_pracownik=%s;

-- odczyt wszystkich możliwych atrakcji z bazy danych
-- funkcja: get_attractions
SELECT id_atrakcje, opis FROM Atrakcje;

-- odczyt wszystkich możliwych statusów rezerwacji z bazy danych
-- funkcja: get_status
SELECT id_status, opis FROM Status;
  
-- odczyt wszystkich możliwych wyposażeń pokoju z bazy danych
-- funkcja: get_equipments
SELECT id_wyposazenie, opis FROM Wyposazenie;

-- odczyt atrakcji danego hotelu
-- funkcja: get_hotel_attractions
SELECT opis FROM atrakcje_hotelu WHERE id_hotel=%s;

-- odczyt wszystkich hoteli wraz z ich sieciami z bazy danych
-- funkcja: get_hotels
SELECT nazwa_sieci, id_hotel, nazwa, adres, email, telefon, kategoria FROM hotele_sieci;

-- odczyt wszystkich hoteli wraz z ich sieciami z bazy danych przefiltrowane przez dostępność atrakcji
-- funkcja: get_filtered_hotels
SELECT nazwa_sieci, id_hotel, nazwa, adres, email, telefon, kategoria FROM filtruj_atrakcje %s;

-- odczyt wszystkich pokoji z danego hotelu przefiltrowane przez dostępność pokoi
-- funkcja: get_filtered_rooms
SELECT numer, id_pokoj, nazwa, opis_typu, dla_palaczy, typ_wezlu_higsan, pietro, liczba_miejsc, 
    opis_pokoju, cena, okres_poczatek, okres_koniec FROM filtruj_pokoje(%s,%s,%s);
  
-- odczyt wolnych terminów pokoju
-- funkcja: get_room_availability
SELECT data_poczatku, data_konca FROM terminy_pokoju WHERE id_pokoj=%s;

-- odczyt wyliczonej przez bazę kwoty za dany pobyt
-- funkcja: get_calculated_price
SELECT * FROM wylicz_cene(%s, %s, %s);

-- odczyt wszystkich rezerwacji złożonych przez danego gościa
-- funkcja: get_guest_reservations
SELECT id_rezerwacja, id_pokoj, data_poczatku, data_konca, data_rezerwacji, opis 
    FROM rezerwacje_goscia WHERE id_gosc=%s AND r=1;

-- odczyt wszystkich rezerwacji złożonych w danym hotelu
-- funkcja: get_hotel_reservations
SELECT id_rezerwacja, id_pokoj, data_poczatku, data_konca, data_rezerwacji, opis, id_gosc, email
FROM rezerwacje_hotelu WHERE id_hotel=%s AND r=1;


-- odczyt wszystkich rezerwacji złożonych w danym hotelu przez gościa o danym adresie email
-- funkcja: get_filtered_hotel_reservations
SELECT id_rezerwacja, id_pokoj, data_poczatku, data_konca, data_rezerwacji, opis, id_gosc, email
    FROM rezerwacje_hotelu WHERE id_hotel=%s AND LOWER(email)=LOWER(%s) AND r=1;

-- odczyt wszystkich pokoi z danego hotelu
-- funkcja: get_rooms
SELECT numer, id_pokoj, nazwa, opis_typu, dla_palaczy, typ_wezlu_higsan, pietro, liczba_miejsc, 
    opis_pokoju, cena, okres_poczatek, okres_koniec FROM pokoje_hotelu WHERE id_hotel=%s;

-- odczyt wszystkich sieci w bazie
-- funkcja: get_chains
SELECT id_siec, nazwa FROM Siec;
   
-- odczyt typów pokoju
-- funkcja: get_types
SELECT id_typ, nazwa, opis_pokoju, dla_palaczy, typ_wezlu_higsan, ilosc, opis_wyposazenia 
    FROM typy_pokojow WHERE id_hotel=%s;

-- odczyt wyposażenia danego pokoju
-- funkcja: get_room_equipments
SELECT ilosc, opis FROM wyposazenie_pokoju WHERE id_pokoj=%s;

-- rejestracja gościa w bazie
-- funkcja: add_guest
INSERT INTO Gosc ( email, haslo, imie, nazwisko, telefon ) VALUES (%s, crypt(%s, gen_salt('bf')), %s, %s, %s);

-- edycja danych gościa o danym id_gosc
-- funkcja: update_guest
UPDATE Gosc SET email = %s WHERE id_gosc = %s;
UPDATE Gosc SET haslo = crypt(%s, gen_salt('bf')) WHERE id_gosc = %s;
UPDATE Gosc SET imie = %s WHERE id_gosc = %s;
UPDATE Gosc SET nazwisko = %s WHERE id_gosc = %s;
UPDATE Gosc SET telefon = %s WHERE id_gosc = %s;


-- rejestracja pracownika
-- funkcja: add_employee
INSERT INTO Pracownik ( id_hotel, email, haslo, imie, nazwisko) 
    VALUES (%s, %s, crypt(%s, gen_salt('bf')), %s, %s);

-- edycja danych pracownika o danym id_pracownik
-- funkcja: update_employee
UPDATE Pracownik SET email = %s WHERE id_pracownik = %s;
UPDATE Pracownik SET haslo = crypt(%s, gen_salt('bf')) WHERE id_pracownik = %s;
UPDATE Pracownik SET imie = %s WHERE id_pracownik = %s;
UPDATE Pracownik SET nazwisko = %s WHERE id_pracownik = %s;

-- sprawdzanie poprawności logowania użytkownika
-- funkcja: login_user
SELECT id_gosc FROM Gosc WHERE email=%s AND haslo = crypt(%s, haslo);
SELECT id_hotel, id_pracownik FROM Pracownik WHERE email=%s AND haslo = crypt(%s, haslo);

-- wylogowanie użytkownika, czyli usunięcie obecnego user_id z bazy
-- funkcja: logout
SET public.user_id TO DEFAULT;

-- dodawanie rezerwacji przez gościa
-- funkcja: add_guest_reservation
SET public.user_id = %s;
INSERT INTO Rezerwacja (id_pokoj, data_poczatku, data_konca, data_rezerwacji) 
    VALUES (%s, %s, %s, CURRENT_DATE);

-- anulowanie danej rezerwacji przez gościa
-- funkcja: cancel_guest_reservation
SELECT * FROM anuluj_rezerwacje(%s);

-- zapłacanie za daną rezerwacje przez gościa
-- funkcja: pay_guest_reservation
INSERT INTO Status_rezerwacji (id_rezerwacja, data_zmiany_stanu, id_status) VALUES (%s, CURRENT_DATE, 2);

-- zmiana statusu danej rezerwacji przez pracownika
-- funkcja: change_guest_reservation
INSERT INTO Status_rezerwacji (id_rezerwacja, data_zmiany_stanu, id_status) VALUES (%s, CURRENT_DATE, %s);

-- dodawanie sieci do bazy
-- funkcja: add_chain
INSERT INTO Siec (nazwa) VALUES (%s);

-- dodawanie hotelu do bazy
-- funkcja: add_hotel
INSERT INTO Hotel (id_siec, nazwa, telefon, email, kategoria, adres) VALUES (%s, %s, %s, %s, %s, %s);

-- dodawanie atrakcji do bazy
-- funkcja: add_attraction
INSERT INTO Atrakcje (opis) VALUES (%s);

-- dodawanie wyposażenia do bazy
-- funkcja: add_equipment
INSERT INTO Wyposazenie (opis) VALUES (%s);

-- przypisywanie wyposażenia do danego typu pokoju
-- funkcja: add_equipment_to_type
INSERT INTO typ_wyp (id_typ, id_wyposazenie, ilosc) VALUES (%s,%s,%s);

-- dodawanie ceny do danego typu pokoju
-- funkcja: add_price_to_type
INSERT INTO Cena_dzien (id_typ, cena, okres_poczatek, okres_koniec) VALUES (%s,%s,%s,%s)

-- przypisywanie atrakcji do danego hotelu
-- funkcja: add_attraction_to_hotel
INSERT INTO hot_atr (id_hotel, id_atrakcje, otwarcie, zamkniecie, cena_godzina) VALUES (%s,%s,%s,%s,%s);

-- dodawanie pokoju dla danego typu
-- funkcja: add_room
INSERT INTO Pokoj (id_typ, pietro, numer, liczba_miejsc, opis) VALUES (%s,%s,%s,%s,%s);

-- dodawanie typu pokoju dla danego hotelu
-- funkcja: add_type
INSERT INTO Typ_pokoju (id_hotel, nazwa, opis, dla_palaczy, typ_wezlu_higsan) VALUES (%s, %s,%s,%s,%s);
