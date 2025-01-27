import pygame
import sys
import grayscale
import solar
import HalftoneImageProcessor
import monochrome
import MonochromeEroseProcessor
import SQLHashTable
import count_dif_symbols
import programData
import findSectors
import adjust_brightness

def create_window(window_width, window_height):
    """Create a Pygame window and return the screen surface."""
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("IMG Compare")
    return screen

def load_image(image_path):
    """Load an image and return the image object and its rect."""
    try:
        image = pygame.image.load(image_path)
        return image, image.get_rect()
    except pygame.error as e:
        print(f"Unable to load image: {e}")
        pygame.quit()
        sys.exit()

def read_image_pixels(image):
    """Read an image pixel by pixel and return a 2D array of pixel values."""
    width, height = image.get_size()
    pixels = []
    for y in range(height):
        row = []
        for x in range(width):
            pixel = image.get_at((x, y))  # Get pixel at (x, y)
            row.append(pixel)
        pixels.append(row)
    return pixels

def main():
    # Initialize Pygame
    pygame.init()

    # Window dimensions
    window_width, window_height = 800, 700

    # Create the window
    screen = create_window(window_width, window_height)

    # Initial image path
    image_path = programData.ProgramData.getPath()
    image, image_rect = load_image(image_path)

    standard_weight, standard_height = 64, 64
    image = pygame.transform.scale(image, (standard_weight, standard_height))

    # Clean up any transparent pixels
    width, height = image.get_size()
    for x in range(width):
        for y in range(height):
            r, g, b, _ = image.get_at((x, y))
            if (r == 0 and g == 0 and b == 0 and _ == 0):
                clr = 0
                image.set_at((x, y), (clr, clr, clr))

    # Center the image
    image_x = (window_width - image.get_width()) // 2
    image_y = (window_height - image.get_height()) // 2

    # Button dimensions and positions
    button_width, button_height = 150, 25
    button_margin = 10

    # Input box and Load button positions (left side)
    load_button_x = 10
    load_button_y = window_height - button_height - 10
    input_box_width = 200
    input_box_x = load_button_x + button_width + button_margin
    input_box_y = load_button_y

    # Right side buttons positions
    right_buttons_x = window_width - button_width - 10

    # Find similar button position at bottom right
    find_similar_y = window_height - button_height - 10
    find_similar_pos = (right_buttons_x, find_similar_y)

    # Generate positions for the 6 right buttons above the find similar button
    right_button_positions = []
    for i in range(6):  # solar to add to db
        y = find_similar_y - (i + 1) * (button_height + button_margin)
        right_button_positions.append((right_buttons_x, y))

    # Reverse to maintain the order: solar, grayscale, Halftone, monochrome, erose, add to db
    right_button_positions.reverse()
    # Combine all button positions
    button_positions = (
        [(load_button_x, load_button_y)] + 
        right_button_positions + 
        [find_similar_pos]
    )

    # Colors
    button_color = (70, 130, 180)
    button_hover_color = (100, 149, 237)
    button_text_color = (255, 255, 255)
    background_color = (230, 230, 230)
    input_box_color = (255, 255, 255)
    input_box_active_color = (200, 200, 200)
    input_box_text_color = (0, 0, 0)

    # Font for button text and output field
    font = pygame.font.Font(None, 36)
    output_font = pygame.font.Font(None, 28)

    # Button labels
    btn_texts = [
        "Load Image",
        "solar", "grayscale", "Halftone",
        "monochrome", "erose", "add to db",
        "find similar"
    ]

    # Text output variable
    output_text = "Ready!"
    ready = False

    # Input box variables
    input_box = pygame.Rect(input_box_x, input_box_y, input_box_width, button_height)
    input_text = "picsBlack/img29.png"
    input_active = False

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle mouse clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                
                # Check Load Image button
                load_rect = pygame.Rect(button_positions[0][0], button_positions[0][1], button_width, button_height)
                if load_rect.collidepoint(mouse_pos):
                    try:
                        new_image, new_rect = load_image(input_text)
                        image_path = input_text
                        new_image = pygame.transform.scale(new_image, (standard_weight, standard_height))
                        # Clean transparent pixels
                        width, height = new_image.get_size()
                        for x in range(width):
                            for y in range(height):
                                r, g, b, _ = new_image.get_at((x, y))
                                if (r == 0 and g == 0 and b == 0 and _ == 0):
                                    clr = 0
                                    new_image.set_at((x, y), (clr, clr, clr))
                        image = new_image
                        image_x = (window_width - new_image.get_width()) // 2
                        image_y = (window_height - new_image.get_height()) // 2
                        output_text = f"Loaded {input_text}"
                    except Exception as e:
                        output_text = f"Error loading image: {e}"
                
                # Check input box
                elif input_box.collidepoint(mouse_pos):
                    input_active = True
                else:
                    input_active = False
                
                # Check other buttons
                for i, (x, y) in enumerate(button_positions[1:]):
                    button_rect = pygame.Rect(x, y, button_width, button_height)
                    if button_rect.collidepoint(mouse_pos):
                        btn_index = i + 1  # Offset for Load Image button
                        if btn_index == 1:  # solar
                            image = adjust_brightness.adjust_brightness(image, 128)
                            output_text = "Brightness adjusted!"
                        elif btn_index == 2:  # grayscale
                            converter = grayscale.GrayscaleConverter(image)
                            image, _ = converter.convert_to_grayscale()
                            output_text = "Grayscale applied!"
                        elif btn_index == 3:  # Halftone
                            converter = HalftoneImageProcessor.HalftoneImageProcessor(image)
                            image, _ = converter.apply_geometric_mean_filter()
                            output_text = "Halftone applied!"
                        elif btn_index == 4:  # monochrome
                            converter = monochrome.MonochromeProcessor(image)
                            image, _ = converter.convert_to_monochrome()
                            output_text = "Monochrome applied!"
                        elif btn_index == 5:  # erose
                            converter = MonochromeEroseProcessor.EroseProcessor(image)
                            image, data = converter.erose()
                            output_text = "Erose processed!"
                            ready = True
                        elif btn_index == 6:  # add to db
                            if ready:
                                sql = SQLHashTable.HashTable()
                                addMe = ''.join(str(item) for item in data)
                                sql.add_element(image_path, addMe)
                                output_text = "Added to database!"
                                ready = True
                        elif btn_index == 7:  # find similar
                            if ready:
                                sql = SQLHashTable.HashTable()
                                list = sql.get_all_elements()
                                output_text = ""
                                for x in range(0, standard_weight):
                                        for y in range(0, standard_height):
                                            pixel_value = image.get_at((x, y))
                    
                                minSimilarity = len(data)
                                indRes = 0
                                name = "UND"
                                strData = ''.join(str(item) for item in data)
                                for idx, record in enumerate(list):
                                    diff = count_dif_symbols.Count.count_different_symbols(record[2], strData)
                                    if diff < minSimilarity:
                                            minSimilarity = diff
                                            indRes = record[0]
                                            name = record[1]

                                percentages = minSimilarity / (standard_height * standard_weight)
                                percentages = percentages * 100
                                output_text += f"Match: Id {indRes}, Name {name}, Difference {int(percentages)}%\n"

            # Handle keyboard input
            elif event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

        # Fill the background
        screen.fill(background_color)

        # Draw the image
        screen.blit(image, (image_x, image_y))

        # Draw all buttons
        for i, (x, y) in enumerate(button_positions):
            mouse_pos = pygame.mouse.get_pos()
            button_rect = pygame.Rect(x, y, button_width, button_height)
            color = button_hover_color if button_rect.collidepoint(mouse_pos) else button_color
            pygame.draw.rect(screen, color, button_rect)
            button_text = font.render(btn_texts[i], True, button_text_color)
            screen.blit(button_text, button_text.get_rect(center=button_rect.center))

        # Draw input box
        input_color = input_box_active_color if input_active else input_box_color
        pygame.draw.rect(screen, input_color, input_box)
        input_surface = font.render(input_text, True, input_box_text_color)
        screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))

        # Render multi-line output text
        text_x, text_y = 10, 50
        max_width = window_width - 20
        lines = []
        current_line = ""

        for word in output_text.split():
            test_line = f"{current_line} {word}".strip()
            test_surface = output_font.render(test_line, True, (0, 0, 0))
            if test_surface.get_width() <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        for line in lines:
            text_surface = output_font.render(line, True, (0, 0, 0))
            screen.blit(text_surface, (text_x, text_y))
            text_y += text_surface.get_height() + 5

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()