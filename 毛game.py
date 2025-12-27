import tkinter as tk
from tkinter import messagebox
import random
import time

class Minesweeper:
    def __init__(self, master):
        self.master = master
        self.master.title("踩地雷 v3（生命值＋提示）")
        self.master.geometry("600x600")  # ← 保證視窗大小

        # ===== 基本設定 =====
        self.rows = 9
        self.cols = 9
        self.mines_count = 10
        self.lives = 3
        self.hints = 3

        # ===== 狀態 =====
        self.buttons = {}
        self.mines = set()
        self.flags = set()
        self.opened = set()
        self.first_click = True
        self.start_time = None
        self.timer_running = False

        # ===== 上方資訊列 =====
        top = tk.Frame(master)
        top.pack(pady=5)

        self.timer_label = tk.Label(top, text="時間：0 秒")
        self.timer_label.pack(side=tk.LEFT, padx=6)

        self.life_label = tk.Label(top, text="生命：❤️❤️❤️")
        self.life_label.pack(side=tk.LEFT, padx=6)

        self.hint_label = tk.Label(top, text="提示：💡💡💡")
        self.hint_label.pack(side=tk.LEFT, padx=6)

        tk.Button(top, text="提示", command=self.use_hint).pack(side=tk.LEFT, padx=4)
        tk.Button(top, text="重新開始", command=self.reset_game).pack(side=tk.LEFT, padx=4)

        # ===== 棋盤 =====
        self.board_frame = tk.Frame(master)
        self.board_frame.pack()

        self.create_board()

    # ===== 建立棋盤 =====
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

    # ===== 左鍵 =====
    def left_click(self, r, c):
        if self.first_click:
            self.place_mines(r, c)
            self.start_time = time.time()
            self.timer_running = True
            self.update_timer()
            self.first_click = False

        if (r, c) in self.mines:
            self.buttons[(r, c)].config(text="💣", bg="red")
            self.lives -= 1
            self.update_lives()
            if self.lives == 0:
                self.game_over(False)
            return

        self.open_cell(r, c)
        if self.check_win():
            self.game_over(True)

    # ===== 右鍵 =====
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

    # ===== 地雷 =====
    def place_mines(self, safe_r, safe_c):
        while len(self.mines) < self.mines_count:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if (r, c) != (safe_r, safe_c):
                self.mines.add((r, c))

    # ===== 開格 =====
    def open_cell(self, r, c):
        if (r, c) in self.opened or (r, c) in self.flags:
            return
        self.opened.add((r, c))
        count = self.count_mines(r, c)
        btn = self.buttons[(r, c)]
        btn.config(text=str(count) if count else "", relief=tk.SUNKEN, bg="lightgray")
        if count == 0:
            for nr in range(r - 1, r + 2):
                for nc in range(c - 1, c + 2):
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        self.open_cell(nr, nc)

    def count_mines(self, r, c):
        return sum(
            (nr, nc) in self.mines
            for nr in range(r - 1, r + 2)
            for nc in range(c - 1, c + 2)
        )

    # ===== 提示功能 =====
    def use_hint(self):
        if self.hints == 0:
            messagebox.showinfo("提示", "提示已用完")
            return

        safe = [
            (r, c) for r in range(self.rows) for c in range(self.cols)
            if (r, c) not in self.mines
            and (r, c) not in self.opened
            and (r, c) not in self.flags
        ]
        if not safe:
            return

        r, c = random.choice(safe)
        self.open_cell(r, c)
        self.hints -= 1
        self.update_hints()

    # ===== 更新顯示 =====
    def update_lives(self):
        self.life_label.config(text="生命：" + "❤️" * self.lives)

    def update_hints(self):
        self.hint_label.config(text="提示：" + "💡" * self.hints)

    # ===== 勝利 =====
    def check_win(self):
        return len(self.opened) == self.rows * self.cols - self.mines_count

    # ===== 結束 =====
    def game_over(self, win):
        self.timer_running = False
        for (r, c) in self.mines:
            self.buttons[(r, c)].config(text="💣")
        messagebox.showinfo("結果", "你贏了！" if win else "遊戲結束")

    # ===== 重來 =====
    def reset_game(self):
        self.board_frame.destroy()
        self.board_frame = tk.Frame(self.master)
        self.board_frame.pack()

        self.buttons.clear()
        self.mines.clear()
        self.flags.clear()
        self.opened.clear()
        self.first_click = True
        self.lives = 3
        self.hints = 3
        self.timer_running = False

        self.timer_label.config(text="時間：0 秒")
        self.update_lives()
        self.update_hints()

        self.create_board()

    # ===== 計時 =====
    def update_timer(self):
        if self.timer_running:
            t = int(time.time() - self.start_time)
            self.timer_label.config(text=f"時間：{t} 秒")
            self.master.after(1000, self.update_timer)

# ===== 主程式 =====
if __name__ == "__main__":
    root = tk.Tk()
    Minesweeper(root)
    root.mainloop()

