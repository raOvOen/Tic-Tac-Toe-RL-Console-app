import random
import os
import time
from contextlib import redirect_stdout
import matplotlib.pyplot as plt

def clear_cmd():
    os.system('cls')

def check_if_end(game_field):
    for winner_number in range(1,3):
        if(((game_field[0] == winner_number) and (game_field[1] == winner_number) and (game_field[2] == winner_number)) or ((game_field[3] == winner_number) and (game_field[4] == winner_number) and (game_field[5] == winner_number)) or ((game_field[6] == winner_number) and (game_field[7] == winner_number) and (game_field[8] == winner_number))):
            return True, winner_number
        elif(((game_field[0] == winner_number) and (game_field[3] == winner_number) and (game_field[6] == winner_number)) or ((game_field[1] == winner_number) and (game_field[4] == winner_number) and (game_field[7] == winner_number)) or ((game_field[2] == winner_number) and (game_field[5] == winner_number) and (game_field[8] == winner_number))):
            return True, winner_number
        elif(((game_field[0] == winner_number) and (game_field[4] == winner_number) and (game_field[8] == winner_number)) or ((game_field[2] == winner_number) and (game_field[4] == winner_number) and (game_field[6] == winner_number))):
            return True, winner_number
    if (game_field.count(0) == 0):
        return True, 0
    return False, winner_number

def int_list_to_str(game_field):
    ret_str = ""
    for i in game_field:
        ret_str += str(i)
    return ret_str

def str_to_int_list(state_string):
    return [int(x) for x in list(state_string)]

def print_values_like_board(values_list):
    print("\n")
    for i in range(3):
        print(" -----------------------------")
        for j in range(3):
            print("  ", end="")
            to_print = values_list[i*3+j]
            if(to_print==-1.0):
                to_print="{0:0.1f}".format(values_list[i*3+j])
            else:
                to_print="{0:0.2f}".format(values_list[i * 3 + j])
            if j == 0:
                print(f"|  {to_print}  ", end="|")
            else:
                print(f"{to_print}  ", end="|")
        print("")
    print(" -----------------------------")
    print("\n")

def print_board(game_field):
    print("\n")
    for i in range(3):
        print(" ---------------------")
        for j in range(3):
            print("  ", end="")
            if game_field[i*3+j] == 1:
                if j == 0:
                    print(f"|  x  ", end="|")
                else:
                    print(f"x  ", end="|")
            elif game_field[i*3+j] == 2:
                if j == 0:
                    print(f"|  o  ", end="|")
                else:
                    print(f"o  ", end="|")
            else:
                if j == 0:
                    print(f"|     ", end="|")
                else:
                    print(f"   ", end="|")
        print("")
    print(" ---------------------")
    print("\n")

def AI_set_mark(game_field, empty_index_list, need_to_explore):
    cur_key_state = int_list_to_str(game_field)
    if (cur_key_state not in AI_exp.keys()):
        cur_key_values = [-1.0] * 9
        for i in empty_index_list:
            cur_key_values[i] = 0.5
        AI_exp[cur_key_state] = cur_key_values
    cur_value_state = AI_exp[cur_key_state]
    if (cur_value_state.count(max(cur_value_state)) > 1):
        max_list_indexes = [n for n, x in enumerate(cur_value_state) if x == max(cur_value_state)]
        put_mark_index = random.choice(max_list_indexes)
    else:
        if ((random.uniform(0.0, 1.0) < epsilon) and need_to_explore):
            put_mark_index = random.choice(empty_index_list)
        else:
            put_mark_index = cur_value_state.index(max(cur_value_state))
    return cur_key_state, put_mark_index

def player_set_mark(game_field, empty_index_list):
    cur_key_state = int_list_to_str(game_field)
    if (cur_key_state not in AI_exp.keys()):
        cur_key_values = [-1.0] * 9
        for i in empty_index_list:
            cur_key_values[i] = 0.5
        AI_exp[cur_key_state] = cur_key_values
    while (True):
        print_board(game_field)
        put_mark_index = int(input("[?] Choose desire position: "))
        if (put_mark_index not in empty_index_list):
            print("\n[!]Incorrect input!\n[*] Choose another cell number...")
            input("[*] Press Enter to continue...")
        else:
            break
        clear_cmd()
    return cur_key_state, put_mark_index

