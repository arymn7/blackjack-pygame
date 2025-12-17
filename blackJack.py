# Black Jack game in Python with pygame and standard libraries
# Aryaman Sharma

# Import required libraries
import copy
import random
import pygame

# initialize all pygame modules
pygame.init()

# Game Variables
# Create multiple decks to prevent 'Card Counting' strategy
cards = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
one_deck = cards * 4
decks = 4
# Playing or not Playing
active = False
# Win / Loss / Push
records = [0,0,0]
player_score = 0
dealer_score = 0
initial_deal = False
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = False
hand_active = False
outcome = 0
add_score = False
results = ['','PLAYER BUSTED :(','PLAYER WINS! :)','DEALER WINS :(','TIE GAME']

# Create GUI using pygame and set up GUI variables
WIDTH = 600
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('BLACKJACK!')
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('holidaysHomework.ttf', 35)

# Draw game cond's and buttons
def draw_game(act,record, result):
    button_list = []
    # Initially on startup (not active) we can only deal new hand
    if not act:
        deal = pygame.draw.rect(screen,(82, 0, 18),[150,20,300,100],0,5,)
        pygame.draw.rect(screen,(143, 1, 1),[150,20,300,100],5,5,)
        deal_text = font.render('DEAL HAND',True,'white')
        screen.blit(deal_text,(170,50))
        button_list.append(deal)
    # Once game started, show hit and stand buttons and win/loss record
    else:
        # Hit button
        hit = pygame.draw.rect(screen,(82, 0, 18),[0,700,300,100],0,5,)
        deal = pygame.draw.rect(screen,(143, 1, 1),[0,700,300,100],5,5,)
        hit_text = font.render('HIT',True,'white')
        screen.blit(hit_text,(120,730))
        button_list.append(hit)
        # Stand button
        stand = pygame.draw.rect(screen,(82, 0, 18),[300,700,300,100],0,5,)
        deal = pygame.draw.rect(screen,(143, 1, 1),[300,700,300,100],5,5,)
        stand_text = font.render('STAND',True,'white')
        screen.blit(stand_text,(380,730))
        button_list.append(stand)
        # Score text
        score_text = font.render(f'Wins: {record[0]}  Losses: {record[1]}  Draw: {record[-1]}', True, 'white')
        screen.blit(score_text, (8, 830))
    # If there is an outcome for the hand that was played, then display a restart button and tell player what happend
    if result != 0:
        screen.blit(font.render(results[result], True, 'white'),(15,25))
        deal = pygame.draw.rect(screen,(82, 0, 18),[150,220,300,100],0,5,)
        pygame.draw.rect(screen,(143, 1, 1),[150,220,300,100],5,5,)
        pygame.draw.rect(screen,(143, 1, 1),[153,223,294,94],5,5,)
        deal_text = font.render('NEW HAND',True,'white')
        screen.blit(deal_text,(170,250))
        button_list.append(deal)
    return button_list

# Deal cards by selecting randomly from deck, make function for one card at a time
def deal_cards(current_hand,current_deck):
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card-1])
    current_deck.pop(card-1)
    return current_hand, current_deck

# draw scores for player and dealer on the screen
def draw_scores(player,dealer):
    screen.blit(font.render(f'Score[{player}]', True, 'white'), (350,400))
    if reveal_dealer:
        screen.blit(font.render(f'Score[{dealer}]', True, 'white'), (350,100))

