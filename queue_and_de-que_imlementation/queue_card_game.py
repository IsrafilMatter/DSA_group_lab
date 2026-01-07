import random

class DeckOfCards:
    def __init__(self):
        self.suits = ["hearts", "diamonds", "clubs", "spades"]
        self.card_names = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]
        self.values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    
    def shuffle_cards(self):
        deck = [(suit, card_name, value) 
                for suit in self.suits 
                for card_name, value in zip(self.card_names, self.values)]
        
        random.shuffle(deck)
        
        player_card = deck.pop(0)
        player_value = player_card[2]
        
        higher_cards = [card for card in deck if card[2] > player_value]
        lower_cards = [card for card in deck if card[2] <= player_value]
        
        total_banker_cards = 5
        needed_higher = int(total_banker_cards * 0.75) # banker's card is always 75% higher than the player's card mwehehehe
        needed_lower = total_banker_cards - needed_higher
        
        if len(higher_cards) < needed_higher:
            needed_higher = len(higher_cards)
            needed_lower = total_banker_cards - needed_higher
        
        if len(lower_cards) < needed_lower:
            needed_lower = len(lower_cards)
            needed_higher = total_banker_cards - needed_lower
        
        banker_cards = random.sample(higher_cards, needed_higher) + random.sample(lower_cards, needed_lower)
        random.shuffle(banker_cards)
        
        remaining_deck = [card for card in deck if card not in banker_cards]
        
        return player_card, banker_cards

class Queue:
    def __init__(self):
        self.queue = []
    
    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        if self.queue:
            return self.queue.pop(0)
        return None
    
    def display(self):
        return self.queue

class Banker(Queue):
    def hold(self):
        return self.display()
    
    def draw(self):
        if self.queue:
            drawn_card = self.dequeue()
            return drawn_card
        else:
            return None
        
    def has_cards(self):
        return len(self.queue) > 0

class Player:
    def __init__(self, initial_cash=0):
        self.cash = initial_cash
    
    def cash_in(self, deposit):
        if deposit > 0:
            self.cash += deposit
            return self.cash
        else:
            print("Deposit must be positive")
            return self.cash
    
    def cash_out(self, amount):
        if amount > 0 and amount <= self.cash:
            self.cash -= amount
            return amount
        else:
            print("Insufficient funds or invalid amount")
            return 0
    
    def check_balance(self):
        return self.cash

class Game:
    def __init__(self, initial_cash=0, min_bet=10):
        self.player = Player(initial_cash)
        self.banker = Banker()
        self.bet = 0
        self.min_bet = min_bet

    def place_bet(self, bet_amount):
        if bet_amount < self.min_bet:
            print(f"Bet must be at least {self.min_bet}.")
            return False
        elif bet_amount > self.player.cash:
            print(f"Insufficient funds. You have {self.player.cash}.")
            return False
        else:
            self.bet = bet_amount
            self.player.cash -= bet_amount
            print("You bet:", self.bet)
            return True
        
    def player_won(self):
        if self.bet > 0:
            winnings = self.bet * 2
            self.player.cash += winnings
            print(f"You win {winnings}! New balance: {self.player.cash}")
            self.bet = 0
            return winnings
        return 0
    
    def player_lost(self):
        if self.bet > 0:
            print(f"You lose {self.bet}. New balance: {self.player.cash}")
            self.bet = 0

#-----initialize game-----#
deck = DeckOfCards()
player_card, banker_cards = deck.shuffle_cards()

game = Game()

#-----enqueueing 5 cards to the banker's queue (hold)-----#
for card in banker_cards:
    game.banker.enqueue(card)

print("Please deposit first before playing the game.")
amount = float(input("\nAmount: "))
balance = game.player.cash_in(amount)
print(f"Your balance: {balance}")
print("\nPlayer's card:", player_card)

#-----actual game-----#
round_number = 1
while game.banker.has_cards():
    print(f"\n--- Round {round_number} ---")
    print(f"Your current balance: ${game.player.check_balance()}")

    #-----betting system-----#
    while True:
        try:
            print("\n(Mininmum bet is 10.)")
            bet = float(input("Place your bet for this round: "))
            if game.place_bet(bet):
                break
        except ValueError:
            print("\nPlease enter a valid number.")

    drawn_card = game.banker.draw()
    print(f"\nBanker draws {drawn_card}")
    print(f"Player has {player_card}")
    
    player_value = player_card[2]
    banker_value = drawn_card[2]
    
    if player_value > banker_value:
        print("\nPlayer wins this round!")
        game.player_won()
    elif player_value < banker_value:
        print("\nBanker wins this round!")
        game.player_lost()
    else:
        print("\nIt's a tie this round!")
        game.player.cash += game.bet # returning player's bet
        game.bet = 0 
        print(f"Bet returned. Balance: {game.player.cash}")

    if game.banker.has_cards():
        while True:
            continue_choice = input("\nWould you like to keep playing? (y/n): ").lower()
            if continue_choice == "y":
                print("\nContinuing...")
                break
            elif continue_choice == "n":
                break
            else:
                print("Enter y or n only.")
        
        if continue_choice == "n":
            break

    #-----when the player has no money-----#
    if game.player.cash == 0:
        print("Oh no... you don't have enough balance. Cash in to play.")
        while True:
            continue_choice = input("\nWould you like to deposit to keep playing? (y/n): ").lower()
            if continue_choice == "y":
                amount = float(input("\nAmount: "))
                balance = game.player.cash_in(amount)
                print(f"Your balance: {balance}")
                break
            elif continue_choice == "n":
                break
            else:
                print("Enter y or n only.")
        
        if continue_choice == "n":
            break
    
    round_number += 1

print("\nGame over!")
print(f"Final balance: ${game.player.check_balance()}")

#-----cashout-----#
while game.player.cash != 0:
    cashout_choice = input("Would you like to withdraw your winnings? (y/n): ").lower()
    
    if cashout_choice == "y":
        while True:
            try:
                cashout_amount = float(input(f"How much do you want to withdraw? (Balance: ${game.player.cash}): "))
                
                if cashout_amount <= 0:
                    print("Withdrawal amount must be positive.")
                elif cashout_amount > game.player.cash:
                    print(f"Insufficient funds. You have ${game.player.cash}.")
                else:
                    withdrawn = game.player.cash_out(cashout_amount)
                    print("Error. Cannot withdraw cash...")
                    print("Just kidding.")
                    print(f"You withdrew: ${withdrawn}")
                    print(f"Remaining balance: ${game.player.cash}")
                    break
                    
            except ValueError:
                print("Please enter a valid number.")
        break
    
    elif cashout_choice == "n":
        print("Saving cash.")
        break
    
    else:
        print("Please enter y or n.")

print("\nThank you for playing.")