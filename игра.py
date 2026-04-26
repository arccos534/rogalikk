import random
import tkinter as tk


class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Игра на память - Запомни двери")
        self.root.geometry("760x620")
        self.level = 1
        self.total_score = 0
        self.correct_doors = []
        self.current_round = 0
        self.round_correct = 0
        self.level_settings = {}
        self.answer_labels = []
        self.remaining = 0
        self.setup_start_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def reset_run(self):
        self.level = 1
        self.total_score = 0

    def get_difficulty_name(self, door_count, memorization_time):
        if door_count >= 7 or memorization_time <= 6:
            return "Критическая"
        if door_count >= 5 or memorization_time <= 9:
            return "Высокая"
        if door_count >= 4 or memorization_time <= 12:
            return "Средняя"
        return "Базовая"

    def get_level_settings(self):
        level_index = self.level - 1
        milestone_bonus = level_index // 4
        elite_modifier = 1 if self.level % 5 == 0 else 0
        rounds = 10 + (level_index * 2) + milestone_bonus
        door_count = min(3 + (level_index // 2) + milestone_bonus, 8)
        memorization_time = max(5, 15 - level_index - milestone_bonus)
        score_per_answer = 1 + (level_index // 2) + milestone_bonus

        return {
            "rounds": rounds,
            "door_count": door_count,
            "memorization_time": memorization_time,
            "score_per_answer": score_per_answer,
            "transition_delay": max(900, 2000 - (level_index * 120)),
            "difficulty_name": self.get_difficulty_name(door_count, memorization_time),
            "elite_level": elite_modifier == 1,
        }

    def show_run_status(self):
        tk.Label(
            self.root,
            text=(
                f"Уровень: {self.level} | Очки: {self.total_score} | "
                f"Сложность: {self.level_settings['difficulty_name']}"
            ),
            font=("Arial", 11),
        ).pack(pady=5)

    def setup_start_screen(self):
        self.clear_window()

        tk.Label(self.root, text="ИГРА НА ПАМЯТЬ", font=("Arial", 24, "bold")).pack(pady=20)
        tk.Label(self.root, text="Запомни двери", font=("Arial", 16)).pack(pady=10)

        rules = """Правила:
1. Нужно запомнить последовательность дверей
2. Потом выбрать правильную дверь в каждом раунде
3. Каждый новый уровень делает забег сложнее
4. Ошибка завершает текущий забег"""

        tk.Label(self.root, text=rules, font=("Arial", 11), justify="left").pack(pady=20)
        tk.Button(
            self.root,
            text="Начать игру",
            command=self.start_level,
            font=("Arial", 14),
            bg="green",
            fg="white",
        ).pack(pady=20)

    def start_level(self):
        self.level_settings = self.get_level_settings()
        self.correct_doors = [
            random.randint(1, self.level_settings["door_count"])
            for _ in range(self.level_settings["rounds"])
        ]
        self.current_round = 0
        self.round_correct = 0
        self.show_memorization_phase()

    def show_memorization_phase(self):
        self.clear_window()

        tk.Label(self.root, text=f"УРОВЕНЬ {self.level}", font=("Arial", 20, "bold")).pack(pady=10)
        self.show_run_status()
        tk.Label(self.root, text="Запомните последовательность", font=("Arial", 14)).pack(pady=5)
        tk.Label(
            self.root,
            text=(
                f"Раундов: {self.level_settings['rounds']} | "
                f"Дверей: {self.level_settings['door_count']} | "
                f"Сложность: {self.level_settings['difficulty_name']}"
            ),
            font=("Arial", 12),
            fg="red",
        ).pack()

        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        block_count = 1
        if self.level_settings["rounds"] > 24:
            block_count = 3
        elif self.level_settings["rounds"] > 12:
            block_count = 2

        rows_per_block = (self.level_settings["rounds"] + block_count - 1) // block_count

        for block in range(block_count):
            column_shift = block * 3
            tk.Label(frame, text="Раунд", font=("Arial", 12, "bold"), width=10).grid(
                row=0,
                column=column_shift,
            )
            tk.Label(frame, text="Правильная дверь", font=("Arial", 12, "bold"), width=15).grid(
                row=0,
                column=column_shift + 1,
            )

        self.answer_labels = []
        for index, door in enumerate(self.correct_doors, 1):
            block = (index - 1) // rows_per_block
            row = ((index - 1) % rows_per_block) + 1
            column_shift = block * 3
            tk.Label(frame, text=str(index), font=("Arial", 11)).grid(row=row, column=column_shift, pady=2)
            label = tk.Label(frame, text=f"Дверь {door}", font=("Arial", 11), fg="green")
            label.grid(row=row, column=column_shift + 1, pady=2)
            self.answer_labels.append(label)

        self.time_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.time_label.pack(pady=10)
        self.remaining = self.level_settings["memorization_time"]
        self.update_timer()

    def start_rounds(self):
        self.current_round = 0
        self.show_question()

    def update_timer(self):
        if self.remaining > 0:
            self.time_label.config(text=f"Осталось: {self.remaining} секунд")
            self.remaining -= 1
            self.root.after(1000, self.update_timer)
        else:
            for label in self.answer_labels:
                label.config(text="???", fg="red")
            self.time_label.config(text="ОТВЕТЫ ИСЧЕЗЛИ")
            self.root.after(self.level_settings["transition_delay"], self.start_rounds)

    def show_question(self):
        self.clear_window()

        tk.Label(self.root, text=f"УРОВЕНЬ {self.level}", font=("Arial", 16, "bold")).pack(pady=10)
        self.show_run_status()
        tk.Label(
            self.root,
            text=f"Раунд {self.current_round + 1} из {self.level_settings['rounds']}",
            font=("Arial", 14),
        ).pack()
        tk.Label(
            self.root,
            text=f"Прогресс: {self.round_correct}/{self.level_settings['rounds']}",
            font=("Arial", 12),
        ).pack(pady=5)
        tk.Label(
            self.root,
            text=f"Цена ответа: {self.level_settings['score_per_answer']} очк.",
            font=("Arial", 11),
            fg="darkgreen",
        ).pack()

        frame = tk.Frame(self.root)
        frame.pack(pady=40)

        for door_number in range(1, self.level_settings["door_count"] + 1):
            button = tk.Button(
                frame,
                text=f"Дверь {door_number}",
                font=("Arial", 18),
                command=lambda value=door_number: self.check_answer(value),
                width=12,
                height=2,
                bg="lightblue",
            )
            row = (door_number - 1) // 3
            column = (door_number - 1) % 3
            button.grid(row=row, column=column, padx=15, pady=15)

    def restart_run(self):
        self.reset_run()
        self.start_level()

    def show_level_complete_screen(self, completed_level):
        self.clear_window()

        next_settings = self.get_level_settings()

        tk.Label(self.root, text="УРОВЕНЬ ПРОЙДЕН", font=("Arial", 20, "bold")).pack(pady=20)
        tk.Label(
            self.root,
            text=(
                f"Вы закрыли уровень {completed_level}.\n"
                f"Счёт за забег: {self.total_score}\n"
                f"Следующий уровень: {self.level}"
            ),
            font=("Arial", 13),
            justify="center",
        ).pack(pady=15)
        tk.Label(
            self.root,
            text=(
                f"Следующий этап: {next_settings['rounds']} раундов, "
                f"{next_settings['door_count']} дверей, "
                f"{next_settings['memorization_time']} секунд на запоминание\n"
                f"Сложность: {next_settings['difficulty_name']}, "
                f"цена ответа: {next_settings['score_per_answer']} очк."
            ),
            font=("Arial", 12),
            fg="darkgreen",
            justify="center",
        ).pack(pady=10)

        if next_settings["elite_level"]:
            tk.Label(
                self.root,
                text="Следующий уровень будет усиленным.",
                font=("Arial", 12, "bold"),
                fg="firebrick",
            ).pack(pady=5)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=25)

        tk.Button(
            button_frame,
            text="Продолжить забег",
            command=self.start_level,
            font=("Arial", 13),
            bg="green",
            fg="white",
            width=18,
        ).grid(row=0, column=0, padx=10)
        tk.Button(
            button_frame,
            text="Закончить",
            command=self.root.quit,
            font=("Arial", 13),
            width=12,
        ).grid(row=0, column=1, padx=10)

    def show_game_over_screen(self, correct):
        self.clear_window()

        reached_level = self.level
        earned_score = self.total_score

        tk.Label(self.root, text="ЗАБЕГ ЗАВЕРШЁН", font=("Arial", 20, "bold")).pack(pady=20)
        tk.Label(
            self.root,
            text=(
                f"Правильная дверь была {correct}.\n"
                f"Вы дошли до уровня {reached_level}.\n"
                f"Угадано дверей на текущем уровне: {self.round_correct}\n"
                f"Общий счёт: {earned_score}"
            ),
            font=("Arial", 13),
            justify="center",
        ).pack(pady=15)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=25)

        tk.Button(
            button_frame,
            text="Начать заново",
            command=self.restart_run,
            font=("Arial", 13),
            bg="green",
            fg="white",
            width=16,
        ).grid(row=0, column=0, padx=10)
        tk.Button(
            button_frame,
            text="Выйти",
            command=self.root.quit,
            font=("Arial", 13),
            width=12,
        ).grid(row=0, column=1, padx=10)

    def check_answer(self, choice):
        correct = self.correct_doors[self.current_round]

        if choice == correct:
            self.round_correct += 1
            self.total_score += self.level_settings["score_per_answer"]
            self.current_round += 1

            if self.current_round == self.level_settings["rounds"]:
                completed_level = self.level
                self.level += 1
                self.show_level_complete_screen(completed_level)
            else:
                self.show_question()
        else:
            self.show_game_over_screen(correct)


if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()
