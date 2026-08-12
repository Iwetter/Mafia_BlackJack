import json
import random
from tools import Deck, Hand
SAVE_FILE = "save_game.json"

class Player:
    def __init__(self, money=100, debt=300, health=100, pressure=20, round_number=1):
        self.money = money
        self.debt = debt
        self.health = health
        self.pressure = pressure
        self.round_number = round_number

    def to_dictionary(self):
        return {
            "money": self.money,
            "debt": self.debt,
            "health": self.health,
            "pressure": self.pressure,
            "round_number": self.round_number
        }


class Dealer:
    def __init__(self, shadiness):
        self.shadiness = shadiness

    def get_hit_limit(self):
        if self.shadiness == "low":
            return 16
        elif self.shadiness == "medium":
            return 17
        else:
            return random.choice([17, 18, 19])


class Game:
    def __init__(self):
        self.player = Player()
        self.deck = Deck()
        self.max_rounds = 8
        self.difficulty = "normal"
        self.dealer = Dealer("medium")

    def title_screen(self):
        print("BLACKJACK: MAFIA DEBT")
        print("You owe the mafia money")
        print("You have limited rounds to win enough cash")
        print("If you fail, you must pay, run, or fight")
        

    def choose_difficulty(self):
        while True:
            print("\nChoose difficulty:")
            print("1. Easy")
            print("2. Normal")
            print("3. Hard")

            choice = input("Choose 1, 2, or 3: ")

            if choice == "1":
                self.difficulty = "easy"
                self.player = Player(money=150, debt=250, health=100, pressure=10)
                self.max_rounds = 10
                self.dealer = Dealer("low")
                print("\nEasy mode selected")
                break

            elif choice == "2":
                self.difficulty = "normal"
                self.player = Player(money=100, debt=300, health=100, pressure=20)
                self.max_rounds = 8
                self.dealer = Dealer("medium")
                print("\nNormal mode selected")
                break

            elif choice == "3":
                self.difficulty = "hard"
                self.player = Player(money=75, debt=400, health=100, pressure=30)
                self.max_rounds = 7
                self.dealer = Dealer("high")
                print("\nHard mode selected")
                print("The mafia is more aggressive and the dealer is shadier")
                break

            else:
                print("Invalid choice.")

    def show_stats(self):
        print("\n         STATS      ")
        print(f"Difficulty: {self.difficulty}")
        print(f"Money: ${self.player.money}")
        print(f"Debt: ${self.player.debt}")
        print(f"Health: {self.player.health}")
        print(f"Mafia Pressure: {self.player.pressure}/100")
        print(f"Round: {self.player.round_number}/{self.max_rounds}\n")

    def save_game(self):
        try:
            save_data = {
                "difficulty": self.difficulty,
                "max_rounds": self.max_rounds,
                "dealer_shadiness": self.dealer.shadiness,
                "player": self.player.to_dictionary()
            }

            with open(SAVE_FILE, "w") as file:
                json.dump(save_data, file)

            print("Game saved")

        except:
            print("Something went wrong")

    def load_game(self):
        try:
            with open(SAVE_FILE, "r") as file:
                data = json.load(file)

            player_data = data["player"]

            self.player = Player(
                money=player_data["money"],
                debt=player_data["debt"],
                health=player_data["health"],
                pressure=player_data["pressure"],
                round_number=player_data["round_number"]
            )

            self.difficulty = data["difficulty"]
            self.max_rounds = data["max_rounds"]
            self.dealer = Dealer(data["dealer_shadiness"])

            print("Game loaded.")

        except FileNotFoundError:
            print("No save file was found.")
        except:
            print("Something went wrong while loading.")

    def get_bet(self):
        while True:
            try:
                bet = int(input("Enter your bet: $"))

                if bet <= 0:
                    print("Bet must be greater than 0")
                elif bet > self.player.money:
                    print("You cannot bet more than you have")
                else:
                    return bet

            except ValueError:
                print("Please enter a valid number")

    def play_blackjack(self):
        print("\nBlackjack round is starting")
        bet = self.get_bet()
        player_hand = Hand()
        dealer_hand = Hand()
        player_hand.add_card(self.deck.deal())
        player_hand.add_card(self.deck.deal())
        dealer_hand.add_card(self.deck.deal())
        dealer_hand.add_card(self.deck.deal())
        can_double_down = True

        while True:
            print("\nYour hand:", player_hand.show())
            print("Your total:", player_hand.get_total())
            print("Dealer shows:", dealer_hand.cards[0])

            if player_hand.get_total() > 21:
                print("You busted!")
                self.player.money -= bet
                self.after_loss()
                return

            print("\nChoose your move:")
            print("1. Hit")
            print("2. Stand")

            if can_double_down and self.player.money >= bet * 2:
                print("3. Double Down")

            choice = input("Choose an option: ")

            if choice == "1":
                player_hand.add_card(self.deck.deal())
                can_double_down = False

            elif choice == "2":
                break

            elif choice == "3" and can_double_down and self.player.money >= bet * 2:
                bet *= 2
                print(f"\nYou doubled down. Your bet is now ${bet}.")
                print("You get exactly one more card.")

                player_hand.add_card(self.deck.deal())

                print("\nYour hand:", player_hand.show())
                print("Your total:", player_hand.get_total())

                if player_hand.get_total() > 21:
                    print("You busted after doubling down!")
                    self.player.money -= bet
                    self.after_loss()
                    return

                break

            else:
                print("Invalid choice!!!!")

        print("\nDealer hand:", dealer_hand.show())
        print("Dealer total:", dealer_hand.get_total())

        hit_limit = self.dealer.get_hit_limit()

        if self.dealer.shadiness == "high":
            print(f"The dealer seems shady. Dealer will hit until at least {hit_limit}.")
        elif self.dealer.shadiness == "low":
            print(f"The dealer is less aggressive. Dealer will hit until {hit_limit}.")
        else:
            print(f"Dealer will hit until {hit_limit}.")

        while dealer_hand.get_total() < hit_limit:
            print("\nDealer hits.")
            dealer_hand.add_card(self.deck.deal())
            print("Dealer hand:", dealer_hand.show())
            print("Dealer total:", dealer_hand.get_total())

        player_total = player_hand.get_total()
        dealer_total = dealer_hand.get_total()

        if dealer_total > 21:
            print("\nDealer busted. You win!")
            self.player.money += bet
            self.after_win()

        elif player_total > dealer_total:
            print("\nYou win!")
            self.player.money += bet
            self.after_win()

        elif player_total < dealer_total:
            print("\nDealer wins.")
            self.player.money -= bet
            self.after_loss()

        else:
            print("\nPush. Nobody wins.")

    def after_win(self):
        if self.difficulty == "easy":
            pressure_drop = 15
        elif self.difficulty == "hard":
            pressure_drop = 5
        else:
            pressure_drop = 10

        self.player.pressure -= pressure_drop

        if self.player.pressure < 0:
            self.player.pressure = 0

        print(f"Mafia pressure went down by {pressure_drop}.")

    def after_loss(self):
        if self.difficulty == "easy":
            pressure_gain = 10
        elif self.difficulty == "hard":
            pressure_gain = 20
        else:
            pressure_gain = 15

        self.player.pressure += pressure_gain

        if self.player.pressure > 100:
            self.player.pressure = 100

        print(f"Mafia pressure went up by {pressure_gain}.")

    def pay_debt(self):
        print("\nYou can pay part of your debt.")
        print(f"You have ${self.player.money}.")
        print(f"You owe ${self.player.debt}.")

        choice = input("Do you want to make a payment? yes/no: ").lower()

        if choice == "yes":
            while True:
                try:
                    amount = int(input("How much do you want to pay? $"))

                    if amount <= 0:
                        print("Payment must be more than 0")
                    elif amount > self.player.money:
                        print("You do not have that much money")
                    elif amount > self.player.debt:
                        print("You do not owe that much(Don't let the Mafia know you have that much shhh!!)")
                    else:
                        self.player.money -= amount
                        self.player.debt -= amount
                        self.player.pressure -= 10

                        if self.player.pressure < 0:
                            self.player.pressure = 0

                        print(f"You paid ${amount}.")
                        break

                except ValueError:
                    print("Please enter a valid number")

    def mafia_event(self):
        event = random.randint(1, 3)
        print("\nMafia event:")
        if event == 1:
            print("A mafia member warns you that time is running out")

            if self.difficulty == "easy":
                pressure_gain = 5
            elif self.difficulty == "hard":
                pressure_gain = 15
            else:
                pressure_gain = 10

            self.player.pressure += pressure_gain
            print(f"Mafia pressure went up by {pressure_gain}.")

        elif event == 2:
            print("You keep a low profile. Nothing happens.")

        else:
            print("The mafia takes $10 from your pocket.")

            if self.player.money >= 10:
                self.player.money -= 10
            else:
                self.player.money = 0

        if self.player.pressure > 100:
            self.player.pressure = 100

    def final_scene(self):
        print("        THE MAFIA FINDS YOU")
       
        while True:
            print("\nWhat do you do?")
            print("1. Pay the debt")
            print("2. Run")
            print("3. Fight")

            choice = input("Choose 1, 2, or 3: ")

            if choice == "1":
                if self.player.money >= self.player.debt:
                    print("You pay the mafia and walk away safely.")
                    print("ENDING: Debt Paid")
                    return True
                else:
                    print("You do not have enough money.")

            elif choice == "2":
                if self.difficulty == "easy":
                    chance = 45 - self.player.pressure // 5
                elif self.difficulty == "normal":
                    chance = 35 - self.player.pressure // 4
                else:
                    chance = 25 - self.player.pressure // 3

                if chance < 10:
                    chance = 10
                if chance > 55:
                    chance = 55

                print(f"Escape chance: {chance}%")

                if random.randint(1, 100) <= chance:
                    print("You escape into the night.")
                    print("ENDING: On the Run")
                    return True
                else:
                    print("You fail to escape. You lose 30 health.")
                    self.player.health -= 30
                    self.player.pressure += 10

                    if self.player.pressure > 100:
                        self.player.pressure = 100

                    if self.player.health <= 0:
                        print("ENDING: Caught by the Mafia")
                        return True

                    print(f"Health left: {self.player.health}")
                    print(f"Mafia pressure is now {self.player.pressure}/100.")

            elif choice == "3":
                chance = 40 + self.player.health // 5 - self.player.pressure // 5

                if self.difficulty == "easy":
                    chance += 10
                elif self.difficulty == "hard":
                    chance -= 10

                if chance < 10:
                    chance = 10
                if chance > 60:
                    chance = 60

                print(f"Fight chance: {chance}%")

                if random.randint(1, 100) <= chance:
                    print("You fight your way out")
                    print("ENDING: Last Stand")
                    return True
                else:
                    print("You lose the fight. You lose 40 health")
                    self.player.health -= 40
                    self.player.pressure += 15

                    if self.player.pressure > 100:
                        self.player.pressure = 100

                    if self.player.health <= 0:
                        print("ENDING: Beatdown")
                        return True

                    print(f"Health left: {self.player.health}")
                    print(f"Mafia pressure is now {self.player.pressure}/100")

            else:
                print("Invalid choice.")

    def check_game_over(self):
        if self.player.debt <= 0:
            print("\nYou paid off the mafia")
            print("ENDING: Free at Last")
            return True

        if self.player.money <= 0:
            print("\nYou ran out of money")
            print("The mafia realizes you are broke. Mafia pressure maxes out")
            self.player.pressure = 100
            return self.final_scene()

        if self.player.pressure >= 100:
            print("\nMafia pressure reached 100")
            return self.final_scene()

        if self.player.round_number > self.max_rounds:
            print("\nYou ran out of rounds")
            return self.final_scene()

        return False

    def main_menu(self):
        while True:
            print("\nMain Menu")
            print("1. Start New Game")
            print("2. Load Game")
            print("3. Instructions")
            print("4. Quit")

            choice = input("Choose an option: ")

            if choice == "1":
                self.choose_difficulty()
                break
            elif choice == "2":
                self.load_game()
                break
            elif choice == "3":
                self.instructions()
            elif choice == "4":
                print("Goodbye.")
                quit()
            else:
                print("Invalid choice.")

    def instructions(self):
        print("""
Blackjack Rules:
Try to get closer to 21 than the dealer
If you go over 21, you bust
The dealer must hit until reaching 17
You can hit, stand, or double down

Double Down:
Doubling down doubles your bet
You receive only one more card
Then your turn automatically ends

Game Rules:
You owe money to the mafia
You have a limited number of rounds to earn enough money
After each round, mafia pressure may change
If pressure reaches 100, or you run out of time or money, the mafia finds you
Then you must pay, run, or fight

Difficulty:
Easy gives you more money, lower debt, and less mafia pressure
Normal is balanced
Hard gives you less money, more debt, more mafia pressure, and a shadier dealer
""")

    def play(self):
        self.title_screen()
        self.main_menu()

        while True:
            self.show_stats()

            if self.check_game_over():
                break

            print("\nChoose your action:")
            print("1. Play Blackjack")
            print("2. Pay Debt")
            print("3. Save Game")
            print("4. Quit")

            choice = input("Choose an option: ")

            if choice == "1":
                self.play_blackjack()
                self.mafia_event()
                self.player.round_number += 1
            elif choice == "2":
                self.pay_debt()
            elif choice == "3":
                self.save_game()
            elif choice == "4":
                print("You're leavin the table and are safe for now...")
                break
            else:
                print("Invalid choice")


game = Game()
game.play()