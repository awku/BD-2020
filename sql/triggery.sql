-- triggery walidujace dane

CREATE OR REPLACE FUNCTION walidacja_rejestracji_goscia()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $$
    BEGIN
    IF NEW.nazwisko IS NULL THEN
        RAISE EXCEPTION 'Nazwisko nie moze byc puste.';
    END IF;
    IF NEW.nazwisko SIMILAR TO '%[0-9]%' THEN
        RAISE EXCEPTION 'Niepoprawne nazwisko.';
    END IF;
    IF NEW.imie IS NULL THEN
        RAISE EXCEPTION 'Imie nie moze byc puste.';
    END IF;
    IF NEW.imie SIMILAR TO '%[0-9]%' THEN
        RAISE EXCEPTION 'Niepoprawne imie.';
    END IF;
    IF NEW.telefon IS NULL THEN
        RAISE EXCEPTION 'Telefon nie moze byc pusty.';
    END IF;
    IF NEW.telefon NOT SIMILAR TO '[\(]?[\+]?[0-9\s\-\(\)]{9,}' THEN
        RAISE EXCEPTION 'Niepoprawny telefon.';
    END IF;
    IF NEW.email IS NULL THEN
        RAISE EXCEPTION 'Email nie moze byc pusty.';
    END IF;
    IF NEW.email NOT LIKE '%@%.%' THEN
        RAISE EXCEPTION 'Niepoprawny email.';
    END IF;
    IF EXISTS(SELECT * FROM public.Gosc WHERE email=NEW.email) OR EXISTS(SELECT * FROM public.Pracownik WHERE email=NEW.email) THEN
        RAISE EXCEPTION 'Email istnieje w bazie.';
    END IF;
    RETURN NEW;                                                          
    END;
    $$;

CREATE TRIGGER gosc_walidacja 
    BEFORE INSERT ON public.Gosc
    FOR EACH ROW EXECUTE PROCEDURE walidacja_rejestracji_goscia();

CREATE OR REPLACE FUNCTION walidacja_edycji_goscia_naz()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $$
    BEGIN
    IF NEW.nazwisko IS NULL THEN
        RAISE EXCEPTION 'Nazwisko nie moze byc puste.';
    END IF;
    IF NEW.nazwisko SIMILAR TO '%[0-9]%' THEN
        RAISE EXCEPTION 'Niepoprawne nazwisko.';
    END IF;
    RETURN NEW;                                                          
    END;
    $$;

CREATE TRIGGER ed_goscia_naz
  BEFORE UPDATE OF nazwisko ON public.Gosc
  FOR EACH ROW EXECUTE PROCEDURE walidacja_edycji_goscia_naz();

CREATE OR REPLACE FUNCTION walidacja_edycji_goscia_im()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $$
    BEGIN
    IF NEW.imie IS NULL THEN
        RAISE EXCEPTION 'Imie nie moze byc puste.';
    END IF;
    IF NEW.imie SIMILAR TO '%[0-9]%' THEN
        RAISE EXCEPTION 'Niepoprawne imie.';
    END IF;
    RETURN NEW;                                                          
    END;
    $$;

CREATE TRIGGER ed_goscia_im
  BEFORE UPDATE OF imie ON public.Gosc
  FOR EACH ROW EXECUTE PROCEDURE walidacja_edycji_goscia_im();

CREATE OR REPLACE FUNCTION walidacja_edycji_goscia_tel()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $$
    BEGIN
    IF NEW.telefon IS NULL THEN
        RAISE EXCEPTION 'Telefon nie moze byc pusty.';
    END IF;
    IF NEW.telefon NOT SIMILAR TO '[\(]?[\+]?[0-9\s\-\(\)]{9,}' THEN
        RAISE EXCEPTION 'Niepoprawny telefon.';
    END IF;
    RETURN NEW;                                                          
    END;
    $$;

CREATE TRIGGER ed_goscia_tel
  BEFORE UPDATE OF Telefon ON public.Gosc
  FOR EACH ROW EXECUTE PROCEDURE walidacja_edycji_goscia_tel();