# Draw cards onto screen
def draw_cards(player,dealer,reveal):
    for i in range(len(player)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 460 + (5 * i), 120, 220], 0, 5)
        screen.blit(font.render(player[i], True, 'black'), (75 + 70*i, 465 + 5*i))
        screen.blit(font.render(player[i], True, 'black'), (75 + 70*i, 635 + 5*i))
        pygame.draw.rect(screen, 'red', [70 + (70 * i), 460 + (5 * i), 120, 220], 5, 5)
    # If player hasn't finished turn, dealer will hide one card
    for i in range(len(dealer)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 160 + (5 * i), 120, 220], 0, 5)
        if i != 0 or reveal:
            screen.blit(font.render(dealer[i], True, 'black'), (75 + 70*i, 165 + 5*i))
            screen.blit(font.render(dealer[i], True, 'black'), (75 + 70*i, 335 + 5*i))
        else:
            screen.blit(font.render('???', True, 'black'), (75 + 70*i, 165 + 5*i))
            screen.blit(font.render('???', True, 'black'), (75 + 70*i, 335 + 5*i))
        pygame.draw.rect(screen, 'blue', [70 + (70 * i), 160 + (5 * i), 120, 220], 5, 5)

# Pass in dealer or player hand and get best score possible (closest to 21)
def calculate_score(hand):
    # Calculate hand score every time and check how many aces we have
    hand_score = 0
    aces_count = hand.count('A')
    for i in range(len(hand)):
        # For values 2 - 8
        for j in range(8):
            if hand[i] == cards[j]:
                hand_score += int(hand[i])
        # for 10 and face cards, add 10
        if hand[i] in ['10','J','Q','K']:
            hand_score += 10
        # For aces add 11 and reduce later
        elif hand[i] == 'A':
            hand_score += 11
    # Determine how many aces need to be converted to a value of 1 to stay under 21 if possible
    if hand_score > 21 and aces_count > 0:
        for i in range(aces_count):
            if hand_score > 21:
                hand_score -= 10
    return hand_score

# Check conditions for endgame
def check_endgame(hand_act,deal_score,play_score,result,totals,add):
    # Check game scenarios if stood busted or blackjack
    # Result; 1 (player bust); 2 (Win); 3(Loss); 4(Push/Draw)
    if not hand_act and deal_score >= 17:
        if play_score > 21:
            result = 1
        elif deal_score < play_score <= 21 or deal_score > 21:
            result = 2
        elif play_score < deal_score <= 21:
            result = 3
        else:
            result = 4
        if add:
            if result == 1 or result == 3:
                totals[1] += 1
            elif result == 2:
                totals[0] += 1
            else:
                totals[2] += 1
            add = False
    return result, totals, add

# Main game loop
run = True
while run:
    # Run game at desired framrate and fill in bg colour
    timer.tick(fps)
    screen.fill((66, 140, 63))
    # Initial deal to player and dealer
    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        initial_deal = False
    # Once game is active, calculate all scores and display cards
    if active:
        player_score = calculate_score(my_hand)
        draw_cards(my_hand, dealer_hand, reveal_dealer)
        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        draw_scores(player_score,dealer_score)
    buttons = draw_game(active, records, outcome)
    # Event handling, if quit pressed, exit the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if not active:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    game_deck = copy.deepcopy(decks * one_deck)
                    my_hand = []
                    dealer_hand = []
                    outcome = 0
                    hand_active = True
                    reveal_dealer = False
                    outcome = 0
                    add_score = True
            else:
                # If player can hit, allow them
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                    my_hand, game_deck = deal_cards(my_hand,game_deck)
                # If player wants to stand, allow them
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False
                elif len(buttons) == 3:
                    if buttons[2].collidepoint(event.pos):
                        active = True
                        initial_deal = True
                        game_deck = copy.deepcopy(decks * one_deck)
                        my_hand = []
                        dealer_hand = []
                        outcome = 0
                        hand_active = True
                        reveal_dealer = False
                        outcome = 0
                        add_score = True
                        dealer_score = 0
                        player_score = 0
    # If player busts, automatically end turn; treat like a stand
    if hand_active and player_score >= 21:
        hand_active = False
        reveal_dealer = True
    outcome,records,add_score = check_endgame(hand_active,dealer_score,player_score,outcome,records,add_score)
    pygame.display.flip()
pygame.quit()