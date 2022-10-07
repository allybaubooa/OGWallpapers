# imports
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
from kivymd.uix.behaviors import FakeRectangularElevationBehavior, HoverBehavior
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextFieldRect
from twilio.rest import Client

Window.size = (390, 700)


# Load class
class LoaderImage(AsyncImage):
    pass


class HoverLabel(HoverBehavior, MDLabel, ButtonBehavior):
    pass


class LabelButton(ButtonBehavior, Label):
    pass


class ImageButton(ButtonBehavior, AsyncImage):
    pass


class NavBar(FakeRectangularElevationBehavior, MDFloatLayout):
    pass


class ProfileCard(FakeRectangularElevationBehavior, MDFloatLayout):
    pass


class But_pressed(MDIconButton):
    pass


class InputField(MDTextFieldRect):
    def __init__(self, **kwargs):
        super().__init__(multiline=False, input_filter="int", **kwargs)


category_list = ["abstract", "animals", "nature", "space"]

# Env Variables
load_dotenv()

EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')
ACCOUNT_SID = os.environ.get('ACCOUNT_SID')
AUTH_TOKEN = os.environ.get('AUTH_TOKEN')


# App Class
class OGWallpaperApp(MDApp):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    database = mysql.connector.Connect(host="localhost", user="root", password="140598", database="login",
                                       auth_plugin='mysql_native_password')
    cursor = database.cursor()
    id = 1

    data = {
        'Contact Us': 'email',
        'Sign Out': 'logout'
    }

    def build(self):
        screen = Builder.load_file("wallpaper.kv")
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        return screen

    # Speed dial stack buttons
    def callback(self, ins):
        if ins.icon == "logout":
            self.root.ids.speed_dial.close_stack()
            self.sign_out()
            toast("You have been signed out!!!", background=[41 / 255, 76 / 255, 96 / 255, 0.8])
        elif ins.icon == "email":
            self.root.ids.speed_dial.close_stack()
            self.root.ids.screen_manager.transition.direction = "left"
            self.root.ids.screen_manager.current = "contactus"
            self.clear_result()

    # Dark/Light mode Switch class
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

    # Welcome Screen animation
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

    # Search_engine
    def search(self, search_image):
        if search_image != "":
            self.root.ids.search_label.text = search_image
            self.root.ids.screen_manager.transition.direction = "left"
            self.root.ids.screen_manager.current = "search_page"
            for image in range(50):
                result = ImageButton(source=f"https://source.unsplash.com/random/180x240/?{search_image}={image}",
                                     pos_hint={"center_x": .5}, size_hint=(None, None), size=("180dp", "240dp"))
                self.root.ids.search_list.add_widget(result)
                result.bind(on_release=lambda x: self.select_image(x.source))

    # Categories Goto
    def goto(self, source):
        self.root.ids.search_label.text = source
        self.root.ids.screen_manager.transition.direction = "left"
        self.root.ids.screen_manager.current = "search_page"
        for image in range(50):
            result = ImageButton(source=f"https://source.unsplash.com/random/180x240/?{source}={image}",
                                 pos_hint={"center_x": .5}, size_hint=(None, None), size=("180dp", "240dp"))
            self.root.ids.search_list.add_widget(result)

    # Clear Search Text
    def clear_result(self):
        self.root.ids.search_image.text = ""
        self.root.ids.search_list.clear_widgets(None)

    # Change Show/Hide Password Icon
    def pw_icon(self, ins):
        if ins in self.root.ids.values():
            current_id = list(self.root.ids.keys())[list(self.root.ids.values()).index(ins)]
            for i in range(2):
                if f"show{i + 1}" == current_id:
                    self.root.ids[f"show{i + 1}"].icon = "eye" \
                        if self.root.ids[f"show{i + 1}"].icon == "eye-off" \
                        else "eye-off"

    # Show/Hide Password
    def show_pw(self, ins):
        if ins in self.root.ids.values():
            current_id = list(self.root.ids.keys())[list(self.root.ids.values()).index(ins)]
            for i in range(2):
                if f"show{i + 1}" == current_id and self.root.ids[f"show{i + 1}"].icon == "eye":
                    self.root.ids[f"password{i + 1}"].password = False
                else:
                    self.root.ids[f"password{i + 1}"].password = True

    # Recent Page
    def recent(self):
        self.root.ids.screen_manager.transition.direction = "left"
        self.root.ids.screen_manager.current = "recent_page"
        a = int(random.randint(1, 10))
        list_of_id = []
        for images in range(10, 200, a):
            list_of_id.append(images)
            results = MDSmartTile(id=f"{images}",
                                  source=f"https://picsum.photos/id/{images}/240/350",
                                  pos_hint={"center_x": .5},
                                  size_hint=(None, None),
                                  size=("240dp", "350dp"))
            results3 = MDIconButton(id=f"dw{images}",
                                    icon="download",
                                    theme_icon_color="Custom",
                                    icon_color=(0, 0, 0, 1),
                                    pos_hint={"center_x": .5, "center_y": .5})
            results3.bind(on_release=lambda y: self.download(y))
            self.root.ids.recent_list.add_widget(results)
            self.root.ids.recent_list.add_widget(results3)

    # Download Image
    def download(self, img_url):
        image_id = img_url.id.replace("dw", "")
        api_call = f"https://picsum.photos/id/{image_id}/800/1200"
        print(api_call)
        request.urlretrieve(api_call, f"downloads/{image_id}.png")
        toast("Image Saved.", background=[41 / 255, 76 / 255, 96 / 255, 0.8])

    # NavBar Color Return Button
    def return_but(self):
        for i in range(1, 3):
            self.root.ids[f"nav{i + 1}"].text_color = rgba(173, 182, 196, 255)
        self.root.ids.nav1.text_color = rgba(253, 275, 277, 255)

    # NavBar Color Change
    def changenav_color(self, ins):
        if ins in self.root.ids.values():
            current_id = list(self.root.ids.keys())[list(self.root.ids.values()).index(ins)]
            for i in range(3):
                if f"nav{i + 1}" == current_id:
                    self.root.ids[f"nav{i + 1}"].text_color = rgba(253, 275, 277, 255)
                else:
                    self.root.ids[f"nav{i + 1}"].text_color = rgba(173, 182, 196, 255)

    # Favorite Icon
    def change_icon(self, ins):
        if ins in self.root.ids.values():
            current_id = list(self.root.ids.keys())[list(self.root.ids.values()).index(ins)]
            for i in range(6):
                if f"bt{i}" == current_id:
                    self.root.ids[f"bt{i}"].icon = "heart" \
                        if self.root.ids[f"bt{i}"].icon == "heart-outline" \
                        else "heart-outline"

    # Add to Fav
    def add_fav(self, image_id, button):
        if button.icon == "heart":
            self.result = MDSmartTile(source=image_id,
                                      pos_hint={"center_x": .5},
                                      size_hint=(None, None),
                                      size=("240dp", "350dp"))
            self.root.ids.fav_list.add_widget(self.result)
            toast("Added To Favorites.", background=[41 / 255, 76 / 255, 96 / 255, 0.8])
        elif button.icon == "heart-outline":
            self.root.ids.fav_list.remove_widget(self.result)
            toast("Removed from Favorites.", background=[41 / 255, 76 / 255, 96 / 255, 0.8])

    # Click on Image
    def select_image(self, source):
        self.root.ids.screen_manager.transition.direction = "left"
        self.root.ids.screen_manager.current = "image_page"
        self.newimage = ImageButton(source=source,
                                    pos_hint={"center_x": .5, "center_y": .8},
                                    size_hint=(None, None),
                                    size=("280dp", "400dp"))
        self.root.ids.sel_image.add_widget(self.newimage)
        self.sel = self.newimage.source
        return self.sel

    # Add Favorite Selected
    def add_fav_new(self, button):
        if button.icon == "heart":
            self.result = MDSmartTile(source=self.sel,
                                      pos_hint={"center_x": .5},
                                      size_hint=(None, None),
                                      size=("240dp", "350dp"))
            self.root.ids.fav_list.add_widget(self.result)
            toast("Added To Favorites.", background=[41 / 255, 76 / 255, 96 / 255, 0.8])
        elif button.icon == "heart-outline":
            self.root.ids.fav_list.remove_widget(self.result)
            toast("Removed from Favorites.", background=[41 / 255, 76 / 255, 96 / 255, 0.8])

    # Return in Select Page
    def return_back(self):
        self.root.ids.screen_manager.transition.direction = "right"
        self.root.ids.screen_manager.current = "home"
        self.root.ids.sel_image.remove_widget(self.newimage)

    # Download in Select Page
    def download_sel(self):
        api_call = self.sel
        img_name = f"new{random.randint(1, 10000)}"
        request.urlretrieve(api_call, f"downloads/{img_name}.png")
        toast("Image Saved.", background=[41 / 255, 76 / 255, 96 / 255, 0.8])

    # Register Login
    def send_data(self, email, password, f_name, l_name, cc, phone_no):
        if re.fullmatch(self.regex, email.text) and email.text != "" and password.text != "" and \
                f_name.text != "" and l_name.text != "":

            self.cursor.execute("select * from logindata")
            list_of_email = []
            for i in self.cursor.fetchall():
                list_of_email.append(i[0])
            if email.text in list_of_email and email.text != "":
                email.text = ""
                toast("Account Already Exist!!", background=[0.8, 0, 0, 1])
            else:
                self.cursor.execute(f"insert into logindata values('{email.text}',"
                                    f"'{password.text}',"
                                    f"'{f_name.text}',"
                                    f" '{l_name.text}')")
                self.database.commit()
                toast("OTP has been sent on your phone!!", background=[41 / 255, 76 / 255, 96 / 255, 0.8])
                self.otp_verification(email, password, f_name, cc, phone_no)
                email.text = ""
                password.text = ""
                f_name.text = ""
                l_name.text = ""
        elif email.text == "" or password.text == "" or f_name.text == "" \
                or l_name.text == "" or cc.text == "" or cc.phone_no == "":
            toast("Please Enter All the Details to Proceed!", background=[0.8, 0, 0, 1])
        else:
            toast("Invalid Details", background=[0.8, 0, 0, 1])

    # OTP Verification
    def otp_verification(self, otpemail, otppassword, f_name, otpcc, otpphone):
        self.user_email = otpemail.text
        self.user_pw = otppassword.text
        self.first_name = f_name.text
        self.root.ids.screen_manager.current = "otp"
        self.otp = random.randint(1000, 9999)
        account_sid = ACCOUNT_SID
        auth_token = AUTH_TOKEN
        self.phone_numer = f"{otpcc.text}{otpphone.text}"

        client = Client(account_sid, auth_token)

        msg = client.messages.create(
            body=f"Your OTP Password is: {self.otp}",
            from_="+19259408526",
            to=self.phone_numer
        )
        return self.user_email, self.user_pw, self.first_name

    # OTP Check
    def check_otp(self, otpInput):
        if int(otpInput) == self.otp:
            self.start(self.first_name)
            toast("You have successfully Registered your account!!", background=[41 / 255, 76 / 255, 96 / 255, 0.8])
        else:
            toast("Wrong OTP! Please Input Correct OTP.", background=[0.8, 0, 0, 1])

    # Resend OTP
    def resend_otp(self):
        self.otp = random.randint(1000, 9999)
        account_sid = ACCOUNT_SID
        auth_token = AUTH_TOKEN
        client = Client(account_sid, auth_token)

        msg = client.messages.create(
            body=f"Your OTP Password is: {self.otp}",
            from_="+19259408526",
            to=self.phone_numer
        )
        toast("OTP has been sent again!!", background=[41 / 255, 76 / 255, 96 / 255, 0.8])

    # Login Verification
    def receive_data(self, email, password, id):
        self.cursor.execute("select * from logindata")
        list_of_email = []
        for i in self.cursor.fetchall():
            list_of_email.append(i[0])
        if email.text in list_of_email and email.text != "":
            self.cursor.execute(f"select password from logindata where email='{email.text}'")
            for j in self.cursor:
                if password.text == j[0]:
                    if id == 0:
                        email.text = ""
                        password.text = ""
                        self.root.ids.screen_manager.current = "home"
                        toast("You have successfully login your account!!",
                              background=[41 / 255, 76 / 255, 96 / 255, 0.8])
                else:
                    toast("Incorrect Password!! Try Again.", background=[0.8, 0, 0, 1])
        elif email.text == "" or password.text == "":
            toast("Please Enter Details to Login!!!", background=[0.8, 0, 0, 1])
        else:
            toast("Please Enter Proper Login Details!!!", background=[0.8, 0, 0, 1])

    # Sign Out
    def sign_out(self):
        self.root.ids.screen_manager.transition.direction = "right"
        self.root.ids.screen_manager.current = "login"

    # Contact Us email
    def send_email(self, name, email_address, message):
        msg = EmailMessage()
        msg["Subject"] = "New User Message!"
        msg["To"] = "allyhb98@gmail.com"
        msg["From"] = formataddr((name.text, email_address.text))
        msg.set_content(f"Hi Team,\n\nMy Name is {name.text}.\n\nMy email address is: {email_address.text}."
                        f"\n\n{message.text}\n\nRegards,\n{name.text}")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL, PASSWORD)
            smtp.send_message(msg)
        name.text = ""
        email_address.text = ""
        message.text = ""
        toast("Message Sent", background=[41 / 255, 76 / 255, 96 / 255, 0.8])


if __name__ == "__main__":
    OGWallpaperApp().run()
