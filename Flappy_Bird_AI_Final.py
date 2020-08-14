
import pygame
import neat
import os
import random
import visualize
import time
import pickle
pygame.font.init() 

WIN_HEIGHT = 540
WIN_WIDTH = 960

floor = 430
drawlines = False
STAT_FONT = pygame.font.SysFont("comicsans", 50)
END_FONT = pygame.font.SysFont("comicsans", 70)

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird in Space")

#BIRD_IMGS = [(pygame.image.load(os.path.join("imgs","ghost2.png"))),(pygame.image.load(os.path.join("imgs","ghost2.png"))),(pygame.image.load(os.path.join("imgs","ghost2.png")))]
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird" + str(x) + ".png"))) for x in range(1,4)]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")).convert_alpha())
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")).convert_alpha())
BG_IMG = pygame.image.load(os.path.join("imgs","bg.jpeg"))

generation = 0

class Bird:
    MAX_ROT = 25
    ROT_VEL = 20
    imgs = BIRD_IMGS
    ANIMATION_TIME = 5

    def __init__(self, a, b):

        self.a = a
        self.b = b
        self.vel = 0
        self.img_count = 0
        self.tick_count = 0
        self.tilt = 0 
        self.height = self.b
        self.img = self.imgs[0]

    def jump(self):

        self.vel = -10.5
        self.tick_count = 0
        self.height = self.b

    def move(self):

        self.tick_count += 1
        d = self.vel*(self.tick_count) + 0.5*(3)*(self.tick_count)**2 

        if d >= 16:
            d = (d/abs(d)) * 16

        if d < 0:
            d -= 2

        self.b = self.b + d

        if d < 0 or self.b < self.height + 50:  
            if self.tilt < self.MAX_ROT:
                self.tilt = self.MAX_ROT
        else: 
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):

        self.img_count += 1

        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.imgs[0]
        elif self.img_count <= self.ANIMATION_TIME*2:
            self.img = self.imgs[1]
        elif self.img_count <= self.ANIMATION_TIME*3:
            self.img = self.imgs[2]
        elif self.img_count <= self.ANIMATION_TIME*4:
            self.img = self.imgs[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.imgs[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.imgs[1]
            self.img_count = self.ANIMATION_TIME*2


        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.a,self.b)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe():

    VEL = 5
    GAP = 200

    def __init__(self, a):

        self.a = a
        self.height = 0

        self.top = 0
        self.bottom = 0

        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(95, 300)
        self.bottom = self.height + self.GAP
        self.top = self.height - self.PIPE_TOP.get_height()

    def move(self):
        self.a -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.a, self.top))
        win.blit(self.PIPE_BOTTOM, (self.a, self.bottom))


    def collide(self, bird, win):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.a - bird.a, self.top - round(bird.b))
        bottom_offset = (self.a - bird.a, self.bottom - round(bird.b))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)

        if t_point or b_point:
            return True

        return False

class Base:

    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, b):

        self.b = b
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):

        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.b))
        win.blit(self.IMG, (self.x2, self.b))


def draw_window(win, birds, pipes, base, score, generation, pipe_index):

    if generation == 0:
        generation = 1
    win.blit(BG_IMG, (0,0))

    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)
    for bird in birds:
        if drawlines:
            try:
                pygame.draw.line(win, (255,0,0), (bird.a+bird.img.get_width()/2, bird.b + bird.img.get_height()/2), (pipes[pipe_index].x + pipes[pipe_index].PIPE_TOP.get_width()/2, pipes[pipe_index].height), 5)
                pygame.draw.line(win, (255,0,0), (bird.a+bird.img.get_width()/2, bird.b + bird.img.get_height()/2), (pipes[pipe_index].x + pipes[pipe_index].PIPE_BOTTOM.get_width()/2, pipes[pipe_index].bottom), 5)
            except:
                pass

        bird.draw(win)

    score_label = STAT_FONT.render("Score: " + str(score),1,(255,255,255))
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))

    score_label = STAT_FONT.render("Gens: " + str(generation-1),1,(255,255,255))
    win.blit(score_label, (10, 10))

    score_label = STAT_FONT.render("Alive: " + str(len(birds)),1,(255,255,255))
    win.blit(score_label, (10, 50))

    pygame.display.update()


def main(genomes, config):

    global WIN, generation
    win = WIN
    generation += 1

    birds = []
    nets = []
    ge = []
    for _, g in genomes:
        g.fitness = 0  
        net = neat.nn.FeedForwardNetwork.create(g, config)
        birds.append(Bird(300,300))
        nets.append(net)
        ge.append(g)

    pipes = [Pipe(700)]
    base = Base(floor)
    score = 0

    clock = pygame.time.Clock()

    run = True
    while run and len(birds) > 0:
        clock.tick(30)

       
        for event in pygame.event.get():
           if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        pipe_index = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].a > pipes[0].a + pipes[0].PIPE_TOP.get_width():  
                pipe_index = 1

        for a, bird in enumerate(birds):  
            ge[a].fitness += 0.1
            bird.move()

            output = nets[birds.index(bird)].activate((bird.b, abs(bird.b - pipes[pipe_index].height), abs(bird.b - pipes[pipe_index].bottom)))

            if output[0] > 0.5:
                bird.jump()

        base.move()

        
        add_pipe = False
        rem = []
        for pipe in pipes:
            pipe.move()

            for bird in birds:
                if pipe.collide(bird, win):
                    ge[birds.index(bird)].fitness -= 1
                    ge.pop(birds.index(bird))
                    nets.pop(birds.index(bird))
                    birds.pop(birds.index(bird))

            if pipe.a + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.a < bird.a:
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(WIN_WIDTH))

        for r in rem:
            pipes.remove(r)

        for bird in birds:
            if bird.b + bird.img.get_height() - 10 >= floor or bird.b < -50:
                ge.pop(birds.index(bird))
                nets.pop(birds.index(bird))
                birds.pop(birds.index(bird))

        draw_window(WIN, birds, pipes, base, score, generation, pipe_index)



def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 50)

    print('\nBest g:\n{!s}'.format(winner))


if __name__ == '__main__':

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
