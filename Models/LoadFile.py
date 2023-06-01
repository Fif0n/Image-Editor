import tkinter as tk
from tkinter import filedialog
import shutil
import os

class LoadFile:
    @staticmethod
    def save_file(path: str, destination: str) -> None:
        file_name = os.path.basename(path)
        destination_path = os.path.join(destination, file_name)

        shutil.copyfile(path, destination_path)

    @classmethod
    def open_file_dialog(cls) -> None:
        file_path = filedialog.askopenfilename(
            initialdir='./', title='Wybierz plik',
            filetypes=[("Zdjęcia", ".jpg .png")]
        )

        if file_path:
            cls.save_file(file_path, './assets/')
        else:
            print("Nie wybrano żadnego pliku.")

    @classmethod
    def open_popup(cls) -> None:
        root = tk.Tk()
        root.withdraw()

        popup = tk.Toplevel()
        popup.title("Edytor obrazu")
        popup.geometry("300x300")

        button = tk.Button(popup, text="Wybierz plik", command=cls.open_file_dialog)
        button.pack(pady=20)

        popup.mainloop()