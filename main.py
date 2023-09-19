################################
##          Hexapawn          ##
# 3 x 3 Chess with only Pawns ##
################################
import pygame
import numpy as np
import math as m
#
FPS=60
FR_TIME_MS=1000//FPS
SCREEN_DIM=(750,600)
# Board
BOARD_DIM=(3,3)
CELL_W,CELL_H=SCREEN_DIM[0]//BOARD_DIM[0],SCREEN_DIM[1]//BOARD_DIM[1]
# Grid State
G_EMPTY,G_W,G_B=0,1,2
G=np.zeros(shape=(BOARD_DIM[1],BOARD_DIM[0]),dtype='uint8')
C_LIGHT=(200,150,75)
C_DARK=(125,75,37)
# Mouse
G_HOV_COL=(0,255,0)
# Pygame
pygame.init()
WINDOW=pygame.display.set_mode(SCREEN_DIM)
WINDOW.fill((255,255,255))
# Pawns
P_DIM=(CELL_W//3,CELL_H * .75)
W_PAWN=(255,255,255)
B_PAWN=(0,0,0)
# Game State
GS_W=0
GS_B=1
GS_FIN=2
GS_RESET=3
#
cur_GS=GS_B
cur_cel=None
cur_winner=None
SCORE_W,SCORE_B=0,0
# UI
FONT=pygame.font.SysFont('Arial',25)
# Init
def init_grid():
    for ii in range(0,3):
        G[0][ii]=G_W
        G[2][ii]=G_B
# Input
def cur_mouse_g_pos():
    m_x,m_y = pygame.mouse.get_pos()
    gpos = (m_x//CELL_W,m_y//CELL_H)
    return gpos
# State
def is_valid_move(cur_cel,col,gpos):
    if abs(cur_cel[0] - gpos[0]) > 1:
        return False
    if col==G_W: # W - r0
        return (G[gpos[1]][gpos[0]]==G_B and gpos[1] - cur_cel[1] == 1) \
                or (gpos[0]==cur_cel[0]  and gpos[1]-cur_cel[1]==1)
    elif col==G_B: # B - r2
        return (G[gpos[1]][gpos[0]]==G_W and cur_cel[1]-gpos[1] == 1) \
                or (gpos[0]==cur_cel[0]  and cur_cel[1]-gpos[1]==1)
#
def has_valid_move(pos,col):
    if col == G_W:
        return pos[1] != 2
    elif col == G_B:
        return pos[1] != 0
#
def is_draw():
    b_stuck,w_stuck=1,1
    for ii in range(BOARD_DIM[1]):
        for jj in range(BOARD_DIM[0]):
            if G[ii][jj] == G_B:
                b_stuck = b_stuck and not has_valid_move((jj,ii),G_B)
            if G[ii][jj] == G_W:
                w_stuck = w_stuck and not has_valid_move((jj,ii),G_W)
    return b_stuck or w_stuck
#
def increment_state():
    global cur_GS,cur_winner
    if max(SCORE_W,SCORE_B)==3 or is_draw():
        cur_winner=G_W if SCORE_W > SCORE_B else G_B if SCORE_B > SCORE_W else None
        cur_GS=GS_FIN
    elif cur_GS == GS_W:
        cur_GS=GS_B
    elif cur_GS == GS_B:
        cur_GS=GS_W
    elif cur_GS == GS_FIN:
        cur_GS=GS_B
#
def update_state(gpos):
    global cur_cel,SCORE_W,SCORE_B
    player = G_W if cur_GS==GS_W else G_B
    op     = G_B if player==G_W else G_W
    if (not cur_cel or G[cur_cel[1]][cur_cel[0]]==player) and G[gpos[1]][gpos[0]] == player:
        cur_cel=gpos
        return
    elif not cur_cel: 
        # Wait for player to click cel to continue
        return
    elif G[gpos[1]][gpos[0]] != player and is_valid_move(cur_cel,player,gpos):
        is_atk=G[gpos[1]][gpos[0]]==op 
        # Move pc
        G[gpos[1]][gpos[0]]=player
        G[cur_cel[1]][cur_cel[0]]=G_EMPTY
        if is_atk:
            if player == G_W:
                SCORE_W += 1
            else:
                SCORE_B += 1
        cur_cel=None
        increment_state()
# Draw
def render_grid():
    for ii in range(G.shape[0]): # R - Y
        for jj in range(G.shape[1]): # C - X
            # Tile
            c = C_DARK if (ii*BOARD_DIM[0] + jj) % 2 == 0 else C_LIGHT
            pygame.draw.rect(WINDOW,c,[jj*CELL_W,ii*CELL_H,CELL_W,CELL_H],0)
            # Pieces
            if G[ii][jj]:
                pcol = W_PAWN if G[ii][jj] == G_W else B_PAWN
                pygame.draw.rect(WINDOW,pcol,[(jj*CELL_W)+((CELL_W-P_DIM[0])//2),(ii*CELL_H)+((CELL_H-P_DIM[1])//2),P_DIM[0],P_DIM[1]],0)
# Mouse hover
def render_cur_mouse(gpos):
    pygame.draw.rect(WINDOW,G_HOV_COL,[gpos[0]*CELL_W,gpos[1]*CELL_H,CELL_W,CELL_H],3)
# Click UI
CL_ACC=0
CL_CUR_GP=None
def render_click(gpos):
    global CL_ACC,CL_CUR_GP
    CL_CUR_GP = gpos if not CL_CUR_GP else CL_CUR_GP
    CL_CUR_ST = 10 - (m.floor(CL_ACC) ** 2)
    if CL_CUR_ST<=0:
        CL_ACC=0
        CL_CUR_GP=None
        return False
    else:
        CL_ACC += .275
        pygame.draw.rect(WINDOW,G_HOV_COL,[CL_CUR_GP[0]*CELL_W,CL_CUR_GP[1]*CELL_H,CELL_W,CELL_H],CL_CUR_ST)
        return True
#
def render_cur_sel():
    if cur_cel:
        pygame.draw.rect(WINDOW,(255,0,0),[cur_cel[0]*CELL_W,cur_cel[1]*CELL_H,CELL_W,CELL_H],5)
#
def render_text_ui():
    global FONT,SCORE_W,SCORE_B
    txtA=FONT.render("Score " + str(SCORE_W),True,(255,255,255))
    txtB=FONT.render("Score " + str(SCORE_B),True,(255,255,255))
    WINDOW.blit(txtA,(0,5))
    WINDOW.blit(txtB,(0,SCREEN_DIM[1]-25))
    if cur_GS == GS_FIN:
        txtW=FONT.render("DRAW!" if cur_winner == None else "Player " + ("A" if cur_winner==G_W else "B") + " Wins!",True,(255 if cur_winner==None else 0,255,0))
        _,_,tw,th=txtW.get_rect()
        WINDOW.blit(txtW,((SCREEN_DIM[0]-tw)//2, (SCREEN_DIM[1]-th)//2))
    else:
        txtPlayer=FONT.render("Player " + ("A" if cur_GS==GS_W else "B" if cur_GS==GS_B else "") + " Turn",True,(255,255,255))
        _,_,tw,th=txtPlayer.get_rect()
        WINDOW.blit(txtPlayer,((SCREEN_DIM[0]-tw)//2, 0 if cur_GS==GS_W else SCREEN_DIM[1]-25))
# Loop
prev_fr=0
acc=0
init_grid()
cur_click=False
while 1:
    t=pygame.time.get_ticks()
    dt=(t-prev_fr)
    prev_fr=t
    acc += dt
    if acc < FR_TIME_MS:
        continue
    acc=0
    # BG
    render_grid()
    # Input
    gpos=cur_mouse_g_pos()
    click=False
    for e in pygame.event.get():
        if e.type==pygame.MOUSEBUTTONUP and not cur_click:
            click=True
        if e.type==pygame.QUIT:
            exit(0)
    # State
    if click:
        update_state(gpos)
    # UI
    render_cur_mouse(gpos)
    if cur_click or click:
        cur_click = render_click(gpos)
    render_cur_sel()
    render_text_ui()
    pygame.display.update()