CREATE OR REPLACE FUNCTION walidacja_edycji_goscia_em()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $$
    BEGIN
    IF NEW.email IS NULL THEN
        RAISE EXCEPTION 'Email nie moze byc pusty.';
    END IF;
    IF NEW.email NOT LIKE '%@%.%' THEN
        RAISE EXCEPTION 'Niepoprawny email.';
    END IF;
    IF EXISTS(SELECT * FROM public.Gosc WHERE email=NEW.email) OR EXISTS(SELECT * FROM public.Pracownik WHERE email=NEW.email) THEN
        RAISE EXCEPTION 'Email istnieje w bazie.';
    END IF;
    RETURN NEW;                                                          
    END;
    $$;

CREATE TRIGGER ed_goscia_em
  BEFORE UPDATE OF email ON public.Gosc
  FOR EACH ROW EXECUTE PROCEDURE walidacja_edycji_goscia_em();

CREATE OR REPLACE FUNCTION walidacja_rejestracji_pracownika()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $$
    BEGIN
    IF NEW.nazwisko IS NULL THEN
        RAISE EXCEPTION 'Nazwisko nie moze byc puste.';
    END IF;
    IF NEW.nazwisko SIMILAR TO '%[0-9]%' THEN
        RAISE EXCEPTION 'Niepoprawne nazwisko.';
    END IF;
    IF NEW.imie IS NULL THEN
        RAISE EXCEPTION 'Imie nie moze byc puste.';
    END IF;
    IF NEW.imie SIMILAR TO '%[0-9]%' THEN
        RAISE EXCEPTION 'Niepoprawne imie.';
    END IF;
    IF NEW.email IS NULL THEN
        RAISE EXCEPTION 'Email nie moze byc pusty.';
    END IF;
    IF NEW.email NOT LIKE '%@%.%' THEN
        RAISE EXCEPTION 'Niepoprawny email.';
    END IF;
    IF EXISTS(SELECT * FROM public.Pracownik WHERE email=NEW.email) OR EXISTS(SELECT * FROM public.Gosc WHERE email=NEW.email) THEN
        RAISE EXCEPTION 'Email istnieje w bazie.';
    END IF;
    RETURN NEW;                                                          
    END;
    $$;

CREATE TRIGGER pracownik_walidacja 
    BEFORE INSERT ON public.Pracownik
    FOR EACH ROW EXECUTE PROCEDURE walidacja_rejestracji_pracownika();

CREATE OR REPLACE FUNCTION walidacja_edycji_pracownika_naz()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $$
    BEGIN
    IF NEW.nazwisko IS NULL THEN
        RAISE EXCEPTION 'Nazwisko nie moze byc puste.';
    END IF;
    IF NEW.nazwisko SIMILAR TO '%[0-9]%' THEN
        RAISE EXCEPTION 'Niepoprawne nazwisko.';
    END IF;
    RETURN NEW;                                                          
    END;
    $$;

CREATE TRIGGER ed_prac_naz
  BEFORE UPDATE OF nazwisko ON public.Pracownik
  FOR EACH ROW EXECUTE PROCEDURE walidacja_edycji_pracownika_naz();

CREATE OR REPLACE FUNCTION walidacja_edycji_pracownika_im()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $$
    BEGIN
    IF NEW.imie IS NULL THEN
        RAISE EXCEPTION 'Imie nie moze byc puste.';
    END IF;
    IF NEW.imie SIMILAR TO '%[0-9]%' THEN
        RAISE EXCEPTION 'Niepoprawne imie.';
    END IF;
    RETURN NEW;                                                          
    END;
    $$;

CREATE TRIGGER ed_prac_im
  BEFORE UPDATE OF imie ON public.Pracownik
  FOR EACH ROW EXECUTE PROCEDURE walidacja_edycji_pracownika_im();

CREATE OR REPLACE FUNCTION walidacja_edycji_pracownika_em()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $$
    BEGIN
    IF NEW.email IS NULL THEN
        RAISE EXCEPTION 'Email nie moze byc pusty.';
    END IF;
    IF NEW.email NOT LIKE '%@%.%' THEN
        RAISE EXCEPTION 'Niepoprawny email.';
    END IF;
    IF EXISTS(SELECT * FROM public.Pracownik WHERE email=NEW.email) OR EXISTS(SELECT * FROM public.Gosc WHERE email=NEW.email) THEN
        RAISE EXCEPTION 'Email istnieje w bazie.';
    END IF;
    RETURN NEW;                                                          
    END;
    $$;

CREATE TRIGGER ed_prac_em
  BEFORE UPDATE OF email ON public.Pracownik
  FOR EACH ROW EXECUTE PROCEDURE walidacja_edycji_pracownika_em();

CREATE OR REPLACE FUNCTION walidacja_sieci()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $$
    BEGIN
    IF NEW.nazwa IS NULL THEN
        RAISE EXCEPTION 'Nazwa nie moze byc pusta.';
    END IF;
    IF EXISTS(SELECT * FROM public.Siec WHERE nazwa=NEW.nazwa) THEN
        RAISE EXCEPTION 'Nazwa istnieje w bazie.';
    END IF;
    RETURN NEW;                                                          
    END;
    $$;

CREATE TRIGGER siec_walidacja 
    BEFORE INSERT ON public.Siec
    FOR EACH ROW EXECUTE PROCEDURE walidacja_sieci();

CREATE OR REPLACE FUNCTION walidacja_rezerwacji()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $$
    DECLARE
    var_r RECORD;
    wynik BOOLEAN;
    BEGIN
    	IF NEW.data_konca < NEW.data_poczatku THEN
        	RAISE EXCEPTION 'Zla kolejnosc dat.';
        END IF;
        IF NEW.data_poczatku < CURRENT_DATE THEN
        	RAISE EXCEPTION 'Data w przeszlosci.';
        END IF;
        FOR var_r IN (SELECT data_poczatku, data_konca FROM terminy_pokoju
                        WHERE id_pokoj=NEW.id_pokoj)  
        LOOP
            SELECT INTO wynik (daterange(var_r.data_poczatku, var_r.data_konca, '[)') && daterange(NEW.data_poczatku, NEW.data_konca, '[)'));
            IF wynik IS True THEN
                RAISE EXCEPTION 'Daty sie nakladaja.';
            END IF;    
    	END LOOP;
    RETURN NEW;                                                          
    END;
    $$;

CREATE TRIGGER rezerwacja_walidacja 
    BEFORE INSERT ON public.Rezerwacja
    FOR EACH ROW EXECUTE PROCEDURE walidacja_rezerwacji();

CREATE OR REPLACE FUNCTION dodawanie_ceny()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $$
    DECLARE
    var_r RECORD;
    temp RECORD;
    wynik BOOLEAN;
    BEGIN
        IF NEW.cena IS NULL THEN
            RAISE EXCEPTION 'Cena nie moze byc pusta .';
        END IF;
        IF CAST(NEW.cena AS varchar) NOT SIMILAR TO '[0-9]*[.]?[0-9]*' THEN
            RAISE EXCEPTION 'Niepoprawna cena.';
        END IF;
        IF NEW.cena<0 THEN
            RAISE EXCEPTION 'Cena nie moze byc ujemna .';
        END IF;
    	IF NEW.okres_poczatek < NEW.okres_poczatek THEN
        	RAISE EXCEPTION 'Zla kolejnosc dat.';
        END IF;
        IF NEW.okres_poczatek < CURRENT_DATE AND NEW.okres_koniec < CURRENT_DATE THEN
        	RAISE EXCEPTION 'Data w przeszlosci.';
        END IF;
        FOR var_r IN (SELECT id_cena, cena, id_typ, okres_poczatek, okres_koniec FROM public.cena_dzien
                        WHERE id_typ=NEW.id_typ)  
        LOOP
            SELECT INTO wynik (daterange(var_r.okres_poczatek, var_r.okres_koniec, '[)') && daterange(NEW.okres_poczatek, NEW.okres_koniec, '[)'));
            IF wynik IS True THEN
                SELECT INTO temp var_r.cena, var_r.id_typ, var_r.okres_poczatek, var_r.okres_koniec FROM public.cena_dzien;
                IF NEW.okres_poczatek>var_r.okres_poczatek AND NEW.okres_koniec<var_r.okres_koniec THEN
                   UPDATE cena_dzien SET okres_koniec = (NEW.okres_poczatek - INTERVAL '1 day') WHERE id_cena = var_r.id_cena; 
                   INSERT INTO cena_dzien (cena, id_typ, okres_poczatek, okres_koniec) VALUES (temp.cena, temp.id_typ, (NEW.okres_koniec + INTERVAL '1 day'), temp.okres_koniec);
                ELSIF NEW.okres_poczatek<var_r.okres_poczatek AND NEW.okres_koniec>var_r.okres_koniec THEN
                	DELETE FROM public.cena_dzien WHERE id_cena = var_r.id_cena;
                ELSIF NEW.okres_poczatek<var_r.okres_poczatek THEN
                    UPDATE cena_dzien SET okres_poczatek = (NEW.okres_koniec + INTERVAL '1 day') WHERE id_cena = var_r.id_cena; 
                ELSE
                    UPDATE cena_dzien SET okres_koniec = (NEW.okres_poczatek - INTERVAL '1 day') WHERE id_cena = var_r.id_cena; 
            	END IF;  
            END IF;  
    	END LOOP;
    RETURN NEW;                                                          
    END;
    $$;

