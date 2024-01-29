import random
import pickle
from time import sleep
from game import BOARD_DIM,get_possible_moves_w
MODEL_FILENAME="RL_HEXAGAME_00.pkl"
# Usage:
# Load Model -> Loop[ Update Model -> Do Move ] -> (Win/Lose) Learn -> Serialize
#
# pth pawn and ith move corresponds to the following spots:
# [0 1 2]
# [3 4 5]
# [6 7 8]
# Board State -> [(Pawn, [Moves])]
model={}
# [(Board State, (Pawn,MoveIdx)]
moves_so_far=[]
#
def idx_to_xy(idx):
    return (idx%BOARD_DIM[1],idx//BOARD_DIM[1])
# Updates model with possible moves for this board state
def update_model(bs):
    global model
    # Init Board State
    if bs not in model:
        model[bs] = []
    pawns=[]
    for ii in range(len(bs)):
        if bs[ii]=='W':
            pawns.append(ii)
    possible_moves=[]
    for pawn in pawns:
        moves=get_possible_moves_w(idx_to_xy(pawn))
        if moves:
            model[bs].append((pawn,moves))
#
def gen_move(bs):
    global moves_so_far
    if bs in model:
        pawn_moves=model[bs][random.randint(0,len(model[bs])-1)]
        move=pawn_moves[1][random.randint(0,len(pawn_moves[1])-1)]
        moves_so_far.append((bs,(pawn_moves[0],move)))
        return (idx_to_xy(pawn_moves[0]),idx_to_xy(move))
    else:
        print(f"ERROR: Board State not found in model! {bs}")
# Perform Reinforcement learning: 
#  - Award winning moves,remove losing moves.
def learn(did_win):
    print(f"CURRENT MODEL: {model}")
    for move in moves_so_far:
        for ii,pawn_move in enumerate(model[move[0]]):
            if pawn_move[0]==move[1][0]: # Find moves for this pawn
                if did_win:
                    model[move[0]][ii][1].append(move[1][1]) # Add one more move
                    break
                else:
                    if max([len(moves) for pawn,moves in model[move[0]]]) > 6:
                        # Remove one instance of losing move
                        for jj,prevm in enumerate(model[move[0]][ii][1]):
                            if prevm==move[1][1]:
                                del model[move[0]][ii][1][jj]
                                break
#
def serialize_model():
    model_fh=open(MODEL_FILENAME,"wb")
    pickle.dump(model,model_fh,protocol=pickle.HIGHEST_PROTOCOL)
    model_fh.close()
#
def load_model():
    global model
    try:
        model_fh=open(MODEL_FILENAME,"rb")
        model=pickle.load(model_fh)
        model_fh.close()
    except OSError:
        print("Unable to load model file! Serialize prior to calling.")

