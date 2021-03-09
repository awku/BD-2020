CREATE OR REPLACE VIEW
    min_max_cena
    AS
    SELECT MIN(cena) AS min_cena, MAX(cena) AS max_cena
        FROM public.cena_dzien;

CREATE OR REPLACE VIEW
    min_max_cena_na_hotel
    AS
    SELECT id_hotel, MIN(cena) AS min_cena, MAX(cena) AS max_cena
    	FROM public.typ_pokoju
        JOIN public.cena_dzien ON cena_dzien.id_typ=typ_pokoju.id_typ
        GROUP BY id_hotel;

CREATE OR REPLACE VIEW
    liczba_hoteli
    AS
    SELECT COUNT(*) AS l_hoteli FROM public.Hotel;

CREATE OR REPLACE VIEW
    liczba_pokoi
    AS
    SELECT COUNT(*) AS l_pokoi FROM public.Pokoj;

CREATE OR REPLACE VIEW
    liczba_pokoi_na_hotel
    AS
    SELECT id_hotel, COUNT(*) AS l_pokoi FROM public.Pokoj JOIN public.Typ_pokoju ON Pokoj.id_typ=Typ_pokoju.id_typ GROUP BY id_hotel;

CREATE OR REPLACE VIEW
    hotele_sieci
    AS
    SELECT siec.nazwa AS nazwa_sieci, hotel.id_hotel, hotel.nazwa AS nazwa, adres, email, telefon, kategoria
        FROM public.Hotel
        JOIN public.Siec ON siec.id_siec=hotel.id_siec
        GROUP BY siec.nazwa, hotel.id_hotel;

CREATE OR REPLACE VIEW
    atrakcje_hotelu
    AS
    SELECT hotel.id_hotel, hotel.nazwa, atrakcje.opis, hot_atr.otwarcie, hot_atr.zamkniecie, hot_atr.cena_godzina
        FROM public.hotel
        JOIN public.hot_atr ON hotel.id_hotel=hot_atr.id_hotel
        JOIN public.atrakcje ON hot_atr.id_atrakcje=atrakcje.id_atrakcje
        GROUP BY hotel.id_hotel, atrakcje.opis, hot_atr.otwarcie, hot_atr.zamkniecie, hot_atr.cena_godzina;

CREATE OR REPLACE VIEW
    pokoje_hotelu
    AS
    SELECT numer, pokoj.id_pokoj, hotel.id_hotel, typ_pokoju.nazwa, 
    typ_pokoju.opis AS opis_typu, typ_pokoju.dla_palaczy, typ_pokoju.typ_wezlu_higsan, 
    pietro, liczba_miejsc, pokoj.opis AS opis_pokoju, cena, okres_poczatek, okres_koniec
        FROM public.Hotel
        JOIN public.Typ_pokoju ON hotel.id_hotel=typ_pokoju.id_hotel
        JOIN public.Pokoj ON pokoj.id_typ=typ_pokoju.id_typ
        JOIN public.cena_dzien ON typ_pokoju.id_typ=cena_dzien.id_typ
        WHERE okres_koniec > CURRENT_DATE
        ORDER BY okres_poczatek ASC;

CREATE OR REPLACE VIEW
    rezerwacje_goscia
    AS
    SELECT gosc.id_gosc, ROW_NUMBER() OVER (PARTITION BY rezerwacja.id_rezerwacja ORDER BY id_st_rez DESC) AS r, rezerwacja.id_rezerwacja, id_pokoj, data_poczatku, data_konca, data_rezerwacji, status.opis
        FROM public.Gosc
        JOIN public.Gosc_rezerw ON Gosc.id_gosc=gosc_rezerw.id_gosc
        JOIN public.Rezerwacja ON Gosc_rezerw.id_rezerwacja=Rezerwacja.id_rezerwacja
        JOIN public.Status_rezerwacji ON Rezerwacja.id_rezerwacja=Status_rezerwacji.id_rezerwacja
        JOIN public.Status ON Status_rezerwacji.id_status=Status.id_status
        GROUP BY gosc.id_gosc, rezerwacja.id_rezerwacja, id_pokoj, status.opis, id_st_rez
        ORDER BY data_rezerwacji;

