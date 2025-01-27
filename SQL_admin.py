import pygame
import sys
import SQLHashTable
import count_dif_symbols
import findSectors
import random

def create_window(window_width, window_height):
    """Create a Pygame window and return the screen surface."""
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("IMG Compare")
    return screen

def main():
    # Initialize Pygame
    pygame.init()

    # Window dimensions
    window_width, window_height = 620, 700

    # Create the window
    screen = create_window(window_width, window_height)

    # Colors
    button_color = (70, 130, 180)
    button_hover_color = (100, 149, 237)
    button_text_color = (255, 255, 255)
    background_color = (230, 230, 230)
    textfield_color = (255, 255, 255)
    textfield_border_color = (0, 0, 0)

    # Font for button text and text input
    font = pygame.font.Font(None, 36)
    input_font = pygame.font.Font(None, 28)  # Smaller font for text input

    # Button labels
    btn_texts = ["get by id", "add", "delete by id", "edit by id", "print all", ]

    # Button dimensions and positions
    button_width, button_height = 150, 25
    button_margin = 10
    button_positions = [
        #((window_width - button_width) // 2, window_height - 6 * button_height - 5 * button_margin),
        ((window_width - button_width) // 2, window_height - 5 * button_height - 4 * button_margin),
        ((window_width - button_width) // 2, window_height - 4 * button_height - 3 * button_margin),
        ((window_width - button_width) // 2, window_height - 3 * button_height - 2 * button_margin),
        ((window_width - button_width) // 2, window_height - 2 * button_height - button_margin),
        ((window_width - button_width) // 2, window_height - button_height),
    ]

    # Text output variable
    output_text = "Ready!"  # Initial message
    input_text = ""  # Text field input

    # Text field dimensions
    textfield_width, textfield_height = 400, 50
    textfield_x = (window_width - textfield_width) // 2
    textfield_y = (window_height - textfield_height) // 2
    active_textfield = False  # Track if the text field is active for input

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # Check if the text field is clicked
                if textfield_x <= mouse_pos[0] <= textfield_x + textfield_width and \
                   textfield_y <= mouse_pos[1] <= textfield_y + textfield_height:
                    active_textfield = True
                else:
                    active_textfield = False

                # Check for button clicks
                for i, (x, y) in enumerate(button_positions):
                    button_rect = pygame.Rect(x, y, button_width, button_height)
                    if button_rect.collidepoint(mouse_pos):
                        #["get by id", "add", "delete by id", "edit by id", "print all", ]
                        sql = SQLHashTable.HashTable()
                        if i == 0:
                            temp = sql.get_element(int(input_text))
                            output_text = str(temp)
                            print (len(temp[2]))
                        elif i == 1:
                            with open('NewHash.txt', 'r') as file:
                                # Read the contents of the file
                                file_contents = file.read()
                            name = input_text
                            sql.add_element(name, file_contents)
                            output_text = "Success"
                        elif i ==2:
                            temp = sql.delete_element(int(input_text))
                            output_text = "i took care of it"
                        elif i==3:
                            with open('NewHash.txt', 'r') as file:
                                # Read the contents of the file
                                file_contents = file.read()
                            inp = input_text.split(';')
                            sql.edit_element(inp[0], inp[1])
                        elif i == 4: 
                            temp = sql.get_all_elements()
                            output_text = ""
                            
                            for i in range (len(temp)):
                                output_text = output_text+ "id="+str(temp[i][0]) + "; name="+str(temp[i][1]) +"; neighbors=" +str(temp[i][3])+".  "


            elif event.type == pygame.KEYDOWN and active_textfield:
                if event.key == pygame.K_RETURN:
                    output_text = f"You entered: {input_text}"
                    input_text = ""  # Clear the input field
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]  # Remove last character
                else:
                    input_text += event.unicode  # Add typed character

        # Fill the background
        screen.fill(background_color)

        # Draw the text field
        pygame.draw.rect(screen, textfield_border_color, (textfield_x, textfield_y, textfield_width, textfield_height), 2)
        pygame.draw.rect(screen, textfield_color, (textfield_x + 2, textfield_y + 2, textfield_width - 4, textfield_height - 4))
        input_surface = input_font.render(input_text, True, (0, 0, 0))
        screen.blit(input_surface, (textfield_x + 10, textfield_y + (textfield_height - input_surface.get_height()) // 2))

        # Draw buttons
        for i, (x, y) in enumerate(button_positions):
            mouse_pos = pygame.mouse.get_pos()
            button_rect = pygame.Rect(x, y, button_width, button_height)
            color = button_hover_color if button_rect.collidepoint(mouse_pos) else button_color
            pygame.draw.rect(screen, color, button_rect)
            button_text = font.render(btn_texts[i], True, button_text_color)
            screen.blit(button_text, button_text.get_rect(center=button_rect.center))

        # Render the text output field as multi-line text at the top
        line_spacing = 5  # Space between lines
        text_x, text_y = 10, 10  # Starting position for text rendering
        max_width = window_width - 20  # Adjust max width for text wrapping
        lines = []
        current_line = ""

        for word in output_text.split():
            test_line = f"{current_line} {word}".strip()
            test_surface = font.render(test_line, True, (0, 0, 0))
            if test_surface.get_width() <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:  # Add the last line if it exists
            lines.append(current_line)

        for line in lines:
            text_surface = font.render(line, True, (0, 0, 0))
            screen.blit(text_surface, (text_x, text_y))
            text_y += text_surface.get_height() + line_spacing

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
