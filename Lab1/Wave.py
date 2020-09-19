import numpy as np
import matplotlib.pyplot as mp
from scipy.fftpack import fft,ifft
import tkinter as tk   #导入窗体控件

x = np.linspace(0, 10, 10000)
n1 = 2
n2 = 3
n3 = 5
n4 = 10
base = np.zeros(10000)
base1 = np.zeros(10000)
y1 = np.zeros(10000)# 方波
y2 = np.zeros(10000)
y3 = np.zeros(10000)
y4 = np.zeros(10000)
y11 = np.zeros(10000)# 三角波
y22 = np.zeros(10000)
y33 = np.zeros(10000)
y44 = np.zeros(10000)

base = 12 / np.pi * np.sin(2 * np.pi * 50 * x)
base1 = 12 / np.pi * np.cos(2 * np.pi * 50 * x)
for i in range(1, n1 + 1):
    j = 2 * i - 1
    y1 += 12 / np.pi / j * np.sin(2 * np.pi * 50 * j * x)
    y11 += 24 / (np.pi ** 2) / (j ** 2) * np.cos(2 * np.pi * 50 * j * x)
for i in range(1, n2 + 1):
    j = 2 * i - 1
    y2 += 12 / np.pi / j * np.sin(2 * np.pi * 50 * j * x)
    y22 += 24 / (np.pi ** 2) / (j ** 2) * np.cos(2 * np.pi * 50 * j * x)
for i in range(1, n3 + 1):
    j = 2 * i - 1
    y3 += 12 / np.pi / j * np.sin(2 * np.pi * 50 * j * x)
    y33 += 24 / (np.pi ** 2) / (j ** 2) * np.cos(2 * np.pi * 50 * j * x)
for i in range(1, n4 + 1):
    j = 2 * i - 1
    y4 += 12 / np.pi / j * np.sin(2 * np.pi * 50 * j * x)
    y44 += 24 / (np.pi ** 2) / (j ** 2) * np.cos(2 * np.pi * 50 * j * x)

yy = fft(y4)
yf = abs(yy)
yf1 = yf / len(x)
yf2 = yf1[range(int(len(x) / 2))]
xf = np.arange(len(y4))
xf2 = xf[range(int(len(x) / 2))]

yy1 = fft(y44)
yf1 = abs(yy1)
yf11 = yf1 / len(x)
yf22 = yf11[range(int(len(x) / 2))]
xf1 = np.arange(len(y44))
xf22 = xf1[range(int(len(x) / 2))]

def show_square():
    mp.clf()
    # mp.grid(linestyle = ":")
    mp.subplot(321)
    mp.plot(x, y1)
    mp.plot(x, base)
    mp.xlabel('t/s')
    mp.ylabel('U/V')
    mp.title('3rd harmonic')
    mp.subplot(322)
    mp.plot(x, y2)
    mp.xlabel('t/s')
    mp.ylabel('U/V')
    mp.title('5th harmonic')
    mp.subplot(325)
    mp.plot(x, y3)
    mp.xlabel('t/s')
    mp.ylabel('U/V')
    mp.title('9th harmonic')
    mp.subplot(326)
    mp.plot(x, y4)
    mp.xlabel('t/s')
    mp.ylabel('U/V')
    mp.title('19th harmonic')
    mp.show()

def show_triangle():
    mp.clf()
    # mp.grid(linestyle = ":")
    mp.subplot(321)
    mp.plot(x, y11)
    mp.plot(x, base1)
    mp.xlabel('t/s')
    mp.ylabel('U/V')
    mp.title('3rd harmonic')
    mp.subplot(322)
    mp.plot(x, y22)
    mp.xlabel('t/s')
    mp.ylabel('U/V')
    mp.title('5th harmonic')
    mp.subplot(325)
    mp.plot(x, y33)
    mp.xlabel('t/s')
    mp.ylabel('U/V')
    mp.title('9th harmonic')
    mp.subplot(326)
    mp.plot(x, y44)
    mp.xlabel('t/s')
    mp.ylabel('U/V')
    mp.title('19th harmonic')
    mp.show()

def wave_analysis():
    mp.clf()
    mp.subplot(131)
    mp.plot(xf2 / 10, yf2, 'b')
    mp.xlabel('f/Hz')
    mp.ylabel('U/V')
    mp.title('square_Fre')
    mp.subplot(132)
    mp.plot(xf22 / 10, yf22, 'r')
    mp.xlabel('f/Hz')
    mp.ylabel('U/V')
    mp.title('triangle_Fre')
    mp.subplot(133)
    mp.plot(xf2 / 10, yf2, 'b')
    mp.plot(xf22 / 10, yf22, 'r')
    mp.xlabel('f/Hz')
    mp.ylabel('U/V')
    mp.title('compare')
    mp.show()

def gui_init():
    root_window = tk.Tk()
    root_window.title('波形合成与分解')
    root_window.resizable(0, 0)
    root_window.geometry('180x384')

    square_btn = tk.Button(root_window,bg = 'White',height = 3,width = 10,text = '矩形波合成',command = show_square)
    square_btn.place(x = 50,y = 50)

    triangle_btn = tk.Button(root_window,bg = 'White',height = 3,width = 10,text = '三角波合成',command = show_triangle)
    triangle_btn.place(x = 50,y = 150)

    analysis_btn = tk.Button(root_window,bg = 'White',height = 3,width = 10,text = '频谱分析',command = wave_analysis)
    analysis_btn.place(x = 50,y = 250)

if __name__ == '__main__':
    gui_init()

