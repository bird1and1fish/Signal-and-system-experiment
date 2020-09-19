import numpy as np
import matplotlib.pyplot as mp
import matplotlib.lines as ml
from scipy.fftpack import fft, ifft
from scipy.signal import butter, lfilter, freqz
import tkinter as tk

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a
 
 
def butter_lowpass_filter(data, cutoff, fs, order):
    b, a = butter_lowpass(cutoff, fs, order = order)
    y = lfilter(b, a, data)
    return y

# 信号产生
x = np.linspace(0, 9.9999, 100000)# 0.0001s为一个最小时间间隔
n = 1000
sign_Fre = 6# 原始信号频率
y_square = np.zeros(100000)
y_triangle = np.zeros(100000)
y_sin = 3 * np.sin(2 * np.pi * sign_Fre * x)
for i in range(1, n + 1):
    j = 2 * i - 1
    y_square += 12 / np.pi / j * np.sin(2 * np.pi * sign_Fre * j * x)
    y_triangle += 24 / (np.pi ** 2) / (j ** 2) * np.cos(2 * np.pi * sign_Fre * j * x)

def sin_sample_under():
    # 采样
    sample_Fre = 7# 采样频率
    sample_num = 10 * sample_Fre
    sample_sign = np.zeros(100000)
    sampled = np.zeros(100000)
    sample_target = y_sin# 选择采样的目标
    for i in range(sample_num):
        sample_sign[int(i * 10000 / sample_Fre)] = 1
        sampled[int(i * 10000 / sample_Fre)] = sample_target[int(i * 10000 / sample_Fre)]

    # 恢复
    restore = butter_lowpass_filter(sampled, 6, 10000, 5)
    restore = restore * 500
    yy = fft(restore)
    yf = abs(yy)
    yf1 = yf / len(x) * 1000
    yf2 = yf1[range(int(len(x) / 2))]
    xf = np.arange(len(restore))
    xf2 = xf[range(int(len(x) / 2))]
    mp.clf()
    mp.subplot(331)
    mp.plot(x, sample_sign)
    mp.xlabel('t/s')
    mp.ylabel('U/V')
    mp.title('sample_function')
    mp.subplot(332)
    mp.plot(x, sample_target)
    mp.xlabel('t/s')
    mp.ylabel('U/V')
    mp.title('origin_signal')
    mp.subplot(333)
    mp.plot(x, sampled)
    mp.xlabel('t/s')
    mp.ylabel('U/V')
    mp.title('sampled_signal')
    mp.subplot(337)
    mp.plot(x, restore)
    mp.xlabel('t/s')
    mp.ylabel('U/V')
    mp.title('restored_signal')
    mp.subplot(339)
    mp.plot(xf2 / 10, yf2 / 200)
    mp.xlabel('f/Hz')
    mp.ylabel('U/V')
    mp.title('fft')
    mp.show()

def sin_sample():
    # 采样
    sample_Fre = 25# 采样频率
    sample_num = 10 * sample_Fre
    sample_sign = np.zeros(100000)
    sampled = np.zeros(100000)
    sample_target = y_sin# 选择采样的目标
    for i in range(sample_num):
        sample_sign[int(i * 10000 / sample_Fre)] = 1
        sampled[int(i * 10000 / sample_Fre)] = sample_target[int(i * 10000 / sample_Fre)]

    # 恢复
    restore = butter_lowpass_filter(sampled, 6, 10000, 5)
    restore = restore * 500
    yy = fft(restore)
    yf = abs(yy)
    yf1 = yf / len(x) * 1000
    yf2 = yf1[range(int(len(x) / 2))]
    xf = np.arange(len(restore))
    xf2 = xf[range(int(len(x) / 2))]
    mp.clf()
    mp.subplot(331)
    mp.plot(x, sample_sign)
    mp.xlabel('t/s')
    mp.ylabel('U/V')
    mp.title('sample_function')
    mp.subplot(332)
    mp.plot(x, sample_target)
    mp.xlabel('t/s')
    mp.ylabel('U/V')
    mp.title('origin_signal')
    mp.subplot(333)
    mp.plot(x, sampled)
    mp.xlabel('t/s')
    mp.ylabel('U/V')
    mp.title('sampled_signal')
    mp.subplot(337)
    mp.plot(x, restore)
    mp.xlabel('t/s')
    mp.ylabel('U/V')
    mp.title('restored_signal')
    mp.subplot(339)
    mp.plot(xf2 / 10, yf2 / 800)
    mp.xlabel('f/Hz')
    mp.ylabel('U/V')
    mp.title('fft')
    mp.show()

