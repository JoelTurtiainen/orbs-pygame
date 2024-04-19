import pygame
import math
from random import randint, choice
print("\033c")

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.FPS = 300
        self.kello = pygame.time.Clock()
        self.screen = pygame.display.set_mode((640, 480))
        self.load_colors()
        self.font = pygame.font.SysFont('Cascadia Code', 24)
        pygame.display.set_caption("Orb Game")
        self.running = False
        self.score = 0

    def load_colors(self):
        self.colors = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
            'yellow': (255, 255, 0)
        }

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.running = True
                    return
                
                if not self.running:
                    return
                
                if event.key == pygame.K_SPACE:
                    self.player_attack = True
                    self.player_direction = -self.player_direction
                if event.key == pygame.K_UP:
                    self.player_size += 5
                if event.key == pygame.K_DOWN:
                    self.player_size -= 5

    def new_game(self):
        self.score = 0
        self.current_colors = []
        self.orb_dict = {}
        self.orb_anim = {}
        self.player_attack = False
        self.player_angle = 0
        self.player_direction = 1
        self.player_size = 20
        self.player_color = None

    def update_player(self):
        self.player_speed = 2 + self.score/10
        if self.player_color not in self.current_colors:
            if self.current_colors:
                self.player_color = choice(self.current_colors)
            else:
                self.player_color = None
            
        self.player_angle = self.player_angle % (math.pi*2)

        self.player_angle += (self.player_speed * self.dt) * self.player_direction
        
        angle1 = (self.player_angle - math.radians(self.player_size)) % (math.pi*2)
        angle2 = (self.player_angle + math.radians(self.player_size)) % (math.pi*2)
         
        x1 = 320 + math.cos(angle1) * 200
        y1 = 240 + math.sin(angle1) * 200
        x2 = 320 + math.cos(angle2) * 200
        y2 = 240 + math.sin(angle2) * 200
        
        
        self.player_pos1 = [x1, y1]
        self.player_pos2 = [x2, y2]

        if self.player_attack:
            angle1 = math.degrees(angle1)
            angle2 = math.degrees(angle2)
            
            print(angle1, angle2)
            if angle1 < angle2:
                hits = [orb for orb in self.orb_dict if angle1 <= orb <= angle2]
            else:
                hits = [orb for orb in self.orb_dict if orb >= angle1 or orb <= angle2]
            
            if hits:
                for hit in hits:
                    print(hit, self.orb_dict[hit]['color'], self.orb_dict[hit]['pos'])
                    if self.orb_dict[hit]['color'] == self.player_color:
                        self.score += 1
                        self.orb_anim[hit] = self.orb_dict[hit]
                        self.orb_dict.pop(hit)
                        print(self.orb_anim)

                    else:
                        self.running = False
        
        self.player_attack = False

    def orbs(self):
        # Spawning
        if len(self.orb_dict) < 4:
            radius = 200
            varatut = self.orb_dict.keys()
            vapaat = []
            for i in range(0, 360, 30):
                if i in varatut:
                    continue
                vapaat.append(i)

            angle = choice(vapaat)
            color = choice(list(self.colors))
            
            x = 320 + math.cos(math.radians(angle)) * radius
            y = 240 + math.sin(math.radians(angle)) * radius
            
            self.orb_dict[angle] = {'color': color, 'pos': [math.trunc(x),math.trunc(y)]}
            self.current_colors = [self.orb_dict[o]['color'] for o in self.orb_dict]
            
        for_deletion = []
        for orb in self.orb_anim:
            if self.orb_anim[orb]['pos'][0] > 320:
                self.orb_anim[orb]['pos'][0] -= 1
            if self.orb_anim[orb]['pos'][0] < 320:
                self.orb_anim[orb]['pos'][0] += 1
            if self.orb_anim[orb]['pos'][1] > 240:
                self.orb_anim[orb]['pos'][1] -= 1
            if self.orb_anim[orb]['pos'][1] < 240:
                self.orb_anim[orb]['pos'][1] += 1
                
            if self.orb_anim[orb]['pos'] == [320, 240]:
                for_deletion.append(orb)
                
        for i in for_deletion:
            self.orb_anim.pop(i)
            
    def draw(self):
        color = self.colors
        self.screen.fill((95, 95, 95))
        
        # Text
        teksti = self.font.render(f"Pisteet: {self.score}", True, color['white'], color['black'])
        self.screen.blit(teksti, (640-teksti.get_width(), 0))
        
        # Player
        if self.player_color != None:
            pygame.draw.circle(self.screen, self.player_color, (320, 240), 20, 0)
            
        pygame.draw.circle(self.screen, color['white'], (320, 240), 200, 1)
        pygame.draw.line(self.screen, color['white'], (320, 240), self.player_pos1, 2)
        pygame.draw.line(self.screen, color['white'], (320, 240), self.player_pos2, 2)

        # Orbs
        for orb in self.orb_dict:
            orb = self.orb_dict[orb]
            pygame.draw.circle(self.screen, orb['color'], orb['pos'], 10)
        
        # Captured orbs
        for orb in self.orb_anim:
            orb = self.orb_anim[orb]
            pygame.draw.circle(self.screen, orb['color'], orb['pos'], 10)

        pygame.display.flip()


    def update(self):
        self.update_player()
        self.orbs()
    
    def menu(self):
        color = self.colors
        font_small = pygame.font.SysFont('Cascadia Code', 14)

        if self.score:
            text1_value = f"Score: {self.score}"
        else:
            text1_value = "Orb Game"

        while not self.running:
            self.event()
            self.screen.fill((70, 70, 70))

            text1 = self.font.render(text1_value, True, color['white'], color['black'])
            text2 = font_small.render(f"Spacebar to interact, Enter to start", True, color['white'])
            self.screen.blit(text1, (320-text1.get_width()/2, 240-text1.get_height()/2))
            self.screen.blit(text2, (320-text2.get_width()/2, 280-text2.get_height()/2))
            pygame.display.flip()


    def run(self):
        while True:
            self.menu()
            self.new_game()
            while self.running:
                self.dt = self.kello.tick(self.FPS)/1000
                self.event()
                self.update()
                self.draw()
if __name__ == "__main__":
    game = Game()
    game.run()