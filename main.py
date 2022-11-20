import time
import tkinter as tk
import threading
import random
from tkinter import filedialog as fd
import datetime


class KeyboardTraining:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Клавиатурный тренажёр")
        self.root.wm_attributes('-fullscreen', True)

        self.default_font = "Comic Sans MS"

        self.source = open("text.txt", "r")
        self.text = self.source.read().split('\n')

        self.is_running = False
        self.seconds = 0
        self.mistake_counter = 0

        self.start_menu()
        self.root.mainloop()

        self.source.close()

    def choose_file(self):
        self.file_selection = fd.askopenfilename()
        self.text = open(self.file_selection, 'r').read().split('\n')

    def start_menu(self):
        self.startGUI = tk.Frame(self.root)

        self.input_line = tk.Label(self.startGUI, text="Клавиатурный тренажер \nВерсия 1.0",
                                   font=(self.default_font, 24))
        self.input_line.grid(row=0, column=0)

        self.start_button = tk.Button(self.startGUI, command=self.game, text="Начать!", font=(self.default_font, 24),
                                      width=13, height=3)
        self.start_button.grid(row=1, column=0)

        self.chosee_button = tk.Button(self.startGUI, command=self.choose_file, text="Выберите файл",
                                       font=(self.default_font, 24), width=13, height=3)
        self.chosee_button.grid(row=2, column=0)

        self.startGUI.place(relx=0.5, rely=0.5, anchor='center')

    def is_valid(self, string):
        if not self.game_line.cget('text').startswith(string):
            self.mistake_counter += 1
        if self.game_line.cget('text')[:] == string:
            self.is_running = False
            self.game_input.config(fg="green")
            self.save_file = open("stats.txt", 'a')
            self.save_file.write("\nDate: \n" +
                                 str(datetime.datetime.now()) + '\n\n' + "Stats:\nChars per seconds: {0:.2f}\nTime: {1:.2f}\nMistakes: {2}\n".format(
                self.cps, self.seconds,
                self.mistake_counter))
            self.save_file.close()
        return self.game_line.cget('text').startswith(string)

    def game(self):
        self.startGUI.destroy()

        self.root.update()

        self.gameGUI = tk.Frame(self.root)
        self.statsGUI = tk.Frame(self.root)

        self.current_line = random.choice(self.text)
        self.game_line = tk.Label(self.gameGUI, text=self.current_line, font=("Comic Sans MS", 16))
        self.game_line.grid(row=0, column=0, padx=4, pady=4)

        self.check = (self.root.register(self.is_valid), "%P")

        self.game_input = tk.Entry(self.gameGUI, fg="black", width=60, font=(self.default_font, 15), validate='key',
                                   validatecommand=self.check)
        self.game_input.grid(row=1, column=0, padx=4, pady=4)
        self.game_input.bind("<KeyPress>", self.start)

        self.game_stats = tk.Label(self.statsGUI, font=(self.default_font, 15),
                                   text="Статистика:\nСимволов в секунду: 0.00\nВремя: 0.00\nОшикби: 0")
        self.game_stats.grid(row=2, column=0, padx=4, pady=4)

        self.restart_button = tk.Button(self.gameGUI, text='Сначала', font=(self.default_font, 15),
                                        command=self.restart)
        self.restart_button.grid(row=3, column=0)

        self.statsGUI.place(relx='0.1', rely='0.5', anchor='center')
        self.gameGUI.place(relx='0.5', rely='0.5', anchor='center')
        self.game_input.focus()

    def start(self, event):
        if not self.is_running:
            if event.keycode in [i for i in range(65, 91)]:  # ASCII код букв a-z
                self.is_running = True
                timer = threading.Thread(target=self.timer_thread)
                timer.start()

    def timer_thread(self):
        while self.is_running:
            time.sleep(0.1)
            self.seconds += 0.1
            self.cps = len(self.game_input.get()) / self.seconds
            self.game_stats.config(font=(self.default_font, 15),
                                   text="Статистика:\nСимволов в секунду: {0:.2f}\nВремя: {1:.2f}\nОшибки: {2}".format(
                                       self.cps, self.seconds,
                                       self.mistake_counter))

    def restart(self):
        self.is_running = False
        self.seconds = 0
        self.mistake_counter = 0
        self.cps = 0

        self.gameGUI.destroy()
        self.startGUI.destroy()

        self.game()


if __name__ == '__main__':
    game = KeyboardTraining()