def square_sample():
    # 采样
    sample_Fre = 1000# 采样频率
    sample_num = 10 * sample_Fre
    sample_sign = np.zeros(100000)
    sampled = np.zeros(100000)
    sample_target = y_square# 选择采样的目标
    for i in range(sample_num):
        sample_sign[int(i * 10000 / sample_Fre)] = 1
        sampled[int(i * 10000 / sample_Fre)] = sample_target[int(i * 10000 / sample_Fre)]

    # 恢复
    restore = butter_lowpass_filter(sampled, 500, 10000, 5)
    restore = restore * 10
    yy = fft(restore)
    yf = abs(yy)
    yf1 = yf / len(x)
    yf2 = yf1[range(int(len(x) / 2))]
    xf = np.arange(len(restore))
    xf2 = xf[range(int(len(x) / 2))]
    mp.clf()
    mp.subplot(331)
    mp.plot(x, sample_sign)
    mp.xlabel('t/s')
    mp.ylabel('U/V')
    mp.title('sample_function')
    mp.subplot(332)
    mp.plot(x, sample_target)
    mp.xlabel('t/s')
    mp.ylabel('U/V')
    mp.title('origin_signal')
    mp.subplot(333)
    mp.plot(x, sampled)
    mp.xlabel('t/s')
    mp.ylabel('U/V')
    mp.title('sampled_signal')
    mp.subplot(337)
    mp.plot(x, restore)
    mp.xlabel('t/s')
    mp.ylabel('U/V')
    mp.title('restored_signal')
    mp.subplot(339)
    mp.plot(xf2 / 10, yf2)
    mp.xlabel('f/Hz')
    mp.ylabel('U/V')
    mp.title('fft')
    mp.show()

def triangle_sample():
    # 采样
    sample_Fre = 1000# 采样频率
    sample_num = 10 * sample_Fre
    sample_sign = np.zeros(100000)
    sampled = np.zeros(100000)
    sample_target = y_triangle# 选择采样的目标
    for i in range(sample_num):
        sample_sign[int(i * 10000 / sample_Fre)] = 1
        sampled[int(i * 10000 / sample_Fre)] = sample_target[int(i * 10000 / sample_Fre)]

    # 恢复
    restore = butter_lowpass_filter(sampled, 500, 10000, 5)
    restore = restore * 10
    yy = fft(restore)
    yf = abs(yy)
    yf1 = yf / len(x)
    yf2 = yf1[range(int(len(x) / 2))]
    xf = np.arange(len(restore))
    xf2 = xf[range(int(len(x) / 2))]
    mp.clf()
    mp.subplot(331)
    mp.plot(x, sample_sign)
    mp.xlabel('t/s')
    mp.ylabel('U/V')
    mp.title('sample_function')
    mp.subplot(332)
    mp.plot(x, sample_target)
    mp.xlabel('t/s')
    mp.ylabel('U/V')
    mp.title('origin_signal')
    mp.subplot(333)
    mp.plot(x, sampled)
    mp.xlabel('t/s')
    mp.ylabel('U/V')
    mp.title('sampled_signal')
    mp.subplot(337)
    mp.plot(x, restore)
    mp.xlabel('t/s')
    mp.ylabel('U/V')
    mp.title('restored_signal')
    mp.subplot(339)
    mp.plot(xf2 / 10, yf2)
    mp.xlabel('f/Hz')
    mp.ylabel('U/V')
    mp.title('fft')
    mp.show()

def gui_init():
    root_window = tk.Tk()
    root_window.title('信号的抽样和内插')
    root_window.resizable(0, 0)
    root_window.geometry('180x512')

    square_btn = tk.Button(root_window,bg = 'White',height = 3,width = 10,text = '正弦波欠采样',command = sin_sample_under)
    square_btn.place(x = 50,y = 50)

    square_btn = tk.Button(root_window,bg = 'White',height = 3,width = 10,text = '正弦波采样',command = sin_sample)
    square_btn.place(x = 50,y = 150)

    triangle_btn = tk.Button(root_window,bg = 'White',height = 3,width = 10,text = '方波采样',command = square_sample)
    triangle_btn.place(x = 50,y = 250)

    analysis_btn = tk.Button(root_window,bg = 'White',height = 3,width = 10,text = '三角波采样',command = triangle_sample)
    analysis_btn.place(x = 50,y = 350)

if __name__ == '__main__':
    gui_init()

