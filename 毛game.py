import tkinter as tk
from tkinter import messagebox
import random
import time

# ==============================
# 踩地雷遊戲主程式
# ==============================

class Minesweeper:
    def __init__(self, master):
        # 設定主視窗
        self.master = master
        self.master.title("踩地雷遊戲")

        # 預設遊戲參數
        self.rows = 9
        self.cols = 9
        self.mines_count = 10

        # 記錄遊戲狀態
        self.buttons = {}          # 儲存每個按鈕
        self.mines = set()          # 地雷位置
        self.flags = set()          # 插旗位置
        self.opened = set()         # 已打開的位置
        self.first_click = True     # 判斷是否為第一次點擊
        self.start_time = None      # 計時開始時間
        self.timer_running = False # 是否正在計時

        # 建立上方控制區域
        self.top_frame = tk.Frame(master)
        self.top_frame.pack()

        # 計時顯示
        self.timer_label = tk.Label(self.top_frame, text="時間：0 秒")
        self.timer_label.pack(side=tk.LEFT, padx=10)

        # 重新開始按鈕
        self.reset_button = tk.Button(self.top_frame, text="重新開始", command=self.reset_game)
        self.reset_button.pack(side=tk.LEFT)

        # 難度選擇
        self.difficulty = tk.StringVar()
        self.difficulty.set("簡單")

        self.difficulty_menu = tk.OptionMenu(
            self.top_frame,
            self.difficulty,
            "簡單", "普通", "困難",
            command=self.change_difficulty
        )
        self.difficulty_menu.pack(side=tk.LEFT, padx=10)

        # 建立遊戲格子區域
        self.board_frame = tk.Frame(master)
        self.board_frame.pack()

        # 初始化遊戲
        self.create_board()

    # ==============================
    # 建立遊戲棋盤
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
    # 左鍵點擊（打開格子）
    # ==============================
    def left_click(self, r, c):
        # 第一次點擊才產生地雷
        if self.first_click:
            self.place_mines(r, c)
            self.start_time = time.time()
            self.timer_running = True
            self.update_timer()
            self.first_click = False

        # 如果踩到地雷
        if (r, c) in self.mines:
            self.buttons[(r, c)].config(text="💣", bg="red")
            self.game_over(False)
            return

        # 開啟安全格子
        self.open_cell(r, c)

        # 檢查是否勝利
        if self.check_win():
            self.game_over(True)

    # ==============================
    # 右鍵點擊（插旗）
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
    # 放置地雷（避開第一次點擊）
    # ==============================
    def place_mines(self, safe_r, safe_c):
        while len(self.mines) < self.mines_count:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)

            if (r, c) != (safe_r, safe_c):
                self.mines.add((r, c))

    # ==============================
    # 打開格子並顯示周圍地雷數
    # ==============================
    def open_cell(self, r, c):
        if (r, c) in self.opened or (r, c) in self.flags:
            return

        self.opened.add((r, c))
        count = self.count_mines(r, c)

        btn = self.buttons[(r, c)]
        btn.config(text=str(count) if count > 0 else "", relief=tk.SUNKEN, bg="lightgray")

        # 如果周圍沒有地雷，自動展開
        if count == 0:
            for nr in range(r - 1, r + 2):
                for nc in range(c - 1, c + 2):
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        self.open_cell(nr, nc)

    # ==============================
    # 計算周圍地雷數量
    # ==============================
    def count_mines(self, r, c):
        count = 0
        for nr in range(r - 1, r + 2):
            for nc in range(c - 1, c + 2):
                if (nr, nc) in self.mines:
                    count += 1
        return count

    # ==============================
    # 判斷是否勝利
    # ==============================
    def check_win(self):
        return len(self.opened) == self.rows * self.cols - self.mines_count

    # ==============================
    # 遊戲結束
    # ==============================
    def game_over(self, win):
        self.timer_running = False

        # 顯示所有地雷
        for (r, c) in self.mines:
            self.buttons[(r, c)].config(text="💣")

        if win:
            messagebox.showinfo("恭喜", "你贏了！")
        else:
            messagebox.showerror("失敗", "你踩到地雷了！")

    # ==============================
    # 重新開始遊戲
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
        self.timer_label.config(text="時間：0 秒")

        self.create_board()

    # ==============================
    # 更新計時器
    # ==============================
    def update_timer(self):
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.config(text=f"時間：{elapsed} 秒")
            self.master.after(1000, self.update_timer)

    # ==============================
    # 變更難度
    # ==============================
    def change_difficulty(self, value):
        if value == "簡單":
            self.rows, self.cols, self.mines_count = 9, 9, 10
        elif value == "普通":
            self.rows, self.cols, self.mines_count = 12, 12, 20
        elif value == "困難":
            self.rows, self.cols, self.mines_count = 16, 16, 40

        self.reset_game()


# ==============================
# 程式進入點
# ==============================
if __name__ == "__main__":
    root = tk.Tk()
    game = Minesweeper(root)
    root.mainloop()
