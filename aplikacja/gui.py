import tkinter as tk
import tkinter.font as tkFont
import tkinter.scrolledtext as st 
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
import datetime
from tkinter import messagebox

class App():
    def __init__(self, root, database):
        """inicjalizacja aplikacji wraz z podstawowym wyglądem kart"""    
        self.database = database
        self.root = root
        self.logged = False
        self.admin_auth = False
        self.authorized_hotel = None
        self.id_user = None
        self.chosen_room = None
        self.chosen_hotel = None
        self.chosen_chain = None
        self.chosen_attraction = None
        self.chosen_equipment = None

        root.title("Rezerwacje miejsc hotelowych")
        root.geometry("500x400")
        root.resizable(0, 0) 
        style = ttk.Style()
        style.layout('TNotebook.Tab', []) 
        
        self.tabs = ttk.Notebook(root)
        self.menu_page = ttk.Frame(self.tabs)
        self.login_page = ttk.Frame(self.tabs)
        self.register_page = ttk.Frame(self.tabs)
        self.offers_page = ttk.Frame(self.tabs)
        self.hotel_page = ttk.Frame(self.tabs)
        self.room_page = ttk.Frame(self.tabs)
        self.adding_page = ttk.Frame(self.tabs)
        self.adding_chain_page = ttk.Frame(self.tabs)
        self.adding_hotel_page = ttk.Frame(self.tabs)
        self.adding_attraction_page = ttk.Frame(self.tabs)
        self.adding_attraction_to_hotel_page = ttk.Frame(self.tabs)
        self.adding_employee_to_hotel_page = ttk.Frame(self.tabs)
        self.adding_room_page = ttk.Frame(self.tabs)
        self.adding_type_page = ttk.Frame(self.tabs)
        self.adding_equipment_page = ttk.Frame(self.tabs)
        self.adding_equipment_to_type_page = ttk.Frame(self.tabs)
        self.adding_price_to_type_page = ttk.Frame(self.tabs)
        self.reservations_page = ttk.Frame(self.tabs)
        self.hotel_reservations_page = ttk.Frame(self.tabs)
        self.user_page = ttk.Frame(self.tabs)

        self.tabs.add(self.menu_page, text='Menu')
        self.tabs.add(self.login_page, text='Logowanie')
        self.tabs.add(self.register_page, text='Rejestracja')
        self.tabs.add(self.offers_page, text='Oferty')
        self.tabs.add(self.adding_page, text='Dodaj dane')
        self.tabs.add(self.adding_chain_page, text='Dodaj siec')
        self.tabs.add(self.adding_hotel_page, text='Dodaj hotel')
        self.tabs.add(self.adding_attraction_page, text='Dodaj atrakcje')
        self.tabs.add(self.adding_attraction_to_hotel_page, text='Dodaj atrakcje do hotelu')
        self.tabs.add(self.adding_employee_to_hotel_page, text='Dodaj pracownika do hotelu')
        self.tabs.add(self.adding_room_page, text='Dodaj pokoj')
        self.tabs.add(self.adding_type_page, text='Dodaj typ pokoju')
        self.tabs.add(self.adding_equipment_page, text='Dodaj wyposazenie')
        self.tabs.add(self.adding_equipment_to_type_page, text='Dodaj wyposazenie do pokoju')
        self.tabs.add(self.adding_price_to_type_page, text='Dodaj cene do pokoju')
        self.tabs.add(self.hotel_page, text='Hotel')
        self.tabs.add(self.room_page, text='Pokoj')
        self.tabs.add(self.reservations_page, text='Moje rezerwacje')
        self.tabs.add(self.hotel_reservations_page, text='Rezerwacje')
        self.tabs.add(self.user_page, text='Edytuj uzytkownika')
        self.tabs.pack(expand=1, fill='both')

        ###############fonts###############

        self.title_font = tkFont.Font(family='Bitstream Charter',size=23)
        self.normal_font=tkFont.Font(family='Bitstream Charter',size=10)
        self.small_font=tkFont.Font(family='Bitstream Charter',size=8)

        ###############init_database_functions###############

        self.database.update_reservations()
        self.hotel_data = self.database.get_hotels()

        ###############menu_page###############

        menu_text=tk.Label(self.menu_page, text="MENU", font=self.title_font)
        menu_text.place(x=0,y=0,width=500,height=40)

        offers=tk.Button(self.menu_page, text="Oferty", cursor="heart", font=self.normal_font, command=self.offers_command)
        offers.place(x=150,y=100,width=200,height=25)

        self.login=tk.Button(self.menu_page, text="Logowanie", cursor="heart", font=self.normal_font, command=self.login_command)
        self.login.place(x=150,y=160,width=200,height=25)

        self.register=tk.Button(self.menu_page, text="Rejestracja", cursor="heart", font=self.normal_font, command=self.register_command)
        self.register.place(x=150,y=190,width=200,height=25)

        self.adding=tk.Button(self.menu_page, text="Dodaj", cursor="heart", font=self.normal_font, command=self.adding_command)
        
        self.logout=tk.Button(self.menu_page, text="Wyloguj", cursor="heart", font=self.normal_font, command=self.logout_command)
        
        self.reservations=tk.Button(self.menu_page, text="Moje rezerwacje", cursor="heart", font=self.normal_font, command=self.reservations_command)
        
        self.hotel_reservations=tk.Button(self.menu_page, text="Rezerwacje", cursor="heart", font=self.normal_font, command=self.hotel_reservations_command)
        
        self.user=tk.Button(self.menu_page, text="Edytuj dane uzytkownika", cursor="heart", font=self.normal_font, command=self.user_command)
        
        self.hotels_stats = self.database.get_statistics()

        self.hotels_stats_text_var = tk.StringVar()
        
        self.hotels_stats_text_var.set("Statystyki:\n Liczba hoteli: {}\tLiczba pokoi:{} \nMinimalna cena za dzien:{}\tMaksymalna cena za dzien: {}".format(
                                        int(self.hotels_stats['liczba_hoteli']), int(self.hotels_stats['liczba_pokoi']), self.hotels_stats['min_cena'], self.hotels_stats['max_cena']))
        
        hotels_stats_text = tk.Label(self.menu_page, textvariable=self.hotels_stats_text_var, font=self.small_font, wraplength='390p')
        
        hotels_stats_text.place(x=0,y=300,width=500,height=75)

        ###############login_page###############

        login_text = tk.Label(self.login_page, text='Logowanie', font=self.title_font)
        login_text.place(x=0,y=0,width=500,height=40)

        login_email_text = tk.Label(self.login_page, text='E-mail:', font=self.normal_font)
        login_email_text.place(x=60,y=100,width=80,height=20)

        self.login_email_input = tk.Entry(self.login_page, width = 20) 
        self.login_email_input.place(x=160,y=100,width=270,height=20)

        login_password_text = tk.Label(self.login_page, text='Haslo:', font=self.normal_font)
        login_password_text.place(x=60,y=130,width=80,height=20)

        self.login_password_input = tk.Entry(self.login_page, width = 20, show="*") 
        self.login_password_input.place(x=160,y=130,width=270,height=20)

        login_submit=tk.Button(self.login_page, text="Zaloguj sie", command=self.login_submit_command, font=self.normal_font)
        login_submit.place(x=200,y=200,width=100,height=25)

        login_menu=tk.Button(self.login_page, text="Powrot do menu", command=self.menu_command, font=self.normal_font)
        login_menu.place(x=0,y=0,width=120,height=20)

        ###############register_page###############

        register_text = tk.Label(self.register_page, text='Rejestracja', font=self.title_font)
        register_text.place(x=0,y=0,width=500,height=40)

        register_email_text = tk.Label(self.register_page, text='E-mail:', font=self.normal_font)
        register_email_text.place(x=60,y=80,width=80,height=20)
        
        self.register_email_input = tk.Entry(self.register_page, width = 20) 
        self.register_email_input.place(x=160,y=80,width=270,height=20)

        register_password_text = tk.Label(self.register_page, text='Haslo:', font=self.normal_font)
        register_password_text.place(x=60,y=110,width=80,height=20)

        self.register_password_input = tk.Entry(self.register_page, width = 20, show="*") 
        self.register_password_input.place(x=160,y=110,width=270,height=20)

        register_name_text = tk.Label(self.register_page, text='Imie:', font=self.normal_font)
        register_name_text.place(x=60,y=140,width=80,height=20)

        self.register_name_input = tk.Entry(self.register_page, width = 20) 
        self.register_name_input.place(x=160,y=140,width=270,height=20)

        register_surname_text = tk.Label(self.register_page, text='Nazwisko:', font=self.normal_font)
        register_surname_text.place(x=60,y=170,width=80,height=20)

        self.register_surname_input = tk.Entry(self.register_page, width = 20) 
        self.register_surname_input.place(x=160,y=170,width=270,height=20)

        register_phone_text = tk.Label(self.register_page, text='Telefon:', font=self.normal_font)
        register_phone_text.place(x=60,y=200,width=80,height=20)

        self.register_phone_input = tk.Entry(self.register_page, width = 20) 
        self.register_phone_input.place(x=160,y=200,width=270,height=20)

        register_submit=tk.Button(self.register_page, text="Zarejestruj sie", command=self.register_submit_command, font=self.normal_font)
        register_submit.place(x=200,y=280,width=100,height=25)

        register_menu=tk.Button(self.register_page, text="Powrot do menu", command=self.menu_command, font=self.normal_font)
        register_menu.place(x=0,y=0,width=120,height=20)
        
        ###############adding_page###############

        adding_text = tk.Label(self.adding_page, text='Dodaj dane', font=self.title_font)
        adding_text.place(x=0,y=0,width=500,height=40)

        self.adding_chain=tk.Button(self.adding_page, text="Dodaj siec", cursor="heart", font=self.normal_font, command=self.adding_chain_command)

        self.adding_hotel=tk.Button(self.adding_page, text="Dodaj hotel", cursor="heart", font=self.normal_font, command=self.adding_hotel_command)

        self.adding_room=tk.Button(self.adding_page, text="Dodaj pokoj", cursor="heart", font=self.normal_font, command=self.adding_room_command)
        self.adding_room.place(x=100,y=110,width=300,height=25)

        self.adding_type=tk.Button(self.adding_page, text="Dodaj typ pokoju", cursor="heart", font=self.normal_font, command=self.adding_type_command)
        self.adding_type.place(x=100,y=140,width=300,height=25)

        self.adding_equipment=tk.Button(self.adding_page, text="Dodaj wyposazenie", cursor="heart", font=self.normal_font, command=self.adding_equipment_command)
        self.adding_equipment.place(x=100,y=170,width=300,height=25)

        self.adding_attraction_to_hotel=tk.Button(self.adding_page, text="Dodaj atrakcje", cursor="heart", font=self.normal_font, command=self.adding_attraction_command)
        self.adding_attraction_to_hotel.place(x=100,y=200,width=300,height=25)

        self.adding_attraction_to_hotel=tk.Button(self.adding_page, text="Dodaj atrakcje do hotelu", cursor="heart", font=self.normal_font, command=self.adding_attraction_to_hotel_command)
        self.adding_attraction_to_hotel.place(x=100,y=230,width=300,height=25)

        self.adding_equipment_to_type=tk.Button(self.adding_page, text="Dodaj wyposazenie do typu pokoju", cursor="heart", font=self.normal_font, command=self.adding_equipment_to_type_command)
        self.adding_equipment_to_type.place(x=100,y=260,width=300,height=25)

        self.price_to_type=tk.Button(self.adding_page, text="Dodaj cene do typu pokoju", cursor="heart", font=self.normal_font, command=self.adding_price_to_type_command)
        self.price_to_type.place(x=100,y=290,width=300,height=25)

        self.adding_attraction_to_hotel=tk.Button(self.adding_page, text="Dodaj pracownika do hotelu", cursor="heart", font=self.normal_font, command=self.adding_employee_to_hotel_command)
        self.adding_attraction_to_hotel.place(x=100,y=320,width=300,height=25)

        adding_menu=tk.Button(self.adding_page, text="Powrot do menu", command=self.menu_command, font=self.normal_font)
        adding_menu.place(x=0,y=0,width=120,height=20)

        ###############adding_employee_to_hotel_page###############

        adding_employee_to_hotel_text = tk.Label(self.adding_employee_to_hotel_page, text='Dodaj pracownika\ndo hotelu', font=self.title_font)
        adding_employee_to_hotel_text.place(x=0,y=0,width=500,height=80)

        adding_employee_to_hotel_hotel_text = tk.Label(self.adding_employee_to_hotel_page, text='Hotel:', font=self.normal_font)
        adding_employee_to_hotel_hotel_text.place(x=60,y=80,width=80,height=20)

        adding_employee_to_hotel_email_text = tk.Label(self.adding_employee_to_hotel_page, text='E-mail:', font=self.normal_font)
        adding_employee_to_hotel_email_text.place(x=60,y=110,width=80,height=20)
        
        self.adding_employee_to_hotel_email_input = tk.Entry(self.adding_employee_to_hotel_page, width = 20) 
        self.adding_employee_to_hotel_email_input.place(x=160,y=110,width=270,height=20)

        adding_employee_to_hotel_password_text = tk.Label(self.adding_employee_to_hotel_page, text='Haslo:', font=self.normal_font)
        adding_employee_to_hotel_password_text.place(x=60,y=140,width=80,height=20)

        self.adding_employee_to_hotel_password_input = tk.Entry(self.adding_employee_to_hotel_page, width = 20, show="*") 
        self.adding_employee_to_hotel_password_input.place(x=160,y=140,width=270,height=20)

        adding_employee_to_hotel_name_text = tk.Label(self.adding_employee_to_hotel_page, text='Imie:', font=self.normal_font)
        adding_employee_to_hotel_name_text.place(x=60,y=170,width=80,height=20)

        self.adding_employee_to_hotel_name_input = tk.Entry(self.adding_employee_to_hotel_page, width = 20) 
        self.adding_employee_to_hotel_name_input.place(x=160,y=170,width=270,height=20)

        adding_employee_to_hotel_surname_text = tk.Label(self.adding_employee_to_hotel_page, text='Nazwisko:', font=self.normal_font)
        adding_employee_to_hotel_surname_text.place(x=60,y=200,width=80,height=20)

        self.adding_employee_to_hotel_surname_input = tk.Entry(self.adding_employee_to_hotel_page, width = 20) 
        self.adding_employee_to_hotel_surname_input.place(x=160,y=200,width=270,height=20)

        adding_employee_to_hotel_submit=tk.Button(self.adding_employee_to_hotel_page, text="Dodaj pracownika", command=self.adding_employee_to_hotel_submit_command, font=self.normal_font)
        adding_employee_to_hotel_submit.place(x=190,y=280,width=120,height=25)

        adding_employee_to_hotel_menu=tk.Button(self.adding_employee_to_hotel_page, text="Powrot do menu", command=self.menu_command, font=self.normal_font)
        adding_employee_to_hotel_menu.place(x=0,y=0,width=120,height=20)

        ###############adding_chain_page###############

        adding_chain_text = tk.Label(self.adding_chain_page, text='Dodaj siec', font=self.title_font)
        adding_chain_text.place(x=0,y=0,width=500,height=40)

        adding_chain_name_text = tk.Label(self.adding_chain_page, text='Nazwa:', font=self.normal_font)
        adding_chain_name_text.place(x=60,y=80,width=80,height=20)
        
        self.adding_chain_name_input = tk.Entry(self.adding_chain_page, width = 20) 
        self.adding_chain_name_input.place(x=160,y=80,width=270,height=20)

        adding_chain_submit=tk.Button(self.adding_chain_page, text="Dodaj", command=self.adding_chain_submit_command, font=self.normal_font)
        adding_chain_submit.place(x=200,y=230,width=100,height=25)

        adding_chain_adding=tk.Button(self.adding_chain_page, text="Powrot", command=self.adding_command, font=self.normal_font)
        adding_chain_adding.place(x=0,y=25,width=120,height=20)

        adding_chain_menu=tk.Button(self.adding_chain_page, text="Powrot do menu", command=self.menu_command, font=self.normal_font)
        adding_chain_menu.place(x=0,y=0,width=120,height=20)

        ###############adding_hotel_page###############
        adding_hotel_text = tk.Label(self.adding_hotel_page, text='Dodaj hotel', font=self.title_font)
        adding_hotel_text.place(x=0,y=0,width=500,height=40)

        adding_hotel_chain_text = tk.Label(self.adding_hotel_page, text='Siec:', font=self.normal_font)
        adding_hotel_chain_text.place(x=60,y=70,width=80,height=20)

        adding_hotel_name_text = tk.Label(self.adding_hotel_page, text='Nazwa:', font=self.normal_font)
        adding_hotel_name_text.place(x=60,y=100,width=80,height=20)

        self.adding_hotel_name_input = tk.Entry(self.adding_hotel_page, width = 20) 
        self.adding_hotel_name_input.place(x=160,y=100,width=270,height=20)

        adding_hotel_address_text = tk.Label(self.adding_hotel_page, text='Adres:', font=self.normal_font)
        adding_hotel_address_text.place(x=60,y=130,width=80,height=20)

        self.adding_hotel_address_input = tk.Entry(self.adding_hotel_page, width = 20) 
        self.adding_hotel_address_input.place(x=160,y=130,width=270,height=20)

        adding_hotel_email_text = tk.Label(self.adding_hotel_page, text='Email:', font=self.normal_font)
        adding_hotel_email_text.place(x=60,y=160,width=80,height=20)

        self.adding_hotel_email_input = tk.Entry(self.adding_hotel_page, width = 20) 
        self.adding_hotel_email_input.place(x=160,y=160,width=270,height=20)

        adding_hotel_phone_text = tk.Label(self.adding_hotel_page, text='Telefon:', font=self.normal_font)
        adding_hotel_phone_text.place(x=60,y=190,width=80,height=20)

        self.adding_hotel_phone_input = tk.Entry(self.adding_hotel_page, width = 20) 
        self.adding_hotel_phone_input.place(x=160,y=190,width=270,height=20)

        adding_hotel_category_text = tk.Label(self.adding_hotel_page, text='Kategoria:', font=self.normal_font)
        adding_hotel_category_text.place(x=60,y=220,width=80,height=20)

        self.hotel_category_var = tk.StringVar()
        self.hotel_category_options = ["", "*", "**", "***", "****", "*****"]
        self.hotel_category_var.set(self.hotel_category_options[0])
        self.optionmenu_category = tk.OptionMenu(self.adding_hotel_page, self.hotel_category_var, *self.hotel_category_options)
        self.optionmenu_category.place(x=160,y=220,width=270,height=20)

        adding_hotel_submit=tk.Button(self.adding_hotel_page, text="Dodaj", command=self.adding_hotel_submit_command, font=self.normal_font)
        adding_hotel_submit.place(x=200,y=260,width=100,height=25)

        adding_hotel_adding=tk.Button(self.adding_hotel_page, text="Powrot", command=self.adding_command, font=self.normal_font)
        adding_hotel_adding.place(x=0,y=25,width=120,height=20)

        adding_hotel_menu=tk.Button(self.adding_hotel_page, text="Powrot do menu", command=self.menu_command, font=self.normal_font)
        adding_hotel_menu.place(x=0,y=0,width=120,height=20)
        
        ###############adding_attraction_page###############

        adding_attraction_text = tk.Label(self.adding_attraction_page, text='Dodaj atrakcje', font=self.title_font)
        adding_attraction_text.place(x=0,y=0,width=500,height=40)

        adding_attraction_description_text = tk.Label(self.adding_attraction_page, text='Opis:', font=self.normal_font)
        adding_attraction_description_text.place(x=60,y=100,width=80,height=20)
        
        self.adding_attraction_description_input = tk.Entry(self.adding_attraction_page, width = 20) 
        self.adding_attraction_description_input.place(x=160,y=100,width=270,height=20)

        adding_attraction_submit=tk.Button(self.adding_attraction_page, text="Dodaj", command=self.adding_attraction_submit_command, font=self.normal_font)
        adding_attraction_submit.place(x=200,y=230,width=100,height=25)

        adding_attraction_adding=tk.Button(self.adding_attraction_page, text="Powrot", command=self.adding_command, font=self.normal_font)
        adding_attraction_adding.place(x=0,y=25,width=120,height=20)

        adding_attraction_menu=tk.Button(self.adding_attraction_page, text="Powrot do menu", command=self.menu_command, font=self.normal_font)
        adding_attraction_menu.place(x=0,y=0,width=120,height=20)

        ###############adding_attraction_to_hotel_page###############

        adding_attraction_to_hotel_text = tk.Label(self.adding_attraction_to_hotel_page, text='Dodaj atrakcje\ndo hotelu', font=self.title_font)
        adding_attraction_to_hotel_text.place(x=0,y=0,width=500,height=80)

        adding_attraction_to_hotel_hotel_text = tk.Label(self.adding_attraction_to_hotel_page, text='Hotel:', font=self.normal_font)
        adding_attraction_to_hotel_hotel_text.place(x=60,y=100,width=80,height=20)

        adding_attraction_to_hotel_attr_text = tk.Label(self.adding_attraction_to_hotel_page, text='Atrakcja:', font=self.normal_font)
        adding_attraction_to_hotel_attr_text.place(x=60,y=130,width=80,height=20)

        adding_attraction_to_hotel_start_text = tk.Label(self.adding_attraction_to_hotel_page, text='Godzina otwarcia\n(format %H:%M, opcjonalne):', font=self.normal_font)
        adding_attraction_to_hotel_start_text.place(x=0,y=160,width=220,height=40)
        
        self.adding_attraction_to_hotel_start_input = tk.Entry(self.adding_attraction_to_hotel_page, width = 20) 
        self.adding_attraction_to_hotel_start_input.place(x=220,y=170,width=170,height=20)

        adding_attraction_to_hotel_end_text = tk.Label(self.adding_attraction_to_hotel_page, text='Godzina zamkniecia\n(format %H:%M, opcjonalne):', font=self.normal_font)
        adding_attraction_to_hotel_end_text.place(x=0,y=210,width=220,height=40)
        
        self.adding_attraction_to_hotel_end_input = tk.Entry(self.adding_attraction_to_hotel_page, width = 20) 
        self.adding_attraction_to_hotel_end_input.place(x=220,y=220,width=170,height=20)

        adding_attraction_to_hotel_price_text = tk.Label(self.adding_attraction_to_hotel_page, text='Cena za godzine\n(opcjonalne):', font=self.normal_font)
        adding_attraction_to_hotel_price_text.place(x=20,y=260,width=120,height=40)
        
        self.adding_attraction_price_input = tk.Entry(self.adding_attraction_to_hotel_page, width = 20) 
        self.adding_attraction_price_input.place(x=160,y=270,width=270,height=20)

        adding_attraction_submit=tk.Button(self.adding_attraction_to_hotel_page, text="Dodaj", command=self.adding_attraction_to_hotel_submit_command, font=self.normal_font)
        adding_attraction_submit.place(x=200,y=300,width=100,height=25)

        adding_attraction_adding=tk.Button(self.adding_attraction_to_hotel_page, text="Powrot", command=self.adding_command, font=self.normal_font)
        adding_attraction_adding.place(x=0,y=25,width=120,height=20)

        adding_attraction_menu=tk.Button(self.adding_attraction_to_hotel_page, text="Powrot do menu", command=self.menu_command, font=self.normal_font)
        adding_attraction_menu.place(x=0,y=0,width=120,height=20)

        ###############adding_room_page###############

        adding_room_text = tk.Label(self.adding_room_page, text='Dodaj pokoj', font=self.title_font)
        adding_room_text.place(x=0,y=0,width=500,height=40)


        adding_room_hotel_text = tk.Label(self.adding_room_page, text='Hotel:', font=self.normal_font)
        adding_room_hotel_text.place(x=60,y=70,width=80,height=20)
        
        adding_room_type_text = tk.Label(self.adding_room_page, text='Typ pokoju:', font=self.normal_font)
        adding_room_type_text.place(x=60,y=100,width=80,height=20)

        adding_room_level_text = tk.Label(self.adding_room_page, text='Pietro:', font=self.normal_font)
        adding_room_level_text.place(x=60,y=130,width=80,height=20)
        
        self.adding_room_level_input = tk.Entry(self.adding_room_page, width = 20) 
        self.adding_room_level_input.place(x=160,y=130,width=270,height=20)

        adding_room_number_text = tk.Label(self.adding_room_page, text='Numer:', font=self.normal_font)
        adding_room_number_text.place(x=60,y=160,width=80,height=20)
        
        self.adding_room_number_input = tk.Entry(self.adding_room_page, width = 20) 
        self.adding_room_number_input.place(x=160,y=160,width=270,height=20)

        adding_room_capacity_text = tk.Label(self.adding_room_page, text='Liczba miejsc:', font=self.normal_font)
        adding_room_capacity_text.place(x=60,y=190,width=82,height=20)
        
        self.adding_room_capacity_input = tk.Entry(self.adding_room_page, width = 20) 
        self.adding_room_capacity_input.place(x=160,y=190,width=270,height=20)

        adding_room_description_text = tk.Label(self.adding_room_page, text='Opis\n(opcjonalnie):', font=self.normal_font)
        adding_room_description_text.place(x=60,y=220,width=80,height=40)
        
        self.adding_room_description_input = tk.Entry(self.adding_room_page, width = 20) 
        self.adding_room_description_input.place(x=160,y=220,width=270,height=20)

        adding_room_submit=tk.Button(self.adding_room_page, text="Dodaj", command=self.adding_room_submit_command, font=self.normal_font)
        adding_room_submit.place(x=200,y=250,width=100,height=25)

        adding_room_adding=tk.Button(self.adding_room_page, text="Powrot", command=self.adding_command, font=self.normal_font)
        adding_room_adding.place(x=0,y=25,width=120,height=20)

        adding_room_menu=tk.Button(self.adding_room_page, text="Powrot do menu", command=self.menu_command, font=self.normal_font)
        adding_room_menu.place(x=0,y=0,width=120,height=20)

        ###############adding_type_page###############
        adding_type_text = tk.Label(self.adding_type_page, text='Dodaj typ pokoju', font=self.title_font)
        adding_type_text.place(x=0,y=0,width=500,height=40)

        adding_room_hotel_text = tk.Label(self.adding_type_page, text='Hotel:', font=self.normal_font)
        adding_room_hotel_text.place(x=60,y=80,width=80,height=20)

        adding_type_name_text = tk.Label(self.adding_type_page, text='Nazwa:', font=self.normal_font)
        adding_type_name_text.place(x=60,y=110,width=80,height=20)
        
        self.adding_type_name_input = tk.Entry(self.adding_type_page, width = 20) 
        self.adding_type_name_input.place(x=160,y=110,width=270,height=20)
        
        self.adding_type_smoking_var = tk.BooleanVar()
        self.adding_type_smoking_input = tk.Checkbutton(self.adding_type_page, text='Dla palaczy',variable=self.adding_type_smoking_var, onvalue=True, offvalue=False)
        self.adding_type_smoking_input.place(x=160,y=140,width=270,height=20)

        adding_type_description_text = tk.Label(self.adding_type_page, text='Opis (opcjonalnie):', font=self.normal_font)
        adding_type_description_text.place(x=20,y=170,width=120,height=20)
        
        self.adding_type_description_input = tk.Entry(self.adding_type_page, width = 20) 
        self.adding_type_description_input.place(x=160,y=170,width=270,height=20)

        adding_type_hs_text = tk.Label(self.adding_type_page, text='Typ wezla\nhigieniczno-sanitarnego\n(opcjonalnie):', font=self.normal_font)
        adding_type_hs_text.place(x=0,y=200,width=160,height=60)
        
        self.adding_type_hs_input = tk.Entry(self.adding_type_page, width = 20) 
        self.adding_type_hs_input.place(x=160,y=220,width=270,height=20)

        adding_type_submit=tk.Button(self.adding_type_page, text="Dodaj", command=self.adding_type_submit_command, font=self.normal_font)
        adding_type_submit.place(x=200,y=270,width=100,height=25)

        adding_type_adding=tk.Button(self.adding_type_page, text="Powrot", command=self.adding_command, font=self.normal_font)
        adding_type_adding.place(x=0,y=25,width=120,height=20)

        adding_type_menu=tk.Button(self.adding_type_page, text="Powrot do menu", command=self.menu_command, font=self.normal_font)
        adding_type_menu.place(x=0,y=0,width=120,height=20)

        ###############adding_equipment_page###############

        adding_equipment_text = tk.Label(self.adding_equipment_page, text='Dodaj wyposazenie', font=self.title_font)
        adding_equipment_text.place(x=0,y=0,width=500,height=40)

        adding_equipment_description_text = tk.Label(self.adding_equipment_page, text='Opis:', font=self.normal_font)
        adding_equipment_description_text.place(x=60,y=100,width=80,height=20)
        
        self.adding_equipment_description_input = tk.Entry(self.adding_equipment_page, width = 20) 
        self.adding_equipment_description_input.place(x=160,y=100,width=270,height=20)

        adding_equipment_submit=tk.Button(self.adding_equipment_page, text="Dodaj", command=self.adding_equipment_submit_command, font=self.normal_font)
        adding_equipment_submit.place(x=200,y=260,width=100,height=25)

        adding_equipment_adding=tk.Button(self.adding_equipment_page, text="Powrot", command=self.adding_command, font=self.normal_font)
        adding_equipment_adding.place(x=0,y=25,width=120,height=20)

        adding_equipment_menu=tk.Button(self.adding_equipment_page, text="Powrot do menu", command=self.menu_command, font=self.normal_font)
        adding_equipment_menu.place(x=0,y=0,width=120,height=20)

        ###############adding_equipment_to_type_page###############

        adding_equipment_to_type_text = tk.Label(self.adding_equipment_to_type_page, text='Dodaj wyposazenie\ndo typu pokoju', font=self.title_font)
        adding_equipment_to_type_text.place(x=0,y=0,width=500,height=80)

        adding_equipment_to_type_hotel_text = tk.Label(self.adding_equipment_to_type_page, text='Hotel:', font=self.normal_font)
        adding_equipment_to_type_hotel_text.place(x=60,y=100,width=80,height=20)

        adding_equipment_to_type_equipment_text = tk.Label(self.adding_equipment_to_type_page, text='Wyposazenie:', font=self.normal_font)
        adding_equipment_to_type_equipment_text.place(x=60,y=130,width=80,height=20)
        
        adding_equipment_to_type_type_text = tk.Label(self.adding_equipment_to_type_page, text='Typ pokoju:', font=self.normal_font)
        adding_equipment_to_type_type_text.place(x=60,y=160,width=80,height=20)

        adding_equipment_to_type_quantity_text = tk.Label(self.adding_equipment_to_type_page, text='Ilosc:', font=self.normal_font)
        adding_equipment_to_type_quantity_text.place(x=60,y=190,width=80,height=20)
        
        self.adding_equipment_to_type_quantity_input = tk.Entry(self.adding_equipment_to_type_page, width = 20) 
        self.adding_equipment_to_type_quantity_input.place(x=160,y=190,width=270,height=20)

        adding_equipment_to_type_submit=tk.Button(self.adding_equipment_to_type_page, text="Dodaj", command=self.adding_equipment_to_type_submit_command, font=self.normal_font)
        adding_equipment_to_type_submit.place(x=200,y=260,width=100,height=25)

        adding_equipment_to_type_adding=tk.Button(self.adding_equipment_to_type_page, text="Powrot", command=self.adding_command, font=self.normal_font)
        adding_equipment_to_type_adding.place(x=0,y=25,width=120,height=20)

        adding_equipment_to_type_menu=tk.Button(self.adding_equipment_to_type_page, text="Powrot do menu", command=self.menu_command, font=self.normal_font)
        adding_equipment_to_type_menu.place(x=0,y=0,width=120,height=20)

        ###############adding_price_to_type_page###############

        adding_price_to_type_text = tk.Label(self.adding_price_to_type_page, text='Dodaj cene\ndo typu pokoju', font=self.title_font)
        adding_price_to_type_text.place(x=0,y=0,width=500,height=80)

        adding_price_to_type_hotel_text = tk.Label(self.adding_price_to_type_page, text='Hotel:', font=self.normal_font)
        adding_price_to_type_hotel_text.place(x=60,y=100,width=80,height=20)

        adding_price_to_type_price_text = tk.Label(self.adding_price_to_type_page, text='Cena:', font=self.normal_font)
        adding_price_to_type_price_text.place(x=60,y=160,width=80,height=20)
        
        self.adding_price_to_type_price_input = tk.Entry(self.adding_price_to_type_page, width = 20) 
        self.adding_price_to_type_price_input.place(x=160,y=160,width=270,height=20)

        adding_price_to_type_type_text = tk.Label(self.adding_price_to_type_page, text='Typ pokoju:', font=self.normal_font)
        adding_price_to_type_type_text.place(x=60,y=130,width=80,height=20)
        
        adding_price_to_type_price_start_text = tk.Label(self.adding_price_to_type_page, text='Poczatek okresu:', font=self.normal_font)
        adding_price_to_type_price_start_text.place(x=40,y=190,width=100,height=20)

        today = datetime.date.today()
        self.room_price_picker_start = DateEntry(self.adding_price_to_type_page, width=12, background='darkblue',
                    foreground='white', borderwidth=2, year=today.year, month=today.month, day=today.day)
        self.room_price_picker_start.place(x=160,y=190,width=270,height=20)

        adding_price_to_type_price_end_text = tk.Label(self.adding_price_to_type_page, text='Koniec okresu:', font=self.normal_font)
        adding_price_to_type_price_end_text.place(x=40,y=220,width=100,height=20)

        self.room_price_picker_end = DateEntry(self.adding_price_to_type_page, width=12, background='darkblue',
                    foreground='white', borderwidth=2, year=today.year, month=today.month, day=today.day)
        self.room_price_picker_end.place(x=160,y=220,width=270,height=20)

        adding_price_to_type_submit=tk.Button(self.adding_price_to_type_page, text="Dodaj", command=self.adding_price_to_type_submit_command, font=self.normal_font)
        adding_price_to_type_submit.place(x=200,y=260,width=100,height=25)

        adding_price_to_type_adding=tk.Button(self.adding_price_to_type_page, text="Powrot", command=self.adding_command, font=self.normal_font)
        adding_price_to_type_adding.place(x=0,y=25,width=120,height=20)

        adding_price_to_type_menu=tk.Button(self.adding_price_to_type_page, text="Powrot do menu", command=self.menu_command, font=self.normal_font)
        adding_price_to_type_menu.place(x=0,y=0,width=120,height=20)

        ###############offers_page###############

        offers_text = tk.Label(self.offers_page, text='Oferty', font=self.title_font)
        offers_text.place(x=0,y=0,width=500,height=40)

        offers_chain_text = tk.Label(self.offers_page, text='Siec hoteli:', font=self.normal_font)
        offers_chain_text.place(x=60,y=70,width=80,height=20)

        hotel_list_text = tk.Label(self.offers_page, text='Hotel:', font=self.normal_font)
        hotel_list_text.place(x=60,y=100,width=80,height=20)

        hotel_list_text = tk.Label(self.offers_page, text='Filtrowanie\npo atrakcjach:', font=self.normal_font)
        hotel_list_text.place(x=40,y=130,width=120,height=40)

        self.hotel_info_text_var = tk.StringVar()
        self.hotel_info_text_var.set("")
        hotel_info_text = tk.Label(self.offers_page, textvariable=self.hotel_info_text_var, font=self.small_font, wraplength='490p')
        hotel_info_text.place(x=0,y=230,width=500,height=100)

        hotel_submit=tk.Button(self.offers_page, text="Przejdz do hotelu", command=self.hotel_command, font=self.normal_font)
        hotel_submit.place(x=280,y=370,width=130,height=20)

        offers_menu=tk.Button(self.offers_page, text="Powrot do menu", command=self.menu_command, font=self.normal_font)
        offers_menu.place(x=0,y=0,width=120,height=20)

        ###############hotel_page###############

        hotel_text = tk.Label(self.hotel_page, text='Hotel', font=self.title_font)
        hotel_text.place(x=0,y=0,width=500,height=40)
        self.hotel_attractions_text_var = tk.StringVar()
        self.hotel_attractions_text_var.set("")
        hotel_attractions_text = tk.Label(self.hotel_page, textvariable=self.hotel_attractions_text_var, font=self.small_font, wraplength='390p')
        hotel_attractions_text.place(x=0,y=40,width=500,height=100)

        hotel_room_text = tk.Label(self.hotel_page, text='Pokoj:', font=self.normal_font)
        hotel_room_text.place(x=60,y=140,width=80,height=20)

        self.room_equipment_text_var = tk.StringVar()
        self.room_equipment_text_var.set("")
        room_equipment_text = tk.Label(self.hotel_page, textvariable=self.room_equipment_text_var, font=self.small_font, wraplength='350p')
        room_equipment_text.place(x=0,y=165,width=500,height=95)

        self.room_price_text_var = tk.StringVar()
        self.room_price_text_var.set("")

        self.room_equipment_button = tk.Button(self.hotel_page, text='Wyposazenie', command=self.room_equipment_command, font=self.normal_font)
        self.room_equipment_button.place(x=320,y=250,width=150,height=20)

        self.room_availability_text = tk.Button(self.hotel_page, text='Wolne terminy', command=self.room_availability_command, font=self.normal_font)
        self.room_availability_text.place(x=320,y=275,width=150,height=20)

        self.room_price_button = tk.Button(self.hotel_page, text='Ceny', command=self.room_price_command, font=self.normal_font)
        self.room_price_button.place(x=320,y=325,width=150,height=20)

        self.hotel_attractions_button = tk.Button(self.hotel_page, text='Atrakcje', command=self.hotel_attractions_command, font=self.normal_font)
        self.hotel_attractions_button.place(x=320,y=300,width=150,height=20)

        self.hotel_room=tk.Button(self.hotel_page, text="Zarezerwuj pokoj", command=self.room_command, font=self.normal_font)

        hotel_filter_text = tk.Label(self.hotel_page, text='Filtruj pokoje\npo dostepnosci:', font=self.normal_font)
        hotel_filter_text.place(x=0,y=330,width=100,height=40)
        
        hotel_date_picker_end_text = ttk.Label(self.hotel_page, text='Start:')
        hotel_date_picker_end_text.place(x=100,y=330,width=100,height=20)

        self.hotel_date_picker_start = DateEntry(self.hotel_page, width=12, background='darkblue',
                    foreground='white', borderwidth=2, year=today.year, month=today.month, day=today.day)
        self.hotel_date_picker_start.place(x=100,y=350,width=100,height=20)

        hotel_date_picker_end_text = ttk.Label(self.hotel_page, text='Koniec:')
        hotel_date_picker_end_text.place(x=200,y=330,width=100,height=20)

        self.hotel_date_picker_end = DateEntry(self.hotel_page, width=12, background='darkblue',
                    foreground='white', borderwidth=2, year=today.year, month=today.month, day=today.day)
        self.hotel_date_picker_end.place(x=200,y=350,width=100,height=20)

        filter_rooms_button=tk.Button(self.hotel_page, text="Filtruj", command=self.filter_rooms, font=self.normal_font)
        filter_rooms_button.place(x=120,y=370,width=120,height=20)

        hotel_offers=tk.Button(self.hotel_page, text="Powrot do ofert", command=self.offers_command, font=self.normal_font)
        hotel_offers.place(x=0,y=25,width=120,height=20)

        hotel_menu=tk.Button(self.hotel_page, text="Powrot do menu", command=self.menu_command, font=self.normal_font)
        hotel_menu.place(x=0,y=0,width=120,height=20)

        ###############room_page###############

        room_text = tk.Label(self.room_page, text='Rezerwacja', font=self.title_font)
        room_text.place(x=0,y=0,width=500,height=40)

        room_av_text = tk.Button(self.room_page, text='Wolne terminy', command=self.room_availability_command, font=self.normal_font)
        room_av_text.place(x=100,y=100,width=300,height=50)

        room_date_picker_text = ttk.Label(self.room_page, text='Wybierz date\npobytu')
        room_date_picker_text.place(x=60,y=180,width=80,height=40)

        room_date_picker_start_text = ttk.Label(self.room_page, text='Start:')
        room_date_picker_start_text.place(x=160,y=180,width=100,height=20)

        today = datetime.date.today()
        self.room_date_picker_start = DateEntry(self.room_page, width=12, background='darkblue',
                    foreground='white', borderwidth=2, year=today.year, month=today.month, day=today.day)
        self.room_date_picker_start.place(x=160,y=200,width=100,height=20)

        room_date_picker_end_text = ttk.Label(self.room_page, text='Koniec:')
        room_date_picker_end_text.place(x=300,y=180,width=100,height=20)

        self.room_date_picker_end = DateEntry(self.room_page, width=12, background='darkblue',
                    foreground='white', borderwidth=2, year=today.year, month=today.month, day=today.day)
        self.room_date_picker_end.place(x=300,y=200,width=100,height=20)

        self.room_date_picker_end.bind("<<DateEntrySelected>>", self.get_calculated_price)

        self.room_calculated_price_text_var = tk.StringVar()
        self.room_calculated_price_text_var.set("")
        room_calculated_price_text = tk.Label(self.room_page, textvariable=self.room_calculated_price_text_var, font=self.small_font, wraplength='390p')
        room_calculated_price_text.place(x=180,y=280,width=150,height=20)

        self.room_submit=tk.Button(self.room_page, text="Rezerwuj", command=self.room_submit_command, font=self.normal_font)
        self.room_submit.place(x=250,y=350,width=120,height=20)

        room_hotel=tk.Button(self.room_page, text="Powrot do hotelu", command=self.hotel_command, font=self.normal_font)
        room_hotel.place(x=0,y=50,width=120,height=20)

        room_offers=tk.Button(self.room_page, text="Powrot do ofert", command=self.offers_command, font=self.normal_font)
        room_offers.place(x=0,y=25,width=120,height=20)

        room_menu=tk.Button(self.room_page, text="Powrot do menu", command=self.menu_command, font=self.normal_font)
        room_menu.place(x=0,y=0,width=120,height=20)

        ###############reservations_page###############

        reservations_text = tk.Label(self.reservations_page, text='Moje rezerwacje', font=self.title_font)
        reservations_text.place(x=0,y=0,width=500,height=40)

        reservations_cancel=tk.Button(self.reservations_page, text="Anuluj rezerwacje", command=self.cancel_reservation_command, font=self.normal_font)
        reservations_cancel.place(x=200,y=290,width=140,height=20)

        reservations_cancel=tk.Button(self.reservations_page, text="Zaplac za rezerwacje", command=self.pay_reservation_command, font=self.normal_font)
        reservations_cancel.place(x=200,y=320,width=140,height=20)

        reservations_menu=tk.Button(self.reservations_page, text="Powrot do menu", command=self.menu_command, font=self.normal_font)
        reservations_menu.place(x=0,y=0,width=120,height=20)

        ###############hotel_reservations_page###############

        hotel_reservations_text = tk.Label(self.hotel_reservations_page, text='Rezerwacje', font=self.title_font)
        hotel_reservations_text.place(x=0,y=0,width=500,height=40)

        hotel_reservations_hotelel_text = tk.Label(self.hotel_reservations_page, text='Hotel:', font=self.normal_font)
        hotel_reservations_hotelel_text.place(x=60,y=40,width=80,height=20)

        self.reservations_filtr=tk.Label(self.hotel_reservations_page, text="Filtruj po gosciu", font=self.normal_font)

        self.reservations_change=tk.Button(self.hotel_reservations_page, text="Zmien status rezerwacji", command=self.change_reservation_command, font=self.normal_font)

        hotel_reservations_menu=tk.Button(self.hotel_reservations_page, text="Powrot do menu", command=self.menu_command, font=self.normal_font)
        hotel_reservations_menu.place(x=0,y=0,width=120,height=20)

        ###############user_page###############
        user_text = tk.Label(self.user_page, text='Edytuj dane', font=self.title_font)
        user_text.place(x=0,y=0,width=500,height=40)

        user_info_text = tk.Label(self.user_page, text='Zaznacz, ktore dane chcesz edytowac', font=self.small_font)
        user_info_text.place(x=0,y=40,width=500,height=20)

        self.user_email_var = tk.BooleanVar()
        self.user_email_var_input = tk.Checkbutton(self.user_page, text='E-mail:',variable=self.user_email_var, onvalue=True, offvalue=False, font=self.small_font)
        self.user_email_var_input.place(x=10,y=80,width=200,height=20)
        
        self.user_email_input = tk.Entry(self.user_page, width = 20) 
        self.user_email_input.place(x=210,y=80,width=270,height=20)

        self.user_password_var = tk.BooleanVar()
        self.user_password_var_input = tk.Checkbutton(self.user_page, text='Haslo:',variable=self.user_password_var, onvalue=True, offvalue=False, font=self.small_font)
        self.user_password_var_input.place(x=10,y=110,width=200,height=20)

        self.user_password_input = tk.Entry(self.user_page, width = 20, show="*") 
        self.user_password_input.place(x=210,y=110,width=270,height=20)

        self.user_name_var = tk.BooleanVar()
        self.user_name_var_input = tk.Checkbutton(self.user_page, text='Imie:',variable=self.user_name_var, onvalue=True, offvalue=False, font=self.small_font)
        self.user_name_var_input.place(x=10,y=140,width=200,height=20)

        self.user_name_input = tk.Entry(self.user_page, width = 20) 
        self.user_name_input.place(x=210,y=140,width=270,height=20)

        self.user_surname_var = tk.BooleanVar()
        self.user_surname_var_input = tk.Checkbutton(self.user_page, text='Nazwisko:',variable=self.user_surname_var, onvalue=True, offvalue=False, font=self.small_font)
        self.user_surname_var_input.place(x=10,y=170,width=200,height=20)

        self.user_surname_input = tk.Entry(self.user_page, width = 20) 
        self.user_surname_input.place(x=210,y=170,width=270,height=20)

        self.user_phone_var = tk.BooleanVar()
        self.user_phone_var_input = tk.Checkbutton(self.user_page, text='Telefon:',variable=self.user_phone_var, onvalue=True, offvalue=False, font=self.small_font)

        self.user_phone_input = tk.Entry(self.user_page, width = 20) 

        user_submit=tk.Button(self.user_page, text="Zapisz", command=self.user_submit_command, font=self.normal_font)
        user_submit.place(x=200,y=280,width=100,height=25)

        user_menu=tk.Button(self.user_page, text="Powrot do menu", command=self.menu_command, font=self.normal_font)
        user_menu.place(x=0,y=0,width=120,height=20)

    def get(self, entry):
        """pomocnicza funkcja zwracająca wpisane dane"""
        value = entry.get()
        if len(value)==0 or value.isspace():
            return None
        else:
            return value
  
    def menu_command(self):
        """przejście do MENU, odświeżenie ogólnych statystyk hoteli w bazie"""
        self.hotels_stats = self.database.get_statistics()

        self.hotels_stats_text_var.set("Statystyki:\n Liczba hoteli: {}\tLiczba pokoi:{} \nMinimalna cena za dzien:{}\tMaksymalna cena za dzien: {}".format(
                                        int(self.hotels_stats['liczba_hoteli']), int(self.hotels_stats['liczba_pokoi']), self.hotels_stats['min_cena'], self.hotels_stats['max_cena']))
        self.tabs.select(self.menu_page)

    def offers_command(self):
        """przejście do strony z ofertami hoteli, odświeżenie list z sieciami i hotelami"""
        self.hotel_data = self.database.get_hotels()
        self.hotel_attractions_list_options = self.database.get_attractions()

        self.hotel_var_a = tk.StringVar()
        self.hotel_var_a.set('')

        self.hotel_var_a.trace('w', self.update_hotel_options)

        self.optionmenu_chain = tk.OptionMenu(self.offers_page, self.hotel_var_a, '')

        menu = self.optionmenu_chain['menu']
        menu.delete(0, 'end')

        for chain, hotel in self.hotel_data.items():
            menu.add_command(label=chain, command=lambda var=chain: self.hotel_var_a.set(var))
        
        self.hotel_var_a.set(list(self.hotel_data.keys())[0])

        hotel_attractions_list_scrollbar = tk.Scrollbar(self.offers_page)
        hotel_attractions_list_scrollbar.place(x=410,y=130,width=20,height=100)
        self.hotel_attractions_listbox = tk.Listbox(self.offers_page, selectmode = "multiple")
        hotel_attractions_list_scrollbar.config(command=self.hotel_attractions_listbox.yview)
        self.hotel_attractions_listbox.place(x=160,y=130,width=250,height=100)
        for option in self.hotel_attractions_list_options:
            self.hotel_attractions_listbox.insert(option[0], option[1])
        self.hotel_attractions_listbox.config(bg = "white", yscrollcommand=hotel_attractions_list_scrollbar.set)
        self.hotel_attractions_listbox.bind("<MouseWheel>", lambda event: self.hotel_attractions_listbox.yview_scroll(int(-4*(event.delta/120)), "units"))

        self.hotel_attractions_listbox.bind("<<ListboxSelect>>", self.update_hotels)

        self.optionmenu_chain.place(x=160,y=70,width=270,height=20)

        self.tabs.select(self.offers_page)

    def update_hotels(self, *args):
        """wysłanie do bazy danych potrzebnych do przefiltrowania hoteli w zależności od atrakcji"""
        selection = list(self.hotel_attractions_listbox.curselection())
        if len(selection)>0:
            for i in range(len(selection)):
                selection[i]=selection[i]+1
            selection = tuple(selection)
            self.hotel_data = self.database.get_filtered_hotels(selection)
            if not self.hotel_data:
                messagebox.showinfo(title=None, message="Brak hoteli spelniajacych wymagania")
                self.hotel_attractions_listbox.selection_clear(0, tk.END)
                self.hotel_data = self.database.get_hotels()
        else:
            self.hotel_data = self.database.get_hotels()

        self.hotel_var_a.set(list(self.hotel_data.keys())[0])
        self.update_hotel_options()

    def update_hotel_options(self, *args):
        """dodanie hoteli do opcji w zależności od wybranej sieci"""
        hotels = self.hotel_data[self.hotel_var_a.get()]

        self.hotel_var_b = tk.StringVar()
        self.hotel_var_b.set('')

        self.optionmenu_hotel = tk.OptionMenu(self.offers_page, self.hotel_var_b, '')
        self.optionmenu_hotel.place(x=160,y=100,width=270,height=20)

        menu = self.optionmenu_hotel['menu']
        menu.delete(0, 'end')

        for hotel in hotels:
            menu.add_command(label=hotel['nazwa'], command=lambda var=hotel: self.set_hotel_info(var))

        self.set_hotel_info(hotels[0])

    def set_hotel_info(self, hotel):
        """wyświetlenie informacji o wybranym hotelu"""
        self.hotel_var_b.set(hotel['nazwa'])
        self.chosen_hotel=hotel
        info_text = "Nazwa: {}, \nAdres: {} \nTelefon: {}, \nE-mail: {}, \nKategoria: {}".format(hotel['nazwa'], hotel['adres'], hotel['telefon'], hotel['email'], hotel['kategoria'])
        self.hotel_info_text_var.set(info_text)

    def hotel_command(self):
        """przejście do strony hotelu, odświeżenie statystyk i pokoi danego hotelu"""
        if self.hotel_var_b.get():
            self.hotel_date_picker_start.set_date(datetime.date.today())
            self.hotel_date_picker_end.set_date(datetime.date.today())
            stats = self.database.get_hotel_statistics(self.chosen_hotel['id_hotel'])
            stats_text = "Liczba pokoi: {}\nMinimalna cena: {}\tMaksymalna cena: {}".format(
                        int(stats['liczba_pokoi']), stats['min_cena'], stats['max_cena'])
            info_text = "Nazwa: {}, Kategoria: {}\nAdres: {} \nTelefon: {}, E-mail: {}".format(
                    self.chosen_hotel['nazwa'], self.chosen_hotel['kategoria'], self.chosen_hotel['adres'],
                    self.chosen_hotel['telefon'], self.chosen_hotel['email'])
            text = "{}\nStatystyki: {}".format(info_text, stats_text)
            self.hotel_attractions_text_var.set(text)

            self.hotel_room_data = self.database.get_rooms(self.chosen_hotel['id_hotel'])
            self.room_var = tk.StringVar()
            self.room_var.set('')

            self.optionmenu_room = tk.OptionMenu(self.hotel_page, self.room_var, '')
            self.optionmenu_room.place(x=160,y=140,width=270,height=20)

            menu = self.optionmenu_room['menu']
            menu.delete(0, 'end')

            for nr, room in self.hotel_room_data.items():
                menu.add_command(label=room[0]['numer'], command=lambda var=room: self.set_room(room))

            self.set_room(self.hotel_room_data[list(self.hotel_room_data.keys())[0]])

            self.tabs.select(self.hotel_page)
        else:
            messagebox.showinfo(title=None, message="Wybierz hotel") 
        if self.logged and not self.authorized_hotel and not self.admin_auth:
            self.hotel_room.place(x=320,y=350,width=150,height=20)
        else:
            self.hotel_room.place_forget()

    def filter_rooms(self, *args):
        """wysłanie do bazy opcji, po których filtrowane mają być pokoje oraz ich późniejsze wyświetlanie"""
        id_hotel = self.chosen_hotel['id_hotel']
        data_start = self.hotel_date_picker_start.get_date()
        data_end = self.hotel_date_picker_end.get_date()
        data = {'id_hotel' : id_hotel,
                'data_start' : data_start,
                'data_end' : data_end}

        self.hotel_room_data = self.database.get_filtered_rooms(data)

        menu = self.optionmenu_room['menu']
        menu.delete(0, 'end')

        for k, room in self.hotel_room_data.items():
            menu.add_command(label=k, command=lambda var=room: self.set_room(var))

        self.set_room(self.hotel_room_data[list(self.hotel_room_data.keys())[0]])

    def set_room(self, room):
        """wyświetlenie informacji o wybranym pokoju"""
        self.room_var.set(room[0]['numer'])
        self.chosen_room = room
        room = self.chosen_room[0]
        self.room_availability = self.database.get_room_availability(room['id_pokoj'])
        smoking = "Dla palaczy, " if room['dla_palaczy'] else ""

        info_text = "Nazwa i opis typu pokoju: {} \n {}, \n {} Typ wezla higieniczno-sanitarnego: {}, \nPietro: {}, liczba miejsc: {} \n {}".format(room['nazwa'], room['opis_typu'], smoking, room['typ_wezlu_higsan'], room['pietro'], int(room['liczba_miejsc']), room['opis_pokoju'])
        self.room_equipment_text_var.set(info_text)

        prices_text=""
        n=0
        for data in self.chosen_room:
            if n<3:
                prices_text += "Cena: {}, okres:{} - {}, \n".format(data['cena'], data['okres_poczatek'], data['okres_koniec'])
                n+=1
        
        self.room_equipment_price_attractions_text_area = st.ScrolledText(self.hotel_page, width = 100, height = 10, font=self.small_font) 
        self.room_equipment_price_attractions_text_area.place(x=5,y=260,width=250,height=50)
        self.room_equipment_price_attractions_text_area.insert('0.0', prices_text)
        self.room_equipment_price_attractions_text_area.configure(state='disabled')
        self.room_price_text_var.set(prices_text)

    def room_availability_command(self):
        """wyświetlenie kalendarza z dostępnością danego pokoju"""
        if self.chosen_room:
            top = tk.Toplevel(self.root)
            cal = Calendar(top, selectmode='none')
            data = self.room_availability
            for date in data:
                start = date['data_poczatku']
                end = date['data_konca']
                n = (end-start).days
                for i in range(n):
                    cal.calevent_create(start + cal.timedelta(days=i), 'Zarezerwowany', 'reminder')

            cal.tag_config('reminder', background='red', foreground='yellow')
            cal.pack(fill="both", expand=True)
        else:
            messagebox.showinfo(title=None, message="Wybierz pokoj")

    def room_price_command(self):
        """pomocnicza funkcja do wyświetlania cen danego pokoju"""
        if self.chosen_room:
            prices_text =""
            for price in self.chosen_room:
                prices_text += "Cena: {}, okres:{} - {}, \n".format(price['cena'], price['okres_poczatek'], price['okres_koniec'])
            self.room_equipment_price_attractions_text_area.configure(state='normal')
            self.room_equipment_price_attractions_text_area.delete('0.0', 'end')
            self.room_equipment_price_attractions_text_area.insert('0.0', prices_text)
            self.room_equipment_price_attractions_text_area.configure(state='disabled')
        else:
            messagebox.showinfo(title=None, message="Wybierz pokoj")
    
    def hotel_attractions_command(self):
        """pomocnicza funkcja do wyświetlania atrakcji danego hotelu"""
        if self.chosen_hotel:
            attractions = self.database.get_hotel_attractions(self.chosen_hotel['id_hotel'])
            attractions_text = ''
            for attraction in attractions:
                attractions_text += "{}: cena za godzine: {}\notwarcie: {}, zamkniecie: {}\n\n".format(attraction[0], attraction[3], attraction[1].strftime("%H:%M"), attraction[2].strftime("%H:%M"))

            self.room_equipment_price_attractions_text_area.configure(state='normal')
            self.room_equipment_price_attractions_text_area.delete('0.0', 'end')
            self.room_equipment_price_attractions_text_area.insert('0.0', attractions_text)
            self.room_equipment_price_attractions_text_area.configure(state='disabled')
        else:
            messagebox.showinfo(title=None, message="Wybierz hotel")

    def room_equipment_command(self):
        """pomocnicza funkcja do wyświetlania wyposażenia danego pokoju"""
        if self.chosen_room:
            equipments = self.database.get_room_equipments(self.chosen_room[0]['id_pokoj'])
            equipments_text = ""
            for equipment in equipments:
                equipments_text += equipment['opis']+" : "+str(int(equipment['ilosc']))+"szt.\n"
            self.room_equipment_price_attractions_text_area.configure(state='normal')
            self.room_equipment_price_attractions_text_area.delete('0.0', 'end')
            self.room_equipment_price_attractions_text_area.insert('0.0', equipments_text)
            self.room_equipment_price_attractions_text_area.configure(state='disabled')
        else:
            messagebox.showinfo(title=None, message="Wybierz pokoj")

    def room_command(self):
        """przejście do strony rezerwacji pokoju"""
        self.room_date_picker_start.set_date(datetime.date.today())
        self.room_date_picker_end.set_date(datetime.date.today())

        self.tabs.select(self.room_page)

    def get_calculated_price(self, *args):
        """wysłanie do bazy danych potrzebnych do obliczenia ceny za pobyt i wyświetlenie jej"""
        price = "Kwota za pobyt: "
        data_poczatku = self.room_date_picker_start.get_date().strftime("%Y-%m-%d")
        data_konca = self.room_date_picker_end.get_date().strftime("%Y-%m-%d")
        id_pokoj = self.chosen_room[0]['id_pokoj']
        data = {'id_pokoj' : id_pokoj,
                'data_poczatku' : data_poczatku,
                'data_konca' : data_konca}
        self.calculated_price_val = self.database.get_calculated_price(data)
        price += str(self.calculated_price_val)
        self.room_calculated_price_text_var.set(price)

    def room_submit_command(self):
        """wysłanie do bazy danych z formularza rezerwacji pokoju"""
        id_gosc = self.id_user
        id_pokoj = self.chosen_room[0]['id_pokoj']
        data_poczatku = self.room_date_picker_start.get_date().strftime("%Y-%m-%d")
        data_konca = self.room_date_picker_end.get_date().strftime("%Y-%m-%d")
        data = {'id_gosc' : id_gosc,
                'id_pokoj' : id_pokoj,
                'data_poczatku' : data_poczatku,
                'data_konca' : data_konca}
        result = self.database.add_guest_reservation(data)
        if result[0]:
            self.room_date_picker_start.set_date(datetime.date.today())
            self.room_date_picker_end.set_date(datetime.date.today())
            self.menu_command()
        messagebox.showinfo(title=None, message=result[1]) 
    
    def register_command(self):
        """przejście do rejestracji gościa"""
        self.tabs.select(self.register_page)
    
    def register_submit_command(self):
        """wysłanie do bazy danych z rejestracji gościa"""
        email = self.get(self.register_email_input)
        haslo = self.get(self.register_password_input)
        imie = self.get(self.register_name_input)
        nazwisko = self.get(self.register_surname_input)
        telefon = self.get(self.register_phone_input)
        data = {'email' : email,
                'haslo' : haslo,
                'imie' : imie,
                'nazwisko' : nazwisko,
                'telefon' : telefon}
        result = self.database.add_guest(data)
        if result[0]:
            self.register_email_input.delete(0,'end')
            self.register_password_input.delete(0,'end')
            self.register_name_input.delete(0,'end')
            self.register_surname_input.delete(0,'end')
            self.register_phone_input.delete(0,'end')
            self.login_command()
        messagebox.showinfo(title=None, message=result[1]) 

    def login_command(self):
        """przejście do logowania"""
        self.tabs.select(self.login_page)
    
    def login_submit_command(self):
        """wysłanie do bazy danych z logowania i w razie pomyślnego zalogowania ustawienie danych do późniejszej identyfikacji"""
        email = self.get(self.login_email_input)
        haslo = self.get(self.login_password_input)
        if email=='admin' and haslo=='admin':
            self.logged = True
            self.admin_auth = True
            self.login_email_input.delete(0,'end')
            self.login_password_input.delete(0,'end')
            self.menu_command()
            message = "Pomyslnie zalogowano admina"
        else:
            data = {'email' : email,
                    'haslo' : haslo}
            result = self.database.login_user(data)
            if result[0]:
                self.logged = True
                message = "Pomyslnie zalogowano"
                if result[1]:
                    message += " pracownika"
                    self.authorized_hotel = result[2]
                    self.id_user = result[3]
                else:
                    self.id_user = result[2]
                self.login_email_input.delete(0,'end')
                self.login_password_input.delete(0,'end')
                self.menu_command()
            else:
                message = "Bledne dane"
        if self.logged:
            self.logout.place(x=150,y=190,width=200,height=25)
            if not self.admin_auth:
                self.user.place(x=150,y=250,width=200,height=25)
            self.login.place_forget()
            self.register.place_forget()
            if self.admin_auth or self.authorized_hotel is not None:
                self.adding.place(x=150,y=160,width=200,height=25)
                self.hotel_reservations.place(x=150,y=220,width=200,height=25)
            else:
                self.reservations.place(x=150,y=160,width=200,height=25)
        messagebox.showinfo(title=None, message=message) 

    def logout_command(self):
        """wylogowanie użytkownika i usunięcie z pamięci danych identyfikujących go"""
        self.logged = False
        self.admin_auth = False
        self.authorized_hotel = None
        self.id_user = None
        self.logout.place_forget()
        self.adding.place_forget()
        self.user.place_forget()
        self.hotel_reservations.place_forget()
        self.reservations.place_forget()
        self.login.place(x=150,y=160,width=200,height=25)
        self.register.place(x=150,y=190,width=200,height=25)
        self.database.logout()

    def user_command(self):
        """przejście do strony edycji danych użytkownika, odczyt danych z bazy w zależności od typu użytkownika (gość/pracownik)"""
        if self.authorized_hotel:
            data = self.database.get_employee(self.id_user)
            self.user_email_var_input.config(text='Email: {}'.format(data['email']))
            self.user_name_var_input.config(text='Imie: {}'.format(data['imie']))
            self.user_surname_var_input.config(text='Nazwisko: {}'.format(data['nazwisko']))
            self.user_phone_var_input.place_forget()
            self.user_phone_input.place_forget()
        else:
            data = self.database.get_guest(self.id_user)
            self.user_email_var_input.config(text='Email: {}'.format(data['email']))
            self.user_name_var_input.config(text='Imie: {}'.format(data['imie']))
            self.user_surname_var_input.config(text='Nazwisko: {}'.format(data['nazwisko']))
            self.user_phone_var_input.config(text='Telefon: {}'.format(data['telefon']))
            self.user_phone_var_input.place(x=10,y=200,width=200,height=20)
            self.user_phone_input.place(x=210,y=200,width=270,height=20)
        self.tabs.select(self.user_page)
    
    def user_submit_command(self):
        """wysłanie do bazy danych z edycji użytkownika"""
        email = haslo = imie = nazwisko = telefon = None
        if self.user_email_var.get():
            email = self.get(self.user_email_input)
        if self.user_password_var.get():
            haslo = self.get(self.user_password_input)
        if self.user_name_var.get():
            imie = self.get(self.user_name_input)
        if self.user_surname_var.get():
            nazwisko = self.get(self.user_surname_input)
        if self.user_phone_var.get():
            telefon = self.get(self.user_phone_input)
        data = {'email' : email,
                'haslo' : haslo,
                'imie' : imie,
                'nazwisko' : nazwisko,
                'telefon' : telefon}
        if self.authorized_hotel:
            result = self.database.update_employee(data, self.id_user)
        else:
            result = self.database.update_guest(data, self.id_user)
        if result[0]:
            self.menu_command()
            self.user_email_var.set(False)
            self.user_password_var.set(False)
            self.user_name_var.set(False)
            self.user_surname_var.set(False)
            self.user_phone_var.set(False)

            self.user_email_input.delete(0,'end')
            self.user_password_input.delete(0,'end')
            self.user_name_input.delete(0,'end')
            self.user_surname_input.delete(0,'end')
            self.user_phone_input.delete(0,'end')

        messagebox.showinfo(title=None, message=result[1]) 
    
    def reservations_command(self):
        """przejście do rezerwacji gościa, odświeżenie listy rezerwacji"""
        self.user_reservation_list=self.database.get_guest_reservations(self.id_user)

        if self.user_reservation_list:
            reservation_list_scrollbary = tk.Scrollbar(self.reservations_page)
            reservation_list_scrollbary.place(x=470,y=80,width=20,height=180)
            
            reservation_list_scrollbarx = tk.Scrollbar(self.reservations_page, orient=tk.HORIZONTAL)
            reservation_list_scrollbarx.place(x=5,y=260,width=465,height=20)

            self.reservation_list_listbox = tk.Listbox(self.reservations_page)
            reservation_list_scrollbarx.config(command=self.reservation_list_listbox.xview)
            reservation_list_scrollbary.config(command=self.reservation_list_listbox.yview)
            self.reservation_list_listbox.place(x=5,y=80,width=465,height=180)
            for k, v in self.user_reservation_list.items():
                text = "Data rezerwacji: {},\n Termin rezerwacji: {} do {}, \nStatus: {}".format(v['data_rezerwacji'],v['data_poczatku'],v['data_konca'], v['opis'])
                self.reservation_list_listbox.insert(k, text)
            self.reservation_list_listbox.config(bg = "white", yscrollcommand=reservation_list_scrollbary.set, xscrollcommand=reservation_list_scrollbarx.set)
            self.reservation_list_listbox.bind("<MouseWheel>", lambda event: self.reservation_list_listbox.yview_scroll(int(-4*(event.delta/120)), "units"))
        
        self.tabs.select(self.reservations_page)

    def cancel_reservation_command(self):
        """wysłanie do bazy anulowania danej rezerwacji przez użytkownika"""
        selection = self.reservation_list_listbox.curselection()
        if selection:
            status = self.user_reservation_list[list(self.user_reservation_list.keys())[selection[0]]]['opis']
            if status != 'Anulowana':
                reservation = list(self.user_reservation_list.keys())[selection[0]]
                result = messagebox.askyesno(title=None, message="Jestes pewny?")
                if result:
                    message = self.database.cancel_guest_reservation(reservation)
                    messagebox.showinfo(title=None, message=message[1])
            else:
                messagebox.showinfo(title=None, message="Ta rezerwacja jest juz anulowana")
        else:
            messagebox.showinfo(title=None, message="Brak zaznaczonej rezerwacji")
    
    def pay_reservation_command(self):
        """wysłanie do bazy informacji o zapłaceniu danej rezerwacji przez użytkownika"""
        selection = self.reservation_list_listbox.curselection()
        if selection:
            status = self.user_reservation_list[list(self.user_reservation_list.keys())[selection[0]]]['opis']
            if status == 'Oczekuje na wpłatę':
                reservation = list(self.user_reservation_list.keys())[selection[0]]
                result = messagebox.askyesno(title=None, message="Zaplacone?")
                if result:
                    message = self.database.pay_guest_reservation(reservation)
                    messagebox.showinfo(title=None, message=message[1])
            else:
                messagebox.showinfo(title=None, message="Nie mozna juz zaplacic za te rezerwacje")
        else:
            messagebox.showinfo(title=None, message="Brak zaznaczonej rezerwacji")

    def hotel_reservations_command(self):
        """przejście do strony z rezerwacjami dla danego hotelu, odczyt możliwych hoteli z bazy"""
        self.hotel_data = self.database.get_hotels()

        self.hotel_reservations_hotel_var = tk.StringVar()
        self.hotel_reservations_hotel_var.set('')

        self.optionmenu_hotel_reservations_hotel = tk.OptionMenu(self.hotel_reservations_page, self.hotel_reservations_hotel_var, '')
        self.optionmenu_hotel_reservations_hotel.place(x=160,y=40,width=270,height=20)

        menu = self.optionmenu_hotel_reservations_hotel['menu']
        menu.delete(0, 'end')

        auth_hotel = None

        for k, hotel in self.hotel_data.items():
            for h in hotel:
                text = k+" "+h['nazwa']
                menu.add_command(label=text, command=lambda var=h: self.set_hotel_r(var))
                if self.authorized_hotel and h['id_hotel']==self.authorized_hotel:
                    auth_hotel = h

        if self.authorized_hotel:
            self.set_hotel_r(auth_hotel)
            self.optionmenu_hotel_reservations_hotel.configure(state="disabled")
        else:
            self.set_hotel_r(self.hotel_data[list(self.hotel_data.keys())[0]][0])   

        self.tabs.select(self.hotel_reservations_page)
    
    def set_hotel_r(self, hotel):
        """pomocnicza funkcja wyświetlająca rezerwacje dla wybranego hotelu"""
        self.hotel_reservations_hotel_var.set(hotel['nazwa'])
        self.chosen_hotel=hotel

        self.hotel_reservation_list=self.database.get_hotel_reservations(self.chosen_hotel['id_hotel'])

        if self.hotel_reservation_list:
            hotel_reservation_list_scrollbary = tk.Scrollbar(self.hotel_reservations_page)
            hotel_reservation_list_scrollbary.place(x=470,y=80,width=20,height=180)

            hotel_reservation_list_scrollbarx = tk.Scrollbar(self.hotel_reservations_page, orient=tk.HORIZONTAL)
            hotel_reservation_list_scrollbarx.place(x=5,y=260,width=465,height=20)

            self.hotel_reservation_list_listbox = tk.Listbox(self.hotel_reservations_page)

            hotel_reservation_list_scrollbary.config(command=self.hotel_reservation_list_listbox.yview)
            hotel_reservation_list_scrollbarx.config(command=self.hotel_reservation_list_listbox.xview)

            self.hotel_reservation_list_listbox.place(x=5,y=80,width=465,height=180)
            for k, v in self.hotel_reservation_list.items():
                text = "Email: {}, Data rezerwacji: {},\n Termin rezerwacji: {}-{}, \nStatus: {}".format(v['email'], v['data_rezerwacji'],v['data_poczatku'],v['data_konca'], v['opis'])
                self.hotel_reservation_list_listbox.insert(k, text)
            self.hotel_reservation_list_listbox.config(bg = "white", yscrollcommand=hotel_reservation_list_scrollbary.set, xscrollcommand=hotel_reservation_list_scrollbarx.set)
            self.hotel_reservation_list_listbox.bind("<MouseWheel>", lambda event: self.hotel_reservation_list_listbox.yview_scroll(int(-4*(event.delta/120)), "units"))

        self.reservations_filtr.place(x=0,y=280,width=140,height=20)
        reservations_email_text = tk.Label(self.hotel_reservations_page, text='E-mail:', font=self.normal_font)
        reservations_email_text.place(x=10,y=300,width=50,height=20)

        self.reservations_email_input = tk.Entry(self.hotel_reservations_page, width = 20) 
        self.reservations_email_input.place(x=60,y=300,width=150,height=20)

        self.reservations_filtr_button=tk.Button(self.hotel_reservations_page, text="Filtruj", command=self.filter_reservation_command, font=self.normal_font)
        self.reservations_filtr_button.place(x=60,y=330,width=80,height=20)

        self.reservations_change.place(x=300,y=300,width=140,height=20)
    
    def filter_reservation_command(self):
        """wysłanie do bazy opcji, po których filtrowane mają być rezerwacje i ich wyświetlenie"""
        email = self.get(self.reservations_email_input)
        if email:
            self.hotel_reservation_list=self.database.get_filtered_hotel_reservations(self.chosen_hotel['id_hotel'], email)
            if not self.hotel_reservation_list:
                messagebox.showinfo(title=None, message="Brak rezerwacji spelniajacych wymagania")
            else:
                self.hotel_reservation_list_listbox.delete(0, 'end')
                for k, v in self.hotel_reservation_list.items():
                    text = "Email: {}, Data rezerwacji: {},\n Termin rezerwacji: {}-{}, \nStatus: {}".format(v['email'], v['data_rezerwacji'],v['data_poczatku'],v['data_konca'], v['opis'])
                    self.hotel_reservation_list_listbox.insert(k, text)
                self.reservations_email_input.delete(0,'end')
        else:
            messagebox.showinfo(title=None, message="Brak emaila")

    def change_reservation_command(self):
        """wyświetlenie rodzaji statusów, na które pracownik może zmienić rezerwację"""
        selection = self.hotel_reservation_list_listbox.curselection()
        if selection:
            reservation = list(self.hotel_reservation_list.keys())[selection[0]]
            status_list = self.database.get_status()

            self.hotel_reservation_res_var = tk.StringVar()
            self.hotel_reservation_res_var.set('')

            self.optionmenu_hotel_reservation_res = tk.OptionMenu(self.hotel_reservations_page, self.hotel_reservation_res_var, '')
            self.optionmenu_hotel_reservation_res.place(x=230,y=330,width=260,height=20)

            menu = self.optionmenu_hotel_reservation_res['menu']
            menu.delete(0, 'end')

            for st in status_list:
                menu.add_command(label=st[1], command=lambda var=st: self.set_stat(var))

            self.reservations_change_ok=tk.Button(self.hotel_reservations_page, text="Potwierdz", command=self.change_reservation_submit_command, font=self.normal_font)
            self.reservations_change_ok.place(x=300,y=360,width=140,height=20)

        else:
            messagebox.showinfo(title=None, message="Brak zaznaczonej rezerwacji")
    
    def set_stat(self, stat):
        """pomocnicza funkcja wyświetlająca zaznaczony status i zapamiętanie jej w pamięci"""
        self.chosen_stat = stat
        self.hotel_reservation_res_var.set(stat[1])
    
    def change_reservation_submit_command(self):
        """wysłanie do bazy zmianu statusu danej rezerwacji przez pracownika"""
        selection = self.hotel_reservation_list_listbox.curselection()
        id_rezerwacja = list(self.hotel_reservation_list.keys())[selection[0]]
        id_status = self.chosen_stat[0]
        data = {'id_rezerwacja' : id_rezerwacja,
                'id_status' : id_status}
        result = self.database.change_guest_reservation(data)
        if result[0]:
            self.reservations_change_ok.place_forget()
        messagebox.showinfo(title=None, message=result[1]) 

    def adding_command(self):
        """przejście do menu dodawania, dodatkowe opcje dla admina"""
        self.adding_chain.place_forget()
        self.adding_hotel.place_forget()

        if self.admin_auth:
            self.adding_chain.place(x=100,y=50,width=300,height=25)
            self.adding_hotel.place(x=100,y=80,width=300,height=25)
        
        self.tabs.select(self.adding_page)
    
    def adding_chain_command(self):
        """przejście do formularza z dodawaniem sieci"""
        self.tabs.select(self.adding_chain_page)

    def adding_chain_submit_command(self):
        """wysłanie do bazy danych z formularza dodawania sieci"""
        nazwa = self.get(self.adding_chain_name_input)
        data = {'nazwa' : nazwa}
        result = self.database.add_chain(data)
        if result[0]:
            self.adding_chain_name_input.delete(0,'end')
            self.adding_command()
        messagebox.showinfo(title=None, message=result[1])

    def adding_hotel_command(self):
        """przejście do formularza dodawania hotelu, odświeżenie możliwych sieci"""
        self.chain_data = self.database.get_chains()
        self.chain_var = tk.StringVar()
        self.chain_var.set('')

        self.optionmenu_adding_hotel = tk.OptionMenu(self.adding_hotel_page, self.chain_var, '')
        self.optionmenu_adding_hotel.place(x=160,y=70,width=270,height=20)

        menu = self.optionmenu_adding_hotel['menu']
        menu.delete(0, 'end')

        for k, chain in self.chain_data.items():
            menu.add_command(label=chain['nazwa'], command=lambda var=chain, index=k: self.set_chain((index,var)))

        ind = list(self.chain_data.keys())[0]
        var = self.chain_data[ind]
        self.set_chain((ind, var))

        self.tabs.select(self.adding_hotel_page)

    def set_chain(self, chain):
        """pomocnicza funkcja wyświetlająca wybraną sieć i zapisująca ją do pamięci"""
        self.chain_var.set(chain[1]['nazwa'])
        self.chosen_chain = chain

    def adding_hotel_submit_command(self):
        """wysłanie do bazy danych z formularza dodawania hotelu"""
        id_siec = self.chosen_chain[0]
        nazwa = self.get(self.adding_hotel_name_input)
        adres = self.get(self.adding_hotel_address_input)
        email = self.get(self.adding_hotel_email_input)
        telefon = self.get(self.adding_hotel_phone_input)
        kategoria = self.hotel_category_var.get()
        data = {'id_siec' : id_siec,
                'nazwa' : nazwa,
                'telefon' : telefon,
                'email' : email,
                'kategoria' : kategoria,
                'adres' : adres}
        result = self.database.add_hotel(data)
        if result[0]:
            self.adding_hotel_name_input.delete(0,'end')
            self.adding_hotel_address_input.delete(0,'end')
            self.adding_hotel_email_input.delete(0,'end')
            self.adding_hotel_phone_input.delete(0,'end')
            self.adding_command()
        messagebox.showinfo(title=None, message=result[1])

    def adding_attraction_command(self):
        """przejście do formularza z dodawaniem atrakcji"""
        self.tabs.select(self.adding_attraction_page)
        
    def adding_attraction_submit_command(self):
        """wysłanie do bazy danych z formularza dodawania atrakcji"""
        opis = self.get(self.adding_attraction_description_input)
        data = {'opis' : opis}
        result = self.database.add_attraction(data)
        if result[0]:
            self.adding_attraction_description_input.delete(0,'end')
            self.adding_command()
        messagebox.showinfo(title=None, message=result[1])

    def adding_equipment_command(self):
        """przejście do formularza dodawania wyposażenia"""
        self.tabs.select(self.adding_equipment_page)

    def adding_equipment_submit_command(self):
        """wysłanie do bazy danych z formularza dodawania wyposażenia"""
        opis = self.get(self.adding_equipment_description_input)
        data = {'opis' : opis}
        result = self.database.add_equipment(data)
        if result[0]:
            self.adding_equipment_description_input.delete(0,'end')
            self.adding_command()
        messagebox.showinfo(title=None, message=result[1])

    def adding_room_command(self):
        """przejście do formularza dodawania pokoju, odświeżenie listy z typami pokojów"""
        self.adding_room_hotel_var = tk.StringVar()
        self.adding_room_hotel_var.set('')

        self.hotel_data = self.database.get_hotels()

        self.optionmenu_adding_room_hotel = tk.OptionMenu(self.adding_room_page, self.adding_room_hotel_var, '')
        self.optionmenu_adding_room_hotel.place(x=160,y=70,width=270,height=20)

        menu = self.optionmenu_adding_room_hotel['menu']
        menu.delete(0, 'end')

        auth_hot = None

        for k, hotel in self.hotel_data.items():
            for h in hotel:
                text = k+" "+h['nazwa']
                menu.add_command(label=text, command=lambda var=h: self.set_hotel_ar(var))
                if self.authorized_hotel and h['id_hotel']==self.authorized_hotel:
                    auth_hot = h

        if self.authorized_hotel:
            self.set_hotel_ar(auth_hot)
            self.optionmenu_adding_room_hotel.configure(state="disabled")
        else:
            self.set_hotel_ar(self.hotel_data[list(self.hotel_data.keys())[0]][0])   

        self.tabs.select(self.adding_room_page)
    
    def set_hotel_ar(self, hotel):
        """funkcja pomocnicza ustawiająca wybrany hotel i zapisująca go w pamięci, a także wyświetlająca typy pokoi z danego hotelu do wyboru"""
        self.adding_room_hotel_var.set(hotel['nazwa'])
        self.chosen_hotel=hotel

        self.type_data = self.database.get_types(self.chosen_hotel['id_hotel'])

        self.adding_room_type_var = tk.StringVar()
        self.adding_room_type_var.set('')

        self.optionmenu_adding_room_type = tk.OptionMenu(self.adding_room_page, self.adding_room_type_var, '')
        self.optionmenu_adding_room_type.place(x=160,y=100,width=270,height=20)

        menu = self.optionmenu_adding_room_type['menu']
        menu.delete(0, 'end')

        for k, rtype in self.type_data.items():
           menu.add_command(label=rtype['nazwa'], command=lambda var=rtype: self.set_type(var, self.adding_room_type_var))

        self.set_type(self.type_data[list(self.type_data.keys())[0]], self.adding_room_type_var)

    def set_type(self, rtype, var):
        """funkcja pomocnicza ustawiająca wybrany typ pokoju i zapisująca go w pamięci"""
        self.chosen_type = rtype
        var.set(rtype['nazwa'])

    def adding_room_submit_command(self):
        """wysłanie do bazy danych z formularza dodawania pokoju"""
        id_typ = self.chosen_type['id_typ']
        pietro = self.get(self.adding_room_level_input)
        numer = self.get(self.adding_room_number_input)
        liczba_miejsc = self.get(self.adding_room_capacity_input)
        opis = self.get(self.adding_room_description_input)
        data = {'id_typ' : id_typ,
                'pietro' : pietro,
                'numer' : numer,
                'liczba_miejsc' : liczba_miejsc,
                'opis': opis}
        result = self.database.add_room(data)
        if result[0]:
            self.adding_room_level_input.delete(0,'end')
            self.adding_room_number_input.delete(0,'end')
            self.adding_room_capacity_input.delete(0,'end')
            self.adding_room_description_input.delete(0,'end')
            self.menu_command()
        messagebox.showinfo(title=None, message=result[1]) 

    def adding_attraction_to_hotel_command(self):
        """przejście do formularza z dodawaniem atrakcji do hotelu, odświeżenie wyboru hoteli i atrakcji"""
        self.hotel_data = self.database.get_hotels()
        self.attractions_data = self.database.get_attractions()

        self.adding_attraction_to_hotel_hotel_var = tk.StringVar()
        self.adding_attraction_to_hotel_hotel_var.set('')

        self.optionmenu_adding_attraction_to_hotel_hotel = tk.OptionMenu(self.adding_attraction_to_hotel_page, self.adding_attraction_to_hotel_hotel_var, '')
        self.optionmenu_adding_attraction_to_hotel_hotel.place(x=160,y=100,width=270,height=20)

        menu = self.optionmenu_adding_attraction_to_hotel_hotel['menu']
        menu.delete(0, 'end')

        auth_hotel = None

        for k, hotel in self.hotel_data.items():
            for h in hotel:
                text = k+" "+h['nazwa']
                menu.add_command(label=text, command=lambda var=h: self.set_hotel(var, self.adding_attraction_to_hotel_hotel_var))
                if self.authorized_hotel and h['id_hotel']==self.authorized_hotel:
                    auth_hotel = h

        if self.authorized_hotel:
            self.set_hotel(auth_hotel, self.adding_attraction_to_hotel_hotel_var)
            self.optionmenu_adding_attraction_to_hotel_hotel.configure(state="disabled")
        else:
            self.set_hotel(self.hotel_data[list(self.hotel_data.keys())[0]][0], self.adding_attraction_to_hotel_hotel_var)   

        self.adding_attraction_to_hotel_attr_var = tk.StringVar()
        self.adding_attraction_to_hotel_attr_var.set('')

        self.optionmenu_adding_attraction_to_hotel_attraction = tk.OptionMenu(self.adding_attraction_to_hotel_page, self.adding_attraction_to_hotel_attr_var, '')
        self.optionmenu_adding_attraction_to_hotel_attraction.place(x=160,y=130,width=270,height=20)

        menu = self.optionmenu_adding_attraction_to_hotel_attraction['menu']
        menu.delete(0, 'end')

        for attraction in self.attractions_data:
            menu.add_command(label=attraction[1], command=lambda var=attraction: self.set_attraction(var))

        self.set_attraction(self.attractions_data[0])
  
        self.tabs.select(self.adding_attraction_to_hotel_page)
    
    def set_hotel(self, hotel, var):
        """funkcja pomocnicza ustawiająca wybrany hotel i zapisująca go w pamięci"""
        var.set(hotel['nazwa'])
        self.chosen_hotel=hotel

    def set_attraction(self, attraction):
        """pomocnicza funkcja wyświetlająca wybraną atrakcję i zapisująca ją w pamięci"""
        self.chosen_attraction = attraction
        self.adding_attraction_to_hotel_attr_var.set(attraction[1])
    
    def adding_attraction_to_hotel_submit_command(self):
        """wysłanie do bazy danych z formularza dodawania atrakcji do hotelu"""
        id_hotel = self.chosen_hotel['id_hotel']
        id_atrakcje = self.chosen_attraction[0]
        try:
            otwarcie = self.get(self.adding_attraction_to_hotel_start_input)
            zamkniecie = self.get(self.adding_attraction_to_hotel_end_input)
            if(otwarcie):
                otwarcie = datetime.datetime.strptime(otwarcie, "%H:%M")
            if(zamkniecie):
                zamkniecie = datetime.datetime.strptime(zamkniecie, "%H:%M")
            cena_godzina = self.get(self.adding_attraction_price_input)
            data = {'id_hotel' : id_hotel,
                    'id_atrakcje' : id_atrakcje,
                    'otwarcie' : otwarcie,
                    'zamkniecie' : zamkniecie,
                    'cena_godzina' : cena_godzina}
            result = self.database.add_attraction_to_hotel(data)
            if result[0]:
                self.adding_attraction_to_hotel_start_input.delete(0,'end')
                self.adding_attraction_to_hotel_end_input.delete(0,'end')
                self.adding_command()
            messagebox.showinfo(title=None, message=result[1])
        except ValueError as e:
            messagebox.showinfo(title=None, message="Niepoprawne godziny")
    
    def adding_equipment_to_type_command(self):
        """przejście do formularza dodawania wyposażenia do typu, odświeżenie list typów i wyposażeń"""
        self.adding_equipment_to_type_hotel_var = tk.StringVar()
        self.adding_equipment_to_type_hotel_var.set('')

        self.hotel_data = self.database.get_hotels()

        self.optionmenu_adding_equipment_to_type_hotel = tk.OptionMenu(self.adding_equipment_to_type_page, self.adding_equipment_to_type_hotel_var, '')
        self.optionmenu_adding_equipment_to_type_hotel.place(x=160,y=100,width=270,height=20)

        menu = self.optionmenu_adding_equipment_to_type_hotel['menu']
        menu.delete(0, 'end')

        auth_hot = None

        for k, hotel in self.hotel_data.items():
            for h in hotel:
                text = k+" "+h['nazwa']
                menu.add_command(label=text, command=lambda var=h: self.set_hotel_et(var))
                if self.authorized_hotel and h['id_hotel']==self.authorized_hotel:
                    auth_hot = h

        if self.authorized_hotel:
            self.set_hotel_et(auth_hot)
            self.optionmenu_adding_equipment_to_type_hotel.configure(state="disabled")
        else:
            self.set_hotel_et(self.hotel_data[list(self.hotel_data.keys())[0]][0])   

        self.tabs.select(self.adding_equipment_to_type_page)

    def set_hotel_et(self, hotel):
        """pomocnicza funkcja wyświetlająca typy pokojów w zależności od wybranego hotelu oraz odświeżająca liste atrakcji"""    
        self.chosen_hotel = hotel
        self.adding_equipment_to_type_hotel_var.set(self.chosen_hotel['nazwa'])
        self.type_data = self.database.get_types(self.chosen_hotel['id_hotel'])
        self.equipment_data = self.database.get_equipments()

        self.adding_equipment_to_type_equipment_var = tk.StringVar()
        self.adding_equipment_to_type_equipment_var.set('')

        self.optionmenu_adding_equipment_to_type_equipment = tk.OptionMenu(self.adding_equipment_to_type_page, self.adding_equipment_to_type_equipment_var, '')
        self.optionmenu_adding_equipment_to_type_equipment.place(x=160,y=130,width=270,height=20)

        menu = self.optionmenu_adding_equipment_to_type_equipment['menu']
        menu.delete(0, 'end')

        for equipment in self.equipment_data:
            menu.add_command(label=equipment[1], command=lambda var=equipment: self.set_equipment(equipment))

        self.set_equipment(self.equipment_data[0]) 

        self.adding_equipment_to_type_type_var = tk.StringVar()
        self.adding_equipment_to_type_type_var.set('')

        self.optionmenu_adding_equipment_to_type_type = tk.OptionMenu(self.adding_equipment_to_type_page, self.adding_equipment_to_type_type_var, '')
        self.optionmenu_adding_equipment_to_type_type.place(x=160,y=160,width=270,height=20)

        menu = self.optionmenu_adding_equipment_to_type_type['menu']
        menu.delete(0, 'end')

        for k, rtype in self.type_data.items():
           menu.add_command(label=rtype['nazwa'], command=lambda var=rtype: self.set_type(var, self.adding_equipment_to_type_type_var))
        
        self.set_type(self.type_data[list(self.type_data.keys())[0]], self.adding_equipment_to_type_type_var)
        
        self.tabs.select(self.adding_equipment_to_type_page)
    
    def set_equipment(self, equipment):
        """pomocnicza funkcja wyświetlająca wybrane wyposażenie i zapisujące je do pamięci"""
        self.chosen_equipment = equipment
        self.adding_equipment_to_type_equipment_var.set(equipment[1])
    
    def adding_equipment_to_type_submit_command(self):
        """wysłanie do bazy danych z formularza dodawania wyposażenia do typu pokoju"""
        id_wyposazenie = self.chosen_equipment[0]
        id_typ = self.chosen_type['id_typ']
        ilosc = self.get(self.adding_equipment_to_type_quantity_input)
        data = {'id_wyposazenie' : id_wyposazenie,
                'id_typ' : id_typ,
                'ilosc' : ilosc}
        result = self.database.add_equipment_to_type(data)
        if result[0]:
            self.adding_equipment_to_type_quantity_input.delete(0,'end')
            self.adding_command()
        messagebox.showinfo(title=None, message=result[1])

    def adding_price_to_type_command(self):
        """przejście do formularza z dodawaniem prices_text do typu pokoju, odświeżenie listy typów"""
        self.adding_price_to_type_hotel_var = tk.StringVar()
        self.adding_price_to_type_hotel_var.set('')

        self.hotel_data = self.database.get_hotels()

        self.optionmenu_adding_price_to_type_hotel = tk.OptionMenu(self.adding_price_to_type_page, self.adding_price_to_type_hotel_var, '')
        self.optionmenu_adding_price_to_type_hotel.place(x=160,y=100,width=270,height=20)

        menu = self.optionmenu_adding_price_to_type_hotel['menu']
        menu.delete(0, 'end')

        auth_hot = None

        for k, hotel in self.hotel_data.items():
            for h in hotel:
                text = k+" "+h['nazwa']
                menu.add_command(label=text, command=lambda var=h: self.set_hotel_pt(var))
                if self.authorized_hotel and h['id_hotel']==self.authorized_hotel:
                    auth_hot = h

        if self.authorized_hotel:
            self.set_hotel_pt(auth_hot)
            self.optionmenu_adding_price_to_type_hotel.configure(state="disabled")
        else:
            self.set_hotel_pt(self.hotel_data[list(self.hotel_data.keys())[0]][0])   
        
        self.tabs.select(self.adding_price_to_type_page)

    def set_hotel_pt(self, hotel):
        """wyświetlenie wybranego hotelu i odświeżenie listy z typami dla danego hotelu"""
        self.chosen_hotel = hotel
        self.adding_price_to_type_hotel_var.set(self.chosen_hotel['nazwa'])
        self.type_data = self.database.get_types(self.chosen_hotel['id_hotel'])

        self.price_to_type_type_var = tk.StringVar()
        self.price_to_type_type_var.set('')

        self.optionmenu_price_to_type_type = tk.OptionMenu(self.adding_price_to_type_page, self.price_to_type_type_var, '')
        self.optionmenu_price_to_type_type.place(x=160,y=130,width=270,height=20)

        menu = self.optionmenu_price_to_type_type['menu']
        menu.delete(0, 'end')

        for k, rtype in self.type_data.items():
           menu.add_command(label=rtype['nazwa'], command=lambda var=rtype: self.set_type(var, self.price_to_type_type_var))

        self.set_type(self.type_data[list(self.type_data.keys())[0]], self.price_to_type_type_var)  
    
    def adding_price_to_type_submit_command(self):
        """wysłanie do bazy danych z formularza dodawania prices_text do typu pokoju"""
        id_typ = self.chosen_type['id_typ']
        cena = self.get(self.adding_price_to_type_price_input)
        okres_poczatek = self.room_price_picker_start.get_date().strftime("%Y-%m-%d")
        okres_koniec = self.room_price_picker_end.get_date().strftime("%Y-%m-%d")
        data = {'cena' : cena,
                'id_typ' : id_typ,
                'okres_poczatek' : okres_poczatek,
                'okres_koniec' : okres_koniec}
        result = self.database.add_price_to_type(data)
        if result[0]:
            self.adding_price_to_type_price_input.delete(0, 'end')
            self.room_price_picker_start.set_date(datetime.date.today())
            self.room_price_picker_end.set_date(datetime.date.today())
            self.adding_command()
        messagebox.showinfo(title=None, message=result[1])
    
    def adding_type_command(self):
        """przejście do formularza dodawania typu pokoju, odświeżenie listy hoteli"""
        self.hotel_data = self.database.get_hotels()

        self.adding_type_hotel_var = tk.StringVar()
        self.adding_type_hotel_var.set('')

        self.optionmenu_adding_type_hotel = tk.OptionMenu(self.adding_type_page, self.adding_type_hotel_var, '')
        self.optionmenu_adding_type_hotel.place(x=160,y=80,width=270,height=20)

        menu = self.optionmenu_adding_type_hotel['menu']
        menu.delete(0, 'end')

        auth_hot = None

        for k, hotel in self.hotel_data.items():
            for h in hotel:
                text = k+" "+h['nazwa']
                menu.add_command(label=text, command=lambda var=h: self.set_hotel(var, self.adding_type_hotel_var))
                if self.authorized_hotel and h['id_hotel']==self.authorized_hotel:
                    auth_hot = h

        if self.authorized_hotel:
            self.set_hotel(auth_hot, self.adding_type_hotel_var)
            self.optionmenu_adding_type_hotel.configure(state="disabled")
        else:
            self.set_hotel(self.hotel_data[list(self.hotel_data.keys())[0]][0], self.adding_type_hotel_var)  

        self.tabs.select(self.adding_type_page)

    def adding_type_submit_command(self):
        """wysłanie do bazy danych z formularza dodawania typu pokoju"""
        id_hotel = self.chosen_hotel['id_hotel']
        nazwa = self.get(self.adding_type_name_input)
        opis = self.get(self.adding_type_description_input)
        dla_palaczy = self.get(self.adding_type_smoking_var)
        typ_wezlu_higsan = self.get(self.adding_type_hs_input)
        data = {'id_hote' : id_hotel,
                'nazwa' : nazwa,
                'opis' : opis,
                'dla_palaczy' : dla_palaczy,
                'typ_wezlu_higsan' : typ_wezlu_higsan}
        result = self.database.add_type(data)
        if result[0]:
            self.adding_type_name_input.delete(0,'end')
            self.adding_type_description_input.delete(0,'end')
            self.adding_type_hs_input.delete(0,'end')
            self.adding_command()
        messagebox.showinfo(title=None, message=result[1])

    def adding_employee_to_hotel_command(self):
        """przejście do formularza z dodawaniem pracownika do hotelu, odczyt możliwych hoteli"""
        self.hotel_data = self.database.get_hotels()

        self.adding_employee_to_hotel_hotel_var = tk.StringVar()
        self.adding_employee_to_hotel_hotel_var.set('')

        self.optionmenu_adding_employee_to_hotel_hotel = tk.OptionMenu(self.adding_employee_to_hotel_page, self.adding_employee_to_hotel_hotel_var, '')
        self.optionmenu_adding_employee_to_hotel_hotel.place(x=160,y=80,width=270,height=20)

        menu = self.optionmenu_adding_employee_to_hotel_hotel['menu']
        menu.delete(0, 'end')

        auth_hotel = None

        for k, hotel in self.hotel_data.items():
            for h in hotel:
                text = k+" "+h['nazwa']
                menu.add_command(label=text, command=lambda var=h: self.set_hotel(var, self.adding_employee_to_hotel_hotel_var))
                if self.authorized_hotel and h['id_hotel']==self.authorized_hotel:
                    auth_hotel = h

        if self.authorized_hotel:
            self.set_hotel(auth_hotel, self.adding_employee_to_hotel_hotel_var)
            self.optionmenu_adding_employee_to_hotel_hotel.configure(state="disabled")
        else:
            self.set_hotel(self.hotel_data[list(self.hotel_data.keys())[0]][0], self.adding_employee_to_hotel_hotel_var)
        self.tabs.select(self.adding_employee_to_hotel_page)

    def adding_employee_to_hotel_submit_command(self):
        """wysłanie do bazy danych z formularza dodawania pracownika do hotelu"""
        id_hotel = self.chosen_hotel['id_hotel']
        email = self.get(self.adding_employee_to_hotel_email_input)
        haslo = self.get(self.adding_employee_to_hotel_password_input)
        imie = self.get(self.adding_employee_to_hotel_name_input)
        nazwisko = self.get(self.adding_employee_to_hotel_surname_input)
        data = {'id_hotel' : id_hotel,
                'email' : email,
                'haslo' : haslo,
                'imie' : imie,
                'nazwisko' : nazwisko}
        result = self.database.add_employee(data)
        if result[0]:
            self.adding_employee_to_hotel_email_input.delete(0,'end')
            self.adding_employee_to_hotel_password_input.delete(0,'end')
            self.adding_employee_to_hotel_surname_input.delete(0,'end')
            self.adding_employee_to_hotel_name_input.delete(0,'end')
            self.menu_command()
        messagebox.showinfo(title=None, message=result[1]) 

    def client_exit(self):
        """zamknięcie aplikacji i bazy danych"""
        self.database.close_database()
        exit()