from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.text import LabelBase



kv = """
#: import ScreenManager kivy.uix.screenmanager.ScreenManager
#: import Screen kivy.uix.screenmanager.ScreenManager
#: import NewGameScreen screen
#: import LoadGameScreen screen
#: import Window kivy.core.window.Window
#:import utils kivy.utils
# Define your background color Template
<BackgroundColor@Widget>
    background_color: 1, 1, 1, 1
    canvas.before:
        Color:
            rgba: root.background_color
        Rectangle:
            size: self.size
            pos: self.pos
# Now you can simply Mix the `BackgroundColor` class with almost
# any other widget... to give it a background.
<BackgroundLabel@Label+BackgroundColor>
    background_color: 0, 0, 0, 0
    # Default the background color for this label
    # to r 0, g 0, b 0, a 0
# Use the BackgroundLabel any where in your kv code like below


<InfoLine>:
    size_hint_y: None
    height: 250
    padding: 0,20,0,20
    BackgroundLabel:
        background_color: 0.94, 0.9, 0.89, 1
        bold: True
        text: root.label_text
        font_size: 38
        halign: 'center'   
        color: utils.get_color_from_hex('455452')
        font_name: 'c'

    CheckBox:
        on_active: root.checkbox_click(self, self.active, root.vitamin)
        background_checkbox_normal: 'qwerty.png'
        background_checkbox_down: 'qwerty1.png'

<Check>:
    size_hint_y: None
    height: 500

    BackgroundLabel:
        background_color: 0.94, 0.9, 0.89, 1
        color: utils.get_color_from_hex('455452')
        font_name: 'c'
        text: root.label   
        font_size: 33
<Answer>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20, 20, 20, 40
        BackgroundLabel:
            background_color: 0.88, 0.82, 0.82, 1
            text: 'Ваш результат'
            size_hint_y: None
            height: 80
            font_size: 30
            color: utils.get_color_from_hex('455452')
            font_name: 'c'
        ScrollView:
            Label:
                color: utils.get_color_from_hex('455452')
                font_name: 'c'
                font_size: 42
                size_hint: None, None
                size: self.texture_size                
                id: A
        BoxLayout:
            size_hint_y: None
            padding: 0, 20, 0, 0
            Button:
                id: back
                text: 
                    '''Проверить свои 
                    результаты'''
                size_hint: (.8, None)
                on_press: root.check()
                background_normal: 'button.png'
                color: utils.get_color_from_hex('455452')
                font_size: 24

            Button:
                text: 'Пройти заново?'
                background_normal: 'button.png'
                color: utils.get_color_from_hex('455452')
                font_size: 24
                size_hint: (.8, None)
                on_press: root.back()
                transition: 'right'


ScreenManager:
    id: man
    manager: 'man'
    Screen:
        name: 'q'
        manager: 'man'
        BoxLayout:
            orientation: 'vertical'
            BackgroundLabel:
                background_color: 0.88, 0.82, 0.82, 1
                text: 'Выберите ваши симптомы: '
                size_hint_y: None
                height: 100
                color: utils.get_color_from_hex('455452')
                font_size: 30
                font_name: 'c'

            ScrollView:
                do_scroll_x: True
                do_scroll_y: True
                scroll_type:['bars', 'content']
                bar_width: 20
                BoxLayout:
                    orientation: 'vertical'
                    id: sv_box
                    size_hint_y: None
                    spacing: 50
                    padding: 20, 40, 20, 50
                    height: self.minimum_height
                            
                    
            Button:
                text: 'Дальше'
                color: utils.get_color_from_hex('455452')
                font_size: 24
                size_hint_y: .1
                size_hint_x: .4
                pos_hint: {'x': .3}
                on_press: man.current = 'a'
                background_normal: 'button.png'
    Answer:
        name: 'a'
"""

class Check(BoxLayout):
    label = StringProperty('')


class InfoLine(BoxLayout):
    label_text = StringProperty('Кровоточивость \nдесен')
    vitamin = StringProperty('C')
    check = []
    def checkbox_click(self, inst, val, top):
        if val:
            self.check.append(top)
        else:
            self.check.remove(top)

        print(self.check)

