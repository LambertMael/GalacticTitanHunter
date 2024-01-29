#CODE ECRIT PAR LE GROUPE SPE NSI EN TERMINALE 2
#GRAPHISME ENTIEREMENT FAIT PAR LE GROUPE SPE NSI EN TERMINALE 2
#MERCI AU SITE freesound.org POUR TOUT LES SONS (ils sont bien tous sans copyright)
import pygame
import os
import random
import sqlite3
import time

pygame.font.init()
pygame.mixer.init()
WIDTH, HEIGHT = 450, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galactic Octopus Titan Hunter")

# Load images
CIRCLE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "space_ship_circle.png"))
PURPLE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "space_ship_purple.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "space_ship_blue.png"))
SMALL_SPACE_SHIP = pygame.image.load(os.path.join("assets", "space_ship_small.png"))
BLACK_SPACE_SHIP = pygame.image.load(os.path.join("assets", "space_ship_black.png"))
AMONGUS_SPACE_SHIP = pygame.image.load(os.path.join("assets", "space_ship_amogus.png"))
BIG_SPACE_SHIP = pygame.image.load(os.path.join("assets", "space_ship_big.png"))
BOSS = pygame.image.load(os.path.join("assets", "boss_calamar.png"))
LOGO = pygame.image.load(os.path.join("assets", "logo.png"))

# Player
PLAYER_RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "space_ship_player_red.png"))
BIG_PLAYER_GOLDEN_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("assets", "space_ship_player_golden.png")), (320, 320))

