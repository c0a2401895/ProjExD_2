import os
import random as randam
import sys
import pygame as pg



WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP: (0, -5),
         pg.K_DOWN: (0, +5),
         pg.K_LEFT: (-5, 0),
         pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # 練習3
def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数 : こうかとんRectまたは爆弾Rect
    戻り値 : 判定結果タプル (横方向, 縦方向)
    画面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True,True # 横,縦方向の変数
    # 横方向判定
    if rct.left < 0 or WIDTH < rct.right: # 画面内だったら
        yoko = False
    # 縦方向判定
    if rct.top < 0 or HEIGHT < rct.bottom: # 画面内だったら
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    # こうかとんの初期化
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200


    # 爆弾初期化
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.center = randam.randint(0, WIDTH), randam.randint(0, HEIGHT)
    bb_img.set_colorkey((0, 0, 0))
    vx,vy = +5, +5 # 爆弾の移動量

    clock = pg.time.Clock()
    tmr = 0


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct): # こうかとんRectと爆弾が衝突したら
            gameover(screen) # ゲームオーバー画面を表示
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] # 左右方向
                sum_mv[1] += mv[1] # 上下方向
    

        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True): # 画面外だったら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) # こうかとんを元の位置に戻す
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx,vy)   # 爆弾移動

        yoko, tate = check_bound(bb_rct) # 爆弾の画面内判定
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct) # 爆弾描画
        pg.display.update()
        tmr += 1
        clock.tick(50)

def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー画面を表示する関数
    引数 : screen : Surface
    戻り値 : なし
    """
    blackout = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(blackout, (0, 0, 0), (0, 0, WIDTH, HEIGHT)) # 画面を黒く塗りつぶす
    blackout.set_alpha(128)  # 半透明に設定
    screen.blit(blackout, (0, 0))

    font = pg.font.Font(None, 80)
    txt = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(txt, [350, 300])
    gameoverkouka_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    gameoverkouka_rct = gameoverkouka_img.get_rect()
    gameoverkouka_rct.center = 300, 320
    gameoverkouka1_rct = gameoverkouka_img.get_rect()
    gameoverkouka1_rct.center = 740, 320
    screen.blit(gameoverkouka_img, gameoverkouka_rct) # こうかとん描画
    screen.blit(gameoverkouka_img, gameoverkouka1_rct)
    pg.display.update()
    pg.time.wait(5000) # 5秒待つ


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
