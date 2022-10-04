# from kivymd.uix.screen import MDScreen
import os
import random
import re
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from urllib import request

from dotenv import load_dotenv

import mysql.connector
from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.utils import rgba
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.toast import toast
from kivymd.uix.button import MDIconButton
from kivymd.uix.imagelist import MDSmartTile
from kivy.uix.image import AsyncImage
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.behaviors import FakeRectangularElevationBehavior

Window.size = (390, 700)


class LoaderImage(AsyncImage):
    pass


class LabelButton(ButtonBehavior, Label):
    pass


class ImageButton(ButtonBehavior, AsyncImage):
    pass


class NavBar(FakeRectangularElevationBehavior, MDFloatLayout):
    pass


class ProfileCard(FakeRectangularElevationBehavior, MDFloatLayout):
    pass


class SmartTileWithStar(MDSmartTile):
    pass


class But_pressed(MDIconButton):
    pass


category_list = ["abstract", "animals", "nature", "space"]

# Env Variables
load_dotenv()

EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')


class OGWallpaperApp(MDApp):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    database = mysql.connector.Connect(host="localhost", user="root", password="140598", database="login",
                                       auth_plugin='mysql_native_password')
    cursor = database.cursor()

    def build(self):
        screen = Builder.load_file("wallpaper.kv")
        self.theme_cls.theme_style = "Light"
        return screen

    def check(self, checkbox, value):
        if value:
            self.root.ids.light_dark.text = "Dark Mode"
            # self.root.ids.collections.box_color = (0, 0, 0, .5)
            self.root.ids.navbar.md_bg_color = (1, 1, 1, .9)
            self.theme_cls.theme_style = "Dark"
            self.root.ids.contact.md_bg_color = (0, 0, 0, 0)
        else:
            self.root.ids.light_dark.text = "Light Mode"
            self.theme_cls.theme_style = "Light"
            self.root.ids.navbar.md_bg_color = (0.2, 0.2, 0.2, 1)
            self.root.ids.contact.md_bg_color = (1, 1, 1, 1)

    id = 1

    def start(self, f_name, *args):
        self.root.ids.screen_manager.current = "hello"
        a = self.root.ids.text1
        a.text = f"Welcome {f_name}."
        animate = Animation(opacity=1, duration=1)
        animate += Animation(opacity=1, duration=2)
        animate += Animation(opacity=0, duration=1)
        animate.bind(on_complete=self.start)
        animate.start(self.root.ids[f"text{self.id}"])

        if self.id < 2:
            self.id += 1
        elif self.id == 2:
            Animation.cancel_all(self.root.ids.text2)
            self.root.ids.screen_manager.current = "home"

    def search(self, search_image):
        if search_image != "":
            self.root.ids.search_label.text = search_image
            self.root.ids.screen_manager.transition.direction = "left"
            self.root.ids.screen_manager.current = "search_page"
            for image in range(50):
                result = LoaderImage(source=f"https://source.unsplash.com/random/180x240/?{search_image}={image}",
                                     pos_hint={"center_x": .5}, size_hint=(None, None), size=("180dp", "240dp"))
                self.root.ids.search_list.add_widget(result)

    def goto(self, source):
        self.root.ids.search_label.text = source
        self.root.ids.screen_manager.transition.direction = "left"
        self.root.ids.screen_manager.current = "search_page"
        for image in range(50):
            result = LoaderImage(source=f"https://source.unsplash.com/random/180x240/?{source}={image}",
                                 pos_hint={"center_x": .5}, size_hint=(None, None), size=("180dp", "240dp"))
            self.root.ids.search_list.add_widget(result)

    def clear_result(self):
        self.root.ids.search_image.text = ""
        self.root.ids.search_list.clear_widgets(None)

    def collections(self):
        for i in category_list:
            col = MDSmartTile(
                box_color=(1, 1, 1, .5),
                source=f"https://source.unsplash.com/120x180/?{i}",
                pos_hint={"center_x": .5, "center_y": .5},
                size_hint=(None, None),
                size=("180dp", "180dp"))
            self.root.ids.collections.add_widget(col)

    def recent(self):
        self.root.ids.screen_manager.transition.direction = "left"
        self.root.ids.screen_manager.current = "recent_page"
        a = int(random.randint(1, 10))
        list_of_id = []
        for images in range(10, 200, a):
            list_of_id.append(images)
            # for i in list_of_id:
            results = MDSmartTile(id=f"{images}",
                                  source=f"https://picsum.photos/id/{images}/240/350",
                                  pos_hint={"center_x": .5},
                                  size_hint=(None, None),
                                  size=("240dp", "350dp"))
            results2 = MDIconButton(id=f"{images}",
                                    icon="heart-outline",
                                    theme_icon_color="Custom",
                                    icon_color=(1, 0, 0, 1),
                                    pos_hint={"center_x": .5, "center_y": .5})
            # results3 = MDIconButton(id=f"{images}",
            #                         icon="download",
            #                         theme_icon_color="Custom",
            #                         icon_color=(0, 0, 0, 1),
            #                         pos_hint={"center_x": .5, "center_y": .5})
            results2.bind(on_release=lambda x=results2: self.pressed(results.id))
            # results3.bind(on_release=lambda x=results3: self.download(img_url))
            self.root.ids.recent_list.add_widget(results)
            self.root.ids.recent_list.add_widget(results2)
            # self.root.ids.recent_list.add_widget(results3)

    def pressed(self, img_url):
        print(img_url)

    def download(self, img_url):
        api_call = f"https://picsum.photos/id/{img_url}/800/1200"
        print(api_call)
        request.urlretrieve(api_call, f"downloads/{img_url}.png")

    def return_but(self):
        for i in range(1, 4):
            self.root.ids[f"nav{i + 1}"].text_color = rgba(173, 182, 196, 255)
        self.root.ids.nav1.text_color = rgba(253, 275, 277, 255)

    def changenav_color(self, ins):
        if ins in self.root.ids.values():
            current_id = list(self.root.ids.keys())[list(self.root.ids.values()).index(ins)]
            for i in range(4):
                if f"nav{i + 1}" == current_id:
                    self.root.ids[f"nav{i + 1}"].text_color = rgba(253, 275, 277, 255)
                else:
                    self.root.ids[f"nav{i + 1}"].text_color = rgba(173, 182, 196, 255)

    def change_icon(self, ins):
        if ins in self.root.ids.values():
            current_id = list(self.root.ids.keys())[list(self.root.ids.values()).index(ins)]
            for i in range(6):
                if f"bt{i}" == current_id:
                    self.root.ids[f"bt{i}"].icon = "heart" if self.root.ids[f"bt{i}"].icon == "heart-outline" \
                        else "heart-outline"

    def add_fav(self, image_id, button):
        if button.icon == "heart":
            self.result = MDSmartTile(source=image_id,
                                      pos_hint={"center_x": .5},
                                      size_hint=(None, None),
                                      size=("240dp", "350dp"))
            self.root.ids.fav_list.add_widget(self.result)
            toast("Added To Favorites.", background=[41/255, 76/255, 96/255, 0.8])
        elif button.icon == "heart-outline":
            self.root.ids.fav_list.remove_widget(self.result)
            toast("Removed from Favorites.", background=[41/255, 76/255, 96/255, 0.8])

    def send_data(self, email, password, f_name, l_name):
        if re.fullmatch(self.regex, email.text):
            self.cursor.execute(f"insert into logindata values('{email.text}', '{password.text}', '{f_name.text}',"
                                f" '{l_name.text}')")
            self.database.commit()
            self.receive_data(email, password, id=1)
            self.start(f_name.text)
            email.text = ""
            password.text = ""
            f_name.text = ""
            l_name.text = ""
        elif email.text == "" and password.text == "" and f_name.text == "" and l_name.text == "":
            toast("Please Enter Your Details to Proceed!", background=[0.8, 0, 0, 1])
        else:
            toast("Invalid Details", background=[0.8, 0, 0, 1])

    def receive_data(self, email, password, id):
        self.cursor.execute("select * from logindata")
        list_of_email = []
        for i in self.cursor.fetchall():
            list_of_email.append(i[0])
        if email.text in list_of_email and email.text != "":
            self.cursor.execute(f"select password from logindata where email='{email.text}'")
            for j in self.cursor:
                if password.text == j[0]:
                    toast("You have successfully login your account!!", background=[41/255, 76/255, 96/255, 0.8])
                    if id == 0:
                        self.root.ids.screen_manager.current = "home"
                else:
                    toast("Incorrect Password!! Try Again.", background=[0.8, 0, 0, 1])
        else:
            toast("Incorrect Email Address!!!", background=[0.8, 0, 0, 1])

    def send_email(self, name, email_address, message):
        msg = EmailMessage()
        msg["Subject"] = "New User Message!"
        msg["To"] = "allyhb98@gmail.com"
        msg["From"] = formataddr((name.text, email_address.text))
        msg.set_content(f"Hi Team,\n\nMy Name is {name.text}.\n\n{message.text}\n\nRegards,\n{name.text}")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL, PASSWORD)
            smtp.send_message(msg)
        name.text = ""
        email_address.text = ""
        message.text = ""
        toast("Message Sent", background=[41/255, 76/255, 96/255, 0.8])


if __name__ == "__main__":
    OGWallpaperApp().run()
