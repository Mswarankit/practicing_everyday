import string
import random
from fpdf import FPDF

word_list = ["Aids", "Fund", "Knowledge", "Literacy", "Read", "Test", "Book", "Future", "Lunch", "Refine", "Train", "Class", "Goals", "Language", "Math", "School"]
word_list = [word.upper() for word in word_list]
title = "Education"

width = 13
height = 13

grid = [[random.choice(string.ascii_uppercase) for _ in range(width)] for _ in range(height)]

word_list = list(set(word_list))
already_taken = []

def put_word(word, grid, already_taken):
    word = random.choice([word, word[::-1]])  
    directions = [[1, 0], [0, 1], [1, 1], [-1, -1], [1, -1], [-1, 1]]  
    d = random.choice(directions)
    
    # Determine the maximum starting positions based on the chosen direction
    xsize = len(grid[0]) if d[0] == 0 else len(grid[0]) - len(word)
    ysize = len(grid) if d[1] == 0 else len(grid) - len(word)
    
    # Adjust for negative directions to ensure starting positions are within bounds
    if d[0] == -1:
        x = random.randrange(len(word) - 1, len(grid[0]))
    else:
        x = random.randrange(0, xsize)
    
    if d[1] == -1:
        y = random.randrange(len(word) - 1, len(grid))
    else:
        y = random.randrange(0, ysize)
    
    # Check if any cell in the word's path is already taken
    for i in range(len(word)):
        y_pos = y + d[1] * i   # Calculate current y-coordinate in the word's path
        x_pos = x + d[0] * i   # Calculate current x-coordinate in the word's path
        if (y_pos, x_pos) in already_taken or not (0 <= y_pos < len(grid) and 0 <= x_pos < len(grid[0])):
            return False       # Return False if any cell in the path is already taken or out of bounds
    
    # Place the word in the grid
    for i in range(len(word)):
        y_pos = y + d[1] * i   
        x_pos = x + d[0] * i  
        already_taken.append((y_pos, x_pos))  
        grid[y_pos][x_pos] = word[i]      
    
    # print(word, "inserted at", [x, y], "direction:", d)  # Print success message with insertion coordinates and direction
    return True
    

for word in word_list:
    placed = False
    attempts = 0
    while not placed and attempts < 100:
        placed = put_word(word, grid, already_taken)
        attempts += 1
        if not placed:
            pass
# print(" ")
# print("\n".join(map(lambda row: "  ".join(row), grid)))

def solve_puzzle(word_list, grid):
    directions = [[1, 0], [0, 1], [1, 1], [-1, 0], [0, -1], [-1, -1], [1, -1], [-1, 1]]
    height, width = len(grid), len(grid[0])
    found_words = []

    # Check each word in all directions
    for word in word_list:
        word = word.upper()
        word_found = False
        for r in range(height):
            for c in range(width):
                for d in directions:
                    dr, dc = d
                    if 0 <= r + (len(word) - 1) * dr < height and 0 <= c + (len(word) - 1) * dc < width:
                        match = True
                        for i in range(len(word)):
                            if grid[r + i * dr][c + i * dc] != word[i]:
                                match = False
                                break
                        if match:
                            found_words.append((word, r, c, dr, dc))
                            word_found = True
                            break
                if word_found:
                    break
            if word_found:
                break

    return found_words

found_words = solve_puzzle(word_list, grid)




# Create PDF with the puzzle and solution
pdf = FPDF(orientation='P', unit='mm', format='A4')
pdf.add_page()
gridx = 200
gridy = 8

# Set style and size of font
pdf.set_font("Arial", size=25)
title = title.upper()
pdf.cell(gridx, 10, txt=title, ln=1, align='C')

pdf.set_font("Courier", size=12)
pdf.cell(gridx, gridy, txt="", ln=1)

# Set the position of the top-left corner of the grid
start_x = 10
start_y = 50
pdf.set_xy(start_x, start_y)

# Create a cell for the puzzle grid
cell_size = 10  # Size of each cell in the grid
for row in grid:
    for char in row:
        pdf.cell(cell_size, cell_size, txt=char, border=1, ln=0, align='C')
    pdf.ln(cell_size)

pdf.set_font("Courier", size=12)
pdf.cell(gridx, gridy, txt="", ln=1)
hints_per_row = 5
split_lists = [word_list[x:x + hints_per_row] for x in range(0, len(word_list), hints_per_row)]
for i in split_lists:
    wordx = ", ".join(i)
    pdf.cell(gridx, 10, txt=wordx, ln=1, align='C')

pdf.add_page()
pdf.set_font("Arial", size=25)
pdf.cell(gridx, 10, txt="Solution".upper(), ln=1, align='C')

# Print solved puzzle grid with highlights
pdf.set_font("Courier", size=12)
pdf.cell(gridx, gridy, txt="", ln=1)

# Set the position of the top-left corner of the grid for the solution
pdf.set_xy(start_x, start_y)

# Draw the grid
for r, row in enumerate(grid):
    for c, char in enumerate(row):
        pdf.cell(cell_size, cell_size, txt=char, border=1, ln=0, align='C')
    pdf.ln(cell_size)

# Highlight found words
pdf.set_fill_color(255, 255, 204)  # Light yellow color for highlighting
for word, r, c, dr, dc in found_words:
    for i in range(len(word)):
        x_pos = start_x + (c + i * dc) * cell_size
        y_pos = start_y + (r + i * dr) * cell_size
        pdf.set_xy(x_pos, y_pos)
        pdf.rect(x_pos, y_pos, cell_size, cell_size, 'F')

# Reprint the grid text over the highlighted cells
pdf.set_xy(start_x, start_y)
for r, row in enumerate(grid):
    for c, char in enumerate(row):
        pdf.cell(cell_size, cell_size, txt=char, border=1, ln=0, align='C')
    pdf.ln(cell_size)

pdf.output("WORD_SEARCH1.pdf")
