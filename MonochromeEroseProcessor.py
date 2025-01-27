import pygame
import numpy as np
from PIL import Image
import programData

class EroseProcessor:
    def __init__(self, image, mask_size=3):
        """
        Инициализация объекта для обработки изображения.

        :param image: Исходное изображение (объект Surface Pygame).
        :param mask_size: Размер квадратной маски для эрозии (по умолчанию 3).
        """
        self.original_image = image
        self.mask_size = mask_size

    def erose(self):
        # Преобразуем изображение в массив NumPy (градации серого)

        #arr = pygame.surfarray.array3d(self.original_image)

        #for i in arr:
            #print (i)
        mask_size = programData.ProgramData.getMaskSize()
        offset = mask_size // 2

        width, height = self.original_image.get_size()
        result = self.original_image

        #pixels_in = original_image.load()
        pixelsRows = pygame.surfarray.array3d(self.original_image)        
        pixels_in = []
        for pixels in pixelsRows:
            pixels_in2 = []
            for pixel in pixels:
                if (pixel[0] == 255):
                    pixels_in2.append(1)
                else:
                    pixels_in2.append(0)
            pixels_in.append(pixels_in2)
        pixels_out = []
        pixelsRows = pygame.surfarray.array3d(result)        
        for pixels in pixelsRows:
            pixels_out2 = []
            for pixel in pixels:
                if (pixel[0] == 255):
                    pixels_out2.append(1)
                else:
                    pixels_out2.append(0)
            pixels_out.append(pixels_out2)
        #pixels_out = result.load()
        


        for y in range(offset, height - offset):
            for x in range(offset, width - offset):
                erode = True
                for dy in range(-offset, offset + 1):
                    for dx in range(-offset, offset + 1):
                        #print (pixels_in[x + dx, y + dy])
                        neighbor = pixels_in[x + dx][y + dy]
                        if neighbor == 1:
                            erode = False
                            break
                    if not erode:
                        break
                pixels_out[x][y] = 0 if erode else 1
        
        result_image = pygame.Surface((width, height))
        enddata = []
        for y in range(height):
            for x in range(width):
                r = pixels_out[x][y]
                if (r==0):
                    color = (0, 0, 0)
                    enddata.append(0)
                else:
                    color = (255, 255, 255)
                    enddata.append(1)

                result_image.set_at((x, y), color)
        return result_image, enddata




    # Пример использования
if __name__ == "__main__":
    pygame.init()

    # Загружаем изображение
    image_path = "pictures/img1.png"  # Путь к изображению
    original_image = pygame.image.load(image_path).convert()

    # Создаем объект для обработки
    converter = EroseProcessor(original_image, mask_size=5)

    # Выполняем эрозию
    monochrome_image = converter.erose()

    # Сохраняем результат
    pygame.image.save(monochrome_image, "pictures/img1.png")

    pygame.quit()