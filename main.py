from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from plyer import gravity
from kivy.properties import NumericProperty
from plyer import vibrator, flash
from kivy.properties import ColorProperty

Builder.load_string('''
<GravityInterface>:
    orientation: 'vertical'
    canvas:
        Color:
            rgba: self.my_color
        Rectangle:
            size: self.size
            pos: self.pos
    Label:
        id: x_label
        text: 'X: '
    Label:
        id: y_label
        text: 'Y: '
    Label:
        id: z_label
        text: 'Z: '

    Button
        text: 'Start Gravity Sensor'
        on_press: root.operations();
''')


class GravityInterface(BoxLayout):    
    my_color = ColorProperty([0, 0, 0, 1])
    def __init__(self):
        super().__init__()
        self.sensorEnabled = False


    def operations(self):
        if not self.sensorEnabled:
            gravity.enable()
            Clock.schedule_interval(self.get_gravity, 1 / 60.) # 1 / 60.
            self.sensorEnabled = True

    def get_gravity(self, dt):
        self.val = gravity.gravity

        if not self.val == (None, None, None):
            if self.val[2] < 5:
                vibrator.vibrate(0.01)
                self.my_color = 1, 0, 0, 1
            else:
                self.my_color = 0, 0, 0, 1
            self.ids.x_label.text = "X: " + str(self.val[0])
            self.ids.y_label.text = str(f"{gravity.gravity[1]: .1f}")
            self.ids.z_label.text = "Z: " + str(self.val[2])


class GravityApp(App):
    def build(self):
        return GravityInterface()


GravityApp().run()
