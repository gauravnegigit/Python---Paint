import pygame
pygame.font.init()

#screen variables
WIDTH , HEIGHT = 600,800
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("MS PAINT USING PYGAME !")
FPS = 120
ROWS = COLS =50
PIXEL_SIZE = WIDTH //ROWS
DRAW_GRID = False
TOOLBAR_HEIGHT = HEIGHT - WIDTH
BUTTON_WIDTH = 50

#color variables
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BG_COLOR = WHITE

#font variables
FONT = pygame.font.SysFont("ARIAL BLACK",10)

#creating class for buttons
class Button:
	def __init__(self, x, y , width , height , color , text = None , text_color = BLACK):
		self.x = x 
		self.y = y 
		self.width = width
		self.height = height
		self.color = color 
		self.text = text
		self.text_color = text_color
	def draw(self, win):
		pygame.draw.rect(win , self.color , (self.x , self.y , self.width , self.height))
		pygame.draw.rect(win , BLACK , (self.x , self.y , self.width , self.height), 5)
		if self.text:
			text = FONT.render(self.text , 1 , self.text_color)
			win.blit(text , (self.x + self.width//2 - text.get_width()//2 , self.y + self.height//2 - text.get_height()//2))
	def clicked(self, pos):
		x, y = pos 
		if self.x < x < self.x + self.width and self.y <y < self.y +self.height:
			return True
		return False

# method for initializing the grid with deault white color
def init_grid(rows,cols,color):
	grid = []
	for i in range(rows):
		grid.append([])
		for j in range(cols):
			grid[i].append(color)
	return grid

def get_rows_columns(pos):
	# method to get the row and column of the grid from the position of the mouse click

	x , y = pos 
	row = y // PIXEL_SIZE
	col = x //PIXEL_SIZE
	if row >= ROWS:
		raise IndexError
	return row , col

def draw_grid(win,grid):
	for i,row in enumerate(grid):
		for j , col in enumerate(row):
			pygame.draw.rect(win , col , (j*PIXEL_SIZE , i*PIXEL_SIZE , PIXEL_SIZE , PIXEL_SIZE))
	if DRAW_GRID :
		for i in range(ROWS +1):
			pygame.draw.line(win ,BLACK , (0 , i*PIXEL_SIZE) , (WIDTH , i*PIXEL_SIZE))
			pygame.draw.line(win , BLACK , (i*PIXEL_SIZE , 0 ) , (i* PIXEL_SIZE , WIDTH))

def draw(win , grid , buttons):
	win.fill(BG_COLOR)
	draw_grid(win , grid)
	for button in buttons :
		button.draw(win)

	pygame.display.update()

def main():
	run = True
	clock = pygame.time.Clock()
	grid = init_grid(ROWS, COLS , BG_COLOR)
	drawing_color = BLACK

	button_y = HEIGHT - TOOLBAR_HEIGHT/2 - BUTTON_WIDTH/2
	buttons = [
		Button(10 , button_y , BUTTON_WIDTH , BUTTON_WIDTH , BLACK),
		Button(70 , button_y , BUTTON_WIDTH , BUTTON_WIDTH , RED),
		Button(130 , button_y , BUTTON_WIDTH , BUTTON_WIDTH , GREEN),
		Button(190 , button_y , BUTTON_WIDTH , BUTTON_WIDTH , BLUE),
		Button(250 , button_y , BUTTON_WIDTH , BUTTON_WIDTH , WHITE , "ERASE" , BLACK),
		Button(310 , button_y , BUTTON_WIDTH , BUTTON_WIDTH , WHITE , "CLEAR" , BLACK),
	]

	while run :
		clock.tick(FPS)
		draw(WIN , grid , buttons)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				break

			#for left mouse click
			if pygame.mouse.get_pressed()[0]:
				pos = pygame.mouse.get_pos()
				try :
					row, col = get_rows_columns (pos)
					grid[row][col] = drawing_color
					
				except IndexError:
					for button in buttons :
						if button.clicked(pos):
							drawing_color = button.color
							if button.text == 'CLEAR':
								grid = init_grid(ROWS, COLS , BG_COLOR)
								drawing_color = BLACK
							break

	pygame.quit()

if __name__ == '__main__':
	main()