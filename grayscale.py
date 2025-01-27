import pygame
import programData

class GrayscaleConverter:
    def __init__(self, image):
        """
        Инициализация класса, загрузка изображения.

        :param image_path: Путь к исходному изображению.
        """
        pygame.init()
        self.original_image = image
        self.width, self.height = self.original_image.get_size()

    def rgb_to_grayscale(self, r, g, b):
        """
        Преобразует RGB-значения в оттенок серого.

        :param r: Компонента красного цвета (R).
        :param g: Компонента зеленого цвета (G).
        :param b: Компонента синего цвета (B).
        :return: Интенсивность серого цвета.
        """
        return int(0.3 * r + 0.59 * g + 0.11 * b)

    def convert_to_grayscale(self):
        """
        Преобразует всё изображение в оттенки серого.

        :return: Новое изображение в оттенках серого.
        """
        grayscale_image = pygame.Surface((self.width, self.height))

        for x in range(self.width):
            for y in range(self.height):
                r, g, b, _ = self.original_image.get_at((x, y))
                if (r == 0 and g == 0 and b == 0 and _ == 0):
                    gray = 255
                else:
                    gray = self.rgb_to_grayscale(r, g, b)
                grayscale_image.set_at((x, y), (gray, gray, gray))
        grayscale_data = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                r, g, b, _ = self.original_image.get_at((x, y))
                gray = self.rgb_to_grayscale(r, g, b)
                row.append(gray)  # Сохраняем только интенсивность (8-битовое значение)
            grayscale_data.append(row)
        #print (grayscale_data)
        return grayscale_image, grayscale_data

    def save_grayscale_image(self, output_path):
        """
        Сохраняет преобразованное изображение в файл.

        :param output_path: Путь для сохранения выходного изображения.
        """
        grayscale_image = self.convert_to_grayscale()
        pygame.image.save(grayscale_image, output_path)

# Пример использования:
# converter = GrayscaleConverter("input_image.png")
# converter.save_grayscale_image("output_image.png")
