import pygame
import programData

class MonochromeProcessor:
    def __init__(self, image):
        """
        Инициализация класса MonochromeProcessor.

        :param image: Исходное изображение в формате Pygame Surface (Grayscale).
        :param threshold: Порог бинаризации (по умолчанию 128).
        """
        if not isinstance(image, pygame.Surface):
            raise TypeError("Input image must be a Pygame Surface.")

        self.image = image
        self.threshold = programData.ProgramData.getMonochromeThreshold()

    def convert_to_monochrome(self):
        """
        Преобразует изображение в монохромное (черно-белое).

        :return: Новое изображение в формате Pygame Surface, содержащее только черный и белый цвета.
        """
        # Создаем новое изображение того же размера, что и исходное
        width, height = self.image.get_size()
        monochrome_image = pygame.Surface((width, height), flags=pygame.SRCALPHA)

        monodata = []
        # Проходимся по каждому пикселю изображения
        for x in range(width):
            for y in range(height):
                # Получаем значение интенсивности пикселя (предполагается Grayscale)
                pixel_value = self.image.get_at((x, y)).r

                # Применяем пороговое преобразование
                color = pygame.Color(255, 255, 255) if pixel_value >= self.threshold else pygame.Color(0, 0, 0)

                

                # Устанавливаем преобразованный пиксель на новом изображении
                monochrome_image.set_at((x, y), color)
                monodata.append(color[0])

        return monochrome_image, monodata

# Пример использования:
if __name__ == "__main__":
    # Инициализация Pygame
    pygame.init()

    # Загружаем изображение (должно быть в формате Grayscale)
    input_image_path = "grayscale_image.png"
    grayscale_image = pygame.image.load(input_image_path).convert()

    # Создаем объект MonochromeProcessor
    threshold=128
    converter = MonochromeProcessor(grayscale_image, 128)

    # Конвертируем изображение в монохромное
    monochrome_image = converter.convert_to_monochrome()

    # Сохраняем результат
    output_image_path = "monochrome_image.png"
    pygame.image.save(monochrome_image, output_image_path)

    print(f"Монохромное изображение сохранено в {output_image_path}")

    # Завершаем работу Pygame
    pygame.quit()
