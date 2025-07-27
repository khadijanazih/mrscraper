# main.py
import tkinter
import customtkinter
from customtkinter import CTkFrame

import functions as fu
import threading

customtkinter.set_default_color_theme("dark-blue")
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        ### WINDOW CONFIG ###
        self.title("my app")
        self.geometry("580x800")
        self.grid_columnconfigure(1, weight=1)
        self.resizable(False, False)
        self.configure(fg_color="#FEFEFE")

        #GUI VARIABLES
        self.radio_option = tkinter.StringVar(value="")
        self.check_value = tkinter.BooleanVar(value=False)
        self.combo_selected   = tkinter.StringVar(value = "")
        self.extracted_data = None
        self.execution_var = None
        self.start_time = None
        self.end_time = None
        self.exported_filepath = None
        ### COMPONENTS ###

            ## 0 - Workflow indicators
        self.workflow_frame = customtkinter.CTkFrame(self, corner_radius=10, border_width=0, border_color="",fg_color="#F8F8F8")
        self.workflow_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        self.number_frames = []
        self.number_labels = []
        for i in range(4):
            self.workflow_frame.grid_columnconfigure(i, weight=1)#Distribute_steps

            self.number_frame = customtkinter.CTkFrame(self.workflow_frame, width=38, height=38, corner_radius=38,fg_color="#e9ecef")#inactive: #e9ecef | active :#007bff | complete:#28a745
            self.number_frame.grid(row=0, column=i , sticky="", padx=20, pady=10)
            self.number_frame.grid_propagate(False)#Prevents the frame to resize to fit content "Don't grow please :) "

            self.number_label = customtkinter.CTkLabel(self.number_frame, text=f"{i+1}", text_color="#6c757d")
            self.number_label.place(relx=0.5, rely=0.5, anchor="center")

            self.step_label = customtkinter.CTkLabel(self.workflow_frame,width=80, wraplength=80, text_color="#0774be", text="Export")
            self.step_label.grid(row=1, column=i, sticky="", padx=20, pady=(0, 8))

            self.number_frames.append(self.number_frame)
            self.number_labels.append(self.number_label)

        self.ofd_frame = customtkinter.CTkFrame(self, corner_radius=8, border_width = 1, border_color="#CCC", fg_color="transparent")
        self.ofd_frame.grid(row = 2, column = 0, columnspan = 2, sticky="ew", padx=20, pady = 15 )

        self.ofd_frame.grid_columnconfigure(0, weight=0)  # Label column - fixed width
        self.ofd_frame.grid_columnconfigure(1, weight=1)  # Content column - can expand

        ## 1 - Open File Dialog ##
        self.file_textbox = customtkinter.CTkEntry(self.ofd_frame,width=400, height =35, corner_radius=5, border_color="#EEE", fg_color="transparent")
        self.file_textbox.grid(row = 0, column = 0, padx=(20,0), pady=10)

        # Pass 'self' to openfile_dialog
        self.browse_button = customtkinter.CTkButton(self.ofd_frame, text="Parcourir...", border_color="#0774be", height =30, corner_radius=2, width= 150, command= lambda :fu.openfile_dialog(self))
        self.browse_button.grid(row = 0, column = 1, padx=20, pady=20)

        self.file_path_label = customtkinter.CTkLabel(self.ofd_frame, text ="Fichier : ", text_color="#0774be")
        self.file_path_label.grid(row=1, column=0, padx=20, pady = 5, sticky="w")

        self.select_sheet_label = customtkinter.CTkLabel(self.ofd_frame, text="Selectionner Une Feuille : ", text_color="#0774be")
        self.select_sheet_label.grid(row=2, column=0, padx=(20,0), pady=5, sticky="w")

        self.sheet_combo = customtkinter.CTkComboBox(self.ofd_frame, width= 350, height =35, corner_radius= 5, border_color="#EEE", values = [''], state= tkinter.DISABLED, fg_color="#FEFEFE")
        self.sheet_combo.grid(row=2, column=0, padx = (0,20), pady = (5,10) , sticky = "e" ,columnspan =2)


            ## 2 - Frame Design ##
        self.process_frame = customtkinter.CTkFrame(self, corner_radius=8, border_width = 1, border_color="#CCC", fg_color="transparent")
        self.process_frame.grid(row = 3, column = 0, columnspan = 2, sticky="ew", padx=20, pady = 15)
        self.process_frame.grid_columnconfigure(0, weight=0)  # Label column - fixed width
        self.process_frame.grid_columnconfigure(1, weight=1)  # Content column - can expand
            ## 3 - Frame Elements ##
        self.print_radio = customtkinter.CTkRadioButton(
            self.process_frame,
            text ="Impression des Factures",
            border_width_unchecked = 2,
            border_width_checked = 6,
            border_color = "#0774be",
            variable = self.radio_option,
            value ="print",
            hover = True)


        self.pns_radio = customtkinter.CTkRadioButton(
            self.process_frame,
            text ="Extraction des PNS",
            border_width_unchecked = 2,
            border_width_checked = 6,
            border_color="#0774be",
            variable = self.radio_option,
            value="pns",
            hover = True)

        self.logo_check = customtkinter.CTkCheckBox(
            self.process_frame,
            text="Imprimer avec Logo",
            border_color="#0774be",
            border_width=2,
            variable=self.check_value,
            hover=True
        )
        self.print_radio.grid(row=3, column=0, padx=20, pady=10, sticky = "w")
        self.logo_check.grid(row=3, column= 1, padx=5, pady= 10, sticky = "w")
        self.pns_radio.grid(row=4, column= 0, padx=20, pady= 10, sticky = "w")


    #ACTIONS_FRAME
        self.actions_frame = customtkinter.CTkFrame(self, corner_radius=10, border_width=0, border_color="",fg_color="#F9F9F9")
        self.actions_frame.grid(row=4, column=0, columnspan=2, sticky="", padx=20, pady=10)
        self.actions_frame.grid_rowconfigure(1, weight=2)

        # Command for extract_button calls a local handler
        self.extract_button = customtkinter.CTkButton(self.actions_frame, text ="Extraire les données", corner_radius = 0,height = 35, width = 80, command=self._handle_extract)
        self.extract_button.grid(row=1, column = 0, padx=20, pady=20, sticky ="")

        # Command for execute_button calls a local handler
        self.execute_button = customtkinter.CTkButton(self.actions_frame, text ="Exécuter", corner_radius = 0, height = 35, width = 80,state= tkinter.DISABLED, command=self._handle_execute)
        self.execute_button.grid(row=1, column=1, padx=20, pady=20, sticky="")

        self.print_button = customtkinter.CTkButton(self.actions_frame, text ="Télécharger", corner_radius = 0, height = 35, width = 80,command=self._handle_print)
        self.print_button.grid(row=1, column=2, padx=20, pady=20, sticky="")

        self.export_button = customtkinter.CTkButton(self.actions_frame, text ="Exporter", corner_radius = 0, height = 35, width = 80,state= tkinter.DISABLED, command=self._handle_export)
        self.export_button.grid(row=1, column=3, padx=20, pady=20, sticky="")

        self.actions_frame.grid_columnconfigure(0, weight=1)
        self.actions_frame.grid_columnconfigure(1, weight=1)
        self.actions_frame.grid_columnconfigure(2, weight=1)
        self.actions_frame.grid_columnconfigure(3, weight=1)

        self.state_frame = customtkinter.CTkFrame(self.process_frame, corner_radius=5, fg_color="transparent")
        self.state_frame.grid(row=5, column=0, padx= 20, pady=(8,10), sticky = "ew", columnspan = 2)

        self.state_frame.grid_columnconfigure(0, weight=1)
        self.state_frame.grid_columnconfigure(1, weight=0)

        self.state_label = customtkinter.CTkLabel(self.state_frame, fg_color="transparent", text = "", wraplength=380, font = customtkinter.CTkFont(size=12))
        self.state_label.grid(row=0 , column=0, padx= 4, pady=4, sticky="ew")

        self.state_close = customtkinter.CTkLabel(self.state_frame, text ="", cursor ="hand2")
        self.state_close.grid(row = 0, column = 1, padx= (2), pady= 2, sticky ="ne", ipadx = (5), ipady= 0)
        self.state_close.bind("<Button-1>", self._clear_status_message) # Add binding to clear message

        self.progress_title = customtkinter.CTkLabel(self, text_color="#0774be", text = 'Progress:')
        self.progress_title.grid(row=6, column=0, padx=(20, 0), pady=5, sticky="w")

        self.progress_value = customtkinter.CTkLabel(self, text_color="#0774be", text = "-")
        self.progress_value.grid(row=6, column=1, padx= (0,20), pady=5, sticky="e")
        self.update_idletasks()
        self.initiate_wf_state()

