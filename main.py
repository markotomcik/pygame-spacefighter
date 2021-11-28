import pygame

MOVE_MAP = {pygame.K_LEFT: pygame.Vector2(-1, 0),
            pygame.K_RIGHT: pygame.Vector2(1, 0),
            pygame.K_UP: pygame.Vector2(0, -1),
            pygame.K_DOWN: pygame.Vector2(0, 1),
            pygame.K_a: pygame.Vector2(-1, 0),
            pygame.K_d: pygame.Vector2(1, 0),
            pygame.K_w: pygame.Vector2(0, -1),
            pygame.K_s: pygame.Vector2(0, 1)}

SCALE = 3

class Enemy:
  def __init__(self, pos, game):
    self.pos = pos
    self.game = game
    self.speed = pygame.Vector2(0, 1)
    self.speed.rotate_ip(90)
    self.image = pygame.image.load("assets/images/enemy.png")
    self.image = pygame.transform.scale(self.image, (19 * SCALE, 18 * SCALE))
    self.rect = self.image.get_rect()
    self.rect.center = self.pos

  def update(self):
    self.pos += self.speed
    self.rect.center = self.pos
    if self.rect.left < 0 or self.rect.right > self.game.screen.get_width():
      self.speed.x *= -1
    if self.rect.top < 0 or self.rect.bottom > self.game.screen.get_height():
      self.speed.y *= -1

  def draw(self, screen):
    screen.blit(self.image, self.pos)

class Player:
  def __init__(self, x, y):
    self.position = pygame.Vector2(x, y)
    self.speed = 2
    self.image = pygame.image.load("assets/images/player.png")
    self.image = pygame.transform.scale(self.image, (15 * SCALE, 18 * SCALE))
    self.bullets = []

  def move(self):
    # determine movement vector
    pressed = pygame.key.get_pressed()
    move_vector = pygame.Vector2(0, 0)
    for m in (MOVE_MAP[key] for key in MOVE_MAP if pressed[key]):
      move_vector += m

    # normalize movement vector if necessary
    if move_vector.length() > 0:
      move_vector.normalize_ip()

    # apply speed to movement vector
    move_vector *= self.speed

    # update position of player
    self.position += move_vector

  def draw(self, screen):
    screen.blit(self.image, [int(x) for x in self.position])
    for bullet in self.bullets:
      bullet.draw(screen)

  def shoot(self):
    self.bullets.append(Bullet(self.position.x + self.image.get_width() / 2, self.position.y))
  
  def update(self):
    for bullet in self.bullets:
      bullet.update()

  def check_collision(self, enemy):
    for bullet in self.bullets:
      if bullet.rect.colliderect(enemy.rect):
        self.bullets.remove(bullet)
        return True

class Bullet:
  def __init__(self, x, y):
    self.position = pygame.Vector2(x, y)
    self.speed = pygame.Vector2(0, -10)
    self.image = pygame.image.load("assets/images/bullet.png")
    self.image = pygame.transform.scale(self.image, (1 * SCALE, 3 * SCALE))
    self.rect = self.image.get_rect()
    self.rect.center = self.position

  def update(self):
    self.position += self.speed
    self.rect.center = self.position

  def draw(self, screen):
    screen.blit(self.image, [int(x) for x in self.position])

class Game:
  def __init__(self):
    self.screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Game')
    self.clock = pygame.time.Clock()
    self.running = True
    self.player = Player(400, 300)
    self.enemy = Enemy((100, 100), self)
    self.start()

  def start(self):
    while self.running:
      self.events()
      self.update()
      self.draw()

  def events(self):
    global speed, pos
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          self.player.shoot()

  def update(self):
    self.player.move()
    self.player.update()
    if self.enemy is not None:
      self.check_collision()
    if self.enemy is not None:
      self.enemy.update()

  def check_collision(self):
    if self.player.check_collision(self.enemy):
      self.enemy = None

  def draw(self):
    self.screen.fill((47, 19, 59))
    self.player.draw(self.screen)
    if self.enemy is not None:
      self.enemy.draw(self.screen)
    pygame.display.flip()
    self.clock.tick(60)

def main():
  game = Game()

if __name__ == '__main__':
  main()
