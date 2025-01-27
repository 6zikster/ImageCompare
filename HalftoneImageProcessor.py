import pygame
import numpy as np
import programData

class HalftoneImageProcessor:
    def __init__(self, image):
        """
        Initialize the HalftoneImageProcessor with an image surface.

        :param image: Pygame surface.
        """
        self.image = image
        self.width, self.height = self.image.get_size()

    def apply_geometric_mean_filter(self):
        """
        Apply a geometric mean filter to the loaded image.

        """
        kernel_size = programData.ProgramData.getKernelSize()
        if kernel_size % 2 == 0:
            raise ValueError("Kernel size must be an odd number.")

        # Convert the Pygame surface to a NumPy array
        image_array = pygame.surfarray.array3d(self.image)

        # Convert RGB to grayscale
        grayscale = np.mean(image_array, axis=2).astype(np.float32)

        # Apply geometric mean filter
        padded_image = np.pad(grayscale, pad_width=kernel_size // 2, mode='edge')
        smoothed_image = np.zeros_like(grayscale)

        for i in range(self.width):
            for j in range(self.height):
                # Extract the kernel region
                kernel_region = padded_image[i:i + kernel_size, j:j + kernel_size]

                # Compute the geometric mean (avoid log(0) by adding a small constant)
                geometric_mean = np.exp(np.mean(np.log(kernel_region + 1e-9)))
                
                smoothed_image[i, j] = geometric_mean

        # Normalize the smoothed image to 0-255 range
        smoothed_image = np.clip(smoothed_image, 0, 255).astype(np.uint8)

        # Convert back to RGB
        final_image = np.stack([smoothed_image] * 3, axis=-1)

        # Create a new Pygame surface from the processed image
        smoothed_surface = pygame.surfarray.make_surface(final_image)
        self.processed_image = final_image  # Store the processed image as a variable

        gray_data = []
        for i in smoothed_image:
            gray_data.append(i)
        


        return smoothed_surface, gray_data

    def save_image(self, surface, output_path):
        """
        Save a Pygame surface to a file.

        :param surface: Pygame surface to save.
        :param output_path: Path to save the image.
        """
        pygame.image.save(surface, output_path)







