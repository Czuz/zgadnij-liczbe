import random
from datetime import datetime


def input_number(label: str) -> int:
    result = None

    while not result:
        try:
            result = int(input(label))
        except ValueError:
            print("Błędna liczba, spróbuj ponownie...")

    return result


def guess_random(min: int, max: int) -> int:
    return random.randrange(min, max) + 1


def game():
    random.seed(datetime.now().timestamp())
    players = []
    results = []
    
    numbers_range = input_number("Z jakiego przedziału losować liczby? Od 1 do... ? ")
    turns_num = input_number("Ile rund chcesz rozegrać? ")
    players_num = input_number("Ilu będzie graczy? ")

    for i in range(0, players_num):
        players.append(input(f"Podaj imię {i+1}. gracza: "))
        results.append(0)

    for i in range(0, turns_num):
        print(f"📢 Runda {i+1}")
        for j in range(0, players_num):
            print(f"📢 Teraz zgaduje {players[j]}")
            secret = random.randrange(0, numbers_range) + 1
            
            guess = 0
            while True:
                guess = guess_random(0, numbers_range) # input_number("Zgadnij tajemniczą liczbę: ")
                results[j] += 1

                if guess < secret:
                    print("Za mało 👆")
                elif guess > secret:
                    print("Za dużo 👇")
                else:
                    print(f"Brawo 🎉, tajemnicza liczba to {guess}")
                    break

    top_scores = dict(zip(sorted(set(results))[:3], ["🥇","🥈","🥉"]))
    ranking = sorted(zip(results, [top_scores.get(result,"  ") for result in results], players))
    result = """
Wyniki:
   Gracz                Średnia liczba prób
-------------------------------------------
"""
    for r in ranking:
        result += f"{r[1]} {r[2]:<20} {r[0]/turns_num:<.2f}\n"

    print(result)


if __name__ == "__main__":
    game()
