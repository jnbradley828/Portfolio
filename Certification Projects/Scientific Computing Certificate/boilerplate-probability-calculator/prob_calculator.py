import copy
import random


# Consider using the modules imported above.

class Hat:  # initialize a hat with a variable number of colors and numbers, formatted like Hat(blue=3, red=4, etc.) Then create a contents list of each individual ball.
    def __init__(self, **kwargs):
        self.color_counts = kwargs
        self.contents = []
        for color in self.color_counts:
            for i in range(0, self.color_counts[color]):
                self.contents.append(color)
        self.contents_perm = copy.deepcopy(self.contents)

    def draw(self, num_balls):  # define a function that draws a certain number of balls at random from the hat.
        if isinstance(num_balls, int) is False:
            return 'That\'s not an integer, bud.'
        else:
            randDraw = []
            if len(self.contents) < num_balls:
                self.contents = copy.deepcopy(self.contents_perm)
            for i in range(0, num_balls):
                if not self.contents:
                    self.contents = copy.deepcopy(self.contents_perm)
                choice = random.choice(self.contents)
                self.contents.remove(choice)
                randDraw.append(choice)
            return randDraw


def experiment(hat, expected_balls, num_balls_drawn, num_experiments): #define the experiment by running draw over and over and storing the result.
    if isinstance(hat, Hat) is False:
        return 'That\'s not a hat.'
    if isinstance(expected_balls, dict) is False:
        return 'Expected balls needs to be a dictionary.'
    if isinstance(num_balls_drawn, int) is False or isinstance(num_experiments, int) is False:
        return 'Experiments and number of balls should be integers.'

    numTrue = 0
    for i in range(0, num_experiments):
        thisDraw = hat.draw(num_balls_drawn)
        true_balls = {}
        thisResult = True
        for ball in thisDraw:
            true_balls[ball] = true_balls.setdefault(ball, 0) + 1
        for key in expected_balls:
            if key not in true_balls or true_balls[key] < expected_balls[key]:
                thisResult = False
        if thisResult is True:
            numTrue += 1

    prob = numTrue / num_experiments
    return prob