def Simple_TicTacToe_algorithm(game_field, empty_index_list, mark_to_set):
    cur_key_state = int_list_to_str(game_field)
    if (cur_key_state not in AI_exp.keys()):
        cur_key_values = [-1.0] * 9
        for i in empty_index_list:
            cur_key_values[i] = 0.5
        AI_exp[cur_key_state] = cur_key_values
    for cur_index in empty_index_list:
        possible_game_field = game_field.copy()
        possible_game_field[cur_index] = mark_to_set
        if(check_if_end(possible_game_field)[0] == True):
            return cur_key_state, cur_index
    put_mark_index = random.choice(empty_index_list)
    return cur_key_state, put_mark_index

def play_game(play_game_type, start_first):
    game_field = [0] * 9
    empty_index_list = list(range(0, 9))
    mark_move = 0
    prev_put_mark_index_P2 = None
    prev_key_state_P2 = None
    prev_put_mark_index_P1 = None
    prev_key_state_P1 = None
    while (True):
        end_game, win_numb = check_if_end(game_field)
        if (end_game):
            if (win_numb == 0):
                give_reward = 0.5
                get_move_experience(prev_key_state_P2, prev_put_mark_index_P2, give_reward)
                break
            get_move_experience(prev_key_state_P2, prev_put_mark_index_P2, 0.0)
            AI_exp[prev_key_state_P1][prev_put_mark_index_P1] = 1.0
            break
        mark_move = (mark_move % 2) + 1
        if(play_game_type==1):
            cur_key_state, cur_put_mark_index = AI_set_mark(game_field, empty_index_list, True)
        elif(play_game_type==2):
            cur_key_state, cur_put_mark_index = player_set_mark(game_field, empty_index_list) if mark_move == start_first else AI_set_mark(game_field, empty_index_list, False)
        elif(play_game_type==11):
            cur_key_state, cur_put_mark_index = AI_set_mark(game_field, empty_index_list, True) if mark_move == start_first else Simple_TicTacToe_algorithm(game_field, empty_index_list, mark_move)
        else:
            cur_key_state, cur_put_mark_index = AI_set_mark(game_field, empty_index_list, True)
        if (prev_put_mark_index_P2 != None):
            cur_value_state = AI_exp[int_list_to_str(game_field)]
            get_move_experience(prev_key_state_P2, prev_put_mark_index_P2, cur_value_state[cur_put_mark_index])
        prev_put_mark_index_P2 = prev_put_mark_index_P1
        prev_key_state_P2 = prev_key_state_P1
        prev_put_mark_index_P1 = cur_put_mark_index
        prev_key_state_P1 = cur_key_state
        game_field[cur_put_mark_index] = mark_move
        empty_index_list.remove(cur_put_mark_index)
    return game_field, win_numb
def get_move_experience(prev_key_state, prev_put_mark_index,reward):
    prev_value_state = AI_exp[prev_key_state]
    V_s = prev_value_state[prev_put_mark_index]
    V_s = V_s + alpha * (reward - V_s)
    prev_value_state[prev_put_mark_index] = V_s
    AI_exp[prev_key_state] = prev_value_state

def train_AI(need_to_train):
    print("\n[*] Starting hard AI training...")
    start_time = time.time()
    for temp_game in range(need_to_train):
        play_game(1, None)
    print(f"[+] The hard training is over! It took: {time.time() - start_time} sec")
    input("[*] Press Enter to continue...")

def play_with_AI(start_first):
    game_field, win_numb = play_game(2, start_first)
    print_board(game_field)
    if ((win_numb == 1 and start_first == 2) or (win_numb == 2 and start_first == 1)):
        print("[+] AI won!\nEasy peasy for such Strong AI!")
    elif(win_numb == 0):
        print("[+] Draw!\nAIt looks like a draw. I wonder if this game can be won?")
    else:
        print("[+] Player won!\nAI need to train harder!")
    input("[*] Press Enter to continue...")

def draw_AI_progression(need_to_play, need_to_get_win_rate, start_first, opponent):
    reset_exp()
    x_cur_game_amount = []
    y_cur_win_rate = []
    print("\n[*] Starting hard AI training and drawing...")
    start_time = time.time()
    AI_won = 0
    for temp_game in range(need_to_play):
        game_field, win_numb = play_game(10 + opponent, start_first)
        if ((win_numb == 1 and start_first == 1) or (win_numb == 2 and start_first == 2)):
            AI_won += 1
        if((temp_game%need_to_get_win_rate == 0) and (temp_game != 0)):
            print(f"[*] AI won for {AI_won}/{temp_game} times! Current win rate is {(AI_won/temp_game) * 100}%")
            x_cur_game_amount.append(temp_game)
            y_cur_win_rate.append((AI_won/temp_game) * 100)
    print(f"[+] The hard training is over! It took: {time.time() - start_time} sec")
    print(f"[*] AI won for {AI_won}/{need_to_play} times!")
    plt.plot(x_cur_game_amount, y_cur_win_rate)
    plt.xlabel('Number of game parties')
    plt.ylabel('Win rate')
    plt.show()
    input("[*] Press Enter to continue...")

