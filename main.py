import tkinter as tk
import requests
from datetime import datetime

start_time = None

def random_text():
    global start_time
    start_time = datetime.now()
    limit = 1
    max_fact_length = 100
    ok = False
    while not ok:
        api_url = 'https://api.api-ninjas.com/v1/facts?limit={}'.format(limit)
        response = requests.get(api_url, headers={'X-Api-Key': 'r+0STrQbpW7pApjTPmO1Pg==92EsPNbxy1av21zA'})
        if response.status_code == requests.codes.ok:
            fact = response.json()[0]['fact']
            if len(fact) <= max_fact_length:
                random_text_label.config(text=fact)
                ok = True
    text_widget.delete("1.0", tk.END)
    result_label.config(text='')
    result_label.config(bg='#F0F0F0', borderwidth=0)
    root.after(100, compare_text_periodically)



def compare_text_periodically():
    if start_time is not None:
        entered_text = (text_widget.get("1.0", "end-1c")).upper()
        random_fact = (random_text_label.cget("text")).upper()
        if entered_text.strip() == random_fact.strip():
            end_time = datetime.now()
            time_spent = (end_time - start_time).total_seconds()
            word_count = len(entered_text.split())  # Count the number of words
            if time_spent > 0:
                words_per_minute = (word_count / time_spent) * 60
                formatted_wps = round(words_per_minute)
                result_label.config(
                    text=f"Time spent: {'{:.2f} sec'.format(time_spent)} Words per minute: {formatted_wps}"
                , font=('Helvetica', 20), fg='green', padx=10, pady=5, borderwidth=2, relief='solid')
            else:
                result_label.config(text="Time spent writing is too short.")
        else:
            root.after(100, compare_text_periodically)
    else:
        # If start_time is None, schedule the comparison function to run again after 100 milliseconds
        root.after(100, compare_text_periodically)



root = tk.Tk()
root.title('Typing speed test')
root.geometry('800x600')
root.resizable(False, False)
root.configure(bg='#F0F0F0')


frame_header = tk.Frame(root)
frame_header.pack()

header_label = tk.Label(frame_header, text='Typing Speed Test', font=('Helvetica', 35), bg='sky blue', width=600)
header_label.pack()

text_frame = tk.Frame(root)
text_frame.pack()

text_label = tk.Label(text_frame, text='To start the test please press Start.', font=('Helvetica', 20))
text_label.pack(pady=30)

random_text_label = tk.Label(text_frame, text='', font=('Helvetica', 12))
random_text_label.pack(pady=20)

start_button = tk.Button(text_frame, text='Start', font=('Helvetica', 12), command=random_text)
start_button.pack(pady=5)

text_widget = tk.Text(text_frame, width=50, height=10, font=('Helvetica', 12))
text_widget.pack(pady=5)

result_label = tk.Label(text_frame, text='')
result_label.pack(pady=5)

# Schedule the compare_text_periodically function to run for the first time after 100 milliseconds
root.after(100, compare_text_periodically)

root.mainloop()