CREATE TRIGGER wal_dodawanie_ceny 
    BEFORE INSERT ON public.cena_dzien
    FOR EACH ROW EXECUTE PROCEDURE dodawanie_ceny();

CREATE OR REPLACE FUNCTION walidacja_hotel()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $$
    BEGIN
    IF NEW.nazwa IS NULL THEN
        RAISE EXCEPTION 'Nazwa nie moze byc pusta.';
    END IF;
    IF EXISTS(SELECT * FROM public.Hotel WHERE nazwa=NEW.nazwa AND id_siec=NEW.id_siec) THEN
        RAISE EXCEPTION 'Nazwa istnieje w bazie tej sieci.';
    END IF;
    IF NEW.adres IS NULL THEN
        RAISE EXCEPTION 'Adres nie moze byc pusty.';
    END IF;
    IF NEW.telefon IS NULL THEN
        RAISE EXCEPTION 'Telefon nie moze byc pusty.';
    END IF;
    IF NEW.telefon NOT SIMILAR TO '[\(]?[\+]?[0-9\s\-\(\)]{9,}' THEN
        RAISE EXCEPTION 'Niepoprawny telefon.';
    END IF;
    IF NEW.email IS NULL THEN
        RAISE EXCEPTION 'Email nie moze byc pusty.';
    END IF;
    IF NEW.email NOT LIKE '%@%.%' THEN
        RAISE EXCEPTION 'Niepoprawny email.';
    END IF;
    IF EXISTS(SELECT * FROM public.Hotel WHERE email=NEW.email) THEN
        RAISE EXCEPTION 'Email istnieje w bazie hoteli.';
    END IF;
    RETURN NEW;                                                          
    END;
    $$;

CREATE TRIGGER hotel_walidacja 
    BEFORE INSERT ON public.Hotel
    FOR EACH ROW EXECUTE PROCEDURE walidacja_hotel();

CREATE OR REPLACE FUNCTION walidacja_pokoj()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $$
    BEGIN
    IF NEW.pietro IS NULL THEN
        RAISE EXCEPTION 'Pietro nie moze byc puste.';
    END IF;
    IF CAST(NEW.pietro AS varchar) NOT SIMILAR TO '[0-9]+' THEN
        RAISE EXCEPTION 'Niepoprawne pietro.';
    END IF;
    IF NEW.numer IS NULL THEN
        RAISE EXCEPTION 'Numer nie moze byc pusty.';
    END IF;
    IF NEW.liczba_miejsc IS NULL THEN
        RAISE EXCEPTION 'Liczba miejsc nie moze byc pusta.';
    END IF;
    IF CAST(NEW.liczba_miejsc AS varchar) NOT SIMILAR TO '[0-9]+' THEN
        RAISE EXCEPTION 'Niepoprawna liczba miejsc.';
    END IF;
    IF NEW.liczba_miejsc < 0 THEN
        RAISE EXCEPTION 'Liczba miejsc nie moze byc ujemna.';
    END IF;
    IF EXISTS(SELECT * FROM Pokoj 
                JOIN Typ_pokoju ON pokoj.id_typ=typ_pokoju.id_typ
                WHERE id_hotel IN (SELECT id_hotel FROM Typ_pokoju WHERE id_typ=NEW.id_typ) AND numer=NEW.numer) THEN 
        RAISE EXCEPTION 'Taki numer istnieje juz w hotelu.';
    END IF;        
    RETURN NEW;                                                          
    END;
    $$;

CREATE TRIGGER pokoj_walidacja 
    BEFORE INSERT ON public.Pokoj
    FOR EACH ROW EXECUTE PROCEDURE walidacja_pokoj();

