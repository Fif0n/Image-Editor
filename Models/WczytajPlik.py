import tkinter as tk
from tkinter import filedialog
import shutil
import os

class WczytajPlik:
    @staticmethod
    def zapisz_plik(sciezka_pliku: str, sciezka_zapisu: str) -> None:
        nazwa_pliku = os.path.basename(sciezka_pliku)
        sciezka_zapisu = os.path.join(sciezka_zapisu, nazwa_pliku)

        shutil.copyfile(sciezka_pliku, sciezka_zapisu)

    @classmethod
    def otworz_dialog(cls) -> None:
        sciezka_pliku = filedialog.askopenfilename(
            initialdir='./', title='Wybierz plik',
            filetypes=[("Zdjęcia", ".jpg .png")]
        )

        if sciezka_pliku:
            cls.zapisz_plik(sciezka_pliku, './assets/')
        else:
            print("Nie wybrano żadnego pliku.")

    @classmethod
    def otworz_okno_startowe(cls) -> None:
        root = tk.Tk()
        root.withdraw()

        popup = tk.Toplevel()
        popup.title("Edytor obrazu")
        popup.geometry("300x300")

        button = tk.Button(popup, text="Wybierz plik", command=cls.otworz_dialog)
        button.pack(pady=20)

        popup.mainloop()