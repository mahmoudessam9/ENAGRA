#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter as tk
from tkinter import ttk
from googletrans import Translator
import pandas as pd
from datetime import datetime
import os
from tkinter import filedialog

def translate_text(event=None):
    translator = Translator()
    source_text = source_text_area.get("1.0", "end-1c")
    
    source_lang = translator.detect(source_text).lang
    translation = translator.translate(source_text, src=source_lang, dest='ar')
    
    translated_text.set(translation.text)
    translated_text_area.delete('1.0', tk.END)
    translated_text_area.insert('1.0', translation.text)
    
    translated_text_area.tag_configure("rtl", justify="right")
    translated_text_area.tag_add("rtl", "1.0", tk.END)
    
    save_to_history(source_text, translation.text)

def save_to_history(source_text, translated_text):
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    translation_data = {
        'Source Text': [source_text],
        'Translated Text': [translated_text],
        'Time': [current_time]
    }

    try:
        try:
            history_df = pd.read_excel(translation_file_path.get())
        except FileNotFoundError:
            history_df = pd.DataFrame()

        new_data_df = pd.DataFrame(translation_data)
        history_df = history_df.append(new_data_df, ignore_index=True)

        with pd.ExcelWriter(translation_file_path.get(), engine='openpyxl') as writer:
            history_df.to_excel(writer, index=False)
        status_label.config(text="Translation saved to history!", foreground="green")
    except Exception as e:
        status_label.config(text="Failed to save translation history. Error: " + str(e), foreground="red")

def open_translation_file():
    file_path = filedialog.askopenfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
    translation_file_path.set(file_path)

def clear_text_area():
    source_text_area.delete('1.0', tk.END)
    translated_text_area.delete('1.0', tk.END)

def set_font_type(font_type):
    source_text_area.config(font=(font_type, 20))
    translated_text_area.config(font=(font_type, 20))

def set_input_background_color(color):
    source_text_area.config(background=color)
    cursor_color = "white" if color == "black" else "black"
    source_text_area.config(insertbackground=cursor_color)
    text_color = "white" if color == "black" else "black"
    source_text_area.config(fg=text_color)

def set_output_background_color(color):
    translated_text_area.config(background=color)
    cursor_color = "white" if color == "black" else "black"
    translated_text_area.config(insertbackground=cursor_color)
    text_color = "white" if color == "black" else "black"
    translated_text_area.config(fg=text_color)

app = tk.Tk()
app.title("English to Arabic Translator")
app.geometry("1200x600")
app.resizable(False, False)
app.configure(bg="dark grey")

input_frame = ttk.Frame(app)
input_frame.pack(side=tk.LEFT, padx=10)

translation_frame = ttk.Frame(app)
translation_frame.pack(side=tk.LEFT, padx=10)

source_label = ttk.Label(input_frame, text="English", font=("Helvetica", 20), foreground="dark blue")
source_label.pack(pady=5)

source_text_area = tk.Text(input_frame, wrap="word", width=40, height=10, font=("Times New Roman", 20),
                           highlightthickness=4, highlightbackground="dark blue", insertbackground="black")
source_text_area.pack(pady=5)

source_text_area.bind("<Return>", translate_text)

font_type_var = tk.StringVar()
font_type_var.set("Times New Roman")

font_radio_frame = ttk.Frame(input_frame)
font_radio_frame.pack(pady=5)

font_types = ["Times New Roman", "Verdana", "Courier New", "Arial"]
for font_type in font_types:
    font_radio = ttk.Radiobutton(font_radio_frame, text=font_type, variable=font_type_var, value=font_type,
                                 command=lambda ft=font_type: set_font_type(ft))
    font_radio.pack(side=tk.LEFT, padx=5)

input_color_radio_frame = ttk.Frame(input_frame)
input_color_radio_frame.pack(pady=5)

input_background_colors = ["black", "white"]
input_background_color_var = tk.StringVar()
input_background_color_var.set("white")

for color in input_background_colors:
    input_bg_radio = ttk.Radiobutton(input_color_radio_frame, text=color.capitalize(), variable=input_background_color_var,
                                     value=color, command=lambda c=color: set_input_background_color(c))
    input_bg_radio.pack(side=tk.LEFT, padx=5)

translate_button_style = ttk.Style()
translate_button_style.configure("TButton", font=("Helvetica", 16), background="dark grey", borderwidth=4, relief="raised")
translate_button = ttk.Button(input_frame, text="Translate", command=translate_text, style="TButton")
translate_button.pack(pady=5)

clear_button = ttk.Button(input_frame, text="Clear", command=clear_text_area, style="TButton")
clear_button.pack(pady=5)

output_label = ttk.Label(translation_frame, text="عربي", font=("Helvetica", 20), foreground="dark blue")
output_label.pack(pady=5)

translated_text = tk.StringVar()
translated_text_area = tk.Text(translation_frame, wrap="word", width=50, height=10, font=("Times New Roman", 20),
                               background="white", insertbackground="black")
translated_text_area.pack(pady=5)

translated_text_area.config(highlightthickness=4, highlightbackground="dark blue")

output_color_radio_frame = ttk.Frame(translation_frame)
output_color_radio_frame.pack(pady=5)

output_background_colors = ["black", "white"]
output_background_color_var = tk.StringVar()
output_background_color_var.set("white")

for color in output_background_colors:
    output_bg_radio = ttk.Radiobutton(output_color_radio_frame, text=color.capitalize(), variable=output_background_color_var,
                                      value=color, command=lambda c=color: set_output_background_color(c))
    output_bg_radio.pack(side=tk.LEFT, padx=5)

translation_file_path = tk.StringVar()

select_excel_button = ttk.Button(translation_frame, text="Select Excel File", command=open_translation_file, style="TButton")
select_excel_button.pack(pady=5)

open_excel_button = ttk.Button(translation_frame, text="Open Excel File", command=lambda: os.startfile(translation_file_path.get()), style="TButton")
open_excel_button.pack(pady=5)

app.mainloop()


# In[ ]:




