# Copyright (c) 2026 Czuz
# Source: https://github.com/Czuz/zgadnij-liczbe
#
# This file is part of a project licensed under the MIT License.
# See the LICENSE file in the project root for full license text.

import random
from datetime import datetime
from math import ceil, log2

numbers_range = 100
secret = 0


def input_number(label: str) -> int:
    result = None

    while not result:
        try:
            result = int(input(label))
        except ValueError:
            print("Błędna liczba, spróbuj ponownie...")

    return result


def input_player_names(label: str):
    yield from input(label).split('\n')


def guess_random(min: int, max: int) -> int:
    return random.randrange(min, max) + 1


class Player:
    def __init__(self, name: str):
        self.name = name
        self.type = "🎮"
        self.attempts = 0
        self.total_attempts = 0
        self.min_guess = 0
        self.max_guess = numbers_range

    def __str__(self):
        return f"[{self.type}] {self.name}"

    def __format__(self, format_spec):
        return format(str(self), format_spec)

    def guess(self) -> int:
        self.attempts += 1
        self.total_attempts += 1
        return input_number("Zgadnij tajemniczą liczbę: ")

    def feedback(self, guess: int, hilo: int):
        if hilo < 0:
            self.max_guess = min(self.max_guess, guess - 1)
        elif hilo > 0:
            self.min_guess = max(self.min_guess, guess)

    def reset(self):
        self.attempts = 0
        self.min_guess = 0
        self.max_guess = numbers_range


class RandomBot(Player):
    def __init__(self, name: str):
        super().__init__(name)
        self.type = "🎲"

    def guess(self) -> int:
        self.attempts += 1
        self.total_attempts += 1
        return guess_random(0, numbers_range)


class SequencingBot(Player):
    def __init__(self, name: str):
        super().__init__(name)
        self.type = "🔢"

    def guess(self) -> int:
        self.attempts += 1
        self.total_attempts += 1
        return self.min_guess % numbers_range + 1


class PersistentBot(Player):
    def __init__(self, name: str):
        super().__init__(name)
        self.type = "📝"

    def guess(self) -> int:
        self.attempts += 1
        self.total_attempts += 1
        return guess_random(self.min_guess, self.max_guess)


class SmartBot(Player):
    def __init__(self, name: str):
        super().__init__(name)
        self.type = "🧠"

    def guess(self) -> int:
        self.attempts += 1
        self.total_attempts += 1
        return (self.min_guess + self.max_guess) // 2 + 1


class CheatingBot(Player):
    def __init__(self, name: str):
        super().__init__(name)
        self.type = "👀"

    def guess(self) -> int:
        self.attempts += 1
        self.total_attempts += 1
        if self.attempts < ceil(log2(numbers_range)) - 1:
            return guess_random(0, numbers_range)
        else:
            return secret


def get_random_bot(name: str) -> Player:
    pct = random.randrange(0, 100) + 1
    if pct <= 10:
        return CheatingBot(name)
    elif pct <= 30:
        return SequencingBot(name)
    elif pct <= 70:
        return PersistentBot(name)
    elif pct <= 90:
        return SmartBot(name)
    else:
        return RandomBot(name)


def game():
    random.seed(datetime.now().timestamp())
    global numbers_range
    global secret
    players = []

    numbers_range = input_number(
        "Z jakiego przedziału losować liczby? Od 1 do... ? ")
    turns_num = input_number("Ile rund chcesz rozegrać? ")

    print("""
Wpisz imiona graczy pojedynczo, oddzielając je klawiszem Enter (użyj „bot Imię”, by dodać komputer).
Po ostatnim graczu naciśnij Enter dwukrotnie, aby rozpocząć rozgrywkę.
Możesz wkleić listę korzystając z kombinacji klawiszy Ctrl+Shift+V
""")

    try:
        end = False
        while not end:
            for name in input_player_names(""):
                if not name:
                    end = True
                    break

                if name.startswith("bot "):
                    players.append(get_random_bot(name[4:]))
                else:
                    players.append(Player(name))
    except EOFError:
        pass

    players_num = len(players)
    if players_num == 0:
        print("Nie dodano żadnych graczy...")
        return

    print(
        f"Zaczynamy grę z {players_num} graczami: {', '.join(str(player) for player in players)}")

    for i in range(0, turns_num):
        print(f"📢 Runda {i+1}")
        for j in range(0, players_num):
            print(f"📢 Teraz zgaduje {players[j]}")
            secret = random.randrange(0, numbers_range) + 1
            guess = 0
            for i in range(0, players_num):
                players[i].reset()

            while True:
                guess = players[j].guess()
                players[j].feedback(guess, secret - guess)

                if players[j].attempts > numbers_range * 5:
                    print(
                        f"Przekroczono limit prób ({numbers_range * 5}), tajemnicza liczba to {secret}")
                    break

                if guess < secret:
                    print(f"{guess} to za mało 👆")
                elif guess > secret:
                    print(f"{guess} to za dużo 👇")
                else:
                    print(f"Brawo 🎉, tajemnicza liczba to {guess}")
                    break

    results = [player.total_attempts for player in players]
    top_scores = dict(zip(sorted(set(results))[:3], ["🥇", "🥈", "🥉"]))
    ranking = sorted(zip(results, [top_scores.get(
        result, "  ") for result in results], [str(player) for player in players]))
    result = """
Wyniki:
   Gracz                 Średnia liczba prób
--------------------------------------------
"""
    for r in ranking:
        result += f"{r[1]} {r[2]:<20} {r[0]/turns_num:<.2f}\n"

    result += """
Legenda:
  🥇 - Pierwsze miejsce         🎮 - gracz                  📝 - bot skrupulatny
  🥈 - Drugie miejsce           🎲 - bot losujący           🧠 - bot sprytny
  🥉 - Trzecie miejsce          🔢 - bot odliczający        👀 - bot cwaniak
"""

    print(result)


if __name__ == "__main__":
    while True:
        game()
        if input("Naciśnij Enter, aby zagrać ponownie lub wpisz 'koniec', aby zakończyć...\n") == "koniec":
            break
