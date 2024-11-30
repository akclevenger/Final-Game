import pygame, simpleGE, random

class Dude(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("dude.png")
        self.setAngle(0)
        self.speed = 0

    def process(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.imageAngle += 5
        if self.isKeyPressed(pygame.K_RIGHT):
            self.imageAngle -= 5
        if self.isKeyPressed(pygame.K_UP):
            self.addForce(0.2, self.imageAngle)
        if self.isKeyPressed(pygame.K_SPACE):
            self.scene.bullet.fire()

class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Score: 0"
        self.center = (100, 30)

class LblTime(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time Left: 30"
        self.center = (500, 30)

class Bullet(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("bullet.gif")
        self.setSize(5, 5)
        self.setBoundAction(self.HIDE)
        self.reset()

    def fire(self):
        self.position = (self.scene.dude.x, self.scene.dude.y)
        self.speed = 12
        self.setAngle(self.scene.dude.imageAngle)

    def reset(self):
        self.position = (-100, -100)
        self.speed = 0

class Rock(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("rock.gif")
        self.reset()

    def process(self):
        self.imageAngle += self.rotSpeed

    def reset(self):
        x = random.randint(0, self.screen.get_width())
        y = random.randint(0, self.screen.get_height())
        self.position = (x, y)

        scale = random.randint(10, 40)
        self.setImage("rock.gif")
        self.setSize(scale, scale)

        self.speed = random.randint(0, 6)
        self.setAngle(random.randint(0, 360))
        self.rotSpeed = random.randint(-5, 5)

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.score = 0  
        
        self.dude = Dude(self)
        self.bullet = Bullet(self)
        self.rocks = [Rock(self) for i in range(10)]

        self.lblScore = LblScore()
        self.lblTime = LblTime()

        self.sprites = [self.bullet, self.dude] + self.rocks + [self.lblScore, self.lblTime]

        self.setCaption("Duderoids!")
        self.background = pygame.image.load("Galaxy.jpg")
        self.background = pygame.transform.scale(self.background, self.screen.get_size())
        self.collision_sound = pygame.mixer.Sound("explosion.mp3")

        self.time_left = 30  
        self.start_ticks = pygame.time.get_ticks()  



    def process(self):
        self.screen.blit(self.background, (0, 0))

        elapsed_time = (pygame.time.get_ticks() - self.start_ticks) // 1000
        self.time_left = max(30 - elapsed_time, 0)
        self.lblTime.text = f"Time Left: {self.time_left}"

        if self.time_left == 0:
            self.show_final_score()  

        for rock in self.rocks:
            if self.dude.collidesWith(rock):
                self.collision_sound.play()
                rock.reset()
                self.score += 1
                #print(f"Score updated: {self.score}")
                self.lblScore.text = f"Score: {self.score}"

                
            if self.bullet.collidesWith(rock):
                self.collision_sound.play()
                rock.reset()
                self.bullet.reset()

        #self.lblScore.text = f"Score: {self.score}"

    def show_final_score(self):
        self.stop()
        final_score_scene = FinalScore(self.score)
        final_score_scene.start()  

class FinalScore(simpleGE.Scene):
    def __init__(self, score):
        super().__init__()
        self.setImage("Galaxy.jpg")

        self.final_score_label = simpleGE.Label()
        self.final_score_label.text = f"Final Score: {score}"
        self.final_score_label.center = (320, 240)
        self.final_score_label.size = (300, 45)

        self.btnRestart = simpleGE.Button()
        self.btnRestart.text = "Restart (up)"
        self.btnRestart.center = (100, 400)

        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit (down)"
        self.btnQuit.center = (550, 400)

        self.sprites = [self.final_score_label, self.btnQuit, self.btnRestart]

    def process(self):
        if self.btnQuit.clicked:
            self.stop()  
        if self.btnRestart.clicked:
            self.start_new_game()  

        if self.isKeyPressed(pygame.K_UP):
            self.start_new_game()  
        if self.isKeyPressed(pygame.K_DOWN):
            self.stop()  

    def start_new_game(self):
        game = Game()
        game.start()  

class Instructions(simpleGE.Scene):
    def __init__(self, score):
        super().__init__()
        self.setImage("Galaxy.jpg")

        self.response = "Play"

        self.instructions = simpleGE.MultiLabel()
        self.instructions.textLines = [
            "You are Fred the destroyer!",
            "Move with the left, right, and up arrow keys",
            "Use the space bar to shoot at the rocks",
            "Destroy as many space rocks as you can",
            "before they hit earth and the timer runs out!",
            "",
        ]

        self.instructions.center = (320, 240)
        self.instructions.size = (500, 250)

        self.btnPlay = simpleGE.Button()
        self.btnPlay.text = "Play (up)"
        self.btnPlay.center = (100, 400)

        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit (down)"
        self.btnQuit.center = (550, 400)

        self.sprites = [self.instructions, self.btnQuit, self.btnPlay]

    def process(self):
        if self.btnQuit.clicked:
            self.response = "Quit"
            self.stop()
        if self.btnPlay.clicked:
            self.response = "Play"
            self.stop()

        if self.isKeyPressed(pygame.K_UP):
            self.response = "Play"
            self.stop()
        if self.isKeyPressed(pygame.K_DOWN):
            self.response = "Quit"
            self.stop()

def main():
    keepGoing = True
    score = 0
    while keepGoing:
        instructions = Instructions(score)
        instructions.start()

        if instructions.response == "Play":
            game = Game()
            game.start()
            score = game.score
        else:
            keepGoing = False

if __name__ == "__main__":
    main()


