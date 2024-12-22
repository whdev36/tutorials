import tkinter as tk
from tkinter import font as tkFont
from sqlalchemy import Column, create_engine, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
e = create_engine('mysql+pymysql://root:Password123+@localhost:3306/dict')
Base = declarative_base()
Session = sessionmaker(bind=e)
s = Session()

# Dictionary model
class Dict(Base):
    __tablename__ = 'dicts'
    id = Column(Integer, primary_key=True)
    uz = Column(String(128))
    en = Column(String(128))

    def __init__(self, uz, en):
        self.uz = uz
        self.en = en

    def __repr__(self):
        return f'({self.id}), ({self.en} - {self.uz})'

Base.metadata.create_all(bind=e)

# GUI setup
root = tk.Tk()
root.title('Dictionary GUI')
root.geometry('600x600')
root.configure(bg='#f0f0f0')

header_font = tkFont.Font(family='Helvetica', size=30, weight='bold')
header = tk.Label(root, text='Dictionary', font=header_font, bg='#f0f0f0')
header.pack(pady=20)

search_frame = tk.Frame(root, bg='#f0f0f0')
search_frame.pack(pady=10)

word = tk.Entry(search_frame, font=['Helvetica', 20], width=20, bd=2, relief='groove')
word.pack(side=tk.LEFT, padx=10)

submit = tk.Button(search_frame, text='Search', font=['Helvetica', 20], command=lambda: search_word(), bg='#4CAF50', fg='white', relief='raised')
submit.pack()

results_frame = tk.Frame(root)
results_frame.pack(pady=10)

results = tk.Listbox(results_frame, font=['Helvetica', 16], width=50, height=15)
results.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar = tk.Scrollbar(results_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

results.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=results.yview)

def search_word():
    query = word.get()
    results.delete(0, tk.END)  # Clear previous results
    results_list = s.query(Dict).filter(Dict.en.like(f'%{query}%')).all()
    
    for item in results_list:
        results.insert(tk.END, f'{item.en} - {item.uz}')

root.mainloop()