#INITIATE_WORKFLOW()
    def initiate_wf_state(self):
        self.number_frames[0].configure(fg_color='#007bff')
        self.number_labels[0].configure(text_color='#FFF')
    def update_wf_state(self):
        if self.file_path_label != None:
            print('file == yes')
        if self.extracted_data != None:
            print('extract == yes')
        if self.exported_filepath != None:
            print("export == yes")
    #This is a MessageBox but speaks Python
    def set_info_msgs(self, theme, message):
        self.after(0, self._update_info_label, theme, message)
    def _update_info_label(self, theme, message):
        if theme == "info":
            self.state_close.configure(text_color='#084298')
            self.state_frame.configure(fg_color='#cfe2ff', border_color='#b6d4fe')
            self.state_label.configure(text_color='#084298')

        elif theme == "alert":
            self.state_close.configure(text_color='#842029')
            self.state_frame.configure(fg_color='#f8d7da', border_color='#f5c2c7')
            self.state_label.configure(text_color='#842029')
        elif theme == "success":
            self.state_close.configure(text_color='#0f5132')
            self.state_frame.configure(fg_color='#d1e7dd', border_color='#badbcc')
            self.state_label.configure(text_color='#0f5132')
        self.state_label.configure(text=message)
        self.state_close.configure(text = 'x')
    def _clear_status_message(self, event=None):
        self.state_label.configure(text="")
        self.state_close.configure(text="")
        self.state_frame.configure(fg_color="transparent", border_color="#CCC")


    #HANDLERS
    def _handle_extract(self):
        # Pass 'self' to fu.extract_data to allow it to call app_instance.set_info_msgs
        self.extracted_data = fu.extract_data(self)
    def _handle_execute(self):
        check_val = self.check_value.get()

        # This progress_callback will be passed to fu.execute
        def progress_callback(label_text, value_text):
            self.after(0, lambda: self.progress_title.configure(text=label_text))
            self.after(0, lambda: self.progress_value.configure(text=value_text))

        # This callback will be passed to the functions in fu.py to update status messages
        def set_info_msgs_callback(theme, message):
            self.set_info_msgs(theme, message)

        def task():
            # Pass the set_info_msgs_callback to fu.execute
            self.execution_var = fu.execute(set_info_msgs_callback, self.extracted_data, check_val, progress_callback, self)
            if isinstance(self.execution_var, tuple) and len(self.execution_var) == 3:
                self.start_time = self.execution_var[1]
                self.end_time = self.execution_var[2]
                self.after(0, lambda: self.progress_title.configure(text="✅ Terminé"))
                self.after(0, lambda: self.progress_value.configure(text="✔️"))
            self.after(0, lambda: self.execute_button.configure(state="normal")) # Re-enable browse_button after task finishes

        # self.execute_button.configure(state="disabled") # Disable browse_button while processing
        threading.Thread(target=task).start()
    def _handle_print(self):
        # No change needed here if print_editions doesn't update GUI
        threading.Thread(target=lambda: fu.print_editions(self.start_time, self.end_time)).start()
    def _handle_export(self):
        # This progress_callback will be passed to fu.execute
        def progress_callback(label_text, value_text):
            self.after(0, lambda: self.progress_title.configure(text=label_text))
            self.after(0, lambda: self.progress_value.configure(text=value_text))

        # This callback will be passed to the functions in fu.py to update status messages
        def set_info_msgs_callback(theme, message):
            self.set_info_msgs(theme, message)

        def task():
            # Pass the set_info_msgs_callback to fu.execute
            self.exported_filepath = fu.export_pns_to_execl(set_info_msgs_callback, self.execution_var)
            if self.exported_filepath:
                self.after(0, lambda: self.progress_title.configure(text="✅ Terminé"))
                self.after(0, lambda: self.progress_value.configure(text="✔️"))

            self.after(0, lambda: self.execute_button.configure(state="normal"))  # Re-enable browse_button after task finishes

        # self.export_button.configure(state="disabled")  # Disable browse_button while processing
        threading.Thread(target=task).start()

if __name__ == "__main__":
    app = App()
    app.mainloop()