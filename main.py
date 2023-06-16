import os
import shutil
import cv2
from abc import ABC
import sys
import numpy as np
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename

class WczytajPlik:
    @staticmethod
    def zapisz_plik(sciezka_pliku: str) -> str:
        try:
            nazwa_pliku = os.path.basename(sciezka_pliku)
            sciezka_zapisu = os.path.join('', nazwa_pliku)

            shutil.copyfile(sciezka_pliku, sciezka_zapisu)

            return sciezka_zapisu
        except PermissionError:
            print('Podano niepoprawną ściężkę do pliku')
        except FileNotFoundError:
            print('Podano niepoprawną ściężkę do pliku')

class Menu:
    @staticmethod
    def wypisz_menu() -> None:
        print("""
1.Zapisz obraz
2.Pokaz obraz
3.Transformacja pomiędzy przestrzeniami barw
4.Negatyw
5.Binaryzacja
6.Sepia
7.Wyrównanie histogramu
8.Kompresja
9.Wygładzanie przez uśrednianie
0.Wyjdź
        """)

    @staticmethod
    def przestrzenie_barw():
        print("""
1.Transformuj HSV
2.Transformuj CMYK
0.Powrot
        """)


class Edytor(ABC):
    def __init__(self, obraz: str):
        if self.__sprawdz_rozszerzenie(obraz):
            self.obraz = cv2.imread(obraz, 1)
            self.sciezka = obraz
            nazwa, rozszerzenie = os.path.splitext(obraz)
            self.rozszerzenie = rozszerzenie[1:]
            self.nazwa = nazwa
        else:
            print("Podano nieporawne rozszerzenie pliku. Dozwolone rozszerzenia to: png, jpg, jpeg")
            self.obraz = None
            self.sciezka = None

    @staticmethod
    def __sprawdz_rozszerzenie(plik: str):
        if plik.endswith('.png') or plik.endswith('.jpg') or plik.endswith('.jpeg'):
            return True
        return False


class EdytorObrazu(Edytor):
    def __init__(self, obraz: str):
        super().__init__(obraz)

    def pokaz_obraz(self):
        cv2.imshow('Image', self.obraz)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def zapisz_obraz(self):
        root = Tk()
        root.withdraw()
        sciezka = asksaveasfilename(
            defaultextension=self.rozszerzenie,
            initialfile=self.nazwa
        )

        if sciezka:
            cv2.imwrite(sciezka, self.obraz)
            print("Zapisano plik")

    def __skala_szarosci(self):
        return cv2.cvtColor(self.obraz, cv2.COLOR_BGR2GRAY)

    def binaryzacja(self):
        szara_skala = self.__skala_szarosci()
        ret, self.obraz = cv2.threshold(szara_skala, 70, 255, 0)

    def wygladzanie_przez_usrednianie(self):
        macierz = (10, 10)
        self.obraz = cv2.blur(self.obraz, macierz)

    def wyrownanie_histogramu(self):
        self.obraz = self.__skala_szarosci()
        self.obraz = cv2.equalizeHist(self.obraz)

    def negatyw(self):
        self.obraz = cv2.bitwise_not(self.obraz)

    def sepia(self):
        # Zmiana wartości pikseli na float
        obraz = np.array(self.obraz, dtype=np.float64)
        # Transformacja obrazu na podstawie macierzy sepi
        obraz = cv2.transform(obraz, np.matrix(self.__macierz_do_ilosci_przestrzeni(obraz.shape[2])))

        # Wartości większe niż 255 zamieniamy na 255 (maksymalna wartość koloru piksela)
        obraz[np.where(obraz > 255)] = 255
        # Zamiana z powrotem na int
        self.obraz = np.array(obraz, dtype=np.uint8)  # converting back to int

    def kompresja(self):
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        result, encimg = cv2.imencode('.jpg', self.obraz, encode_param)
        self.obraz = cv2.imdecode(encimg, 1)

    def rgb_do_hsv(self):
        self.obraz = cv2.cvtColor(self.obraz, cv2.COLOR_BGR2HSV)

    def rgb_do_cmyk(self):
        # Make float and divide by 255 to give BGRdash
        obraz = self.obraz.astype(np.float64) / 255.

        # Przstrzen dla czarnego
        K = 1 - np.max(obraz, axis=2)
        # Przestrzen dla cyjanu
        C = (1 - obraz[..., 2] - K) / (1 - K)

        # Przestrzen dla magenty
        M = (1 - obraz[..., 1] - K) / (1 - K)

        # Przestrzen dla zoltego
        Y = (1 - obraz[..., 0] - K) / (1 - K)

        # Laczymy przestrzenie i zamieniamy z powrotem na int
        self.obraz = (np.dstack((C, M, Y, K)) * 255).astype(np.uint8)
    @staticmethod
    def __macierz_do_ilosci_przestrzeni(ilosc_przestrzeni: int):
        if ilosc_przestrzeni == 3:
            return [
                [0.272, 0.534, 0.131],
                [0.349, 0.686, 0.168],
                [0.393, 0.769, 0.189],
                [0.393, 0.769, 0.189]
            ]
        if ilosc_przestrzeni == 4:
            return [
                [0.272, 0.534, 0.131, 0],
                [0.349, 0.686, 0.168, 0],
                [0.393, 0.769, 0.189, 0],
                [0, 0, 0, 1]
            ]


wczytaj_plik = WczytajPlik()

sciezka_do_pliku = input("Podaj scieżkę do pliku: ")
sciezka_zapisanego_pliku = wczytaj_plik.zapisz_plik(sciezka_do_pliku)

if sciezka_zapisanego_pliku:
    edytor = EdytorObrazu(sciezka_zapisanego_pliku)

    if edytor.obraz is None:
        sys.exit()

    menu = Menu()
    menu.wypisz_menu()

    while True:
        opcja = input()
        if opcja == '1':
            edytor.zapisz_obraz()
        elif opcja == '2':
            edytor.pokaz_obraz()
        elif opcja == '3':
            menu.przestrzenie_barw()
            pod_opcja = input()
            wiadomosc_zwrotna = "Powrócono do menu głównego"

            if pod_opcja == '1':
                edytor.rgb_do_hsv()
            elif pod_opcja == '2':
                edytor.rgb_do_cmyk()
            elif pod_opcja == '0':
                menu.wypisz_menu()
            else:
                wiadomosc_zwrotna = "Brak takiej opcji. Powrócono do menu głównego"
                menu.wypisz_menu()
            print(wiadomosc_zwrotna)
        elif opcja == '4':
            edytor.negatyw()
        elif opcja == '5':
            edytor.binaryzacja()
        elif opcja == '6':
            edytor.sepia()
        elif opcja == '7':
            edytor.wyrownanie_histogramu()
        elif opcja == '8':
            edytor.kompresja()
        elif opcja == '9':
            edytor.wygladzanie_przez_usrednianie()
        elif opcja == '0':
            cv2.destroyAllWindows()
            break
        menu.wypisz_menu()
