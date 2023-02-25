import turtle
import time
import random
import pickle as pkl

class Game:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.delay = 0.1
        try:
            with open('saved_scores.pkl', 'rb') as fp:
                self.high_score = pkl.load(fp)
        except (FileNotFoundError, EOFError):
            self.high_score = 0

        # window
        self.wn = turtle.Screen()
        self.wn.title("Snake Game")
        self.wn.bgcolor('grey')
        self.wn.setup(width=600, height=600)
        self.wn.tracer(0)

        # head
        self.head = turtle.Turtle()
        self.head.speed(0)
        self.head.shape("square")
        self.head.color("green")
        self.head.penup()
        self.head.goto(0, 0)
        self.head.direction = "stop"

        # food
        self.food = turtle.Turtle()
        self.food.speed(0)
        self.food.shape("square")
        self.food.color("red")
        self.food.penup()
        self.food.goto(0, 100)

        # scoreboards
        self.sc = turtle.Turtle()
        self.sc.speed(0)
        self.sc.shape("square")
        self.sc.color("black")
        self.sc.penup()
        self.sc.hideturtle()
        self.sc.goto(0, 260)
        self.sc.write("score: 0  High score: {}".format(self.high_score), align="center", font=("ds-digital", 24, "normal"))

        self.segments = []

    def go_up(self):
        if self.head.direction != "down":
            self.head.direction = "up"

    def go_down(self):
        if self.head.direction != "up":
            self.head.direction = "down"

    def go_left(self):
        if self.head.direction != "right":
            self.head.direction = "left"

    def go_right(self):
        if self.head.direction != "left":
            self.head.direction = "right"

    def move(self):
        if self.head.direction == "up":
            y = self.head.ycor()
            self.head.sety(y + 20)
        if self.head.direction == "down":
            y = self.head.ycor()
            self.head.sety(y - 20)
        if self.head.direction == "left":
            x = self.head.xcor()
            self.head.setx(x - 20)
        if self.head.direction == "right":
            x = self.head.xcor()
            self.head.setx(x + 20)

    def main_loop(self):
        self.wn.listen()
        self.wn.onkeypress(self.go_up, "w")
        self.wn.onkeypress(self.go_down, "s")
        self.wn.onkeypress(self.go_left, "a")
        self.wn.onkeypress(self.go_right, "d")

        while True:
            while True:
                self.wn.update()

                if self.head.xcor() > 290 or self.head.xcor() < -290 or self.head.ycor() > 290 or self.head.ycor() < -290:
                    time.sleep(1)
                    self.head.goto(0, 0)
                    self.head.direction = "stop"

                    for segment in self.segments:
                        segment.goto(1000, 1000)
                    self.segments.clear()
                    self.score = 0
                    self.delay = 0.1
                    self.sc.clear()
                    self.sc.write("score: {}  High score: {}".format(self.score, self.high_score), align="center",
                             font=("ds-digital", 24, "normal"))

                    with open('saved_scores.pkl', 'wb') as fp:
                        pkl.dump(self.high_score, fp)

                if self.head.distance(self.food) < 20:
                    x = random.randint(-290, 290)
                    y = random.randint(-290, 290)
                    self.food.goto(x, y)

                    # add a new segment to the head
                    new_segment = turtle.Turtle()
                    new_segment.speed(0)
                    new_segment.shape("square")
                    new_segment.color("green")
                    new_segment.penup()
                    self.segments.append(new_segment)

                    # shorten the delay
                    self.delay -= 0.001
                    # increase the score
                    self.score += 10

                    if self.score > self.high_score:
                        self.high_score = self.score
                    self.sc.clear()
                    self.sc.write("score: {}  High score: {}".format(self.score, self.high_score), align="center",
                             font=("ds-digital", 24, "normal"))

                    # move the segments in reverse order
                for index in range(len(self.segments) - 1, 0, -1):
                    x = self.segments[index - 1].xcor()
                    y = self.segments[index - 1].ycor()
                    self.segments[index].goto(x, y)
                # move segment 0 to head
                if len(self.segments) > 0:
                    x = self.head.xcor()
                    y = self.head.ycor()
                    self.segments[0].goto(x, y)

                self.move()

                # check for collision with body
                for segment in self.segments:
                    if segment.distance(self.head) < 20:
                        time.sleep(1)
                        self.head.goto(0, 0)
                        self.head.direction = "stop"

                        # hide segments
                        for segment in self.segments:
                            segment.goto(1000, 1000)
                        self.segments.clear()
                        self.score = 0
                        self.delay = 0.1

                        # update the score
                        self.sc.clear()
                        self.sc.write("score: {}  High score: {}".format(self.score, self.high_score), align="center",
                                 font=("ds-digital", 24, "normal"))

                        with open('saved_scores.pkl', 'wb') as fp:
                            pkl.dump(highscore, fp)  # write the pickle file

                time.sleep(self.delay)
            self.wn.mainloop()


def main():
    game = Game()
    game.main_loop()


if __name__ == "__main__":
    main()
