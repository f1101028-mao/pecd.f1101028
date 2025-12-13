import tkinter as tk
from tkinter import messagebox

# 建立主視窗
win = tk.Tk()
# 設定視窗大小：寬 x 高（像素）
win.geometry("1000x500")
# 設定視窗標題
win.title("我的程式設計")

# ----------------------------
# 標題標籤（Label）：顯示歡迎文字
# ----------------------------
title_label = tk.Label(win, text="歡迎使用我的程式", font=("Arial", 16, "bold"))
# 使用 pack 佈局並設定上下外距（pady）
title_label.pack(pady=20)

# ----------------------------
# 輸入提示標籤（Label）：提示使用者輸入名稱
# ----------------------------
input_label = tk.Label(win, text="請輸入您的名字：")
input_label.pack(pady=10)

# ----------------------------
# 輸入欄位（Entry）
# - width: 以字元為單位的欄位寬度
# ----------------------------
name_entry = tk.Entry(win, width=30)
name_entry.pack(pady=10)

# ----------------------------
# 按鈕事件處理函式
# - 取得輸入欄內容，若有輸入則顯示問候，否則顯示警告
# ----------------------------
def on_button_click():
    # 讀取 Entry 裡的文字
    name = name_entry.get()
    if name:
        # 顯示訊息視窗（資訊）
        messagebox.showinfo("問候", f"您好，{name}！")
    else:
        # 顯示警告視窗（請使用者輸入名字）
        messagebox.showwarning("警告", "請輸入您的名字！")

# ----------------------------
# 按鈕（Button）
# - command: 指定按下按鈕時要呼叫的函式
# - bg: 背景顏色；padx/pady: 按鈕內邊距（水平/垂直）
# ----------------------------
button = tk.Button(win, text="點擊我", command=on_button_click, bg="lightblue", padx=20, pady=10)
button.pack(pady=20)

# ----------------------------
# 補充說明標籤（Label）
# - 顯示程式用途或提示
# ----------------------------
info_label = tk.Label(win, text="這是一個簡單的 tkinter 程式範例", fg="gray")
info_label.pack(pady=10)

# ----------------------------
# 啟動 Tkinter 的事件迴圈（必要）
# ----------------------------
win.mainloop()