kivy_dat = ("""
<RedLabel@Label>:
    color: 0.728, 0.536, 0.2, 1
    size_hint: (1, 0.25)
    outline_width: 1
    canvas.before:
        Color:
            rgba: 0.332, 0.22, 0.244, 1
        Rectangle:
            pos: self.pos
            size: self.size
            
        Color:
            rgba: (1, 1, 1, 1)
        Line:
            width: 1
            rectangle: self.x, self.y, self.width, self.height

<ValueLabel@Label>
    color: (0, 1, 0, 1)
    canvas.before:
        Line:
            points: self.x, self.y,self.x+self.width, self.y
            
<aButton@Button>:
    background_color: 0.688, 0.644, 0.66, 1
    color: 0.953, 0.957, 0.945, 1
    
<calButton@Button>:
    halign: "right"
    valign: "top"
    text_size: self.size
    background_color: (.3, .6, .7, 1)
    padding: ("15", "10")
    
<CryptoButton@Button>
    color: 0.728, 0.536, 0.2, 1
    size_hint: (1, 0.25)
    
<MainLayout@GridLayout>
    name: "main_layout"
    cols: 7
                
<MenuWindow>:
    name: "menu"
    BoxLayout:
        id: menu_layout
        cols: 1
        orientation: "vertical"
        
        BoxLayout:
            orientation: "horizontal"
    
            Label:
                text: 'Criptomonedas:'
                
            TextInput:
                id: criptos
                write_tab: False
                multiline: False
                hint_text: "Criptos"
                

        aButton:
            text: "Enter"
            on_press: root.enter()
        
        aButton:
            text: "Exit"
            on_press: app.exit()

<MainWindow>:
    name: "main"
    MainLayout:
        id: "main_layout"
        cols: 7

""")