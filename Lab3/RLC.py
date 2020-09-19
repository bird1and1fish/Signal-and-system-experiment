import tkinter as tk
import tkinter.messagebox
import matplotlib.pyplot as mp
import numpy as np
import math

t = np.arange(0, 50, 0.01)
u = 1

def is_positive_digit(data1, data2, data3):
    try:
        float(data1)
        float(data2)
        float(data3)
    except ValueError:
        return False
    else:
        if(float(data1) >= 0 and float(data2) >= 0 and float(data3) >= 0):
            return True
        else:
            return False

def show_func():
    global i_L, v_c, title_label
    R = R_txt.get()
    L = L_txt.get()
    C = C_txt.get()
    key = is_positive_digit(R, L, C)
    if(key):# 输入电路参数正确
        R = float(R)
        L = float(L)
        C = float(C)
        alpha = R / (2 * L)
        w0 = 1 / math.sqrt(L * C)
        if(R == 0):# 无阻尼
            title_label = '无阻尼'
            i_L = L * w0 * np.sin(w0 * t)
            v_c = 1 - np.cos(w0 * t)
        elif(alpha > w0):# 过阻尼
            title_label = '过阻尼'
            beta = math.sqrt(alpha ** 2 - w0 ** 2)
            i_L = (1 / L) * np.exp(-alpha * t) * np.sinh(beta * t) / (beta * u)
            v_c = np.exp(-alpha * t) / (2 * beta * L * C) * (np.exp(-alpha * t) / (alpha + beta) - np.exp(-alpha * t) / (alpha - beta)) + 1
        elif(alpha == w0):# 临界阻尼
            title_label = '临界阻尼'
            i_L = 1 / L * t * np.exp(-alpha * t)
            v_c = 1 / (L * C * alpha * alpha) * (1 - (alpha * t + 1) * np.exp(-alpha * t))
        elif(alpha < w0):# 欠阻尼
            title_label = '欠阻尼'
            w1 = math.sqrt(w0 ** 2 - alpha ** 2)
            i_L = w1 * L * np.exp(-alpha * t) * np.sin(w1 * t)
            v_c = 1 - np.exp(-alpha * t) * (np.cos(w1 * t) + np.sin(w1 * t))
        draw_curve()
    else:
        tk.messagebox.showerror("错误","请输入正确的电路参数")

def draw_curve():
    mp.figure(title_label + '状态轨迹')
    mp.clf()
    mp.subplot(161)
    mp.plot(t, i_L)
    mp.xlabel('t/s')
    mp.ylabel('i_L/A')
    mp.title('t - i_L')
    mp.subplot(163)
    mp.plot(t, v_c)
    mp.xlabel('t/s')
    mp.ylabel('v_c/V')
    mp.title('t - v_c')
    mp.subplot(165)
    mp.plot(v_c, i_L)
    mp.xlabel('v_c/V')
    mp.ylabel('i_L/A')
    mp.title('v_c - i_L')
    mp.show()

def win_init():
    global R_txt, L_txt, C_txt
    root_window = tk.Tk()
    root_window.title('二阶状态轨迹显示')
    root_window.resizable(0, 0)
    root_window.geometry('450x330')

    R_lab = tk.Label(root_window, text = '电阻值：')
    R_lab.place(x = 20, y = 50)
    R_txt = tk.Entry(root_window, bd = 2)
    R_txt.place(x = 80, y = 50)

    L_lab = tk.Label(root_window, text = '电感值：')
    L_lab.place(x = 20, y = 150)
    L_txt = tk.Entry(root_window, bd = 2)
    L_txt.place(x = 80, y = 150)

    C_lab = tk.Label(root_window, text = '电容值：')
    C_lab.place(x = 20, y = 250)
    C_txt = tk.Entry(root_window, bd = 2)
    C_txt.place(x = 80, y = 250)

    show_btn = tk.Button(root_window,bg = 'White',height = 4,width = 12,text = '二阶轨迹显示',command = show_func)
    show_btn.place(x = 300,y = 120)

if __name__ == '__main__':
    win_init()
