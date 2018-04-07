from kivy.app import App
from kivy.lang import Builder
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.properties import ListProperty, StringProperty
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image as kivyImage

Builder.load_string('''
#: set dummy './icons/dummy.png'
<MyRoot>:
	orientation: 'vertical'
	bgcolor: 1,1,1,1
	canvas.before:
		Color:
			rgba: self.bgcolor
		Rectangle:
			size: self.size
			pos: self.pos
	ScreenManager:
		id: scm
		size_hint_y: 0.9
		scno: 1
		on_current:
			root.bgcolor = self.current_screen.bgcolor
		on_scno:
			self.current = 'sc'+str(self.scno)
	BoxLayout:
		size_hint_y: 0.1
		orientation: 'horizontal'
		Label: # スペーサ
			size_hint_x: 0.7
		Button:
			size_hint_x: 0.1
			text: 'home'
			on_press:
				scm.transition.direction = 'down'
				scm.scno = 1
		Button:
			size_hint_x: 0.1
			text: '←'
			on_press:
				scm.transition.direction = 'right'
				if scm.scno > 1: scm.scno += -1
		Button:
			size_hint_x: 0.1
			text: '→'
			on_press:
				scm.transition.direction = 'left'
				if scm.scno < 4: scm.scno += 1

<MyScreen>:
	BoxLayout:
		orientation: 'vertical'
		Label:
			size_hint_y: 0.1
			text: root.title
			font_size: 32
		FloatLayout: 
			id: contents
			size_hint_y: 0.9

<ThumbnailScrn>:
    thumb : thumb
	BoxLayout:
		orientation: 'vertical'
		Label:
			size_hint_y: 0.1
			text: "表示対象を選んでください"
			font_size: 32
		GridLayout: 
			id: thumb
			size_hint_y: 0.9
            cols: 5
            rows: 4
            spacing: 2
            padding: 4

<Label>:
	font_size: 32
''')

LabelBase.register(DEFAULT_FONT, 'ipaexg.ttf')

class MyScreen(Screen):
    title = StringProperty()
    bgcolor = ListProperty()

class MyRoot(BoxLayout):
    pass

class ThumbnailScrn(Screen):
    title = StringProperty()
    bgcolor = ListProperty()
    thumb = ObjectProperty()
    def __init__(self, **kwargs):
        super(ThumbnailScrn,self).__init__(**kwargs)
        dummyimg = './icons/dummy.png'
        for i in range(5):
            for j in range(4):
                img = kivyImage(source = dummyimg)
                self.thumb.add_widget(img)

class TransitionExampleApp(App):
    def build(self):
        root = MyRoot()
        sc1 = MyScreen(name='sc1', title='画面1', bgcolor=[0.8,0.8,0.8,1])
        sc2 = ThumbnailScrn(name='sc2', bgcolor=[0.6,0.6,0.8,1])
        sc3 = MyScreen(name='sc3', title='画面3', bgcolor=[0.9,0.8,0.2,1])
        sc4 = MyScreen(name='sc4', title='画面4', bgcolor=[0.6,0.4,0.0,1])
        root.ids['scm'].add_widget(sc1)
        root.ids['scm'].add_widget(sc2)
        root.ids['scm'].add_widget(sc3)
        root.ids['scm'].add_widget(sc4)
        return root

TransitionExampleApp().run()