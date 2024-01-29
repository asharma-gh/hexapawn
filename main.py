import pygame
from game import G_W,GS_W,GS_FIN,FPS,FR_TIME_MS,init_window,init_grid,on_tick,do_move,render
from model import load_model,update_model,gen_move,learn,serialize_model
#
def init_game():
    load_model()
    init_grid()
    init_window()
    run() # Start loop
#
def run():
    prev_fr=0
    acc=0
    while 1:
        t=pygame.time.get_ticks()
        dt=(t-prev_fr)
        prev_fr=t
        acc += dt
        if acc < FR_TIME_MS:
            continue
        acc=0
        gs=on_tick(dt) # Game
        if gs and gs[0]==GS_W:
            update_model(gs[1])
            pawn,move=gen_move(gs[1])
            do_move(pawn,G_W,move)
            pygame.time.wait(100) # Delay to slow CPU move
        elif gs and gs[0]==GS_FIN:
            end_game(gs[1])
            return
        render()
#
def end_game(result):
    if result != None:
        learn(result)
        serialize_model()
#
if __name__ == "__main__":
    init_game()
