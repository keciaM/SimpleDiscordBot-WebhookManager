from customtkinter import *
import tkinter as tk
from scripts.config import discord_bot_version, GUI_build_number
import sys

class MainApp():
    def __init__(self):
        self.app = CTk()
        self.app.title(f"SimpleDiscordBot Launcher v{GUI_build_number}")
        self.app.geometry("1280x720")

        self.app.mainloop()

if __name__ == "__main__":
    app = MainApp()


    
