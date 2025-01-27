import pygame
from pygame import Surface
from collections import deque

class ImageSegmenter:
    def __init__(self, image):
        """
        Initializes the ImageSegmenter with the given image.
        :param image_path: Path to the input black-and-white image.
        """
        pygame.init()
        self.image = image 
        self.width, self.height = self.image.get_size()
        self.visited = set()  # To keep track of visited pixels

    def is_valid_pixel(self, x, y, color):
        """
        Check if a pixel is valid for flood fill.
        :param x: X-coordinate of the pixel
        :param y: Y-coordinate of the pixel
        :param color: Color to match
        :return: True if pixel is valid, False otherwise
        """
        if 0 <= x < self.width and 0 <= y < self.height and (x, y) not in self.visited:
            return self.image.get_at((x, y)) == color
        return False

    def flood_fill(self, x, y, color):
        """
        Flood fill algorithm to extract a connected region.
        :param x: Starting X-coordinate
        :param y: Starting Y-coordinate
        :param color: Color to match
        :return: A set of pixels belonging to the connected region
        """
        queue = deque([(x, y)])
        pixels = set()
        self.visited.add((x, y))

        while queue:
            cx, cy = queue.popleft()
            pixels.add((cx, cy))
            
            # Check 4-connected neighbors
            for nx, ny in [(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)]:
                if self.is_valid_pixel(nx, ny, color):
                    self.visited.add((nx, ny))
                    queue.append((nx, ny))
        return pixels

    def extract_regions(self):
        """
        Extract all non-connected white regions from the image.
        :return: List of Pygame Surfaces, each containing a connected white region.
        """
        regions = []
        white = pygame.Color(255, 255, 255, 255)  # Define white color

        for y in range(self.height):
            for x in range(self.width):
                color = self.image.get_at((x, y))
                if (x, y) not in self.visited and color == white:
                    # Extract the connected region
                    pixels = self.flood_fill(x, y, color)
                    region_surface = self.create_region_surface(pixels, white)
                    regions.append(region_surface)
        return regions

    def create_region_surface(self, pixels, color):
        """
        Create a new surface for the connected region.
        :param pixels: Set of pixels belonging to the region
        :param color: Color of the region (white)
        :return: Pygame Surface containing the region
        """
        # Find bounding box of the region
        min_x = min(p[0] for p in pixels)
        max_x = max(p[0] for p in pixels)
        min_y = min(p[1] for p in pixels)
        max_y = max(p[1] for p in pixels)

        # Create a transparent surface
        region_surface = Surface((max_x - min_x + 1, max_y - min_y + 1), pygame.SRCALPHA)
        region_surface.fill((0, 0, 0, 0))  # Fill with transparent pixels

        # Draw the region onto the new surface
        for x, y in pixels:
            region_surface.set_at((x - min_x, y - min_y), color)

        return region_surface