class Answer(Screen):
    
    def check(self):

        s = ''

        for i in Main().vitamin:
            for j in i.split(','):
                cnt = 0
                for k in InfoLine().check:
                    cnt += k.split(',').count(j)
                if f'Нехватка "{j}" на {int((cnt/Main().anmout[j])*10000)/100}%\n' in s:
                    pass
                else: 
                    if int((cnt/Main().anmout[j])*10000)/100 != 0.0:
                        s += f'Нехватка "{j}" на {int((cnt/Main().anmout[j])*10000)/100}%\n'

        self.ids.A.text = s



    def back(self):
        self.ids.back.text = "Обновить результаты?"
        self.manager.current = "q"


class Main(App):
    vitamin = {'Глицин,Цитруллин,D,B1,C': ["Слабость"],
    "Глицин,Валин,B3,B6": ['Проблемы \nсо сном', "Повышеная \nнервная\nвозбудимость¹"],
    "Глутаминовая кислота,Валин,Фенилаланин": ["Ухудшение \nпамяти"],
    "Глутаминовая кислота,Валин,Цитруллин,Изолейцин,A,C": ['Ослабление \nиммунитета','Температурные \nизменения \n("Мне холодно")'],
    "Глутаминовая кислота": ["Нарушение \nработы желу-\nдочного тракта²"],
    "Валин,Изолейцин,Цитруллин": ["Мышечная \nдистрофия³"],
    "Метионин,C,B1": ["Оттечность", "Проблемы с \nволосами⁴"],
    "Валин": ["Трещины на \nслизистых \nоболочках"],
    "Фенилаланин,Тирозин": ["Снижение \nаппетита"],
    "Фенилаланин": ["Резкое \nпохудение"],
    "Тирозин,Изолейцин": ["Быстрая \nутомляемость"],
    "Тирозин": ["Плохая \nстрессо-\nустойчивость", "Резкие \nперепады \nнастроения"],
    "Изолейцин": ["Сильные \nголовные боли/\nголовокружение", "Раздражи-\nтельность"],
    "A,B6,B3": ["Сухость кожи", "Бледность"],
    "D,B3,B1": ["Снижение \nпрочности\nкостной ткани", "Мышечные боли", "Усталость","Нарушение \nчувстви-\nтельности⁵"],
    "PP,B3": ["Воспаление\nкожи"],
    "PP": ["Поражение пи-\nщеварительной \nсистемы", "Поражение \nнервной \nсистемы"],
    "C": ["Кровоточи-\nвость десен", 'Воспаления рта']
        }

    vit = ['Глицин', 'Цитруллин', 'D', 'B1', 'C', 'Валин', 'B3', 'B6', 'Глутаминовая кислота', 'Фенилаланин', 'Изолейцин', 'A', 'C', 'Метионин', 'Тирозин', 'PP']
    anmout = {}
    for j in vit:
        cnt = 0
        for i in vitamin:
            a = i.split(',')
            if j in a:
                cnt += len(vitamin[i])
        anmout[j] = cnt
    

    def build(self):
        Window.clearcolor = (0.99, 0.96, 0.95, 1)
        return Builder.load_string(kv)

    def on_start(self):

        for i in self.vitamin:
            for j in self.vitamin[i]:
                self.root.ids.sv_box.add_widget(InfoLine(label_text=j, vitamin=i))

        self.root.ids.sv_box.add_widget(Check(label='''            1. Нервозность, раздражительность, 
            бессоница
            2. Жжение, метиоризм, отрыжка
            3. Напряжения вызывают боли, 
            мышечные боли
            4. Ломкость, выпадение, 
            обесцвечивание
            5. Обычные ощущения приобретают 
            неестевственно резкий характер.
            Воспринимаются слабые 
            раздражители'''))

LabelBase.register(name='c', 
                   fn_regular='centuryschoolbook.ttf')

Main().run()