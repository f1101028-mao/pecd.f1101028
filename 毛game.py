

import tkinter as tk
from tkinter import messagebox
import random
import time

# ==============================
# 踩地雷遊戲（第二版：生命值模式）
# ==============================

class Minesweeper:
    def __init__(self, master):
        self.master = master
        self.master.title("踩地雷遊戲 v2（生命值模式）")

        # -------- 遊戲基本設定 --------
        self.rows = 9
        self.cols = 9
        self.mines_count = 10
        self.lives = 3  # ❤️ 生命值（新增）

        # -------- 遊戲狀態 --------
        self.buttons = {}
        self.mines = set()
        self.flags = set()
        self.opened = set()
        self.first_click = True
        self.start_time = None
        self.timer_running = False

        # -------- 上方資訊區 --------
        self.top_frame = tk.Frame(master)
        self.top_frame.pack()

        self.timer_label = tk.Label(self.top_frame, text="時間：0 秒")
        self.timer_label.pack(side=tk.LEFT, padx=10)

        # ❤️ 生命值顯示（新增）
        self.life_label = tk.Label(self.top_frame, text="生命：❤️❤️❤️")
        self.life_label.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(
            self.top_frame, text="重新開始", command=self.reset_game
        )
        self.reset_button.pack(side=tk.LEFT)

        # -------- 難度選擇 --------
        self.difficulty = tk.StringVar(value="簡單")
        tk.OptionMenu(
            self.top_frame,
            self.difficulty,
            "簡單", "普通", "困難",
            command=self.change_difficulty
        ).pack(side=tk.LEFT, padx=10)

        # -------- 棋盤區 --------
        self.board_frame = tk.Frame(master)
        self.board_frame.pack()

        self.create_board()

    # ==============================
    # 建立棋盤
    # ==============================
    def create_board(self):
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(
                    self.board_frame,
                    width=3,
                    height=1,
                    command=lambda x=r, y=c: self.left_click(x, y)
                )
                btn.bind("<Button-3>", lambda e, x=r, y=c: self.right_click(x, y))
                btn.grid(row=r, column=c)
                self.buttons[(r, c)] = btn

    # ==============================
    # 左鍵點擊
    # ==============================
    def left_click(self, r, c):
        if self.first_click:
            self.place_mines(r, c)
            self.start_time = time.time()
            self.timer_running = True
            self.update_timer()
            self.first_click = False

        # 💣 踩到地雷（不直接結束）
        if (r, c) in self.mines:
            self.buttons[(r, c)].config(text="💣", bg="red")
            self.lives -= 1
            self.update_lives()

            # 生命歸零才結束
            if self.lives == 0:
                self.game_over(False)
            return

        self.open_cell(r, c)

        if self.check_win():
            self.game_over(True)

    # ==============================
    # 右鍵插旗
    # ==============================
    def right_click(self, r, c):
        if (r, c) in self.opened:
            return

        btn = self.buttons[(r, c)]
        if (r, c) in self.flags:
            btn.config(text="")
            self.flags.remove((r, c))
        else:
            btn.config(text="🚩")
            self.flags.add((r, c))

    # ==============================
    # 放置地雷（避開第一次）
    # ==============================
    def place_mines(self, safe_r, safe_c):
        while len(self.mines) < self.mines_count:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if (r, c) != (safe_r, safe_c):
                self.mines.add((r, c))

    # ==============================
    # 開啟格子
    # ==============================
    def open_cell(self, r, c):
        if (r, c) in self.opened or (r, c) in self.flags:
            return

        self.opened.add((r, c))
        count = self.count_mines(r, c)

        btn = self.buttons[(r, c)]
        btn.config(
            text=str(count) if count > 0 else "",
            relief=tk.SUNKEN,
            bg="lightgray"
        )

        if count == 0:
            for nr in range(r - 1, r + 2):
                for nc in range(c - 1, c + 2):
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        self.open_cell(nr, nc)

    # ==============================
    # 計算周圍地雷
    # ==============================
    def count_mines(self, r, c):
        return sum(
            (nr, nc) in self.mines
            for nr in range(r - 1, r + 2)
            for nc in range(c - 1, c + 2)
        )

    # ==============================
    # 更新生命值顯示（新增）
    # ==============================
    def update_lives(self):
        self.life_label.config(text="生命：" + "❤️" * self.lives)

    # ==============================
    # 判斷勝利
    # ==============================
    def check_win(self):
        return len(self.opened) == self.rows * self.cols - self.mines_count

    # ==============================
    # 遊戲結束
    # ==============================
    def game_over(self, win):
        self.timer_running = False
        for (r, c) in self.mines:
            self.buttons[(r, c)].config(text="💣")

        if win:
            messagebox.showinfo("勝利", "恭喜你過關！")
        else:
            messagebox.showerror("失敗", "生命用完，遊戲結束")

    # ==============================
    # 重新開始
    # ==============================
    def reset_game(self):
        self.board_frame.destroy()
        self.board_frame = tk.Frame(self.master)
        self.board_frame.pack()

        self.buttons.clear()
        self.mines.clear()
        self.flags.clear()
        self.opened.clear()
        self.first_click = True
        self.timer_running = False
        self.lives = 3  # ❤️ 重設生命
        self.timer_label.config(text="時間：0 秒")
        self.update_lives()

        self.create_board()

    # ==============================
    # 計時器
    # ==============================
    def update_timer(self):
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.config(text=f"時間：{elapsed} 秒")
            self.master.after(1000, self.update_timer)

    # ==============================
    # 切換難度
    # ==============================
    def change_difficulty(self, value):
        if value == "簡單":
            self.rows, self.cols, self.mines_count = 9, 9, 10
        elif value == "普通":
            self.rows, self.cols, self.mines_count = 12, 12, 20
        else:
            self.rows, self.cols, self.mines_count = 16, 16, 40
        self.reset_game()


if __name__ == "__main__":
    root = tk.Tk()
    Minesweeper(root)
    root.mainloop()

