import random
import os
import time

def clear_cmd():
    os.system('cls')

def check_if_end(game_field):
    for i in range(1,3):
        if(((game_field[0] == i) and (game_field[1] == i) and (game_field[2] == i)) or ((game_field[3] == i) and (game_field[4] == i) and (game_field[5] == i)) or ((game_field[6] == i) and (game_field[7] == i) and (game_field[8] == i))):
            return True, i
        elif(((game_field[0] == i) and (game_field[3] == i) and (game_field[6] == i)) or ((game_field[1] == i) and (game_field[4] == i) and (game_field[7] == i)) or ((game_field[2] == i) and (game_field[5] == i) and (game_field[8] == i))):
            return True, i
        elif(((game_field[0] == i) and (game_field[4] == i) and (game_field[8] == i)) or ((game_field[2] == i) and (game_field[4] == i) and (game_field[6] == i))):
            return True, i
    return False, i

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

def AI_set_mark(mark_to_set, game_field, empty_index_list, moves_history, need_to_explore):
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
    game_field[put_mark_index] = mark_to_set
    empty_index_list.remove(put_mark_index)
    moves_history[cur_key_state] = put_mark_index
    return game_field, empty_index_list, moves_history

def player_set_mark(mark_to_set, game_field, empty_index_list, moves_history):
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
    game_field[put_mark_index] = mark_to_set
    empty_index_list.remove(put_mark_index)
    moves_history[cur_key_state] = put_mark_index
    return game_field, empty_index_list, moves_history

def get_more_experience(moves_history, give_reward):
    cur_value_state = AI_exp[list(moves_history.keys())[-1]]
    cur_value_state[list(moves_history.values())[-1]] = give_reward
    moves_amount = len(moves_history.keys())
    for i in range(1, moves_amount + 1):
        cur_value_state = AI_exp[list(moves_history.keys())[moves_amount - i]]
        V_s = cur_value_state[list(moves_history.values())[moves_amount - i]]
        V_s = V_s + alpha * (give_reward - V_s)
        give_reward = V_s
        cur_value_state[list(moves_history.values())[moves_amount - i]] = V_s
        AI_exp[list(moves_history.keys())[moves_amount - i]] = cur_value_state

def train_AI(need_to_train):
    print("\n[*] Starting hard AI training...")
    start_time = time.time()
    for temp_game in range(need_to_train):
        game_field = [0]*9
        empty_index_list = list(range(0, 9))
        moves_history_P1 = {}
        moves_history_P2 = {}
        while(True):
            game_field, empty_index_list, moves_history_P1 = AI_set_mark(1, game_field, empty_index_list, moves_history_P1, True)
            if(check_if_end(game_field)[0] or game_field.count(0) == 0):
                break
            game_field, empty_index_list, moves_history_P2 = AI_set_mark(2, game_field, empty_index_list, moves_history_P2, True)
            if(check_if_end(game_field)[0] or game_field.count(0) == 0):
                break
        end_game, win_numb = check_if_end(game_field)
        #Give rewards for P1
        if(end_game):
            if(win_numb==1):
                give_reward = 1.0
            else:
                give_reward = 0.0
        else:
            give_reward = 0.5
        get_more_experience(moves_history_P1, give_reward)
        # Give rewards for P2
        if(end_game):
            if(win_numb==2):
                give_reward = 1.0
            else:
                give_reward = 0.0
        else:
            give_reward = 0.5
        get_more_experience(moves_history_P2, give_reward)
    print(f"[+] The hard training is over! It took: {time.time() - start_time} sec")
    input("[*] Press Enter to continue...")

