import tkinter

import customtkinter
from customtkinter import CTkFrame, CTkLabel
import functions as fu

class Login(customtkinter.CTk):
    MAIN_COLOR = "#3489cc"
    TEXT_COLOR = "#FFF"
    BORDER_COLOR = "#DDD"
    FONT_FAMILY ='Trebuchet MS'
    FONT_SIZE = 14

    #MESSAGE_COLORS
    #('bg_color', 'text_color', 'border_color')
    ERROR_MESSAGE_STYLE = ('#f8d7da', '#842029', '#f5c2c7')
    INFO_MESSAGE_STYLE = ('#cfe2ff', '#084298', '#b6d4fe')
    SUCCESS_MESSAGE_STYLE = ('#d1e7dd', '#0f5132', '#badbcc')
    # Layout constants
    WINDOW_SIZE = "295x300"
    LOGIN_TAG = None
    LOGIN_STORAGE = None
    INFO_MESSAGE = None
    def handle_login(self):
        (self.LOGIN_TAG, self.LOGIN_STORAGE, self.INFO_MESSAGE) = fu.waterp_login(self.username_textbox.get(), self.password_textbox.get())
        if self.LOGIN_TAG == 1 and self.LOGIN_STORAGE != None:
            try:
                self.show_message_container()
                import gui
                self.withdraw()
                gui.App().mainloop()
                # self.quit()  # Exit the mainloop

            except ImportError as e:
                self.show_message_container(f"Error importing gui.py {e}", 'error')

        else:
            # Handle failed login
            self.show_message_container()
            # You might want to show an error message to the user
    def activate_login_btn(self):
        if self.username_textbox.get() and self.password_textbox.get():
            self.login_button.configure(state = 'normal')
        else: self.login_button.configure(state = 'disabled')
    def hide_message_container(self):
        if self.message_frame_container:
            self.message_frame_container.grid_forget()
            self.message_frame_container = None
            self.message_label = None
    def show_message_container(self, message = None, type = None):
        if self.message_frame_container:
            self.hide_message_container()
        self.message_frame_container = CTkFrame(self, width=280, corner_radius=8, fg_color=self._fg_color,
                                                cursor="hand2")
        self.message_frame_container.grid(row=5, column=0, sticky='ns', padx=5, pady=(25, 0))

        self.message_label = CTkLabel(self.message_frame_container, width=275, wraplength=265,
                                      justify=tkinter.CENTER, text='', cursor="hand2")
        self.message_label.grid(row=0, column=0, sticky='ns', padx=5, pady=5, ipady=5)
        self.message_label.bind("<Button-1>", lambda event: self.hide_message_container())
        if message == None and type == None:
            if self.LOGIN_TAG == 1:
                self.message_frame_container.configure(fg_color=self.SUCCESS_MESSAGE_STYLE[0], border_width=2, border_color=self.SUCCESS_MESSAGE_STYLE[2])
                self.message_label.configure(text_color = self.SUCCESS_MESSAGE_STYLE[1])
            else:
                self.message_frame_container.configure(fg_color=self.ERROR_MESSAGE_STYLE[0], border_width=2, border_color=self.ERROR_MESSAGE_STYLE[2])
                self.message_label.configure(text_color = self.ERROR_MESSAGE_STYLE[1])

            self.message_label.configure(text = self.INFO_MESSAGE)

        else:
            if type == 'error':
                self.message_frame_container.configure(fg_color=self.ERROR_MESSAGE_STYLE[0], border_width=2, border_color=self.ERROR_MESSAGE_STYLE[2])
                self.message_label.configure(text_color = self.ERROR_MESSAGE_STYLE[1])
                self.message_label.configure(text=message)

    def __init__(self):

        super().__init__()

        ### WINDOW CONFIG ###
        self.title("my app")
        self.geometry(self.WINDOW_SIZE)
        self.configure(fg_color=self.MAIN_COLOR)
        self.resizable(False, False)

        # MESSAGE_FRAME_CONTAINER HIDDEN BY DEFAULT
        self.message_frame_container = None
        self.message_label = None


        #WIDGETS: CREATION + POSITIONNING
        self.username_textbox = customtkinter.CTkEntry(self,width=250,
                                                       height =20,
                                                       border_width= 0,
                                                       corner_radius=0,
                                                       placeholder_text="nazih.k",
                                                       placeholder_text_color= "#DDD",
                                                       text_color=self.TEXT_COLOR,
                                                       font = customtkinter.CTkFont(family= self.FONT_FAMILY, size=self.FONT_SIZE),
                                                       fg_color= self._fg_color
                                                  )

        self.username_border = customtkinter.CTkFrame(self, height= 2, width = 240, fg_color="#DDD", corner_radius=0)


        self.password_textbox = customtkinter.CTkEntry(self,width=250,
                                                       height =20,
                                                       border_width= 0,
                                                       corner_radius=0,
                                                       placeholder_text="Log2W@t3rp",
                                                       show = '*',
                                                       placeholder_text_color= "#EEE",
                                                       text_color = self.TEXT_COLOR,
                                                       font = customtkinter.CTkFont(family= self.FONT_FAMILY, size=self.FONT_SIZE),
                                                       fg_color= self._fg_color,
                                                       )


        self.password_border = customtkinter.CTkFrame(self, height=2, width = 240, fg_color = self.BORDER_COLOR, corner_radius=0 )

        self.login_button = customtkinter.CTkButton(self,
                                                      text = "Connexion",
                                                      corner_radius = 0,
                                                      width = 100,
                                                      state= customtkinter.DISABLED,
                                                      text_color= "#3489cc",
                                                      font =  customtkinter.CTkFont(family= self.FONT_FAMILY, size=self.FONT_SIZE),
                                                      fg_color = "#FFF",
                                                      command= lambda : self.handle_login()
                                                    )


        self.username_textbox.grid(row = 0, column = 0, padx=(20,0), pady=(25,0))
        self.username_border.grid(row = 1, column = 0, padx=(20, 0), pady=(0, 20))
        self.password_textbox.grid(row = 2, column = 0, padx=(20,0), pady=(25,0))
        self.password_border.grid(row = 3, column = 0, padx=(20, 0), pady=(0, 20))
        self.login_button.grid(row = 4, column = 0, sticky = 'ns')

        self.username_textbox.bind("<KeyRelease>", lambda e: self.activate_login_btn())
        self.password_textbox.bind("<KeyRelease>", lambda e: self.activate_login_btn())

        self.username_textbox.insert(0, "khounch.s")
        self.password_textbox.insert(0, "Form2026*")

if __name__ == "__main__":
    login_gui = Login()
    login_gui.mainloop()
