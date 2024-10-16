import random

# board dimensions
board_width = 200
board_height = 400
color_list = [color(255,51,52), color(12,150,228), color(30,183,66), color(246,187,0), color(76,0,153), color(255,255,255), color(0,0,0)]
picked = random.choice(color_list)

# calculate the number of rows and columns
cell_height = 20
cell_width = 20
num_rows = board_height // cell_height
num_columns = board_width // cell_width
block_list = []


def setup():
    size(board_width, board_height)
    background(210)
    i = 50
    frameRate(i)
    
# drawing the board grid and displaying all text
def draw():
    # bless you for providing this script
    if frameCount % (max(1, int(8 - game.speed))) == 0 or frameCount == 1:
        background(210)
        draw_grid()
        game.spawn()
        game.update()  # move the current block down
        game.display()  # display all blocks including the current one
    
    textSize(15)            
    fill(0)                
    text("Score: {}".format(score),board_width-100,20)
    
    if game.game_over:
        fill(255, 0, 0)
        text("Game Over", (board_width / 2) - 50, (board_height / 2))

            
# function for drawing the grid according to dimesions of board
def draw_grid():
    stroke(180)
    noFill()
    for x in range(0, board_width, 20):
        for y in range(0, board_height, 20):
            block = Block(x, y, paint=210)
            block.display() 
    
# creating the block class with required attributed
class Block:
    
    def __init__(self, x, y, w=20, h=20, paint=picked):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.paint = paint
        
# display the block
    def display(self):
        fill(self.paint)
        stroke(0)
        strokeWeight(0)  
        rect(self.x, self.y, self.w, self.h)  
        
# creating the game class with all required functionality and features
class Game:
    def __init__(self):
        self.current_block = None
        self.blocks = []
        self.game_over = False
        self.speed = 0
        self.reset_game()
        
        # checking if the column is full, so to avoid spawning in such column
    def column_is_full(self, column_x):
        # count the blocks in the specified column
        blocks_in_column = [block for block in self.blocks if block.x == column_x]
        # a column is full if there's a block for every row
        return len(blocks_in_column) >= num_rows
    
    # spawning blocks into a column
    def spawn(self):
        # check is block is already falling, and if thats true then do not spawn another block
        if self.current_block is None:
            # stopping blocks from being spawned in full columns
            available_columns = [x for x in range(num_columns) if not self.column_is_full(x * cell_width)]
            if available_columns:
                # randomly select from available columns
                column_x = random.choice(available_columns) * cell_width
                self.current_block = Block(column_x, 0, paint=random.choice(color_list))
                self.blocks.append(self.current_block)
                # incrementing speed after every block spawned
                self.speed += 0.25

            else:
                self.game_over = True
                
    # block falling logic, checking under block for board minimum
    def update(self):
        if self.current_block:
            if self.current_block.y + cell_height < board_height and not self.is_block_below(self.current_block):
                self.current_block.y += cell_height
            else:
                self.current_block = None
                self.check_and_remove_stacked()
                
    # block falling logic 2, checking under block for other block
    def is_block_below(self, block):
        for other in self.blocks:
            if other != block and other.x == block.x and other.y == block.y + cell_height:
                return True
        return False

    def display(self):
        # displaying all spawned blocks, even the ones who have stopped moving
        for block in self.blocks:
            block.display()
            
    # deleting stacks of four colors
    def check_and_remove_stacked(self):
        global score
        # here i create a list of all the blocks that are to be destroyed if there is a stack of identical colors, and if there is really 4, i remove all of them from the grid
        to_remove = []
        for block in self.blocks:
            count = 1
            for y_offset in range(cell_height, cell_height*4, cell_height):
                for other in self.blocks:
                    if other != block and other.x == block.x and other.y == block.y + y_offset and other.paint == block.paint:
                        count += 1
                        break
            if count == 4:
                to_remove.append(block)
                for y_offset in range(cell_height, cell_height*4, cell_height):
                    for other in self.blocks:
                        if other != block and other.x == block.x and other.y == block.y + y_offset and other.paint == block.paint:
                            to_remove.append(other)
                    # setting speed of game to 0 once stack is deleted
                    self.speed = 0
                break  # once a matching set is found program stop checking

        # remove the blocks after checking to avoid modifying list during iteration
        for block in to_remove:
            if block in self.blocks:
                self.blocks.remove(block)
                score += 0.25
                
        # checking collisions so to avoid overlapping, if x and y are equal we return false and stop movement
    def is_collision(self, x, y):
        for block in self.blocks[:-1]:  # check all blocks except the currently falling block
            if block.x == x and block.y == y:
                return True
        return False
                
    def move_current_block(self, direction): # movement of the block logic
        if self.current_block:
            new_x = self.current_block.x + (cell_width * direction)
            if 0 <= new_x <= board_width - cell_width and not self.is_collision(new_x, self.current_block.y):
                # check boundaries and collision with other blocks
                self.current_block.x = new_x
                
    def reset_game(self): #function for reseting the game, purely to work with the mouse input
        self.current_block = None
        self.blocks = []  # clear all blocks from grid
        self.game_over = False
        self.speed = 0 

# keybaord input to move block accordingly
def keyPressed():
    if keyCode == RIGHT:
        game.move_current_block(1)  # Move right
    elif keyCode == LEFT:
        game.move_current_block(-1)  # Move left
        
# mouse input response
def mousePressed():
    global score
    score = 0  # reset score
    game.reset_game()  # restart game state by calling function
        

score = 0
        
game = Game()
