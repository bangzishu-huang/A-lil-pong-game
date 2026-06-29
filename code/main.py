# /// script
# dependencies = [
#     "pygame-ce",
# ]
# /// 

from settings import *
from sprites import *
from groups import AllSprites
import json
import asyncio
import os

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('A Lil Pong Game')
        self.clock = pygame.time.Clock()
        self.running = True

        self.state = 'menu'

        # some sprites
        self.all_sprites = AllSprites()
        self.paddle_sprites = pygame.sprite.Group()
        self.player = Player((self.all_sprites, self.paddle_sprites))
        self.ball = Ball(self.all_sprites, self.paddle_sprites, self.update_score)
        Opp((self.all_sprites, self.paddle_sprites), self.ball)

        # score stuff
        
        try:
            with open(join('data', 'score.txt')) as score_file:
                self.score = json.load(score_file)
        except:
            self.score = {'player':0, 'opp': 0}  # for original start
        # self.score = {'player': 0, 'opp': 0}
        self.font = pygame.font.Font(None, 180)

        # startup menu
        self.title_font = pygame.font.Font(None, 90)
        self.button_font = pygame.font.Font(None, 50)
        button_width, button_height = 360, 90
        center_x = WINDOW_WIDTH / 2
        self.continue_rect = pygame.FRect(0, 0, button_width, button_height)
        self.continue_rect.center = (center_x, WINDOW_HEIGHT / 2)
        self.new_game_rect = pygame.FRect(0, 0, button_width, button_height)
        self.new_game_rect.center = (center_x, WINDOW_HEIGHT / 2 + 130)

    def save_score(self):
        os.makedirs('data', exist_ok= True)
        with open(join('data', 'score.txt'), 'w') as score_file:
            json.dump(self.score, score_file)


    def display_score(self):

        # player score
        player_surface = self.font.render(str(self.score['player']), True, COLORS['bg detail'])
        player_rect = player_surface.get_frect(center = (WINDOW_WIDTH / 2 + 100, WINDOW_HEIGHT / 2))
        self.display_surface.blit(player_surface, player_rect)

        # opponent score
        opp_surface = self.font.render(str(self.score['opp']), True, COLORS['bg detail'])
        opp_rect = opp_surface.get_frect(center = (WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2))
        self.display_surface.blit(opp_surface, opp_rect)

        # score line
        pygame.draw.line(self.display_surface, COLORS['bg detail'], (WINDOW_WIDTH / 2, 0), (WINDOW_WIDTH / 2, WINDOW_HEIGHT), 14)

    def update_score(self, side):
        self.score['player' if side == 'player' else 'opp'] += 1

    def draw_button(self, rect, text, hovered):
        base_color = COLORS['paddle'] if hovered else COLORS['bg detail']
        pygame.draw.rect(self.display_surface, base_color, rect, 0 ,10)
        pygame.draw.rect(self.display_surface, COLORS['paddle shadow'], rect, 4, 10)

        text_surface = self.button_font.render(text, True, COLORS['button text'])
        text_rect = text_surface.get_frect(center = rect.center)
        self.display_surface.blit(text_surface, text_rect)

    def display_menu(self):
        self.display_surface.fill(COLORS['background'])

        title_surface = self.title_font.render('A Lil Pong Game :)', True, COLORS['title'])
        title_rect = title_surface.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 180))

        self.display_surface.blit(title_surface, title_rect)

        mouse_pos = pygame.mouse.get_pos()

        # Continue Button
        self.draw_button(self.continue_rect, 'Continue', self.continue_rect.collidepoint(mouse_pos))

        # New Game Button
        self.draw_button(self.new_game_rect, 'New Game', self.new_game_rect.collidepoint(mouse_pos))

    def handle_menu_click(self, mouse_pos):
        if self.continue_rect.collidepoint(mouse_pos):
            self.state = 'game'
        elif self.new_game_rect.collidepoint(mouse_pos):
            self.score = {'player': 0, "opp": 0}
            self.state = 'game'


    async def run(self):
        while self.running:
            dt = self.clock.tick() / 1000  # miliseconds
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.save_score()

                if self.state == 'menu':
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.handle_menu_click(event.pos)
                
            if self.state == 'menu':
                self.display_menu()
            else:
                # update part
                self.all_sprites.update(dt)

                # draw part
                self.display_surface.fill(COLORS['background'])
                self.display_score()
                self.all_sprites.draw()
            
            pygame.display.update()

            await asyncio.sleep(0)

        pygame.quit()

async def main():
    game = Game()
    await game.run()

asyncio.run(main()) 