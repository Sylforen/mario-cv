import cv2


def load_images(world=1, level=1):
    
    mario = cv2.imread('assets/sprites/mario/mario-small-right.png', 0)
    goomba1 = cv2.imread('assets/sprites/enemies/goomba1.png', 0)
    goomba2 = cv2.imread('assets/sprites/enemies/goomba2.png', 0)
    koopa1 = cv2.imread('assets/sprites/enemies/koopa1.png', 0)
    koopa2 = cv2.imread('assets/sprites/enemies/koopa2.png', 0)
    koopa3 = cv2.imread('assets/sprites/enemies/koopa3.png', 0)
    koopa4 = cv2.imread('assets/sprites/enemies/koopa-shell.png', 0)


    koopa5 = cv2.imread('assets/sprites/enemies/koopa5.png', 0)
    koopa6 = cv2.imread('assets/sprites/enemies/koopa6.png', 0)
    koopa7 = cv2.imread('assets/sprites/enemies/koopa7.png', 0)
    koopa8 = cv2.imread('assets/sprites/enemies/koopa8.png', 0)
    koopa9 = cv2.imread('assets/sprites/enemies/koopa9.png', 0)
    koopa10 = cv2.imread('assets/sprites/enemies/koopa10.png', 0)
    piranha_plant = cv2.imread('assets/sprites/enemies/piranha_plant.png', 0)
    bill_blaster = cv2.imread('assets/sprites/enemies/bill_blaster.png', 0)
    bullet_bill1 = cv2.imread('assets/sprites/enemies/bullet_bill1.png', 0)
    bullet_bill2 = cv2.imread('assets/sprites/enemies/bullet_bill2.png', 0)
    beetle1 = cv2.imread('assets/sprites/enemies/beetle1.png', 0)
    beetle2 = cv2.imread('assets/sprites/enemies/beetle2.png', 0)

    chiseled = cv2.imread('assets/sprites/obstacle/block-chiseled.png', 0)
    brick = cv2.imread('assets/sprites/misc/brick.png', 0)
    pipe1 = cv2.imread('assets/sprites/obstacle/pipe-up.png', 0)
    block = cv2.imread('assets/sprites/misc/rock.png', 0)
    rock = cv2.imread('assets/sprites/misc/rock.png', 0)
    flagpole = cv2.imread('assets/sprites/misc/flagpole.png', 0)
    question1 = cv2.imread('assets/sprites/misc/question1.png', 0)
    question2 = cv2.imread('assets/sprites/misc/question2.png', 0)
    question3 = cv2.imread('assets/sprites/misc/question3.png', 0)


    question4 = cv2.imread('assets/sprites/misc/question4.png', 0)
    underground_brick = cv2.imread('assets/sprites/misc/underground_brick.png', 0)
    underground_rock = cv2.imread('assets/sprites/misc/underground_rock.png', 0)
    underground_block = cv2.imread('assets/sprites/obstacle/underground_block.png', 0)



    power_mushroom = cv2.imread('assets/sprites/collectibles/power_mushroom.png', 0)
    level_mushroom = cv2.imread('assets/sprites/collectibles/level_mushroom.png', 0)
    fire_flower = cv2.imread('assets/sprites/collectibles/fire_flower.png', 0)
    super_star = cv2.imread('assets/sprites/collectibles/super_star.png', 0)
    coin = cv2.imread('assets/sprites/collectibles/coin.png', 0)





    # because openCV is BGR
    red = (0, 0, 255)
    green = (0, 255, 0)
    blue = (255, 0, 0)


    if world == 1 and level == 1:
        mario_list = [(mario, 0.8, mario.shape[0], mario.shape[1], green, 'Mario')]

        
        enemy_list = [(goomba1, 0.7, goomba1.shape[0], goomba1.shape[1], red, 'Goomba'),
                      (goomba2, 0.7, goomba2.shape[0], goomba2.shape[1], red, 'Goomba'),
                      (koopa1, 0.7, koopa1.shape[0], koopa1.shape[1], red, 'Koopa'),
                      (koopa2, 0.7, koopa2.shape[0], koopa2.shape[1], red, 'Koopa'),
                      (koopa3, 0.7, koopa3.shape[0], koopa3.shape[1], red, 'Koopa'),
                      (koopa4, 0.7, koopa4.shape[0], koopa4.shape[1], red, 'Koopa'),
                      (koopa5, 0.7, koopa5.shape[0], koopa5.shape[1], red, 'Koopa'),
                      (koopa6, 0.7, koopa6.shape[0], koopa6.shape[1], red, 'Koopa'),
                      (koopa7, 0.7, koopa7.shape[0], koopa7.shape[1], red, 'Koopa'),
                      (koopa8, 0.7, koopa8.shape[0], koopa8.shape[1], red, 'Koopa'),
                      (koopa9, 0.7, koopa9.shape[0], koopa9.shape[1], red, 'Koopa'),
                      (koopa10, 0.7, koopa10.shape[0], koopa10.shape[1], red, 'Koopa'),
                      (piranha_plant, 0.7, piranha_plant.shape[0], piranha_plant.shape[1], red, 'Piranha Plant'),
                      (bill_blaster, 0.7, bill_blaster.shape[0], bill_blaster.shape[1], red, 'Bill Blaster'),
                      (bullet_bill1, 0.7, bullet_bill1.shape[0], bullet_bill1.shape[1], red, 'Bullet Bill'),
                      (bullet_bill2, 0.7, bullet_bill2.shape[0], bullet_bill2.shape[1], red, 'Bullet Bill'),
                      (beetle1, 0.7, beetle1.shape[0], beetle1.shape[1], red, 'Beetle'),
                      (beetle2, 0.7, beetle2.shape[0], beetle1.shape[1], red, 'Beetle1')]
        
        obstacle_list = [(pipe1, 0.7, pipe1.shape[0], pipe1.shape[1], blue),
                         (chiseled, 0.7, chiseled.shape[0], chiseled.shape[1], blue),
                         #(underground_block, 0.7, underground_block.shape[0], underground_block.shape[1], blue)
                         ]
        
        brick_list = [(brick, 0.7, brick.shape[0], brick.shape[1], blue),
                      (question1, 0.7, question1.shape[0], question1.shape[1], blue),
                      (question2, 0.7, question2.shape[0], question2.shape[1], blue),
                      (question3, 0.7, question3.shape[0], question3.shape[1], blue),
                      #(question4, 0.7, question4.shape[0], question4.shape[1], blue),
                      #(underground_brick, 0.7, underground_brick.shape[0], underground_brick.shape[1], blue)
                      ]
        
        rock_list = [(rock, 0.7, rock.shape[0], rock.shape[1], blue),
                     #(underground_rock, 0.7, underground_rock.shape[0], underground_rock.shape[1], blue)
                     ]

        #collectible_list = []

        collectible_list = [(coin, 0.7, coin.shape[0], coin.shape[1], green)]

        # collectible_list = [(power_mushroom, 0.7, power_mushroom.shape[0], power_mushroom.shape[1], green),
        #                     (level_mushroom, 0.7, level_mushroom.shape[0], level_mushroom.shape[1], green),
        #                     (fire_flower, 0.7, fire_flower.shape[0], fire_flower.shape[1], green),
        #                     (super_star, 0.7, super_star.shape[0], super_star.shape[1], green),
        #                     (coin, 0.7, coin.shape[0], coin.shape[1], green)]
    
    return mario_list, enemy_list, obstacle_list, brick_list, rock_list, collectible_list
