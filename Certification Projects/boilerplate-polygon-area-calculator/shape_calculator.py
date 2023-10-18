class Rectangle:
    def __init__(self, width, height):  # initialize an instance of a rectangle.
        if isinstance(width, int):
            self.width = width
        else:
            return 'Your width is not an integer.'
        if isinstance(height, int):
            self.height = height
        else:
            return 'Your height is not an integer.'

    def set_width(self, width):  # change the width at will.
        if isinstance(width, int):
            self.width = width
            if isinstance(self, Square):
                self.height = width
                self.side = width
        else:
            return 'Your width is not an integer.'

    def set_height(self, height):  # change the height at will.
        if isinstance(height, int):
            self.height = height
            if isinstance(self, Square):
                self.width = height
                self.side = height
        else:
            return 'Your height is not an integer.'

    def get_area(self):  # retrieve the area.
        return (self.width * self.height)

    def get_perimeter(self):  # retrieve the perimeter.
        return (2 * (self.width + self.height))

    def get_diagonal(self):  # retrieve the length of the diagonal.
        return ((self.width ** 2 + self.height ** 2) ** .5)

    def get_picture(self):  # retrieve an image of the rectangle.
        if self.width > 50 or self.height > 50:
            return 'Too big for picture.'
        line = ''
        String = ''
        for i in range(0, self.width):
            line += '*'
        for n in range (0, self.height):
            String += f'{line}\n'
        return String

    def get_amount_inside(self, other_rect): #retrieve the number of times another rectangle can fit inside of this rectangle.
        if isinstance(other_rect, Rectangle) is False:
            return 'That is not a rectangle'
        else:
            widFit = int(self.width / other_rect.width)
            heiFit = int(self.height / other_rect.height)
            numFit = widFit * heiFit
            return numFit

    def __str__(self):
        return f'Rectangle(width={self.width}, height={self.height})'


class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side) #this calls the def __init__ from the parent class (Square) and just inputs side as both width and height.
        self.side = side

    def set_side(self, side): #set side so that it changes side as well as the height/width of the rectangle parent class.
        if isinstance(side, int):
            self.side = side
            self.width = self.side
            self.height = self.side
        else:
            return 'Your side length is not an integer.'

    def __str__(self):
        return f'Square(side={self.side})'