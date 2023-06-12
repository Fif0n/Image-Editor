import os
import shutil
import cv2

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


class Edytor:
    def __init__(self, obraz: str):
        self.obraz = cv2.imread(obraz, 1)
        self.sciezka = obraz

    def pokaz_obraz(self):
        cv2.imshow('Image', self.obraz)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def zapisz_obraz(self):
        cv2.imwrite('zapisany_obraz.png', self.obraz)

wczytaj_plik = WczytajPlik()

sciezka_do_pliku = input("Podaj scieżkę do pliku: ")
sciezka_zapisanego_pliku = wczytaj_plik.zapisz_plik(sciezka_do_pliku)

if sciezka_zapisanego_pliku:
    Menu().wypisz_menu()

    edytor = Edytor(sciezka_zapisanego_pliku)

    while True:
        opcja = input()
        if opcja == '1':
            edytor.zapisz_obraz()
        elif opcja == '2':
            edytor.pokaz_obraz()
        elif opcja == '0':
            break
