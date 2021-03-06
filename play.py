from game import GoGame
#import agent
from agent import Agent
import sys
import numpy as np
import argparse
import os.path
import random
"""
ARGUMENTS
"""
parser = argparse.ArgumentParser()
parser.add_argument('--interactive', default=False, help='Text interactive interface', action='store_true')
parser.add_argument('--cycle', default=-1, type=int, help='Number of cycle')
parser.add_argument('--black', default='random', choices=['agent','random'], help='AI for black')
parser.add_argument('--white', default='random', choices=['agent','random'], help='AI for white')
parser.add_argument('--ngames', default=500, type=int, help='Number of episodes to play')
parser.add_argument('--save', default=False, help='Save self-play episodes', action='store_true')
parser.add_argument('--save_dir', default='./data',type=str,help='Directory for save')
args = parser.parse_args()

interactive = args.interactive
cycle = args.cycle
black = args.black
white = args.white
ngames = args.ngames
save = args.save
save_dir = args.save_dir

"""
SOME INITS
"""
boardsize = 9

game = GoGame(boardsize)

if black == 'agent' or white == 'agent' or interactive:
    if cycle == -1:
        agent = Agent(eps=0)
    else:
        agent = Agent(eps=1.0/(1+cycle))

ai_color = {'black':black, 'white':white}

game_results = [0,0,0]

"""
MAIN GAME LOOP
"""
while True:

    if interactive:
        game.print_board()
        vertex = raw_input('%s plays:'%game.current_color)
        if vertex == 'agent':
            vertex = agent.play(game.current_color,game.legal_states())
    else:
        legal_states = game.legal_states()
        ai_type = ai_color[game.current_color]
        if ai_type == 'agent':
            vertex = agent.play(game.current_color,legal_states)
        elif ai_type == 'random':
#            _tmp = np.random.randint(len(legal_states))
#            vertex = legal_states[_tmp][0]
            vertex = random.choice(legal_states.keys())
            
    game.play(vertex) 

    if game.end:
        if interactive:
            play_more = raw_input('Play more?')
            if play_more == 'y':
                game.reset()
            else:
                break
        else:
            if game.winner == 'black':
                game_results[0] += 1
            elif game.winner == 'white':
                game_results[1] += 1
            else:
                game_results[2] += 1
            ngames -= 1
            if save:
                _n = 0
                while os.path.isfile('%s/ep%d'%(save_dir,_n)):
                    _n += 1
                game.save('%s/ep%d'%(save_dir,_n))
            sys.stdout.write('\rGames remaining:%d Results(b/w/d):%d/%d/%d'%(ngames,game_results[0],game_results[1],game_results[2]))
            sys.stdout.flush()
            if ngames == 0:
                break
            else:
                game.reset()
            
        
