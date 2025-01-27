import numpy as np
import pygame
import programData

import pygame
import programData

class Solarize:
    def __init__(self, image):
        """
        Инициализация класса, загрузка изображения.

        :param image_path: Путь к исходному изображению.
        """
        pygame.init()
        self.original_image = image
        self.width, self.height = self.original_image.get_size()

    def solarize_channel(self, pixel, threshold):
        '''agga = False
        if (pixel[0] != 255) and (pixel[1] != 255) and (pixel[2] != 255):
            if (pixel[0] != 0) and (pixel[1] != 0) and (pixel[2] != 0):

                print ("was " + str(pixel[0]) + "; " + str(pixel[1]) + "; " + str(pixel[2]))
                agga = True'''

        # Применяем соляризацию: если значение канала больше порога, инвертируем его
        if ((pixel[0] > threshold[0])):
            pixel[0] = 255 - pixel[0]
        if (pixel[1] > threshold[1]):
            pixel[1] = 255 - pixel[1]
        if (pixel[2] > threshold[2]):
            pixel[2] = 255 - pixel[2]
        
            return pixel

    def convert_to_solarized(self):
        """
        Преобразует всё изображение в оттенки серого.

        :return: Новое изображение в оттенках серого.
        """
        threshold = programData.ProgramData.getThreshold()
        pixelsRows = pygame.surfarray.array3d(self.original_image)
        for pixels in pixelsRows:
            for pixel in pixels:
                pixel = self.solarize_channel(pixel, threshold)


        # Собираем обратно изображение
        result_image = pygame.Surface((self.width, self.height))

        for y in range(self.height):
            for x in range(self.width):
                r = pixelsRows[x][y][0]
                g = pixelsRows[x][y][1]
                b = pixelsRows[x][y][2]
                color = (r, g, b)

                result_image.set_at((x, y), color)

    

        return result_image


