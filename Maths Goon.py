import random
import time
from tkinter import *
from tkinter import messagebox
import os


try:
   from playsound import playsound
   sound_available = True
except ImportError:
   sound_available = False


class Question:
   def __init__(self):
       self.operations = ['+', '-', '*', '/']
       self.generate_question()


   def generate_question(self):
       operation = random.choice(self.operations)
       if operation == '+':
           self.generate_addition()
       elif operation == '-':
           self.generate_subtraction()
       elif operation == '*':
           self.generate_multiplication()
       else:
           self.generate_division()


   def generate_addition(self):
       self.num1 = random.randint(1, 12)
       self.num2 = random.randint(1, 12)
       self.operation = '+'
       self.answer = self.num1 + self.num2


   def generate_subtraction(self):
       self.num1 = random.randint(1, 12)
       self.num2 = random.randint(1, self.num1)
       self.operation = '-'
       self.answer = self.num1 - self.num2


   def generate_multiplication(self):
       self.num1 = random.randint(1, 12)
       self.num2 = random.randint(1, 12)
       self.operation = '×'
       self.answer = self.num1 * self.num2


   def generate_division(self):
       self.num2 = random.randint(1, 12)
       self.answer = random.randint(1, 12)
       self.num1 = self.num2 * self.answer
       self.operation = '÷'


   def get_question_text(self):
       return f"{self.num1} {self.operation} {self.num2} = ?"


class Game:
   def __init__(self, level='E'):
       self.level = level
       self.score = 0
       self.question_count = 0
       self.current_question = None
       self.timer_value = 0
       self.max_questions = 10
       if level == 1:
           self.time_limit = 20
       elif level == 2:
           self.time_limit = 10
       else:
           self.time_limit = 0


   def generate_question(self):
       self.current_question = Question()
       return self.current_question


   def check_answer(self, user_answer):
       try:
           return int(user_answer) == self.current_question.answer
       except ValueError:
           return False


   def update_score(self):
       self.score += 1


   def next_question(self):
       self.question_count += 1
       return self.question_count < self.max_questions


   def get_results(self):
       percentage = (self.score / self.max_questions) * 100
       return {
           'score': self.score,
           'total': self.max_questions,
           'percentage': percentage
       }