# Lasers
PLAYER_RED_LASER = pygame.image.load(os.path.join("assets", "laser_red_player.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "laser_green.png"))
BLACK_LASER = pygame.image.load(os.path.join("assets", "laser_black.png"))
PURPLE_LASER = pygame.image.load(os.path.join("assets", "laser_purple.png"))
ROCKET = pygame.image.load(os.path.join("assets", "laser_rocket.png"))

# Background
BG1 = pygame.image.load(os.path.join("assets", "Background1.png"))

#Bonus
HEAL_BONUS = pygame.image.load(os.path.join("assets", "bonus_heal.png"))
COOLDOWN_BONUS = pygame.image.load(os.path.join("assets", "bonus_shoot.png"))
FULL_HEAL_BONUS = pygame.image.load(os.path.join("assets", "bonus_full_heal.png"))
SPEED_BONUS = pygame.image.load(os.path.join("assets", "bonus_speed.png"))

#Sounds
DAMAGE_SOUND = pygame.mixer.Sound(os.path.join("sounds", "damage.wav"))
DEATH_SOUND = pygame.mixer.Sound(os.path.join("sounds", "death.wav"))
SHOOT_SOUND = pygame.mixer.Sound(os.path.join("sounds", "shoot.wav"))
TRANULT_SOUND = pygame.mixer.Sound(os.path.join("sounds", "transitiontoulti.wav"))
ULT_SOUND = pygame.mixer.Sound(os.path.join("sounds", "ulti.wav"))
PICKUP_SOUND = pygame.mixer.Sound(os.path.join("sounds", "pickup_bonus.wav"))
BOSS_DEATH_SOUND = pygame.mixer.Sound(os.path.join("sounds", "boss_death.wav"))
LOOP_SONG = pygame.mixer.Sound(os.path.join("sounds", "musicloop.wav"))
BOSS_BATTLE_SONG = pygame.mixer.Sound(os.path.join("sounds", "ulti.wav"))

#Volume
DAMAGE_SOUND.set_volume(0.05)
DEATH_SOUND.set_volume(0.05)
SHOOT_SOUND.set_volume(0.05)
TRANULT_SOUND.set_volume(0.05)
ULT_SOUND.set_volume(0.05)
LOOP_SONG.set_volume(0.05)
PICKUP_SOUND.set_volume(0.05)
BOSS_BATTLE_SONG.set_volume(0.05)
BOSS_DEATH_SOUND.set_volume(0.05)

class Background():
    '''
    Permet de sélectionner le fond qui défilera pendant le jeu
    '''
    def __init__(self, bg):
        '''Attribut : image, les longueur de l'image, les coordonnées de l'image (bgY1 et bgX1), la vitesse et un compteur  '''
        self.bgimage = bg
        self.rectBGimg = self.bgimage.get_rect()
        self.portions = (self.rectBGimg.height//HEIGHT)
        self.bgY1 = -self.rectBGimg.height*(self.portions-1)//self.portions
        self.bgX1 = 0
        self.moving_speed = 1
        self.count = 0
         
    def update(self):
        '''Permet de faire défiler le niveau et de l'arrêter quand on arrive au bout du fond'''
        if self.count == 5:
            self.bgY1 += self.moving_speed
            self.count = 0
        else :
            self.count += 1
        
        if self.bgY1 == 0 and self.moving_speed >= 0:
            self.moving_speed = 0
        
        if self.bgY1 < -self.rectBGimg.height*(self.portions-1)//self.portions:
            self.bgY1 = -self.rectBGimg.height*(self.portions-1)//self.portions
            self.moving_speed = 1
     
    def render(self):
        '''Permet le rafraichissement de l'image'''
        WIN.blit(self.bgimage, (self.bgX1, self.bgY1))

class Bonus:
    ''' Implémentation de la classe bonus qui facilite le jeu'''
    LIST_BONUS_SPRITE = {
        'heal' : HEAL_BONUS,
        'cooldown': COOLDOWN_BONUS,
        'full' : FULL_HEAL_BONUS,
        'speed' : SPEED_BONUS
        }
    #Dico des bonus disponible, on associe chaque bonus à son visuel

    def __init__(self, x, y, bonus):
        '''Attribut : coordonnées (x et y), nom du bonus(id), image, hitbox'''
        self.x = x
        self.y = y
        self.bonus = bonus
        self.img = self.LIST_BONUS_SPRITE[bonus]
        self.mask = pygame.mask.from_surface(self.img)      #Permet de délimité correctement la hitbox (zone de l'image qui sera touchable par les autre objets)

    def draw(self, window):
        '''Affiche le bonus en jeu'''
        window.blit(self.img, (self.x, self.y))

    def off_screen(self, height): 
        '''Detecte si le bonus est passé en dessous de l'écran'''                   
        return not(self.y <= height)

    def move(self, vel, liste):
        '''Gère le déplacement des bonus'''
        self.y += vel
        if self.off_screen(HEIGHT):
                liste.remove(self)
    
    def collision(self, obj):
        '''Gère les collision entre le bonus et tout autre objet (obj)'''
        return collide(self, obj)

class Laser:                                            
    def __init__(self, x, y, img):
        '''Attribut : coordonnées (x et y), image, hitbox'''                      
        self.x = x                                      
        self.y = y                                      
        self.img = img                                  
        self.mask = pygame.mask.from_surface(self.img)  

    def draw(self, window):                            
        '''Affiche le laser en jeu''' 
        window.blit(self.img, (self.x, self.y))        

    def move(self, vel):                   
        '''Gère le déplacement des lasers uniquement'''
        self.y += vel                               
  
    def off_screen(self, height):
        '''Verifie si les lasers sont hors de l'écran, (renvoie 'True' si c'est le cas et 'False' si le laser est toujours visible sur l'écran)'''
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        '''Gère les collisions entre le laser et tout autre objet (obj)'''
        return collide(self, obj)

class Ship:
    '''Class mère 'Ship' qui'''

    def __init__(self, x, y, health=100):
        '''Attribut :'''
        self.x = x          #coordonnées (x et y)
        self.y = y
        self.health = health    #la santé
        self.ship_img = None    #image du vaisseau
        self.laser_img = None   #l'image du laser correspondant au vaisseau
        self.lasers = []    #la liste des lasers tirés toujours visible à l'écran
        self.cool_down_counter = 0  #temps nécessaire avant de pouvoir tiré un nouveau laser
        self.cooldown_max = 30
        self.timer_bonus_cooldown = 0
        self.timer_bonus_speed = 0

    def draw(self, window):
        '''Affiche le vaisseau, ainsi que tous les lasers tiré par le vaisseau et la barre de santé du vaisseau'''
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
        self.healthbar(window)
    
    def move_lasers(self, vel, obj):
        '''Gère la déplacement et la disparition de tous les laser tiré par le vaisseau'''
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                obj.combo = 1
                pygame.mixer.Sound.play(DAMAGE_SOUND)
                pygame.mixer.music.stop()
                self.lasers.remove(laser)

    def cooldown(self):
        '''Gère le cooldown du vaisseau'''
        if self.cool_down_counter >= self.cooldown_max:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        '''Gère la création de projectile du vaisseau'''
        if self.cool_down_counter == 0:
            laser = Laser(self.x + self.get_width()//2, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
            if self.ship_img == PLAYER_RED_SPACE_SHIP:
                pygame.mixer.Sound.play(SHOOT_SOUND)
                pygame.mixer.music.stop()   

    def get_width(self):
        '''renvoie la largeur du vaisseau'''
        return self.ship_img.get_width()

    def get_height(self):
        '''renvoie la hauteur du vaisseau'''
        return self.ship_img.get_height()
    
    def healthbar(self, window):
        '''Affiche la barre de santé (superpose une barre verte qui a une taille variable sur une barre rouge à taille fixe)'''
        if self.health != self.max_health :
            pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 5, self.ship_img.get_width(), 5))                                      #barre rouge
            pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 5, self.ship_img.get_width() * (self.health/self.max_health), 5))      #barre verte