CREATE OR REPLACE FUNCTION walidacja_atr_hot()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $$
    BEGIN
    IF NEW.cena_godzina IS NOT NULL AND CAST(NEW.cena_godzina AS varchar) NOT SIMILAR TO '[0-9]*[.]?[0-9]*' THEN
        RAISE EXCEPTION 'Niepoprawna cena.';
    END IF;
    IF EXISTS(SELECT * FROM public.hot_atr WHERE id_hotel=NEW.id_hotel AND id_atrakcje=NEW.id_atrakcje) THEN
        RAISE EXCEPTION 'Atrakcja jest juz przypisana do hotelu.';
    END IF;
    RETURN NEW;                                                          
    END;
    $$;

CREATE TRIGGER atr_hot_walidacja 
    BEFORE INSERT ON public.hot_atr
    FOR EACH ROW EXECUTE PROCEDURE walidacja_atr_hot();

CREATE OR REPLACE FUNCTION walidacja_wyp_pok()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $$
    BEGIN
    IF NEW.ilosc IS NULL THEN
        RAISE EXCEPTION 'Ilosc nie moze byc pusta.';
    END IF;
    IF CAST(NEW.ilosc AS varchar) NOT SIMILAR TO '[0-9]+' THEN
        RAISE EXCEPTION 'Niepoprawna ilosc.';
    END IF;
    IF NEW.ilosc<0 THEN
        RAISE EXCEPTION 'Ilosc nie moze byc ujemna.';
    END IF;
    IF EXISTS(SELECT * FROM public.typ_wyp WHERE id_typ=NEW.id_typ AND id_wyposazenie=NEW.id_wyposazenie) THEN
        RAISE EXCEPTION 'Wyposazenie jest juz przypisana do typu.';
    END IF;
    RETURN NEW;                                                          
    END;
    $$;

CREATE TRIGGER typ_wyp_walidacja 
    BEFORE INSERT ON public.typ_wyp
    FOR EACH ROW EXECUTE PROCEDURE walidacja_wyp_pok();

CREATE OR REPLACE FUNCTION walidacja_wyposazenie()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $$
    BEGIN
    IF NEW.opis IS NULL THEN
        RAISE EXCEPTION 'Opis nie moze byc pusty.';
    END IF;
    IF EXISTS(SELECT * FROM public.Wyposazenie WHERE opis=NEW.opis) THEN
        RAISE EXCEPTION 'Opis istnieje w bazie.';
    END IF;
    RETURN NEW;                                                          
    END;
    $$;

CREATE TRIGGER wyp_walidacja 
    BEFORE INSERT ON public.Wyposazenie
    FOR EACH ROW EXECUTE PROCEDURE walidacja_wyposazenie();

CREATE OR REPLACE FUNCTION walidacja_typ()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $$
    BEGIN
    IF NEW.nazwa IS NULL THEN
        RAISE EXCEPTION 'Nazwa nie moze byc pusta.';
    END IF;
    IF EXISTS(SELECT * FROM public.Typ_pokoju WHERE nazwa=NEW.nazwa AND id_hotel=NEW.id_hotel) THEN
        RAISE EXCEPTION 'Typ istnieje w bazie.';
    END IF;
    RETURN NEW;                                                          
    END;
    $$;

CREATE TRIGGER typ_walidacja 
    BEFORE INSERT ON public.Typ_pokoju
    FOR EACH ROW EXECUTE PROCEDURE walidacja_typ();

-- trigger wstawiajacy odpowiednie dane do tabeli Gosc_rezerw i Status_rezerwacji
CREATE OR REPLACE FUNCTION tworzenie_rezerwacji()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $$
    DECLARE
        id_g INTEGER;
        id_r INTEGER;
    BEGIN
        SELECT INTO id_g current_setting('public.user_id', 't');
        IF id_g IS NULL THEN
        	RETURN NULL;
        END IF;
        SELECT INTO id_r currval('rezerwacja_id_rezerwacja_seq');
        INSERT INTO public.Gosc_rezerw (id_rezerwacja, id_gosc) VALUES (id_r, id_g);
        INSERT INTO public.Status_rezerwacji (id_rezerwacja, data_zmiany_stanu, id_status) VALUES (id_r, CURRENT_DATE, 2);
        RETURN NULL;                                                          
    END;
    $$;

CREATE TRIGGER rezerwacja_tworzenie 
    AFTER INSERT OR UPDATE ON public.Rezerwacja
    FOR EACH ROW EXECUTE PROCEDURE tworzenie_rezerwacji();