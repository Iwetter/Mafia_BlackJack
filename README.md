# Blackjack: Mafia Debt

A command-line Blackjack game written in **Python** that combines traditional Blackjack mechanics with a risk-based mafia debt system.

The player begins the game owing money to the mafia and has a limited number of rounds to earn enough money to survive. Winning and losing affects not only the player's money, but also **mafia pressure**, debt, and the possible ending of the game.

## 🎮 Game Overview

You owe money to the mafia.

Your goal is to use Blackjack to earn enough money to pay off your debt before time runs out or mafia pressure reaches its limit.

Between rounds, random events can increase the pressure, cost you money, or leave you alone.

If you fail to pay the debt in time, the mafia finds you and you must decide whether to:

* Pay
* Run
* Fight

Your decisions, health, difficulty level, money, and mafia pressure determine your chances of survival.

## ✨ Features

* Traditional Blackjack gameplay
* Hit and stand actions
* Double-down mechanic
* Ace value adjustment
* Randomized 52-card deck
* Three difficulty levels
* Dynamic dealer behavior
* Player money and debt system
* Mafia pressure mechanic
* Random mafia events
* Health system
* Debt-payment system
* JSON save/load functionality
* Multiple possible endings

## 🃏 Blackjack System

The game uses a standard 52-card deck containing:

* Hearts
* Diamonds
* Clubs
* Spades

Face cards are worth **10**, while aces initially count as **11**.

If a hand exceeds 21, aces automatically change from 11 to 1 when possible to prevent the player from unnecessarily busting.

Players can:

1. **Hit** — draw another card
2. **Stand** — keep their current hand
3. **Double Down** — double the bet, receive exactly one additional card, and automatically end the turn

The player wins by finishing closer to 21 than the dealer without exceeding 21.

## 🎚️ Difficulty Levels

### Easy

* Starting Money: **$150**
* Starting Debt: **$250**
* Starting Mafia Pressure: **10**
* Maximum Rounds: **10**
* Less aggressive dealer behavior

### Normal

* Starting Money: **$100**
* Starting Debt: **$300**
* Starting Mafia Pressure: **20**
* Maximum Rounds: **8**
* Balanced dealer behavior

### Hard

* Starting Money: **$75**
* Starting Debt: **$400**
* Starting Mafia Pressure: **30**
* Maximum Rounds: **7**
* More aggressive mafia pressure
* Shadier dealer behavior

## 💰 Debt System

Players can use their winnings to make payments toward their mafia debt.

Payments:

* Reduce available money
* Reduce remaining debt
* Reduce mafia pressure

Paying the entire debt unlocks the **Free at Last** ending.

## 🚨 Mafia Pressure

Mafia pressure represents how close the player is to being confronted.

Pressure can change based on:

* Winning Blackjack rounds
* Losing Blackjack rounds
* Difficulty level
* Making debt payments
* Random mafia events

If mafia pressure reaches **100**, the mafia finds the player.

## 🎲 Random Events

After Blackjack rounds, random mafia events can occur.

Examples include:

* A mafia member warning the player that time is running out
* Losing money to the mafia
* Successfully keeping a low profile

These events create additional risk outside of the Blackjack table.

## 🏃 Final Confrontation

If the player runs out of rounds, reaches maximum mafia pressure, or loses all available money, the mafia confronts them.

The player can choose to:

### Pay

If enough money has been earned, the debt can be paid and the player walks away.

### Run

The chance of escaping depends on:

* Difficulty
* Mafia pressure

Higher mafia pressure makes escaping more difficult.

### Fight

The chance of winning a fight depends on:

* Player health
* Mafia pressure
* Difficulty

Failed attempts reduce health and increase mafia pressure.

## 🏁 Endings

The game contains several possible endings, including:

* **Free at Last**
* **Debt Paid**
* **On the Run**
* **Last Stand**
* **Caught by the Mafia**
* **Beatdown**

## 💾 Save System

The game supports saving and loading progress using JSON.

Saved information includes:

* Difficulty
* Maximum rounds
* Dealer behavior
* Money
* Debt
* Health
* Mafia pressure
* Current round

This allows the player's game state to be reconstructed when a saved game is loaded.

## 🧱 Program Structure

The project is separated into two main Python files.

### `game.py`

Contains the primary game systems, including:

* `Player`
* `Dealer`
* `Game`
* Blackjack rounds
* Difficulty selection
* Betting
* Mafia events
* Debt management
* Save/load functionality
* Ending logic

### `tools.py`

Contains the reusable card-game components:

* `Card`
* `Deck`
* `Hand`

This separates the Blackjack card logic from the larger game-state and story systems.

## 🛠️ Technologies

* **Python**
* Object-Oriented Programming
* JSON file handling
* Randomization
* File I/O
* Input validation
* Game-state management

No external Python libraries are required.

## ▶️ Running the Game

Make sure Python 3 is installed.

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/Blackjack-Mafia-Debt.git
```

Enter the project directory:

```bash
cd Blackjack-Mafia-Debt
```

Run:

```bash
python game.py
```

## 📚 What I Learned

This project helped me practice designing a larger Python program using object-oriented programming rather than placing all functionality inside a single script.

I gained experience with:

* Designing and interacting with multiple classes
* Separating game components across Python modules
* Managing changing game state
* Implementing probability-based events
* Validating user input
* Reading and writing JSON files
* Building save/load functionality
* Translating Blackjack rules into program logic
* Creating difficulty-dependent gameplay systems
* Designing multiple game outcomes

The project also gave me experience expanding a simple card game into a larger system where different mechanics interact with each other.

## 🔮 Future Improvements

Possible future additions include:

* Graphical user interface
* Card graphics and animations
* Improved Blackjack rules
* Natural Blackjack payouts
* Betting statistics
* More mafia events
* More story decisions
* Additional endings
* Improved save-file management
* Sound effects and music

## Author

**Ian Hall**
Electrical Engineering
Georgia Institute of Technology
