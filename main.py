import os
import shutil
import cv2
from abc import ABC, abstractmethod
import sys
import numpy

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
1.Transformuj do RGB
2.Transformuj do CMYK
3.Transformuj do HSV
0.Powrot
        """)


class Edytor(ABC):
    def __init__(self, obraz: str):
        if self.__sprawdz_rozszerzenie(obraz):
            self.obraz = cv2.imread(obraz, 1)
            self.sciezka = obraz
        else:
            print("Podano nieporawne rozszerzenie pliku. Dozwolone rozszerzenia to: png, jpg, jpeg")
            sys.exit()

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
        cv2.imwrite('zapisany_obraz.png', self.obraz)

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
        wyrownanie = cv2.equalizeHist(self.obraz)
        self.obraz = numpy.hstack((self.obraz, wyrownanie))

wczytaj_plik = WczytajPlik()

sciezka_do_pliku = input("Podaj scieżkę do pliku: ")
sciezka_zapisanego_pliku = wczytaj_plik.zapisz_plik(sciezka_do_pliku)

if sciezka_zapisanego_pliku:
    menu = Menu()
    menu.wypisz_menu()

    edytor = EdytorObrazu(sciezka_zapisanego_pliku)

    while True:
        opcja = input()
        if opcja == '1':
            edytor.zapisz_obraz()
        elif opcja == '2':
            edytor.pokaz_obraz()
        elif opcja == '3':
            menu.przestrzenie_barw()
            pod_opcja = input()
            if pod_opcja == '1':
                pass
            elif pod_opcja == '2':
                pass
            elif pod_opcja == '3':
                pass
            elif pod_opcja == '0':
                print("Powrócono do menu głównego")
                menu.wypisz_menu()
            else:
                print("Brak takiej opcji. Powrócono do menu głównego")
                menu.wypisz_menu()
        elif opcja == '5':
            edytor.binaryzacja()
        elif opcja == '7':
            edytor.wyrownanie_histogramu()
        elif opcja == '9':
            edytor.wygladzanie_przez_usrednianie()
        elif opcja == '0':
            cv2.destroyAllWindows()
            break