CREATE OR REPLACE VIEW
    rezerwacje_hotelu
    AS
    SELECT gosc.id_gosc, gosc.email, ROW_NUMBER() OVER (PARTITION BY rezerwacja.id_rezerwacja ORDER BY id_st_rez DESC) AS r, rezerwacja.id_rezerwacja, rezerwacja.id_pokoj, data_poczatku, data_konca, data_rezerwacji, status.opis, id_hotel
        FROM public.Gosc
        JOIN public.Gosc_rezerw ON Gosc.id_gosc=gosc_rezerw.id_gosc
        JOIN public.Rezerwacja ON Gosc_rezerw.id_rezerwacja=Rezerwacja.id_rezerwacja
        JOIN public.Status_rezerwacji ON Rezerwacja.id_rezerwacja=Status_rezerwacji.id_rezerwacja
        JOIN public.Status ON Status_rezerwacji.id_status=Status.id_status
        JOIN public.Pokoj ON Rezerwacja.id_pokoj=Pokoj.id_pokoj
        JOIN public.Typ_pokoju ON Pokoj.id_typ=Typ_pokoju.id_typ
        GROUP BY gosc.id_gosc, rezerwacja.id_rezerwacja, Typ_pokoju.id_hotel, status.opis, id_st_rez
        ORDER BY data_rezerwacji;

CREATE OR REPLACE VIEW
    terminy_pokoju
    AS
    SELECT id_pokoj, data_poczatku, data_konca
        FROM public.Rezerwacja 
        JOIN public.Status_rezerwacji ON Rezerwacja.id_rezerwacja=Status_rezerwacji.id_rezerwacja
        WHERE id_status != 3;

CREATE OR REPLACE VIEW
    typy_pokojow
    AS
    SELECT id_hotel, typ_pokoju.id_typ, nazwa, typ_pokoju.opis AS opis_pokoju, dla_palaczy, typ_wezlu_higsan, ilosc, wyposazenie.opis AS opis_wyposazenia
        FROM public.Typ_pokoju
        JOIN public.typ_wyp ON typ_pokoju.id_typ=typ_wyp.id_typ
        JOIN public.Wyposazenie ON typ_wyp.id_wyposazenie=wyposazenie.id_wyposazenie
        GROUP BY typ_pokoju.id_typ, ilosc, wyposazenie.opis;

CREATE OR REPLACE VIEW
    wyposazenie_pokoju
    AS
    SELECT id_pokoj, ilosc, wyposazenie.opis
        FROM public.Pokoj
        JOIN public.Typ_pokoju ON typ_pokoju.id_typ=pokoj.id_typ
        JOIN public.typ_wyp ON typ_pokoju.id_typ=typ_wyp.id_typ
        JOIN public.Wyposazenie ON typ_wyp.id_wyposazenie=wyposazenie.id_wyposazenie
        GROUP BY id_pokoj, wyposazenie.opis, typ_wyp.ilosc;

CREATE OR REPLACE VIEW
    rezerwacje_lista
    AS
    SELECT ROW_NUMBER() OVER (PARTITION BY rezerwacja.id_rezerwacja ORDER BY id_st_rez DESC) AS r, rezerwacja.id_rezerwacja, data_poczatku, data_konca, data_rezerwacji, status.id_status, data_zmiany_stanu
        FROM public.Rezerwacja
        JOIN public.Status_rezerwacji ON Rezerwacja.id_rezerwacja=Status_rezerwacji.id_rezerwacja
        JOIN public.Status ON Status_rezerwacji.id_status=Status.id_status
        GROUP BY rezerwacja.id_rezerwacja, id_pokoj, status.id_status, id_st_rez
        ORDER BY data_rezerwacji;