class Player(Ship):
    def __init__(self, x, y, health=100):
        '''Attribut : , , , , , , '''
        super().__init__(x, y, health)      #coordonnées et santé repris de la classe 'Ship'
        self.ship_img = PLAYER_RED_SPACE_SHIP   #image
        self.laser_img = PLAYER_RED_LASER   #image des lasers liés au vaisseau
        self.mask = pygame.mask.from_surface(self.ship_img)     #hitbox
        self.max_health = health        #santé maximale
        self.ulti = 0   #la charge de la transformation (besoin de 10 pour lancé l'ulti)
        self.ulti_cooldown = 0      #la durée de la transformation
        self.combo = 1

    def move_lasers(self, vel, objs):
        global score
        global level
        '''Gère le déplacement et la disparition de tous les lasers lié au vaisseau'''
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        obj.health -= 10
                        if obj.health <= 0:
                            objs.remove(obj)
                            self.combo += 1
                            if self.ulti < 500 and self.ship_img != BIG_PLAYER_GOLDEN_SPACE_SHIP:
                                self.ulti += 25
                            score += (1*level)*self.combo
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        '''Affiche le vaisseau sur l'écran ainsi que sa barre de vie'''
        super().draw(window)
        self.healthbar(window)
    
    def titan(self):
        '''Active la transformation en titan'''
        if self.ulti >= 500:
            self.health = 2000
            self.max_health = 2000
            self.ship_img = BIG_PLAYER_GOLDEN_SPACE_SHIP
            self.mask = pygame.mask.from_surface(self.ship_img)
            if self.ulti == 500:
                pygame.mixer.Sound.play(TRANULT_SOUND)
                pygame.mixer.music.stop()

    def shoot_titan(self): 
        '''  Tir trois lasers au lieu d'un seul lorsque le vaisseau est transformé'''
        if self.cool_down_counter == 0:
            laser = Laser(self.x + self.get_width()//2, self.y, self.laser_img)
            laser2 = Laser(self.x + self.get_width()//5 - 10, self.y+self.y//2, self.laser_img)
            laser3 = Laser(self.x + self.get_width()*4//5 + 10, self.y+self.y//2, self.laser_img)
            self.lasers.append(laser)
            self.lasers.append(laser2)
            self.lasers.append(laser3)
            self.cool_down_counter = 1
            pygame.mixer.Sound.play(SHOOT_SOUND)
            pygame.mixer.music.stop()
    
    def back_titan(self):
        '''Désactive la transformation'''
        self.max_health = 100
        self.health = 100
        self.ship_img = PLAYER_RED_SPACE_SHIP
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.ulti = 0

class Enemy(Ship):
    
    COLOR_MAP = {
                "circle": (CIRCLE_SPACE_SHIP, GREEN_LASER, 1),
                "blue": (BLUE_SPACE_SHIP, BLACK_LASER, 1), 
                "purple": (PURPLE_SPACE_SHIP, ROCKET, 11),
                "small": (SMALL_SPACE_SHIP, BLACK_LASER, 1),
                "black": (BLACK_SPACE_SHIP, BLACK_LASER, 1),
                "amongus" : (AMONGUS_SPACE_SHIP, GREEN_LASER, 11),
                "big" : (BIG_SPACE_SHIP,  ROCKET, 21),
                "boss" : (BOSS, ROCKET, 100)
                }

    def __init__(self, x, y, color, health=100):
        '''Attribut:'''
        super().__init__(x, y, health)      #Coordonnées et santé
        self.ship_img, self.laser_img, self.health = self.COLOR_MAP[color]      #image + image laser
        self.max_health = self.health   #santé
        self.mask = pygame.mask.from_surface(self.ship_img)     #hitbox
        self.step = 1   #uniquement utile au boss, sert à la sélection d'un script

    def move(self, vel):
        '''Gère le déplacement des vaisseaux ennemies'''
        if self.ship_img != BOSS:
            self.y += vel
        #Gère les déplacement du boss
        else:
            '''Gère les déplacement du boss uniquement, en selectionnant aléatoirement un des script'''
            if self.step == 1:
                if self.y < 300:
                    self.y += vel
                else:
                    self.step = random.randrange(1, 14)

            if self.step == 2:
                if self.x < 300 :
                    self.x += vel
                if self.y > 200:
                    self.y -= vel/4
                if not(self.x < 300) and not(self.y > 200):
                    self.step = random.randrange(1, 14)

            if self.step == 3:
                if self.x > 100:
                    self.x -= vel/2
                else :
                    self.step = random.randrange(1, 14)
            
            if self.step == 4:
                if self.y > 50:
                    self.y -= vel
                if self.x < 300:
                    self.x += vel/4
                if not(self.y > 50):
                    self.step = 5
                if not(self.x < 300):
                    self.step = random.randrange(1, 14)
                
            if self.step == 5:
                if self.y < 100:
                    self.y += vel
                if self.x < 300:
                    self.x += vel/4
                if not(self.y < 100):
                    self.step = 4
                if not(self.x < 300):
                    self.step = random.randrange(1, 14)
            
            if self.step == 6:
                if self.x > 150:
                    self.x -= vel
                else:
                    self.step = random.randrange(1, 14)
            
            if self.step == 7:
                if self.y < 450:
                    self.y += vel
                else:
                    self.step = random.randrange(1, 14)
            
            if self.step == 8:
                if self.x > 0:
                    self.x -= vel
                else:
                    self.step = random.randrange(1, 14)
            
            if self.step == 9:
                if self.x < 350:
                    self.x += vel
                if self.y > 0:
                    self.y -= vel/4
                if not(self.x < 350):
                    self.step = 10
                if not(self.y > 0):
                    self.step = random.randrange(1, 14)
            
            if self.step == 10:
                if self.x > 0:
                    self.x -= vel
                if self.y > 0:
                    self.y -= vel/4
                if not(self.x > 0):
                    self.step = 9
                if not(self.y > 0):
                    self.step = random.randrange(1, 14)
            
            if self.step == 11:
                if self.x < 350:
                    self.x += vel
                if self.y < 450:
                    self.y += vel/4
                if not(self.x < 350):
                    self.step = 12
                if not(self.y < 450):
                    self.step = random.randrange(1, 14)
            
            if self.step == 12:
                if self.x > 0:
                    self.x -= vel
                if self.y < 450:
                    self.y += vel/4
                if not(self.x > 0):
                    self.step = 11
                if not(self.y < 450):
                    self.step = random.randrange(1, 14)
            
            if self.step == 13:
                if self.y > 50:
                    self.y -= vel
                if self.x > 50:
                    self.x -= vel/4
                if not(self.y > 50):
                    self.step = 14
                if not(self.x > 50):
                    self.step = random.randrange(1, 14)
                
            if self.step == 14:
                if self.y < 100:
                    self.y += vel
                if self.x > 50:
                    self.x -= vel/4
                if not(self.y < 100):
                    self.step = 13
                if not(self.x > 50):
                    self.step = random.randrange(1, 14)
        
            if random.randrange(0, 2) == 1:
                self.shoot()

    def new_hp(self, level):
        if self.ship_img != BOSS:
            self.max_health += level
        else:
            self.max_health *= level
        self.health = self.max_health
                
def collide(obj1, obj2):
    '''Permet de vérifier si deux objets sont en collision'''
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
    '''On définit toute les variables et données nécéssaire '''
    global level
    global score
    run = True
    FPS = 60
    level = 0
    lives = 5
    score = 0
    spawn_bonus = 1200
    combo_max = 1
    
    Boss = True             #Booléen qui indique si le joueur n'a pas encore affronté le boss
    Boss_in_game = False    #Booléen qui indique si le joueur affronte un boss
    Boss_Dead = False       #Booléen qui indique si le Boss a été battu

    main_font = pygame.font.Font(os.path.join("fonts", "font_pixel.ttf"), 40)
    sub_font = pygame.font.Font(os.path.join("fonts", "font_pixel.ttf"), 20)
    lost_font = pygame.font.Font(os.path.join("fonts", "font_pixel.ttf"), 60)

    enemies = []
    list_bonus = []
    wave_length = 5

    enemy_vel = 1
    player_vel = 5
    laser_vel = 10
    bonus_vel = 2
    
    player = Player(200, 600)
    background_object = Background(BG1)
    clock = pygame.time.Clock()

    lost = False
    lost_count = 0
    
    pygame.mixer.Sound.play(LOOP_SONG, -1)
    pygame.mixer.music.stop()

    def redraw_window():
        global score_label
        background_object.update()  # Fait défiler l'écran
        background_object.render()  # Rafraichit l'écran

        '''On définit les label pour le texte à afficher'''

        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))

        '''Affiche le Score d'une couleur différente'''
        if score <= 100:
            score_label = sub_font.render(f"Score: {score}", 1, (255,255,255))  #blanc
        elif score > 100 and score <= 500:
            score_label = sub_font.render(f"Score: {score}", 1, (255,0,255))    #violet
        elif score > 500 and score <= 1000:
            score_label = sub_font.render(f"Score: {score}", 1, (0,0,255))      #bleu foncé
        elif score > 1000 and score <= 5000:
            score_label = sub_font.render(f"Score: {score}", 1, (0,255,255))    #bleu ciel
        elif score > 5000 and score <= 10000:
            score_label = sub_font.render(f"Score: {score}", 1, (0,255,0))      #vert
        elif score > 10000 and score <= 50000:
            score_label = sub_font.render(f"Score: {score}", 1, (255,255,0))    #jaune
        elif score > 50000 and score <= 100000:
            score_label = sub_font.render(f"Score: {score}", 1, (255,0,0))      #rouge
        elif score > 100000:
            score_label = sub_font.render(f"Score: {score}", 1, (0,0,0))        #noir

        '''Affiche le combo d'une couleur différente'''
        if player.combo == 1:
            combo_label = sub_font.render(f"Combo: {player.combo}x", 1, (255,255,255))  #blanc
        elif player.combo > 1 and player.combo <= 20:
            combo_label = sub_font.render(f"Combo: {player.combo}x", 1, (255,0,255))    #violet
        elif player.combo > 20 and player.combo <= 40:
            combo_label = sub_font.render(f"Combo: {player.combo}x", 1, (0,0,255))      #bleu
        elif player.combo > 40 and player.combo <= 60:
            combo_label = sub_font.render(f"Combo: {player.combo}x", 1, (0,255,255))    #cyan
        elif player.combo > 60 and player.combo <= 80:
            combo_label = sub_font.render(f"Combo: {player.combo}x", 1, (0,255,0))      #vert
        elif player.combo > 80 and player.combo <= 100:
            combo_label = sub_font.render(f"Combo: {player.combo}x", 1, (255,255,0))    #jaune
        elif player.combo > 100 and player.combo <= 120:
            combo_label = sub_font.render(f"Combo: {player.combo}x", 1, (255,0,0))      #rouge
        elif player.combo > 120:
            combo_label = sub_font.render(f"Combo: {player.combo}x", 1, (0,0,0))        #noir

        enemies_left_label = sub_font.render(f"Enemies Left: {len(enemies)}", 1, (255, 255, 255))
        ulti_label = sub_font.render(f"Ulti: {player.ulti}/500", 1, (255,255, 255))

        '''Affiche 'BOSS', si on affronte un boss et le niveau dans le cas contraire'''
        if Boss_in_game:
            level_label = main_font.render("BOSS", 1, (255,255,255))
        else:
            level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

        #Affichage de l'ATH
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        WIN.blit(enemies_left_label, (WIDTH - enemies_left_label.get_width(), level_label.get_height() + 10 ))
        WIN.blit(ulti_label, (10, lives_label.get_height() + 10))
        WIN.blit(score_label,(5,665))
        WIN.blit(combo_label, (5, 640))

        '''Dessine tous les ennemies présent dans la liste contenant tous les ennemies ainsi que les lasers qui leurs y sont lié'''
        for enemy in enemies:
            enemy.draw(WIN)
        
        '''Même chose avec les bonus'''
        for bonus in list_bonus:
            bonus.draw(WIN)

        '''Dessine le joueur et les lasers qui lui y sont lié'''
        player.draw(WIN)

        '''En cas de défaite : affiche le label de défaite'''
        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        '''!!! rafraichit l'image et met à jour les élements qui sont affichés !!!'''
        pygame.display.update()

    while run:
        clock.tick(FPS)     #Cale le jeu sur un nombre de tick par second
        redraw_window()

        '''detecte si le joueur a perdu'''
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
            background_object.moving_speed = 0 
            pygame.mixer.pause()
            pygame.mixer.Sound.play(DEATH_SOUND)
            pygame.mixer.music.stop()
            time.sleep(2)
            highscore()
        
        '''lance un compte à rebourd pour fermer la partie'''
        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue
        '''Créée des ennemies quand tous ceux créées sont détruit'''
        if len(enemies) == 0:

            '''Lance le combat de boss si les condition sont remplie
               condition : le défilement de l'écran est terminé ET le boss n'a pas encore été affronté'''
            if background_object.bgY1 == 0 and Boss == True:
                Boss_in_game = True
                calamar = Enemy(-(BOSS.get_width()-WIDTH)/2, -500, "boss")
                calamar.new_hp(level)
                enemies.append(calamar)
                enemy_vel = 4
                Boss = False
            else:
                if Boss_in_game == True:
                    Boss_in_game = False
                    Boss_Dead = True
                if Boss_Dead == True:
                    pygame.mixer.pause()
                    pygame.mixer.Sound.play(BOSS_DEATH_SOUND)
                    pygame.mixer.music.stop()
                    score += 10*level*player.combo
                    background_object.moving_speed = -100
                    Boss = True
                    Boss_Dead = False
                    pygame.mixer.Sound.play(LOOP_SONG,-1)
                    pygame.mixer.music.stop()
                enemy_vel = 1
                level += 1
                wave_length += 5
                for i in range(wave_length):
                    enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-150-(50*wave_length), -100), random.choice(["amongus", "black", "blue", "circle", "purple", "small", "big"], ))
                    enemy.new_hp(level)
                    enemies.append(enemy)

        '''Créée des bonus aléatoirement'''
        if random.randrange(0,1000) == 1 or spawn_bonus <= 0:
            b = Bonus(random.randrange(50, WIDTH-100), random.randrange(-150, -100), random.choice(['heal' for i in range(5)]+['cooldown' for i in range(2)]+['full']+['speed' for i in range(3)]))
            list_bonus.append(b)
        
        '''Permet de rendre l'appariton de bonus moins aléatoire, toutes les 20 seconde un bonus apparait'''
        if spawn_bonus > 0:
            spawn_bonus -= 1
        elif spawn_bonus <= 0:
            spawn_bonus = 1200
        
        '''Detécte si des touches sont pressés'''
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_q]) and player.x - player_vel > 0: # left
            player.x -= player_vel
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.x + player_vel + player.get_width() < WIDTH: # right
            player.x += player_vel
        if (keys[pygame.K_UP] or keys[pygame.K_z]) and player.y - player_vel > 0: # up
            player.y -= player_vel
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.y + player_vel + player.get_height() + 15 < HEIGHT: # down
            player.y += player_vel
        if keys[pygame.K_SPACE]:    #tir ou tir multiple
            if player.ship_img != BIG_PLAYER_GOLDEN_SPACE_SHIP:
                player.shoot()
            else:
                player.shoot_titan()
        if keys[pygame.K_a] or keys[pygame.K_LCTRL]:    #active transformation si la charge de l'ulti est terminé
            player.titan()

        '''Déplace les lasers et les vaisseau ennemies'''
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel//2, player)

            '''les fait tirés aléatoirement'''
            if random.randrange(0, 2*60) == 1:
                enemy.shoot()
            
            '''Vérifie les collisions et les positions'''
            if collide(enemy, player):
                if enemy.ship_img == BOSS:
                    player.health = 0
                    pygame.mixer.Sound.play(DAMAGE_SOUND)
                    pygame.mixer.music.stop()                    
                else:
                    player.health -= enemy.health
                    player.combo = 1
                    pygame.mixer.Sound.play(DAMAGE_SOUND)
                    pygame.mixer.music.stop()
                    enemies.remove(enemy)

                '''Si le vaisseau passe derrière le joueur, une vie lui est retiré '''    
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        '''Déplace les lasers lié au vaisseau'''
        player.move_lasers(-laser_vel, enemies)

        '''Déplace les bonus, vérifie leur collision avec le joueur'''
        for b in list_bonus:
            b.move(bonus_vel, list_bonus)
            if collide(b, player):
                pygame.mixer.Sound.play(PICKUP_SOUND)
                pygame.mixer.music.stop()
                if b.bonus == 'heal':
                    '''Rend 10 PV au joueur'''
                    if player.health < player.max_health:
                        player.health += 10
                if b.bonus == 'cooldown':
                    '''Permet de tiré trois fois plus vite temporairement'''
                    player.cooldown_max = 10
                    player.timer_bonus_cooldown = 600
                if b.bonus == 'full':
                    '''Rend tous ses PV au joueur'''
                    player.health = player.max_health
                if b.bonus == 'speed':
                    '''Permet de se déplacer plus vite temporairement'''
                    player_vel = 8
                    player.timer_bonus_speed = 300
                list_bonus.remove(b)
        
        '''timer de la duré du bonus de baisse de cooldown'''
        if player.timer_bonus_cooldown > 0:
            player.timer_bonus_cooldown -= 1
        if player.timer_bonus_cooldown <= 0:
            player.cooldown_max = 30
        
        '''timer de la duré du bonus de vitesse'''
        if player.timer_bonus_speed > 0:
            player.timer_bonus_speed -= 1
        if player.timer_bonus_speed <= 0:
            player_vel = 5
        
        '''timer de la duré de transformation du joueur'''
        if player.ulti > 500 or player.ship_img == BIG_PLAYER_GOLDEN_SPACE_SHIP:
            player.ulti -= 1
            if player.ulti == 0:
                player.back_titan()
            if player.ulti == 450:    
                pygame.mixer.Sound.play(ULT_SOUND)
                pygame.mixer.music.stop()
        
        '''Sauveagarde le combo max'''
        if player.combo > combo_max:
            combo_max = player.combo
        
        '''Permet de quitter le programme à tout momment'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

def highscore():
    #fonction qui s'occupe de l'ajout des scores et pseudos à la database
    pygame.mixer.pause()
    color_inactive = pygame.Color((255, 127, 127)) 
    color_active = pygame.Color((139, 0, 0)) 
    color = color_inactive
    active = False
    text = ''
    runhs = True
    input_box = pygame.Rect(WIDTH/2-100, HEIGHT/4, 200, 75)
    font = pygame.font.Font(os.path.join("fonts", "font_pixel.ttf"), 60)
    death_label = font.render("GAME OVER", 1, (255, 255, 255))
    WIN.fill((30, 30, 30))

    while runhs:
        afficher_highscore()
        #affiche le text (les lettres pressée)
        txt_surface = font.render(text, True, color)

        #Agrandi le rectangle si le text dépasse
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        WIN.blit(txt_surface, (input_box.x+5, input_box.y-10))
        pygame.draw.rect(WIN, color, input_box, 2)
        WIN.blit(score_label,(WIDTH/4+WIDTH/6,125))
        WIN.blit(death_label,(WIDTH/7,30))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Change la couleur de l'input box si selectionné ou non
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        #si la touche enter est pressée alors ça sauvegarde le pseudo et le score dans la
                        #  data base
                        data = {"name" : text, "score" : score}
                        cursor.execute("""INSERT INTO users(name, score) VALUES(:name, :score)""", data)
                        conn.commit()
                        text = ''
                        runhs = False
                        WIN.fill((30, 30, 30))
                        main_menu()

                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                        WIN.fill((30, 30, 30))

                    else:
                        text += event.unicode
                        WIN.fill((30, 30, 30))

            #permet de créer/se connecter à la data base
            conn = sqlite3.connect('Highscoredatabase.db')
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                    name TEXT,
                    score INTEGER
                )
            """)

            if event.type == pygame.QUIT:
                runhs = False
                pygame.quit()

def afficher_highscore():
    '''fonction qui permet d'afficher les 5 premiers highscore'''
    pygame.mixer.pause()
    conn = sqlite3.connect('Highscoredatabase.db')
    cursor = conn.cursor()
    conn.commit()

    #creer la table users si elle n'existe pas (avec un id qui s'autoincremente)
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                    name TEXT,
                    score INTEGER
                )
            """)

    cursor.execute(""" SELECT name, score FROM users ORDER BY score DESC LIMIT 5; """)
    hs = cursor.fetchall()
    hsList = list(hs)
    font = pygame.font.Font(os.path.join("fonts", "font_pixel.ttf"), 30)
    text_surface = font.render('BEST PLAYERS', False, (171, 171, 0))
    WIN.blit(text_surface, (WIDTH/4,250))
    count = 0

    for x in hsList:
        #affiche les noms et scores des joueurs
        count+=1 #compteur qui permet d'afficher à différents hauteur les scores
        a,b = x
        ja = font.render(a, True, (171,0,0))
        jb = font.render(str(b), True, (171,0,0))
        WIN.blit(ja, (WIDTH/4-50,250+count*30))
        WIN.blit(jb, (WIDTH/2+50,250+count*30))
        pygame.display.update()

def button(WIN, position, textbutton, size, colors="white on blue"):
    '''fonction qui permet de creer un bouton en faisant un rectangle entouré de traits'''
    fg, bg = colors.split(" on ")
    font = pygame.font.Font(os.path.join("fonts", "font_pixel.ttf"), size)
    text_render = font.render(textbutton, 1, fg)
    x, y, w , h = text_render.get_rect()
    x, y = position
    pygame.draw.line(WIN, (150, 150, 150), (x, y), (x + w , y), 5)
    pygame.draw.line(WIN, (150, 150, 150), (x, y - 2), (x, y + h), 5)
    pygame.draw.line(WIN, (50, 50, 50), (x, y + h), (x + w , y + h), 5)
    pygame.draw.line(WIN, (50, 50, 50), (x + w , y+h), [x + w , y], 5)
    pygame.draw.rect(WIN, bg, (x, y, w , h))
    return WIN.blit(text_render, (x, y))

def main_menu():
    pygame.mixer.pause()
    #menu principal
    WIN.fill((30, 30, 30))
    run = True
    #affiche les éléments du menu (boutons, highscore et logo)
    b1 = button(WIN, (WIDTH-175, HEIGHT-100), "Quit", 50, "red on yellow")
    b2 = button(WIN, (50, HEIGHT-100), "Play", 50, "white on green")
    WIN.blit(LOGO, (WIDTH/4, 0))
    afficher_highscore()  
    while run:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                #permet de savoir sur quel bouton on clique grace au coordonnée de la souris
                if b1.collidepoint(pygame.mouse.get_pos()):
                    #bouton quit
                    run = False
                elif b2.collidepoint(pygame.mouse.get_pos()):
                    #bouton play
                    main()
  
        pygame.display.update()
    pygame.quit()

main_menu()