def play_with_AI(start_first):
    global total_played_games
    game_field = [0] * 9
    empty_index_list = list(range(0, 9))
    moves_history_Player = {}
    moves_history_AI = {}
    while(True):
        if(start_first==1):
            game_field, empty_index_list, moves_history_Player = player_set_mark(1, game_field, empty_index_list, moves_history_Player)
            if (check_if_end(game_field)[0] or game_field.count(0) == 0):
                break
            game_field, empty_index_list, moves_history_AI = AI_set_mark(2, game_field, empty_index_list, moves_history_AI, False)
            if (check_if_end(game_field)[0] or game_field.count(0) == 0):
                break
        else:
            game_field, empty_index_list, moves_history_AI = AI_set_mark(1, game_field, empty_index_list, moves_history_AI, False)
            if (check_if_end(game_field)[0] or game_field.count(0) == 0):
                break
            game_field, empty_index_list, moves_history_Player = player_set_mark(2, game_field, empty_index_list, moves_history_Player)
            if (check_if_end(game_field)[0] or game_field.count(0) == 0):
                break
    end_game, win_numb = check_if_end(game_field)
    # Give rewards for AI
    if (end_game):
        if ((win_numb == 1 and start_first == 2) or (win_numb == 2 and start_first == 1)):
            give_reward = 1.0
        else:
            give_reward = 0.0
    else:
        give_reward = 0.5
    get_more_experience(moves_history_AI, give_reward)
    # Give rewards for Player
    if (end_game):
        if ((win_numb == 1 and start_first == 1) or (win_numb == 2 and start_first == 2)):
            give_reward = 1.0
        else:
            give_reward = 0.0
    else:
        give_reward = 0.5
    get_more_experience(moves_history_Player, give_reward)
    print_board(game_field)
    if (end_game):
        if ((win_numb == 1 and start_first == 2) or (win_numb == 2 and start_first == 1)):
            print("[+] AI won!\nEasy peasy for such Strong AI!")
            input("[*] Press Enter to continue...")
        else:
            print("[+] Player won!\nAI need to train harder!")
            input("[*] Press Enter to continue...")
    else:
        print("[+] Draw!\nAIt looks like a draw. I wonder if this game can be won?")
        input("[*] Press Enter to continue...")
    total_played_games += 1

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
        print(f'\n[*] Available options:\n1) Train AI\n2) Play with AI\n3) Change settings\n4) Show AI experience\n5) Reset AI experience\n6) Exit')
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
            start_first=int(input("\n[?] I want to start: "))
            play_with_AI(start_first)
        elif(chosen_option=="3"):
            clear_cmd()
            print(f"[?] What you want to change?\n1) Alpha (Learning rate): {alpha}\n2) Epsilon (Random chance): {epsilon}")
            option_to_change = int(input("\n[?] Choose desire option: "))
            if(option_to_change==1):
                alpha = float(input("[?] Choose desire Alpha (Learning rate) amount (from 0.0 to 1.0, default - 0.3): "))
            elif(option_to_change==2):
                epsilon = float(input("[?] Choose desire Epsilon (Random chance) amount (from 0.0 to 1.0, default - 0.3): "))
            print("[+] Successful parameter change!")
            input("[*] Press Enter to continue...")
        elif(chosen_option=="4"):
            clear_cmd()
            print("[*] Okay, lets start!")
            for i in range(len(AI_exp.keys())):
                print("-------------------------------------------------")
                current_state = list(AI_exp.keys())[i]
                print(f"\n[{i} state] {current_state}")
                print_board(str_to_int_list(current_state))
                print_values_like_board(AI_exp[current_state])
                print("-------------------------------------------------")
            if(len(AI_exp.keys()) == 0):
                print("[*] Hm... It looks like AI doesn't know how to play Tic-Tac-Toe! Necessary to teach him this.")
                input("[*] Press Enter to continue...")
            else:
                print("\n[+] Oooh... That was hard enough.")
                input("[*] Press Enter to continue...")
        elif(chosen_option=="5"):
            clear_cmd()
            reset_exp()
            print("[+] Well, the AI has lost all its experience. So sad...")
            input("[*] Press Enter to continue...")
        elif(chosen_option=="6"):
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