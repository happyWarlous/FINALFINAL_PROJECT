import time
import tkinter as tk
import threading
import random
from tkinter import filedialog as fd


class KeyboardTraining:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Клавиатурный тренажёр")
        self.root.geometry("800x600")

        self.source = open("text.txt", "r")

        self.is_running = False
        self.seconds = 0
        self.mistake_counter = 0

        self.start_menu()
        self.root.mainloop()

        self.source.close()

    def is_valid(self, string):
        print(string)
        print(self.game_line.cget('text'))
        if not self.game_line.cget('text').startswith(string):
            self.mistake_counter += 1
        return self.game_line.cget('text').startswith(string)

    def start_menu(self):
        self.startGUI = tk.Frame(self.root)

        self.input_line = tk.Label(self.startGUI, text="Клавиатурный тренажер \nВерсия 1.0", font=("Comic Sans MS", 24))
        self.input_line.grid(row=0, column=0)

        self.start_button = tk.Button(self.startGUI, command=self.game, text="Начать!", font=("Comic Sans", 24),
                                      width=15, height=5)
        self.start_button.grid(row=1, column=0)

        self.chosee_button = tk.Button(self.startGUI, command=self.choose_file, text="Выберите файл",
                                       font=("Comic Sans", 24), width=15, height=5)
        self.chosee_button.grid(row=2, column=0)

        self.startGUI.place(relx=0.5, rely=0.5, anchor='center')

    def choose_file(self):
        self.file_selection = fd.askopenfilename()
        self.current_file = open(self.file_selection, 'r')
        self.source = self.current_file

    def game(self):
        self.input_line.destroy()
        self.start_button.destroy()
        self.startGUI.destroy()

        self.root.update()

        self.current_line = random.choice(self.source.read().split('\n'))

        self.gameGUI = tk.Frame(self.root)
        self.statsGUI = tk.Frame(self.root)

        self.game_line = tk.Label(self.gameGUI, text=self.current_line)
        self.game_line.grid(row=0, column=0)

        self.check = (self.root.register(self.is_valid), "%P")

        self.game_input = tk.Entry(self.gameGUI, width=40, validate='key', validatecommand=self.check)
        self.game_input.grid(row=1, column=0)
        self.game_input.bind("<KeyPress>", self.start)

        self.game_stats = tk.Label(self.statsGUI, text="Статистика:\nСимволов в секунду: 0.00\nВремя: 0.00\nОшикби: 0")
        self.game_stats.grid(row=2, column=0)

        self.restart_button = tk.Button(self.gameGUI, text='Сначала', command=self.restart)
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
        if self.game_input.get() == self.game_line.cget('text')[:-1]:
            self.is_running = False
            self.game_input.config(fg="green")

    def timer_thread(self):
        while self.is_running:
            time.sleep(0.1)
            self.seconds += 0.1
            cps = len(self.game_input.get()) / self.seconds
            self.game_stats.config(
                text="Статистика:\nСимволов в секунду: {0:.2f}\nВремя: {1:.2f}\nОшибки: {2}".format(cps, self.seconds,
                                                                                                    self.mistake_counter))

    def restart(self):
        self.is_running = False
        self.seconds = 0.1
        self.game_input.delete(0, tk.END)
        self.game


if __name__ == '__main__':
    game = KeyboardTraining()
