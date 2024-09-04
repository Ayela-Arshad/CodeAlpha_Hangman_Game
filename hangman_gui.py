import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from hangman_game import get_random_word, get_word_meaning

def load_hangman_image(tries):
    images = [
        "hangman6.png",  # The final state image
        "hangman5.png",
        "hangman4.png",
        "hangman3.png",
        "hangman2.png",
        "hangman1.png",
        "hangman0.png",  # Initial empty state image
    ]
    return ImageTk.PhotoImage(Image.open(images[tries]))

class HangmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.root.geometry("600x500")
        self.root.config(bg="#2F4F4F")  # Dark Slate Gray

        self.word = get_random_word()
        self.word_completion = "_" * len(self.word)
        self.tries = 6
        self.guessed_letters = []
        self.wrong_letters = []

        # Frame for aligning hangman and word display
        self.top_frame = tk.Frame(self.root, bg="#2F4F4F")
        self.top_frame.pack(pady=10)

        # Hangman display with image
        self.hangman_image = load_hangman_image(self.tries)
        self.hangman_label = tk.Label(self.top_frame, image=self.hangman_image, bg="#2F4F4F")
        self.hangman_label.grid(row=0, column=0, sticky="w")

        # Word display
        self.word_label = tk.Label(self.top_frame, text=" ".join(self.word_completion), font=("Helvetica", 24), bg="#2F4F4F", fg="#FFFFFF")  # White Text
        self.word_label.grid(row=1, column=0, pady=20)

        # Entry field for guesses
        self.guess_entry = tk.Entry(self.root, font=("Helvetica", 18), bg="#444444", fg="#FFFFFF")  # Dark Gray Background with White Text
        self.guess_entry.pack(pady=10)
        self.guess_entry.bind("<Return>", self.make_guess)

        # Buttons and displays
        self.guess_button = tk.Button(self.root, text="Guess", command=self.make_guess, font=("Helvetica", 16), bg="#20B2AA", fg="#FFFFFF")  # Light Sea Green Background with White Text
        self.guess_button.pack(pady=10)

        self.attempts_label = tk.Label(self.root, text=f"Attempts left: {self.tries}", font=("Helvetica", 14), bg="#2F4F4F", fg="#FFFFFF")  # Dark Slate Gray Background with White Text
        self.attempts_label.pack(pady=10)

        self.wrong_label = tk.Label(self.root, text="Wrong letters: ", font=("Helvetica", 14), bg="#2F4F4F", fg="#FFFFFF")  # Dark Slate Gray Background with White Text
        self.wrong_label.pack(pady=10)

        self.right_label = tk.Label(self.root, text="Right letters: ", font=("Helvetica", 14), bg="#2F4F4F", fg="#FFFFFF")  # Dark Slate Gray Background with White Text
        self.right_label.pack(pady=10)

        # Message display panel
        self.message_panel = tk.Label(self.root, text="", font=("Helvetica", 14), bg="#333333", fg="#FFFFFF", wraplength=900, justify="left")  # Dark Charcoal Background with White Text
        self.message_panel.pack(pady=(10, 10), fill=tk.BOTH, expand=True)

        # Restart button in the top left corner
        self.restart_button = tk.Button(self.root, text="Restart", command=self.restart_game, font=("Helvetica", 16), bg="#696969", fg="#FFFFFF", width=10, height=1)  # Dim Gray Background with White Text
        self.restart_button.place(x=10, y=10, anchor="nw")  # Position at the top left corner

        # Quit button in the top right corner
        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.quit, font=("Helvetica", 16), bg="#696969", fg="#FFFFFF", width=10, height=1)  # Dim Gray Background with White Text
        self.quit_button.place(relx=1.0, y=10, anchor="ne", x=-10)  # Position at the top right corner

    def make_guess(self, event=None):
        guess = self.guess_entry.get().lower()
        self.guess_entry.delete(0, tk.END)

        if len(guess) == 1 and guess.isalpha():
            if guess in self.guessed_letters or guess in self.wrong_letters:
                self.update_message(f"You already guessed the letter '{guess}'.")
            elif guess not in self.word:
                self.tries -= 1
                self.wrong_letters.append(guess)
                self.update_gui()
                self.update_message(f"'{guess}' is not in the word.")
            else:
                self.guessed_letters.append(guess)
                word_as_list = list(self.word_completion)
                indices = [i for i, letter in enumerate(self.word) if letter == guess]
                for index in indices:
                    word_as_list[index] = guess
                self.word_completion = "".join(word_as_list)
                self.update_gui()
                self.update_message(f"Good job! '{guess}' is in the word!")
                if "_" not in self.word_completion:
                    self.update_message("Congratulations, you guessed the word!")
                    self.ask_for_meaning()
        elif len(guess) == len(self.word) and guess.isalpha():
            if guess == self.word:
                self.word_completion = self.word
                self.update_gui()
                self.update_message("Congratulations, you guessed the word!")
                self.ask_for_meaning()
            else:
                self.tries -= 1
                self.update_gui()
                self.update_message(f"'{guess}' is not the correct word.")
        else:
            self.update_message("Invalid guess. Please enter a single letter or the full word.")

        if self.tries == 0:
            self.update_message(f"Sorry, you've run out of attempts. The word was '{self.word}'.")
            self.ask_for_meaning()

    def update_gui(self):
        self.hangman_image = load_hangman_image(self.tries)
        self.hangman_label.config(image=self.hangman_image)
        self.word_label.config(text=" ".join(self.word_completion))
        self.attempts_label.config(text=f"Attempts left: {self.tries}")
        self.wrong_label.config(text=f"Wrong letters: {', '.join(self.wrong_letters)}")
        self.right_label.config(text=f"Right letters: {', '.join(self.guessed_letters)}")

    def update_message(self, message):
        self.message_panel.config(text=message)

    def ask_for_meaning(self):
        if messagebox.askyesno("Hangman", f"Would you like to know the meaning of the word '{self.word}'?"):
            meaning = get_word_meaning(self.word)
            self.update_message(f"The meaning of '{self.word}' is:\n{meaning}")

    def restart_game(self):
        self.word = get_random_word()
        self.word_completion = "_" * len(self.word)
        self.tries = 6
        self.guessed_letters = []
        self.wrong_letters = []
        self.update_gui()
        self.update_message("")

def main():
    root = tk.Tk()
    game = HangmanGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