def reset_exp():
    global total_played_games
    global AI_exp
    total_played_games = 0
    AI_exp = {}

def menu():
    global total_played_games
    global alpha
    global epsilon
    global AI_exp
    while(True):
        clear_cmd()
        print('[OvO] Tic Tac Toe Reinforcement Learning by raOvOen')
        print(f'\n[*] You current settings\n - Alpha (Learning rate): {alpha}\n - Epsilon (Random chance): {epsilon}\n - Total played games: {total_played_games}')
        print(f'\n[*] Available options:\n1) Train AI\n2) Play with AI\n3) Draw AI progression graph (will reset AI experience)\n4) Change settings\n5) Print to txt AI experience\n6) Reset AI experience\n7) Exit')
        chosen_option = input("\n[?] Choose desire option: ")
        if(chosen_option=="1"):
            clear_cmd()
            print("[?] How many games AI need to play?")
            games_amount=int(input("\n[?] Choose desire amount: "))
            train_AI(games_amount)
            total_played_games += games_amount
        elif(chosen_option=="2"):
            clear_cmd()
            print("[?] Choose the move you will start with (1 or 2):")
            start_position=int(input("\n[?] I want to start: "))
            play_with_AI(start_position)
            total_played_games += 1
        elif(chosen_option=="3"):
            clear_cmd()
            print("[?] How many game AI need to play?:")
            games_amount=int(input("\n[?] Choose desire amount: "))
            print("[?] How often is it necessary to fix the win rate")
            win_rate_freq_amount = int(input("\n[?] Choose game amount to get win rate: "))
            print(f"[?] Who will be the AI's opponent?\n1) Simple Tic Tac Toe algorithm\n2) AI himself")
            opponent = int(input("\n[?] Choose desire opponent number: "))
            print("[?] Choose the move AI will start with (1 or 2):")
            start_position = int(input("\n[?] AI will start: "))
            draw_AI_progression(games_amount, win_rate_freq_amount, start_position,opponent)
            total_played_games += games_amount
        elif(chosen_option=="4"):
            clear_cmd()
            print(f"[?] What you want to change?\n1) Alpha (Learning rate): {alpha}\n2) Epsilon (Random chance): {epsilon}")
            option_to_change = int(input("\n[?] Choose desire option: "))
            if(option_to_change==1):
                alpha = float(input("[?] Choose desire Alpha (Learning rate) amount (from 0.0 to 1.0, default - 0.3): "))
            elif(option_to_change==2):
                epsilon = float(input("[?] Choose desire Epsilon (Random chance) amount (from 0.0 to 1.0, default - 0.3): "))
            print("[+] Successful parameter change!")
            input("[*] Press Enter to continue...")
        elif(chosen_option=="5"):
            clear_cmd()
            if(len(AI_exp.keys()) == 0):
                open('AI_experience.txt', 'w').close()
                print("[*] Hm... It looks like AI doesn't know how to play Tic-Tac-Toe! Necessary to teach him this.")
                input("[*] Press Enter to continue...")
                continue
            print("[*] Saving AI progress to 'AI_experience.txt'...")
            with open('AI_experience.txt', 'w') as f:
                with redirect_stdout(f):
                    for i in range(len(AI_exp.keys())):
                        print("-------------------------------------------------")
                        current_state = list(AI_exp.keys())[i]
                        print(f"\n[{i} state] {current_state}")
                        print_board(str_to_int_list(current_state))
                        print_values_like_board(AI_exp[current_state])
                        print("-------------------------------------------------")
                print("[+] Oooh... That was hard enough.")
                input("[*] Press Enter to continue...")
        elif(chosen_option=="6"):
            clear_cmd()
            reset_exp()
            print("[+] Well, the AI has lost all its experience. So sad...")
            input("[*] Press Enter to continue...")
        elif(chosen_option=="7"):
            break
        else:
            clear_cmd()
            print("[!] Incorrect input. Enter the number of the desired option!")
            input("[*] Press Enter to continue...")

if __name__ == '__main__':
    alpha = 0.3
    epsilon = 0.3
    total_played_games = 0
    AI_exp = {}
    menu()