class MathsGoon:
   def __init__(self, root):
       self.root = root
       self.root.title("Maths Goon")
       self.root.geometry("400x500")
       self.root.resizable(False, False)
       self.bg_color = "#FFFFFF"
       self.primary_color = "#000000"
       self.accent_color = "#007ACC"
       self.secondary_color = "#555555"
       self.success_color = "#4CAF50"
       self.error_color = "#F44336"
       self.root.configure(bg=self.bg_color)
       self.game = None
       self.timer_id = None
       self.welcome_frame = Frame(self.root, bg=self.bg_color)
       self.game_frame = Frame(self.root, bg=self.bg_color)
       self.results_frame = Frame(self.root, bg=self.bg_color)
       self.fps_counter = 0
       self.last_fps_time = time.time()
       self.setup_welcome_screen()
       self.setup_game_screen()
       self.setup_results_screen()
       self.show_welcome_screen()


   def setup_welcome_screen(self):
       Label(self.welcome_frame, text="Maths Goon", font=("Helvetica", 32, "bold"), bg=self.bg_color, fg=self.primary_color).pack(pady=20)
       Label(self.welcome_frame, text="Simple and engaging maths practice.", font=("Helvetica", 16), bg=self.bg_color, fg=self.secondary_color).pack(pady=10)
       Label(self.welcome_frame, text="Select Difficulty Level:", font=("Helvetica", 14), bg=self.bg_color, fg=self.primary_color).pack(pady=10)
       level_frame = Frame(self.welcome_frame, bg=self.bg_color)
       level_frame.pack(pady=10)
       levels = [("Level E: No Time Limit", 'E'), ("Level 1: 20 Second Limit", 1), ("Level 2: 10 Second Limit", 2)]
       self.level_var = StringVar()
       self.level_var.set('E')
       for text, level in levels:
           Radiobutton(level_frame, text=text, variable=self.level_var, value=level, font=("Helvetica", 12), bg=self.bg_color, fg=self.primary_color, activeforeground=self.primary_color, activebackground=self.bg_color).pack(anchor=W, pady=5)
       Button(self.welcome_frame, text="Start Game", font=("Helvetica", 14, "bold"), bg=self.accent_color, fg="#FFFFFF", command=self.start_game, padx=20, pady=10, relief=RAISED, bd=0).pack(pady=20)
       Button(self.welcome_frame, text="Help", font=("Helvetica", 12), bg=self.secondary_color, fg="#FFFFFF", command=self.show_help, padx=10, pady=5, relief=RAISED, bd=0).pack(pady=10)


   def setup_game_screen(self):
       info_frame = Frame(self.game_frame, bg=self.bg_color)
       info_frame.pack(fill=X, pady=10)
       self.timer_label = Label(info_frame, text="Time: --", font=("Helvetica", 14), bg=self.bg_color, fg=self.primary_color)
       self.timer_label.pack(side=LEFT, padx=20)
       self.question_counter = Label(info_frame, text="Question: 1/10", font=("Helvetica", 14), bg=self.bg_color, fg=self.primary_color)
       self.question_counter.pack(side=RIGHT, padx=20)
       self.fps_label = Label(info_frame, text="FPS: --", font=("Helvetica", 10), bg=self.bg_color, fg=self.primary_color)
       self.fps_label.pack(side=RIGHT, padx=20)
       self.score_label = Label(self.game_frame, text="Score: 0", font=("Helvetica", 16, "bold"), bg=self.bg_color, fg=self.accent_color)
       self.score_label.pack(pady=10)
       self.question_label = Label(self.game_frame, text="", font=("Helvetica", 24, "bold"), bg=self.bg_color, fg=self.primary_color)
       self.question_label.pack(pady=20)
       self.answer_var = StringVar()
       self.answer_entry = Entry(self.game_frame, textvariable=self.answer_var, font=("Helvetica", 18), width=10, justify=CENTER, bd=1, relief=SOLID)
       self.answer_entry.pack(pady=10)
       numpad_frame = Frame(self.game_frame, bg=self.bg_color)
       numpad_frame.pack(pady=20)
       for i in range(3):
           for j in range(3):
               num = i * 3 + j + 1
               Button(numpad_frame, text=str(num), font=("Helvetica", 14), width=3, height=1, bg=self.bg_color, fg=self.primary_color, bd=1, relief=SOLID, command=lambda n=num: self.add_to_answer(n)).grid(row=i, column=j, padx=5, pady=5)
       Button(numpad_frame, text="0", font=("Helvetica", 14), width=3, height=1, bg=self.bg_color, fg=self.primary_color, bd=1, relief=SOLID, command=lambda: self.add_to_answer(0)).grid(row=3, column=1, padx=5, pady=5)
       Button(numpad_frame, text="C", font=("Helvetica", 14), width=3, height=1, bg=self.error_color, fg="#FFFFFF", bd=1, relief=SOLID, command=self.clear_answer).grid(row=3, column=0, padx=5, pady=5)
       Button(numpad_frame, text="✓", font=("Helvetica", 14), width=3, height=1, bg=self.success_color, fg="#FFFFFF", bd=1, relief=SOLID, command=self.submit_answer).grid(row=3, column=2, padx=5, pady=5)


   def setup_results_screen(self):
       Label(self.results_frame, text="Game Results", font=("Helvetica", 24, "bold"), bg=self.bg_color, fg=self.primary_color).pack(pady=20)
       self.results_label = Label(self.results_frame, text="", font=("Helvetica", 18), bg=self.bg_color, fg=self.primary_color)
       self.results_label.pack(pady=20)
       self.feedback_label = Label(self.results_frame, text="", font=("Helvetica", 16), bg=self.bg_color, fg=self.secondary_color)
       self.feedback_label.pack(pady=10)
       button_frame = Frame(self.results_frame, bg=self.bg_color)
       button_frame.pack(pady=20)
       Button(button_frame, text="Play Again", font=("Helvetica", 14), bg=self.success_color, fg="#FFFFFF", command=self.restart_game, padx=10, pady=5, bd=0).pack(side=LEFT, padx=10)
       Button(button_frame, text="Main Menu", font=("Helvetica", 14), bg=self.primary_color, fg="#FFFFFF", command=self.show_welcome_screen, padx=10, pady=5, bd=0).pack(side=RIGHT, padx=10)


   def show_welcome_screen(self):
       self.game_frame.pack_forget()
       self.results_frame.pack_forget()
       self.welcome_frame.pack(fill=BOTH, expand=True)


   def show_game_screen(self):
       self.welcome_frame.pack_forget()
       self.results_frame.pack_forget()
       self.game_frame.pack(fill=BOTH, expand=True)
       self.answer_entry.focus_set()
       self.last_fps_time = time.time()
       self.fps_counter = 0
       self.update_fps_loop()


   def show_results_screen(self):
       if self.timer_id:
           self.root.after_cancel(self.timer_id)
           self.timer_id = None
       self.welcome_frame.pack_forget()
       self.game_frame.pack_forget()
       results = self.game.get_results()
       self.results_label.config(text=f"Score: {results['score']}/{results['total']}\n{results['percentage']}%")
       if results['percentage'] >= 90:
           feedback = "Excellent job! You're a maths wizard!"
           self.feedback_label.config(fg=self.success_color)
       elif results['percentage'] >= 70:
           feedback = "Great work! Keep practising!"
           self.feedback_label.config(fg=self.success_color)
       elif results['percentage'] >= 50:
           feedback = "Good effort! You're improving!"
           self.feedback_label.config(fg=self.secondary_color)
       else:
           feedback = "Keep practising, you'll get better!"
           self.feedback_label.config(fg=self.error_color)
       self.feedback_label.config(text=feedback)
       self.results_frame.pack(fill=BOTH, expand=True)
       self.play_sound("complete")
   #ALSO ADDED THE HELP BUTTON
   def show_help(self):
       message = ("Maths Goon Instructions:\n\n"
                  "Answer the arithmetic questions by entering the correct number.\n"
                  "Select a difficulty level:\n"
                  "Level E: No Time Limit\n"
                  "Level 1: 20 Second Limit\n"
                  "Level 2: 10 Second Limit\n\n"
                  "Use the on-screen number pad to enter your answer.\n"
                  "Good luck!")
       messagebox.showinfo("Help", message)


   def start_game(self):
       level = self.level_var.get()
       self.game = Game(level)
       self.clear_answer()
       self.score_label.config(text="Score: 0")
       self.show_game_screen()
       self.display_question()


   def restart_game(self):
       self.start_game()


   def display_question(self):
       question = self.game.generate_question()
       self.question_label.config(text=question.get_question_text())
       self.question_counter.config(text=f"Question: {self.game.question_count + 1}/{self.game.max_questions}")
       if self.game.time_limit > 0:
           self.start_timer()


   def start_timer(self):
       if self.timer_id:
           self.root.after_cancel(self.timer_id)
       self.game.timer_value = self.game.time_limit
       self.update_timer()


   def update_timer(self):
       if self.game.timer_value <= 0:
           self.timer_label.config(text="Time's up!", fg=self.error_color)
           self.play_sound("wrong")
           self.root.after(1000, self.process_next_question)
           return
       if self.game.timer_value <= 5:
           self.timer_label.config(fg=self.error_color)
           if self.game.timer_value == 5:
               self.play_sound("tick")
       else:
           self.timer_label.config(fg=self.primary_color)
       self.timer_label.config(text=f"Time: {self.game.timer_value}")
       self.game.timer_value -= 1
       self.timer_id = self.root.after(1000, self.update_timer)


   def add_to_answer(self, num):
       current = self.answer_var.get()
       self.answer_var.set(current + str(num))
       self.play_sound("click")


   def clear_answer(self):
       self.answer_var.set("")
       self.play_sound("click")


   def submit_answer(self):
       user_answer = self.answer_var.get()
       if not user_answer:
           return
       if self.game.check_answer(user_answer):
           self.game.update_score()
           self.score_label.config(text=f"Score: {self.game.score}")
           self.play_sound("correct")
           self.answer_entry.config(bg=self.success_color)
       else:
           self.play_sound("wrong")
           self.answer_entry.config(bg=self.error_color)
       self.root.after(500, lambda: self.answer_entry.config(bg="white"))
       self.root.after(1000, self.process_next_question)


   def process_next_question(self):
       if self.timer_id:
           self.root.after_cancel(self.timer_id)
           self.timer_id = None
       self.clear_answer()
       if self.game.next_question():
           self.display_question()
       else:
           self.show_results_screen()
 #ADDED THE FPS COUNTER
   def update_fps_loop(self):
       self.fps_counter += 1
       current_time = time.time()
       elapsed = current_time - self.last_fps_time
       if elapsed >= 1.0:
           fps = self.fps_counter / elapsed
           self.fps_label.config(text=f"FPS: {int(fps)}")
           self.fps_counter = 0
           self.last_fps_time = current_time
       self.root.after(16, self.update_fps_loop)


   def play_sound(self, sound_type):
       if not sound_available:
           return
       sounds = {
           "correct": "sounds/correct.wav",
           "wrong": "sounds/wrong.wav",
           "click": "sounds/click.wav",
           "tick": "sounds/tick.wav",
           "complete": "sounds/complete.wav"
       }
      


if __name__ == "__main__":
   root = Tk()
   app = MathsGoon(root)
   root.mainloop()
