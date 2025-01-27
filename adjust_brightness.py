import pygame
import numpy as np


def adjust_brightness(image, target_brightness):
    # Получаем массив пикселей изображения
    array = pygame.surfarray.array3d(image).astype(np.float32)

    # Корректируем яркость каждого канала
    for channel in range(3):  # Для каналов R, G и B
        mean_brightness = np.mean(array[:, :, channel]) #Вычисление средней яркости канала (сумма всех знач в канале)
        if mean_brightness != 0:
            correction_factor = target_brightness / mean_brightness #починеная яркость
            array[:, :, channel] = np.clip(array[:, :, channel] * correction_factor, 0, 255)

    # Преобразуем обратно в Surface
    corrected_image = pygame.surfarray.make_surface(array.astype(np.uint8))
    return corrected_image

