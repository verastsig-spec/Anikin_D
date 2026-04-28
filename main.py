import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.filename = "books.json"
        self.books = self.load_data()

        # Интерфейс ввода
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack(side=tk.TOP, fill=tk.X)

        tk.Label(frame, text="Название:").grid(row=0, column=0)
        self.title_entry = tk.Entry(frame)
        self.title_entry.grid(row=0, column=1)

        tk.Label(frame, text="Автор:").grid(row=0, column=2)
        self.author_entry = tk.Entry(frame)
        self.author_entry.grid(row=0, column=3)

        tk.Label(frame, text="Жанр:").grid(row=1, column=0)
        self.genre_entry = tk.Entry(frame)
        self.genre_entry.grid(row=1, column=1)

        tk.Label(frame, text="Страниц:").grid(row=1, column=2)
        self.pages_entry = tk.Entry(frame)
        self.pages_entry.grid(row=1, column=3)

        tk.Button(frame, text="Добавить книгу", command=self.add_book).grid(row=2, column=0, columnspan=4, pady=10)

        # Интерфейс фильтрации
        filter_frame = tk.LabelFrame(self.root, text="Фильтрация", padx=10, pady=5)
        filter_frame.pack(fill=tk.X, padx=10)

        tk.Label(filter_frame, text="Жанр:").pack(side=tk.LEFT)
        self.filter_genre = tk.Entry(filter_frame)
        self.filter_genre.pack(side=tk.LEFT, padx=5)

        tk.Label(filter_frame, text="Мин. страниц:").pack(side=tk.LEFT)
        self.filter_pages = tk.Entry(filter_frame, width=5)
        self.filter_pages.pack(side=tk.LEFT, padx=5)

        tk.Button(filter_frame, text="Применить", command=self.update_table).pack(side=tk.LEFT, padx=5)
        tk.Button(filter_frame, text="Сброс", command=self.reset_filter).pack(side=tk.LEFT)

        # Таблица
        self.tree = ttk.Treeview(self.root, columns=("Title", "Author", "Genre", "Pages"), show="headings")
        self.tree.heading("Title", text="Название")
        self.tree.heading("Author", text="Автор")
        self.tree.heading("Genre", text="Жанр")
        self.tree.heading("Pages", text="Страниц")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.update_table()

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages = self.pages_entry.get().strip()

        if not (title and author and genre and pages):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        if not pages.isdigit():
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return

        new_book = {"title": title, "author": author, "genre": genre, "pages": int(pages)}
        self.books.append(new_book)
        self.save_data()
        self.update_table()
        
        # Очистка полей
        for entry in (self.title_entry, self.author_entry, self.genre_entry, self.pages_entry):
            entry.delete(0, tk.END)

    def update_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        genre_f = self.filter_genre.get().lower()
        pages_f = self.filter_pages.get()

        for book in self.books:
            if genre_f and genre_f not in book['genre'].lower():
                continue
            if pages_f and book['pages'] < int(pages_f):
                continue
            self.tree.insert("", tk.END, values=(book['title'], book['author'], book['genre'], book['pages']))

    def reset_filter(self):
        self.filter_genre.delete(0, tk.END)
        self.filter_pages.delete(0, tk.END)
        self.update_table()

    def save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()
