import sys
import pygame
from game import G_W,GS_W,GS_FIN,GS_FORCE_QUIT,FR_TIME_MS,init_window,init_grid,on_tick,do_move,render
from model import load_model,update_model,gen_move,learn,serialize_model
#
def init_game(autoplay=False):
    load_model()
    init_grid()
    init_window()
    run(autoplay) # Start loop
#
def run(autoplay):
    prev_fr=0
    acc=0
    shall_end=False
    while 1:
        t=pygame.time.get_ticks()
        dt=(t-prev_fr)
        prev_fr=t
        acc += dt
        if acc < FR_TIME_MS:
            continue
        acc=0
        gs=on_tick(dt,autoplay) # Game
        if gs and gs[0]==GS_FORCE_QUIT:
            if autoplay:
                shall_end=True
            else:
                sys.exit(0)
        elif gs and gs[0]==GS_FIN:
            end_game(gs[1])
            if shall_end:
                return
        if gs and gs[0]==GS_W:
            update_model(gs[1])
            pawn,move=gen_move(gs[1])
            do_move(pawn,G_W,move)
            pygame.time.wait(100) # Delay to slow CPU move

        render()
#
def end_game(result=None):
    if result != None:
        learn(result)
        serialize_model()
#
# 1 to play [default], 2 for auto-play
if __name__ == "__main__":
    init_game(len(sys.argv) > 1 and int(sys.argv[1])==2)
