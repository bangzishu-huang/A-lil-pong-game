from settings import *
from sprites import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('A Lil Pong Game')
        self.clock = pygame.time.Clock()
        self.running = True

        # some sprites
        self.all_sprites = pygame.sprite.Group()
        self.paddle_sprites = pygame.sprite.Group()
        self.player = Player((self.all_sprites, self.paddle_sprites))
        
        self.ball = Ball(self.all_sprites, self.paddle_sprites)

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000  # miliseconds
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            
            # update part
            self.all_sprites.update(dt)

            # draw part
            self.display_surface.fill(COLORS['background'])
            self.all_sprites.draw(self.display_surface)
            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()