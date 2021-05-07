# -*- coding: utf-8 -*-
import multiprocessing as mp
     
if __name__ == '__main__':
    mp.freeze_support()

    from kivy.app import App
    from kivy.clock import Clock
    from kivy.lang import Builder
    from kivy.uix.widget import Widget
    from kivy.core.window import Window
    from kivy.uix.screenmanager import *
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.textinput import TextInput
    from kivy.uix.gridlayout import GridLayout
    from kivy.properties import ObjectProperty
    from kivy.uix.screenmanager import Screen
    
    from functools import partial
    
    import pandas as pd
    
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    from kraken_kivy_classes import *
    import kraken_data as kr_dat
    from main_kivy import kivy_dat
    
    # Screens dimensions
    menu_size = (600, 150)
    main_size = (1500, 800)
    
    # Useful variable to center the window on screen change
    ini_center = tuple([x/2 for x in menu_size])
    
    # Builder
    Builder.load_string(kivy_dat)
            
    class WindowManager(ScreenManager):
        pass
    
    # Login window
    class MenuWindow(Screen):    
        def enter(self):
            """
            Sends you to the sign up screen.
            """
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = "main"
            cripto_input = self.ids.criptos.text
            cripto_input = [cripto_input if cripto_input != "" else cripto_list][0]
    
            sc_center(main_size)
            self.p1 = mp.Process(target=kr_dat.main, \
                                 args=(cripto_input, path, ""))
            self.p1.start()
                
    class MainWindow(Screen):
        def __init__(self, **kwargs):
            super(MainWindow, self).__init__(**kwargs)
            self.add_widget(MainLayout())
    
    class MainLayout(GridLayout):
        def __init__(self, **kwargs):
            super(MainLayout, self).__init__(**kwargs)
            self.main_center = Window.center

            self.build_times()
            self.test = "1m"

            Clock.schedule_interval(self.after_init, 0.1)
        
        def build_times(self):
            self.add_widget(RedLabel(text = "Cripto"))
            
            times = ["1m", "5m", "15m", "30m", "1h", "4h"]
            self.button_list = []
            
            for i in times:
                btn = CryptoButton(i, text=i)
                btn.bind(on_press = self.button_sort)
                self.button_list.append(btn)
                self.add_widget(btn)
            
        def after_init(self, dt):
            self.excel = pd.read_excel ("data/rsi_placeholder.xlsx", index_col = [0])
            self.index = self.excel.index
            
            try:
                self.remove()
            except AttributeError:
                pass
            
            self.update()
            
        def button_sort(self, instance):
            self.test = instance.get_time()
        
        def rsi_sort(self, time: str):
            sort_dict: dict = {}
            sort_list: list = []
            keys_list: list = []
        
            for k in self.index:
                sort_dict[self.excel[time][k]] = k
                sort_list.append(self.excel[time][k])
            
            sort_list.sort()
            
            for i in sort_list:
                keys_list.append(sort_dict[i])
            
            dt = pd.DataFrame({k: self.excel.T[k] for k in keys_list})
            
            self.excel = dt.T
            self.index = self.excel.index
            
            
        def update(self):
            # Creamos la lista para acceder a las labels mas tarde
            self.label_list = []
            self.rsi_sort(self.test)
            
            # i es el nombre de la criptomoneda
            for i in self.index:
                crypto_name = RedLabel(text=i)
                self.label_list.append(crypto_name)
                self.add_widget(crypto_name)

                # k es el tiempo
                for k in self.excel:
                    text = f"{self.excel[k][i]:.2f}".format()
  
                    color = (1, 1, 1, 1)
                    if self.excel[k][i] <= 30:
                        color = (1, 0, 0, 1)
                    
                    elif self.excel[k][i] >= 70:
                        color = (0.6, 0.20, 0.8, 1)
                        
                    if self.excel[k][i] == 0:
                        text = ""
                
                    crypto_value = ValueLabel(color, text=text)
                    self.label_list.append(crypto_value)

                    self.add_widget(crypto_value)
        
        def remove(self):
            for i in self.label_list:
                self.remove_widget(i)
            
    
    # Main App from which everything else is built 
    class Main(App):
        def build(self):
            self.title = "KrakenRSI"
            self.ini_center = Window.center
            
            Window.size = menu_size
            x_var = Window.center[0] - self.ini_center[0]
            y_var = Window.center[1] - self.ini_center[1]
            
            Window.left -= x_var
            Window.top -= y_var
                
            sm.add_widget(MenuWindow(name="menu"))
            sm.add_widget(MainWindow(name="main"))
            
            return sm
    
    
    def sc_center(Window_size: tuple, Inverse: bool = False, \
                  center: tuple = ini_center, win: object = Window):
        """
        This function centers a Window that has changed size
        
        Parameters
        ----------
        
        Window_size: tuple, The new size of the window
        center: tuple, The place where the window will be centered
        Inverse: bool (boolean, Default: False), To specify if you are going back
                                                 a previous window
        win: object (Default: Window), The object to which the changes will apply
        """
        if Inverse == False:
            win.size = Window_size
            variation_x = win.center[0] - center[0]
            variation_y = win.center[1] - center[1]
            win.left -= variation_x
            win.top -= variation_y
        
        if Inverse == True:
            variation_x = win.center[0] - center[0]
            variation_y = win.center[1] - center[1]
            win.left += variation_x
            win.top += variation_y
            win.size = Window_size
    
    path = sys.executable
    path_index = path[::-1].index("\\")
    path = path[:-path_index]

    data_path = path+"\data"
    cripto_path = path+"\cripto_list.txt"

    if os.path.exists(data_path):
        pass
    else:
        os.mkdir(data_path)

    if os.path.exists(cripto_path):
        cripto_list = open(cripto_path)
        cripto_list = cripto_list.read()

    else:
        cripto_list = open(cripto_path, "w+")
        cripto_list.write("BTC/EUR, ETH/EUR, ADA/EUR, DOT/EUR, LINK/EUR")
        cripto_list = open(cripto_path)
        cripto_list = cripto_list.read()

    kr_dat.main("BTC/EUR", path, "STOP")
    sm = ScreenManager(transition=NoTransition())
    Main().run()
