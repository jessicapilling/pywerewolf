#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 22:41:30 2022

@author: jp735
"""
possible_roles = ['villager', 'village idiot', 'werewolf', 
                  'bodyguard', 'seer', 'prostitute', 
                  'witch', 'necromancer']

# Making the classes ---------------------------------------------------

class Villager:
    """
    The parent class for all player types. Also acts as the village idiot.
    
    :param: str player_name: The name of the player, only the first name please.
    :param: str character: The character they are playing, eg. werewolf, bodyguard etc.
    :param: bool alive: Set to True if character is alive.
    :param: bool visited: Set to True if the character has been visited by the prositute.
    :param: bool guarded: Set to True f the character has been guarded by the bodyguard.
    """
    def __init__(self, player_name: str, character: str, alive: bool, visited: bool, guarded: bool) -> None:
        self.player_name = player_name
        self.character_type = character
        self.life_status = alive
        self.visited_status = visited
        self.guarded_status = guarded

class Werewolf(Villager):
    """Werewolf subclass."""
    
    def __init__(self, player_name: str, character: str, alive: bool, visited: bool, guarded: bool) -> None:
        
        # Call the init from Villager
        super().__init__(player_name, character, alive, visited, guarded)
        
    def murder(self,chosen_player: str) -> None:
        '''
        Controlling the murder of a non werewolf by a werewolf.

        :param: str chosen_player: the name of the player the werewolf intends to murder.
        '''
        # Player dict is a dictionary of the player name and their instance
        if not player_dict[chosen_player].guarded_status and not self.visited_status: # Only proceeding if they are not guarded
            player_dict[chosen_player].life_status = False 
            print(f'{chosen_player} has been killed')
            if player_dict[chosen_player].visited_status: # If the prostitute is at the chosen players house, they also die
                prostitute_player = role_finder('prostitute') # Finding name of the player with the prostitute role
                player_dict[prostitute_player].life_status = False
                print(f'{prostitute_player} has been killed')

class Bodyguard(Villager):
    """Bodyguard subclass."""
    
    def __init__(self, player_name: str, character: str, alive: bool, visited: bool, guarded: bool) -> None:
        
        # Call the init from Villager
        super().__init__(player_name, character, alive, visited, guarded)
    
    def guard(self,chosen_player) -> None:
        '''
        Controlling guarding of a player by the bodyguard.

        :param str chosen_player: the name of the player the bodyguard intends to guard.
        '''
        if not self.visited_status : # Only doing the function if they havent been visited
            # Player dict is a dictionary of the player name and their instance
            player_dict[chosen_player].guarded_status = True
            print(f'{chosen_player} has been guarded')

class Seer(Villager):
    """Seer subclass."""
    def __init__(self, player_name: str, character: str, alive: bool, visited: bool, guarded: bool) -> None:
        
        # Call the init from Villager
        super().__init__(player_name, character, alive, visited, guarded)
    
    def crystal_ball(self,chosen_player: str) -> None:
        '''
        Revealing to the seer if the person they are investigating is a werewolf.

        :param str chosen_player: the name of the player the seer intends to investigate.
        '''
        if not self.visited_status : # Only doing the function if they havent been visited
            # Player dict is a dictionary of the player name and their instance
            if player_dict[chosen_player].character == 'werewolf':
                print(f' Tell the seer that {chosen_player} is a werewolf')
            else:
                print(f' Tell the seer that {chosen_player} is not werewolf')

class Prostitute(Villager):
      """Prostitute subclass."""
      def __init__(self, player_name: str, character: str, alive: bool, visited: bool, guarded: bool) -> None:
          
        # Call the init from Villager
        super().__init__(player_name, character, alive, visited, guarded)
    
      def visit(self,chosen_player: str) -> None:
        '''
        Controlling the prostitute visiting someone.

        :param str chosen_player: the name of the player the prostitute intends to visit.
        '''
        # Player dict is a dictionary of the player name and their instance
        player_dict[chosen_player].visited_status = True
        print(f'{chosen_player} has been visited by the prostitute')

class Witch(Villager):
    """Witch subclass."""
    def __init__(self, player_name: str, character: str, 
                 alive: bool, visited: bool, guarded: bool, apothecary: tuple(bool, bool)) -> None:
        
      # Call the init from Villager
      super().__init__(player_name, character, alive, visited, guarded)
      self.apothecary = (True, True)
    

# Defining all the necessary functions -----------------------------------------------------------

def clean_input(input_str: str) -> str:
    """ 
    A wrapper function to safely take inputs from the user without erroring 
    and ending the game.
    
    :param str input_str: input string obviously
    :return: cleaned string in correct format so it doesn't break the code later'
    :rtype: str
    """
    
    # Get the response from the user
    output_str = input(input_str).lower().strip()
    
    # Check it is a valid input
    if output_str in player_dict or output_str == "skip":  # is it a player name
        return output_str
    elif output_str in possible_roles:  # is it a valid role
        return output_str
    else:
        print("Invalid input!")
        return clean_input(input_str)

def alive_people_checker() -> None:
    '''
    Checking which people are still alive and adding them to a dictionary.

    :return: dictionary where keys are the people who are still alive, and values are their character types
    :rtype: dict
    '''
  
    alive_player_dict = {} # Creating the empty dictionary
    
    for player in players: # Looping over all players, where players is defined later by the user input
        if player_dict[player].life_status == True:   # Collecting the players who are still alive
            # Adding them and their roles to the dictionary
            alive_player_dict[player_dict[player].player_name] = player_dict[player].character_type 
    return alive_player_dict

    
def werewolf_information(alive_player_dict: dict) -> tuple(int, int, list):
    '''
    Checking which people are still alive and adding them to a dictionary.
    
    :param dict alive_player_dict: dictionary with alive players as keys and roles as values
    :return werewolf_counter: number of werewolves left alive in the game
    :rtype: int
    :return: number of werewolves left alive in the game, number of non werewolves left alive in the game,
        name of one of/ the werewolf
    :rtype: tuple(int, int, list )
    '''
    werewolf_counter = 0
    non_wolf_counter = 0
    name_of_werewolf = []
    
    for key in alive_player_dict.keys(): # Going through each player who is still alive
        if alive_player_dict[key] == 'werewolf':
            werewolf_counter += 1 # Adding one to werewolf_counter if they are a werewolf
            name_of_werewolf.append(key) # Saving name of the werewolf
        else:
            non_wolf_counter += 1

    return werewolf_counter, non_wolf_counter, name_of_werewolf


def game_status_checker() -> bool:
    '''
    Return True if the game is over
    
    :return: whether the game is over 
    :rtype: bool
    '''
    alive_player_dict = alive_people_checker() # Keys are the player names, values are their character types
    werewolf_counter, non_wolf_counter, name_of_werewolf = werewolf_information(alive_player_dict) 

    if werewolf_counter == non_wolf_counter: # Checking if the werewolves have won
        print('Game Over, the village has been lost to the wolves.')
        return True
    elif werewolf_counter == 0: # Checking if non wolves have won
         print('Game Over, the werewolves have lost')
         return True
    else:
        return False

def role_finder(role: str) -> str:
    '''
    Finding a players name from their role/character 
    
    :param str role: name of the role/character you want to find the player name for
    :return person[0]: the name of the person with that role
    :rtype: str
    '''
    # Cycles through all the values in player dict (which are the instances)
    # If the role matches the role we are looking for, it appends the corresponding key of the player dict
    person = [k for k, item in player_dict.items() if item.character_type == role]
    return person[0]

def reset_values() -> None:
    '''
    Reseting the guarded and visited status for all players so that another round can begin.
    '''
    for player in player_dict:
        player_dict[player].guarded_status = False
        player_dict[player].visited_status = False
        
def Night() -> None:
    '''
    Controlling all the happenings that occur in the night.
    '''
    print('We enter the night')
    print('Everyone close their eyes')
    
    if 'prostitute' in roles_in_game: # Seeing if there is a prostitute in the game
        print('Prostitute, wake up')
        visited_player = clean_input('Who is the prostitute visiting: ')
        prostitute_player = role_finder('prostitute')  # Name of the player who is a prostitute
        player_dict[prostitute_player].visit(visited_player) # Changing the visited player's status to True
        print('Prostitute, go back to sleep')
    
    if 'bodyguard' in roles_in_game: # Seeing if there is a bodyguard in the game
        # The bodyguard protocol
        print('Bodyguard, wake up')
        guarded_player = clean_input('Who is the bodyguard guarding: ')
        body_guard_player = role_finder('bodyguard')  # Name of the player who is a bodyguard
        player_dict[body_guard_player].guard(guarded_player) # Changing the guarded player's status to True
        print('Bodyguard, go back to sleep')

    if 'seer' in roles_in_game: # Seeing if there is a seer in the game
        # The seer protocol
        print('Seer, wake up')
        investigated_player = clean_input('Who is the Seer investigating: ')
        seer_player = role_finder('seer') # Name of the player who is a seer
        player_dict[seer_player].crystal_ball(investigated_player) # Investigating the person
        print('Seer, go back to sleep')
    
    # Gathering information needed to proceed with the werewolf protocol
    alive_player_dict = alive_people_checker() 
    werewolf_counter, non_wolf_counter,name_of_werewolf = werewolf_information(alive_player_dict)
    
    # Deciding who the werewolves are killing
    print('Werewolves, wake up')
    if werewolf_counter < 1: # If there are more than one wolves use the plural
        chosen_player = input('Who are the werewolves killing: ')
        for wolf in name_of_werewolf:
            player_dict[wolf].murder(chosen_player)
        print('Werewolves, go back to sleep')
        Voting() # go to the day
    elif werewolf_counter == 1: # Changing what the string says so it is gramatticaly correct for one wolf
        chosen_player = input('Who is the werewolf killing: ')
        player_dict[name_of_werewolf].murder(chosen_player)
        print('Werewolves, go back to sleep')
        Voting() # go to the day


def Voting() -> None:
    '''
    Controlling all the happenings that occur in the day, mainly voting.
    '''
    reset_values() # resetting everyones guarded and visited statuses to False
    
    alive_player_dict = alive_people_checker() # Keys are the player names, values are their character types
    alive_players = alive_player_dict.keys() # Collecting names of players who are still alive
    werewolf_counter, non_wolf_counter, name_of_werewolf = werewolf_information(alive_player_dict) 
    
    # Has anyone won
    if game_status_checker():
        return
    
    vote_dict = {}  # Keys are the player names, # values are how many votes they have recieved
    # Adding the players who are still alive to a dictionary to count votes later
    for player in alive_players:
        if player_dict[player].life_status == True:
            vote_dict[player_dict[player].player_name] = 0
    
    # Asking each player who is still alive who they are voting for
    for player in alive_players:
        voted_player = clean_input(f'{player} is voting for (type skip if they are not voting this round): ')
        if voted_player == 'skip':
            pass
        else:
            vote_dict[voted_player] += 1
    
    # Deciding the outcome of the vote
    max_value = max(vote_dict.values()) # Value of the most votes
    max_keys = [k for k, v in vote_dict.items() if v == max_value] # Who has this many votes 
    print(max_keys[0])
    
    if len(max_keys) > 1:  # Seeing if it is a draw 
        Night() # Then go straight into the night
    elif max_value > (len(alive_player_dict)/2): # If it is a majority
        player_dict[max_keys[0]].life_status = False
        print(f'{max_keys[0]} has been voted out')
        if game_status_checker():
            return
        Night()
    else: # If is isn't a majority
        Night() # Then go straight into the night

# GAME BEGINS ---------------------------------------------------------------------------

# Number of players
# Getting input from the gamemaster
player_number = input('Enter the number of players: ')
player_number = int(player_number.strip())

# Creating an array of the players names
players = []
for i in range(0,player_number):
    player_name = input(f'Player {i+1} ').lower().strip()
    players.append(player_name)

# Create dictionary for players
player_dict = {}
roles_in_game = []

# Assigning a class to each player
for player in players:
    class_name_str = clean_input(f'{player} is a:')
    
    # Create the right class
    if class_name_str == "werewolf":
        player_dict[player] = Werewolf(player, class_name_str, 
                                       True, False, False)
        roles_in_game.append('werewolf')
    elif class_name_str == "villager":
        player_dict[player] = Villager(player, class_name_str, 
                                       True, False, False)
        roles_in_game.append('villager')
    elif class_name_str == "bodyguard":
        player_dict[player] = Bodyguard(player, class_name_str, 
                                        True, False, False)
        roles_in_game.append('bodyguard')
    elif class_name_str == "seer":
        player_dict[player] = Seer(player, class_name_str, 
                                        True, False, False)
        roles_in_game.append('seer')
    elif class_name_str == "village idiot":
        player_dict[player] = Villager(player, class_name_str, 
                                        True, False, False)
        roles_in_game.append('villager')
    elif class_name_str == "prostitute":
        player_dict[player] = Prostitute(player, class_name_str, 
                                        True, False, False)
        roles_in_game.append('prostitute')

Night()

#    # Converting string into class
#    class_name = globals()[class_name_str.capitalize()]
#    # Assigning the class to the player
#    globals()[player] = class_name(player, class_name_str, True, False, False)