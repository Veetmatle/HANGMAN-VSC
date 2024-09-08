import tkinter as tk
from tkinter import PhotoImage
import database_słowa
import sqlite3

class HangmanGame:
    def __init__(self, root):
        """
        Inicjalizuje grę w wisielca.

        Args:
            root (tk.Tk): Główne okno aplikacji tkinter.
        """
        self.root = root
        self.root.title("Wisielec")
        self.root.geometry("1000x800")  
        self.root.config(bg="black")  

        self.słowo = self.losuj_słowo()  
        self.odgadnięte_litery = []
        self.zgadywane_litery = [] 
        self.niepoprawne_próby = 0
        self.max_życia = 7

        self.obrazki = [PhotoImage(file=f"hangman_images/hangman_{i}.png").subsample(2, 2) for i in range(1, 8)] 
        self.canvas = tk.Canvas(root, width=400, height=400, bg="black", highlightbackground="white", highlightthickness=2)
        self.canvas.create_image(200, 200, image=self.obrazki[0])
        self.canvas.pack(pady=20)

        self.label_słowo = tk.Label(root, text=self.wyświetl_stan_gry(), font=("Arial", 30), bg="black", fg="white")
        self.label_słowo.pack(pady=20)

        self.entry_litera = tk.Entry(root, font=("Arial", 20), bg="gray", fg="white")
        self.entry_litera.pack()

        self.button_zgaduj = tk.Button(root, text="Zgadnij", command=self.zgaduj_literę, font=("Arial", 16), bg="gray", fg="white")
        self.button_zgaduj.pack(pady=10)

        self.label_życia = tk.Label(root, text=f"Pozostało żyć: {self.max_życia}", font=("Arial", 16), bg="black", fg="white")
        self.label_życia.pack(pady=10)

        self.label_komunikat = tk.Label(root, text="", font=("Arial", 16), bg="black", fg="white")
        self.label_komunikat.pack(pady=10)

        self.label_zgadywane = tk.Label(root, text="Zgadywane litery: ", font=("Arial", 16), bg="black", fg="white")
        self.label_zgadywane.pack(pady=10)

    def losuj_słowo(self):
        """
        Losuje słowo z bazy danych.

        Returns:
            str: Losowe słowo z bazy danych w formie małych liter.
        """
        conn = sqlite3.connect('slowa.db')
        c = conn.cursor()

        c.execute('SELECT slowo FROM slowa ORDER BY RANDOM() LIMIT 1')
        slowo = c.fetchone()[0]

        conn.close()
        return slowo.lower()

    def wyświetl_stan_gry(self):
        """
        Wyświetla aktualny stan gry.

        Returns:
            str: Tekst reprezentujący aktualny stan gry z odgadniętymi literami i miejscami na nieodgadnięte litery.
        """
        wynik = ''
        for litera in self.słowo:
            if litera in self.odgadnięte_litery:
                wynik += litera + ' '
            else:
                wynik += '_ '
        return wynik.strip()

    def zgaduj_literę(self):
        """
        Obsługuje zgadywanie litery przez użytkownika.

        Aktualizuje stan gry, obrazek wisielca, liczbę pozostałych żyć oraz komunikaty o błędach lub zakończeniu gry.
        """
        self.label_komunikat.config(text="", fg="white") 

        litera = self.entry_litera.get().lower()
        self.entry_litera.delete(0, tk.END)

        if not litera or len(litera) != 1:
            self.label_komunikat.config(text="Podaj jedną literę.", fg="red")
            return

        if litera in self.zgadywane_litery:
            self.label_komunikat.config(text="Już zgadywałeś tę literę.", fg="red")
            return

        self.zgadywane_litery.append(litera)
        self.label_zgadywane.config(text=f"Zgadywane litery: {', '.join(self.zgadywane_litery)}")

        if litera in self.słowo:
            self.odgadnięte_litery.append(litera)
            self.label_słowo.config(text=self.wyświetl_stan_gry())
            if all(l in self.odgadnięte_litery for l in self.słowo):
                self.koniec_gry("YOU WON! \n Congrats!", "green")
                return
        else:
            self.niepoprawne_próby += 1
            self.label_życia.config(text=f"Pozostało żyć: {self.max_życia - self.niepoprawne_próby}")
            if self.niepoprawne_próby != self.max_życia:
                self.canvas.create_image(200, 200, image=self.obrazki[self.niepoprawne_próby])

            if self.niepoprawne_próby == self.max_życia:
                self.koniec_gry(f"YOU LOST! \nSłowo to: \n{self.słowo}", "red")
                return  

    def koniec_gry(self, komunikat, color):
        """
        Kończy grę, wyświetlając komunikat o wyniku.

        Args:
            komunikat (str): Tekstowy komunikat o wyniku gry.
            color (str): Kolor tekstu komunikatu.
        """
        self.canvas.delete("all")  
        self.canvas.create_text(200, 200, text=komunikat, font=("Arial", 40), fill=color, anchor="center", justify="center")
        self.button_zgaduj.config(state=tk.DISABLED)
        
        self.root.geometry("800x600")


root = tk.Tk()
gra = HangmanGame(root)
root.mainloop()
