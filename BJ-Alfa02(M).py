import numpy as np
import random
import copy
import os
import time


class ResetFunkcji(Exception):
    pass


WARTOSCI = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
            'J': 10, 'Q': 10, 'K': 10, 'A': 11}


def gra():
    money = 1000
    debt = 2000
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=== NEW HAND ===")
        print("Money: ", money)
        print("Debt: ", debt)
        money, debt = bet(money, debt)

        if debt > 0:
            debt = int(debt * 1.05)
            print(f"Interest applied (+5%). New Debt: {debt}")

        print("\n-------------------")
        dalej = input("Play another hand? (y/n): ").lower()
        if dalej not in ("y", "yes", "tak"):
            menu_aktywne = True
            while menu_aktywne:
                print(f"\nCurrent Balance - Money: {money}, Debt: {debt}")
                print("1. Pay off debt")
                print("2. Change mind (Continue playing)")
                print("3. Quit game")
                wybor = input("Choose an option (1-3): ")
                if wybor == "1":
                    if debt <= 0:
                        print("You have no debt to pay off!")
                        continue
                    try:
                        splata = int(input(f"How much do you want to pay off? "))
                        if splata <= 0:
                            print("Amount must be positive!")
                        elif splata > money:
                            print("You don't have enough money!")
                        else:
                            money -= splata
                            debt -= splata
                            print(f"Paid off {splata}. New Debt: {debt}, Money left: {money}")
                    except ValueError:
                        print("Please enter a valid number!")
                elif wybor == "2":
                    menu_aktywne = False
                elif wybor == "3":
                    print(f"\nThank you for playing! Final Balance - Money: {money}, Debt: {debt}")
                    return


def bet(money, debt):
    while True:
        try:
            bet_a = int(input("Bet money: "))
            break
        except ValueError:
            print("Please enter a valid number!")

    money -= bet_a
    print("Money left:", money)
    while money < 0:
        money, debt = kredyt(money, debt)
    if bet_a > 0 and money >= 0:
        money, debt = blackjack(money, debt, bet_a)
    return money, debt


def hit_me(deck):
    if len(deck) == 0:
        print("Deck is empty!")
        return None, deck
    card = deck[0]
    updated_deck = np.delete(deck, 0)
    return card, updated_deck


def oblicz_punkty(reka_gracza):
    suma = sum(WARTOSCI[str(karta)] for karta in reka_gracza)
    asy = sum(1 for karta in reka_gracza if str(karta) == 'A')
    while suma > 21 and asy > 0:
        suma -= 10
        asy -= 1
    return suma


def blackjack(money, debt, bet_a):
    karty = np.arange(2, 15).astype(object)
    karty[9] = "J"
    karty[10] = "Q"
    karty[11] = "K"
    karty[12] = "A"
    grupowane = np.repeat(karty, 4)
    przetasowane = copy.deepcopy(grupowane)

    tasowane = input("Shuffle? ").lower()
    if tasowane in ("y", "yes", "tak"):
        random.shuffle(przetasowane)
        print(przetasowane)
    else:
        matrix()
        time.sleep(5)
        raise ResetFunkcji

    zaczynasz = input("Start? (y/n): ").lower()
    if zaczynasz in ("y", "yes", "tak"):
        os.system("cls" if os.name == "nt" else "clear")
        reka_gracza = []
        reka_dilera = []
        for _ in range(2):
            karta_g, przetasowane = hit_me(przetasowane)
            reka_gracza.append(karta_g)
            karta_d, przetasowane = hit_me(przetasowane)
            reka_dilera.append(karta_d)

        punkty_gracza = oblicz_punkty(reka_gracza)
        print(f"Your cards: {', '.join(map(str, reka_gracza))} (Sum: {punkty_gracza})")
        print(f"Dealer's card: {reka_dilera[0]}, [Hidden]")
        print(f"Cards left: {len(przetasowane)}")

        if punkty_gracza == 21:
            print("\n★ NATURAL BLACKJACK! (Ace + 10 value card) ★")
            punkty_dilera = oblicz_punkty(reka_dilera)
            if punkty_dilera == 21:
                print(f"Dealer also has Blackjack ({', '.join(map(str, reka_dilera))})! Stand-off.")
                money += bet_a
            else:
                print("Dealer does not have Blackjack. You win 3:2!")
                money += int(bet_a * 2.5)
            print(f"New Balance: {money}, In debt: {debt}")
            return money, debt
    else:
        matrix()
        time.sleep(6)
        raise ResetFunkcji

    rece_gracza = [reka_gracza]
    stawki = [bet_a]
    return hitstand(przetasowane, rece_gracza, reka_dilera, money, debt, stawki)


