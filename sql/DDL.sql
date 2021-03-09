DROP TABLE Atrakcje CASCADE;
DROP TABLE Wyposazenie CASCADE;
DROP TABLE Cena_dzien CASCADE;
DROP TABLE Typ_pokoju CASCADE;
DROP TABLE typ_wyp CASCADE;
DROP TABLE Siec CASCADE;
DROP TABLE Gosc CASCADE;
DROP TABLE Hotel CASCADE;
DROP TABLE hot_atr CASCADE;
DROP TABLE Pracownik CASCADE;
DROP TABLE Pokoj CASCADE;
DROP TABLE Rezerwacja CASCADE;
DROP TABLE Status_rezerwacji CASCADE;
DROP TABLE Gosc_rezerw CASCADE;
DROP TABLE Status CASCADE;

CREATE TABLE Atrakcje (
    id_atrakcje SERIAL PRIMARY KEY,
    opis VARCHAR NOT NULL); 
CREATE TABLE Wyposazenie (
    id_wyposazenie SERIAL PRIMARY KEY,
    opis VARCHAR NOT NULL);
CREATE TABLE Cena_dzien (
    id_cena SERIAL PRIMARY KEY,
    id_typ INTEGER NOT NULL,
    cena REAL NOT NULL,
    okres_poczatek DATE NOT NULL,
    okres_koniec DATE NOT NULL);
CREATE TABLE Typ_pokoju (
    id_typ SERIAL PRIMARY KEY,
    id_hotel INTEGER NOT NULL,
    nazwa VARCHAR NOT NULL,
    opis VARCHAR,
    typ_wezlu_higsan VARCHAR,
    dla_palaczy BOOLEAN NOT NULL);
CREATE TABLE typ_wyp (
    id_typ INTEGER NOT NULL,
    id_wyposazenie INTEGER NOT NULL,
    ilosc INTEGER NOT NULL);
CREATE TABLE Siec (
    id_siec SERIAL PRIMARY KEY,
    nazwa VARCHAR NOT NULL);
CREATE TABLE Gosc (
    id_gosc SERIAL PRIMARY KEY,
    email VARCHAR NOT NULL,
    haslo VARCHAR,
    imie VARCHAR NOT NULL,
    nazwisko VARCHAR NOT NULL,
    telefon VARCHAR NOT NULL);
CREATE TABLE Hotel (
    id_hotel SERIAL PRIMARY KEY,
    id_siec INTEGER NOT NULL,
    kategoria VARCHAR NOT NULL,
    nazwa VARCHAR NOT NULL,
    adres VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    telefon VARCHAR NOT NULL);
CREATE TABLE hot_atr (
    id_hotel INTEGER NOT NULL,
    id_atrakcje INTEGER NOT NULL,
    otwarcie TIME,
    zamkniecie TIME,
    cena_godzina REAL);
CREATE TABLE Pracownik (
    id_pracownik SERIAL PRIMARY KEY,
    email VARCHAR NOT NULL,
    haslo VARCHAR,
    id_hotel INTEGER NOT NULL,
    imie VARCHAR NOT NULL,
    nazwisko VARCHAR NOT NULL);
CREATE TABLE Pokoj (
    id_pokoj SERIAL PRIMARY KEY,
    id_typ INTEGER NOT NULL,
    pietro INTEGER NOT NULL,
    numer VARCHAR NOT NULL,
    liczba_miejsc INTEGER NOT NULL,
    opis VARCHAR);
CREATE TABLE Rezerwacja (
    id_rezerwacja SERIAL PRIMARY KEY,
    id_pokoj INTEGER NOT NULL,
    data_poczatku DATE NOT NULL,
    data_konca DATE NOT NULL,
    data_rezerwacji DATE NOT NULL);
CREATE TABLE Status_rezerwacji (
    id_st_rez SERIAL PRIMARY KEY,
    id_status INTEGER NOT NULL,
    id_rezerwacja INTEGER NOT NULL,
    data_zmiany_stanu DATE NOT NULL);
CREATE TABLE Gosc_rezerw (
    id_gosc INTEGER NOT NULL,
    id_rezerwacja INTEGER NOT NULL);
CREATE TABLE Status (
    id_status SERIAL PRIMARY KEY,
    opis VARCHAR NOT NULL);

ALTER TABLE hot_atr ADD FOREIGN KEY (id_atrakcje)
    REFERENCES Atrakcje (id_atrakcje);
ALTER TABLE typ_wyp ADD FOREIGN KEY (id_wyposazenie)
    REFERENCES Wyposazenie (id_wyposazenie);
ALTER TABLE Pokoj ADD FOREIGN KEY (id_typ)
    REFERENCES Typ_pokoju (id_typ);
ALTER TABLE typ_wyp ADD FOREIGN KEY (id_typ)
    REFERENCES Typ_pokoju (id_typ);
ALTER TABLE Hotel ADD FOREIGN KEY (id_siec)
    REFERENCES Siec (id_siec);
ALTER TABLE Gosc_rezerw ADD FOREIGN KEY (id_gosc)
    REFERENCES Gosc (id_gosc);
ALTER TABLE Typ_pokoju ADD FOREIGN KEY (id_hotel)
    REFERENCES Hotel (id_hotel);
ALTER TABLE Pracownik ADD FOREIGN KEY (id_hotel)
    REFERENCES Hotel (id_hotel);
ALTER TABLE hot_atr ADD FOREIGN KEY (id_hotel)
    REFERENCES Hotel (id_hotel);
ALTER TABLE Cena_dzien ADD FOREIGN KEY (id_typ)
    REFERENCES Typ_pokoju (id_typ);   
ALTER TABLE Rezerwacja ADD FOREIGN KEY (id_pokoj)
    REFERENCES Pokoj (id_pokoj);
ALTER TABLE Gosc_rezerw ADD FOREIGN KEY (id_rezerwacja)
    REFERENCES Rezerwacja (id_rezerwacja);
ALTER TABLE Status_rezerwacji ADD FOREIGN KEY (id_rezerwacja)
    REFERENCES Rezerwacja (id_rezerwacja);
ALTER TABLE Status_rezerwacji ADD FOREIGN KEY (id_status)
    REFERENCES Status (id_status);
