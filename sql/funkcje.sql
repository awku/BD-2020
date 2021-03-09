-- filtruje liste hoteli po dostepnosci wybranych atrakcji
CREATE OR REPLACE FUNCTION filtruj_atrakcje(VARIADIC atr INTEGER[])
    RETURNS TABLE ( nazwa_sieci VARCHAR, id_hotel INTEGER, nazwa VARCHAR, adres VARCHAR, email VARCHAR, telefon VARCHAR, kategoria VARCHAR ) AS
$$
DECLARE
    id_atr INTEGER;
BEGIN
    CREATE TEMP TABLE A(nazwa_sieci VARCHAR, id_hotel INTEGER, nazwa VARCHAR, adres VARCHAR, email VARCHAR, telefon VARCHAR, kategoria VARCHAR, id_atrakcje INTEGER) ON COMMIT DROP;
    CREATE TEMP TABLE B(nazwa_sieci VARCHAR, id_hotel INTEGER, nazwa VARCHAR, adres VARCHAR, email VARCHAR, telefon VARCHAR, kategoria VARCHAR, id_atrakcje INTEGER) ON COMMIT DROP;
    CREATE TEMP TABLE C(nazwa_sieci VARCHAR, id_hotel INTEGER, nazwa VARCHAR, adres VARCHAR, email VARCHAR, telefon VARCHAR, kategoria VARCHAR, id_atrakcje INTEGER) ON COMMIT DROP;
    
    INSERT INTO A 
        SELECT hotele_sieci.nazwa_sieci, hot_atr.id_hotel AS id_hotel, hotele_sieci.nazwa, hotele_sieci.adres, hotele_sieci.email, hotele_sieci.telefon, hotele_sieci.kategoria, hot_atr.id_atrakcje AS id_atrakcje
            FROM hotele_sieci 
            JOIN public.hot_atr ON hotele_sieci.id_hotel=hot_atr.id_hotel;
    
    FOREACH id_atr IN ARRAY atr
    LOOP
        DELETE FROM C;
        INSERT INTO C SELECT * FROM A;
    	DELETE FROM B;
        INSERT INTO B SELECT * FROM C WHERE C.id_atrakcje=id_atr;
        DELETE FROM A;
        INSERT INTO A SELECT B.nazwa_sieci, B.id_hotel, B.nazwa, 
        	B.adres, B.email, B.telefon, B.kategoria, C.id_atrakcje 
        	FROM B JOIN C ON B.id_hotel=C.id_hotel;
    END LOOP;

    RETURN QUERY 
    SELECT B.nazwa_sieci, B.id_hotel, B.nazwa, B.adres, B.email, B.telefon, B.kategoria FROM B;
END; 
$$ LANGUAGE 'plpgsql';

-- filtruje pokoje po wybranej dostepnosci
CREATE OR REPLACE FUNCTION filtruj_pokoje(data_start DATE, data_end DATE, id_h INTEGER)
    RETURNS TABLE ( numer VARCHAR, id_pokoj INTEGER, id_hotel INTEGER, nazwa VARCHAR, 
    opis_typu VARCHAR, dla_palaczy BOOLEAN, typ_wezlu_higsan VARCHAR, 
    pietro INTEGER, liczba_miejsc INTEGER, opis_pokoju VARCHAR, cena REAL, okres_poczatek DATE, okres_koniec DATE ) AS
$$
BEGIN

    RETURN QUERY
    SELECT ph.numer, ph.id_pokoj, ph.id_hotel, ph.nazwa, ph.opis_typu, ph.dla_palaczy, ph.typ_wezlu_higsan, ph.pietro,
    ph.liczba_miejsc, ph.opis_pokoju, ph.cena, ph.okres_poczatek, ph.okres_koniec
    	FROM pokoje_hotelu ph
        LEFT JOIN (SELECT r.id_pokoj
                    FROM terminy_pokoju r
                    WHERE (daterange(data_start, data_end, '[)') && daterange(r.data_poczatku, r.data_konca, '[)'))) A
                    ON A.id_pokoj = ph.id_pokoj
        WHERE A.id_pokoj IS NULL AND ph.id_hotel = id_h;
END; 
$$ LANGUAGE 'plpgsql';

-- liczy cene pobytu
CREATE OR REPLACE FUNCTION wylicz_cene(data_start DATE, data_end DATE, id_p INTEGER)
    RETURNS REAL AS
$$

BEGIN
    RETURN SUM(cena*n) FROM(
        SELECT cena, COUNT(*) AS n FROM
            (SELECT d::date AS one_day FROM generate_series(data_start, data_end, '1 day') d) dates
	        LEFT JOIN
            pokoje_hotelu ON dates.one_day BETWEEN okres_poczatek AND okres_koniec WHERE id_pokoj=id_p
    GROUP BY 1) as temp;

END; 
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION aktualizuj_rezerwacje()
    RETURNS void AS
$$
DECLARE
    rec RECORD;
BEGIN
    FOR rec IN (SELECT id_rezerwacja, data_poczatku, data_konca, data_rezerwacji, id_status, data_zmiany_stanu FROM rezerwacje_lista WHERE r=1)  
        LOOP
            IF rec.id_status = 1 AND (DATE_PART('day', AGE(CURRENT_DATE, rec.data_rezerwacji))>3 OR DATE_PART('day', AGE(CURRENT_DATE, rec.data_poczatku))<1) THEN
                INSERT INTO Status_rezerwacji (id_rezerwacja, data_zmiany_stanu, id_status) VALUES (rec.id_rezerwacja, CURRENT_DATE, 3);
            END IF;
            IF rec.id_status = 2 AND CURRENT_DATE = rec.data_poczatku THEN
                INSERT INTO Status_rezerwacji (id_rezerwacja, data_zmiany_stanu, id_status) VALUES (rec.id_rezerwacja, CURRENT_DATE, 4);
            END IF;
            IF rec.id_status = 4 AND CURRENT_DATE = rec.data_konca THEN
                INSERT INTO Status_rezerwacji (id_rezerwacja, data_zmiany_stanu, id_status) VALUES (rec.id_rezerwacja, CURRENT_DATE, 5);
            END IF;
    	END LOOP;
END; 
$$ LANGUAGE 'plpgsql';

-- anulowanie wybranej rezerwacji po wczesniejszym sprawdzeniu warunku (min 10 dni przed)
CREATE OR REPLACE FUNCTION anuluj_rezerwacje(id_r INTEGER)
    RETURNS void AS
$$
DECLARE
    d INTEGER;
BEGIN
    SELECT INTO d dni FROM
    	(SELECT DATE_PART('day', AGE(data_poczatku, CURRENT_DATE)) AS dni
        	FROM rezerwacje_lista WHERE r=1 AND id_rezerwacja=id_r) A;
    IF d > 10 THEN
        INSERT INTO Status_rezerwacji (id_rezerwacja, data_zmiany_stanu, id_status) VALUES (id_r, CURRENT_DATE, 3);
    ELSE 
        RAISE EXCEPTION 'Rezerwacje mozna anulowac minimum 10 dni przed jej rozpoczeciem!';
    END IF;
END; 
$$ LANGUAGE 'plpgsql';