def hitstand(przetasowane, rece_gracza, reka_dilera, money, debt, stawki):
    i = 0
    while i < len(rece_gracza):
        reka_aktualna = rece_gracza[i]
        while True:
            punkty_gracza = oblicz_punkty(reka_aktualna)
            if punkty_gracza >= 21:
                break

            print(f"\n--- Playing Hand {i + 1} of {len(rece_gracza)} ---")
            print(f"Your cards: {', '.join(map(str, reka_aktualna))} (Sum: {punkty_gracza})")

            opcje = "hit or stand"
            moze_split = len(reka_aktualna) == 2 and WARTOSCI[str(reka_aktualna[0])] == WARTOSCI[str(reka_aktualna[1])]
            moze_double = len(reka_aktualna) == 2 and money >= stawki[i]

            if moze_split: opcje += ", split"
            if moze_double: opcje += ", double"

            hit_card = input(f"To {opcje}: ").lower()

            if "hit" in hit_card:
                os.system("cls" if os.name == "nt" else "clear")
                wyciagnieta_karta, przetasowane = hit_me(przetasowane)
                reka_aktualna.append(wyciagnieta_karta)
                print(f"You drew: {wyciagnieta_karta}")
                if oblicz_punkty(reka_aktualna) > 21:
                    print(f"Your cards: {', '.join(map(str, reka_aktualna))} (Sum: {oblicz_punkty(reka_aktualna)})")
                    print("Bust! You exceeded 21 points on this hand.")
                    break
            elif "stand" in hit_card:
                os.system("cls" if os.name == "nt" else "clear")
                break
            elif "double" in hit_card and moze_double:
                os.system("cls" if os.name == "nt" else "clear")
                money -= stawki[i]
                stawki[i] *= 2
                print(f"Bet doubled to: {stawki[i]}. Money left: {money}")
                wyciagnieta_karta, przetasowane = hit_me(przetasowane)
                reka_aktualna.append(wyciagnieta_karta)
                print(f"You drew your only double card: {wyciagnieta_karta}")
                print(f"Your cards: {', '.join(map(str, reka_aktualna))} (Sum: {oblicz_punkty(reka_aktualna)})")
                if oblicz_punkty(reka_aktualna) > 21:
                    print("Bust! You exceeded 21 points.")
                break
            elif "split" in hit_card and moze_split:
                os.system("cls" if os.name == "nt" else "clear")
                money -= stawki[i]
                print(f"Hand split! Additional bet placed. Money left: {money}")
                karta_do_nowej_reki = reka_aktualna.pop(1)
                nowa_reka = [karta_do_nowej_reki]
                karta_dobrana1, przetasowane = hit_me(przetasowane)
                reka_aktualna.append(karta_dobrana1)
                karta_dobrana2, przetasowane = hit_me(przetasowane)
                nowa_reka.append(karta_dobrana2)
                rece_gracza.insert(i + 1, nowa_reka)
                stawki.insert(i + 1, stawki[i])
                continue
        i += 1
    return dealerturn(reka_dilera, przetasowane, rece_gracza, money, debt, stawki)


def dealerturn(reka_dilera, przetasowane, rece_gracza, money, debt, stawki):
    os.system("cls" if os.name == "nt" else "clear")
    wszystkie_busted = all(oblicz_punkty(reka) > 21 for reka in rece_gracza)

    print(f"Dealer's cards: {', '.join(map(str, reka_dilera))}")
    punkty_dilera = oblicz_punkty(reka_dilera)

    if not wszystkie_busted:
        while punkty_dilera < 17:
            print("Dealer's turn")
            time.sleep(1)
            nowa_karta, przetasowane = hit_me(przetasowane)
            reka_dilera.append(nowa_karta)
            punkty_dilera = oblicz_punkty(reka_dilera)
            print(f"Dealer takes: {nowa_karta} (Dealer's sum: {punkty_dilera})")
    else:
        print("Dealer wins automatically because all your hands busted.")

    print("\n--- Results ---")
    print(f"Dealer's final points: {punkty_dilera}")

    for idx, reka in enumerate(rece_gracza):
        punkty_gracza = oblicz_punkty(reka)
        print(f"\nHand {idx + 1} ({', '.join(map(str, reka))}): {punkty_gracza} points")

        if punkty_gracza > 21:
            print(f"Hand {idx + 1} busted! You lost {stawki[idx]}.")
        elif punkty_dilera > 21:
            print(f"Hand {idx + 1} wins {stawki[idx] * 2}!")
            money += stawki[idx] * 2
        elif punkty_gracza > punkty_dilera:
            print(f"Hand {idx + 1} wins {stawki[idx] * 2}!")
            money += stawki[idx] * 2
        elif punkty_gracza < punkty_dilera:
            print(f"Hand {idx + 1} loses against Dealer.")
        else:
            print(f"Hand {idx + 1} is a Draw! Bet {stawki[idx]} is returned.")
            money += stawki[idx]

    print(f"\nNew Balance: {money}, In debt: {debt}")
    return money, debt


def kredyt(money, debt):
    kredyta = [500, 2500, 5000]
    while True:
        opcja1 = input("Take a loan, or game over Cristopher? (y/n): ").lower()
        if opcja1 in ("y", "yes", "tak"):
            print("Fine.")
            try:
                opcja2 = int(input("How much: 500, 2500, 5000? "))
                if opcja2 in kredyta:
                    money += opcja2
                    debt += opcja2
                    print(f"New balance: {money}, In debt: {debt}")
                    return money, debt
                else:
                    print("There is no such option.")
            except ValueError:
                print("Please enter a valid amount!")
        else:
            print("Game Over Cristopher")
            exit()


def confirm():
    while True:
        start = input("START? (y/n): ").lower()
        if start in ("y", "yes", "tak"):
            print(start + " has been chosen, starting")
            gra()
            return start
        elif start in ("n", "no", "nie"):
            print("chosen not to start")
        else:
            print(start + " is not an option, try again")


def matrix():
    print("\n", "We don't need you in our squad")
    print("Adios amigo")
    time.sleep(4)
    os.system("cls" if os.name == "nt" else "clear")
    print("1T5 JU5T 4 M4TR1X")
    time.sleep(2)
    os.system("cls" if os.name == "nt" else "clear")


while True:
    try:
        confirm()
        break
    except ResetFunkcji:
        print("\n[!] Reloading the Matrix - Resetting Game...\n")
        continue
