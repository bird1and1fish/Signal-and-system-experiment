from scipy.fftpack import fft, fftshift, ifft
from scipy.io import wavfile
import matplotlib.pyplot as mp
import numpy as np
import tkinter as tk
import tkinter.messagebox
import math
import pyaudio
import time
import threading
import wave

class Recorder():
    def __init__(self, chunk=1024, channels=1, rate=64000):
        self.CHUNK = chunk
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = channels
        self.RATE = rate
        self._running = True
        self._frames = []
    def start(self):
        threading._start_new_thread(self.__recording, ())
    def __recording(self):
        self._running = True
        self._frames = []
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        while(self._running):
            data = stream.read(self.CHUNK)
            self._frames.append(data)
 
        stream.stop_stream()
        stream.close()
        p.terminate()
 
    def stop(self):
        self._running = False
 
    def save(self, filename):
        
        p = pyaudio.PyAudio()
        if not filename.endswith(".wav"):
            filename = filename + ".wav"
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self._frames))
        wf.close()

def record():
    global rec
    end_record_btn.place(x = 400, y = 300)
    rec = Recorder()
    rec.start()

def end_record():
    rec.stop()
    rec.save('myvoice.wav')
    end_record_btn.place_forget()

def stable_sound():
    global y, yr, seq_str, fs
    # fs, y = wavfile.read('Ding.wav')
    fs, y = wavfile.read('ring.wav')
    y = y[:, 0]
    leng = len(y)
    # 取其中1024个点
    yr = y[10000:10000 + 1024]
    seq_str = ''
    fourier2048()
    fourier1024()
    ifourier()
    max_sin()
    mp.show()

def changing_sound():
    stop_btn.place(x = 100, y = 220)
    next_btn.place(x = 200, y = 220)
    global yr, y, seq_str, leng, seq, window_end, fs
    # fs, y = wavfile.read('Ding.wav')
    fs, y = wavfile.read('myvoice.wav')
    # y = y[:, 0]
    leng = len(y)
    seq = 0# 加窗起点
    window_end = seq + 1024
    if(window_end < leng):
        yr = y[seq:window_end]
        seq_str = str(seq) + '-' + str(window_end)
        fourier1024()
        seq = window_end
        window_end = seq + 1024
        mp.show()

# 取幅度谱并显示，首先是fs = 2048
def fourier2048():
    global YR2048
    YR2048 = fft(yr, 2048)
    yf = abs(YR2048)
    yf1 = yf / len(yf)
    yf2 = yf1[range(int(len(yf) / 2))]
    xf = np.arange(len(yf)) * 44100 / 1024 / 2
    xf2 = xf[range(int(len(yf) / 2))]
    
    mp.figure('2048 Sample_Fre')
    mp.clf()
    mp.subplot(311)
    mp.plot(xf2, yf2 * 2)
    mp.xlabel('Fre/Hz')
    mp.ylabel('loud')
    mp.title('FFT')
    mp.subplot(313)
    mp.plot(xf - len(xf) * 44100 / 1024 / 2, fftshift(abs(YR2048)) / 1000)
    mp.xlabel('Fre/Hz')
    mp.ylabel('loud')
    mp.title('FFTshift')

# fs = 1024
def fourier1024():
    global YR1024
    YR1024 = fft(yr, 1024)
    yf = abs(YR1024)
    yf1 = yf / len(yf)
    yf2 = yf1[range(int(len(yf) / 2))]
    xf = np.arange(len(yf)) * 44100 / 1024
    xf2 = xf[range(int(len(yf) / 2))]
    mp.figure('1024 Sample_Fre  ' + seq_str)
    mp.clf()
    mp.subplot(311)
    mp.plot(xf2, yf2)
    mp.xlabel('Fre/Hz')
    mp.ylabel('loud')
    mp.title('FFT')
    mp.subplot(313)
    mp.plot(xf - len(xf) * 44100 / 1024 / 2, fftshift(abs(YR1024)) / 1000)
    mp.xlabel('Fre/Hz')
    mp.ylabel('loud')
    mp.title('FFTshift')

# 反傅里叶变换
def ifourier():
    global yr1024
    yr1024 = ifft(YR1024).real
    mp.figure('1024 ifft')
    mp.clf()
    mp.subplot(311)
    mp.plot(np.arange(len(yr)) / fs, yr)
    mp.xlabel('t/s')
    mp.ylabel('loud')
    mp.title('origin signal')
    mp.subplot(313)
    mp.plot(np.arange(len(yr1024)) / fs, yr1024)
    mp.xlabel('t/s')
    mp.ylabel('loud')
    mp.title('ifft')

# 寻找最大正弦分量
def max_sin():
    global maxsin
    peaki = np.argmax(abs(YR1024[0:512]))
    maxpeak = max(abs(YR1024[0:512]))
    MAXSIN = np.zeros(1024)
    MAXSIN[peaki] = maxpeak
    MAXSIN[1024 - peaki] = maxpeak
    maxsin = ifft(MAXSIN)
    mp.figure('max Sin')
    mp.clf()
    mp.subplot(311)
    mp.plot(np.arange(len(yr1024)) / fs, yr1024)
    mp.xlabel('t/s')
    mp.ylabel('loud')
    mp.title('ifft signal')
    mp.subplot(313)
    mp.plot(np.arange(len(maxsin)) / fs, maxsin)
    mp.xlabel('t/s')
    mp.ylabel('loud')
    mp.title('max sin wav')

def stop_wav():
    stop_btn.place_forget()
    next_btn.place_forget()
    mp.close('all')

def next_wav():
    global yr, y, seq_str, leng, seq, window_end
    if(window_end < leng):
        yr = y[seq:window_end]
        seq_str = str(seq) + '-' + str(window_end)
        fourier1024()
        seq = window_end
        window_end = seq + 1024
        mp.show()
    else:
        tk.messagebox.showerror("错误","已是最后一张")

def win_init():
    global stop_btn, next_btn, end_record_btn
    root_window = tk.Tk()
    root_window.title('Wav信号的波形分析')
    root_window.resizable(0, 0)
    root_window.geometry('512x384')

    stable_btn = tk.Button(root_window, bg = 'White', height = 4, width = 16, text = '持续音的频谱分析', command = stable_sound)
    stable_btn.place(x = 300, y = 50)
    changing_btn = tk.Button(root_window, bg = 'White', height = 4, width = 16, text = '时变音的频谱分析', command = changing_sound)
    changing_btn.place(x = 300, y = 200)
    stop_btn = tk.Button(root_window, bg = 'White', height = 2, width = 8, text = '停止', command = stop_wav)
    next_btn = tk.Button(root_window, bg = 'White', height = 2, width = 8, text = '下一个', command = next_wav)
    start_record_btn = tk.Button(root_window, bg = 'White', height = 2, width = 8, text = '开始录音', command = record)
    start_record_btn.place(x = 300, y = 300)
    end_record_btn = tk.Button(root_window, bg = 'White', height = 2, width = 8, text = '结束录音', command = end_record)    

if __name__ == '__main__':
    win_init()



