from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class SimpleApp(BoxLayout):
    def __init__(self, **kwargs):
        super(SimpleApp, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 50
        self.spacing = 20

        self.add_widget(Label(
            text="Smart Camera Is Working!",
            font_size='22sp'
        ))

        self.btn = Button(
            text="Click Me",
            font_size='20sp',
            size_hint=(1, 0.3)
        )
        self.btn.bind(on_press=self.on_button_click)
        self.add_widget(self.btn)

    def on_button_click(self, instance):
        self.btn.text = "Button Clicked Successfully!"

class MainApp(App):
    def build(self):
        return SimpleApp()

if __name__ == '__main__':
    MainApp().run()
