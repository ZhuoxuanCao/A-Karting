import pygame
from abc import ABC, abstractmethod
BLOCK_SIZE = 50
class TrackBlock(ABC):
    def __init__(self, x, y, color):
        self.__rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        self.__color = color
    @abstractmethod
    def draw(self, screen):
        pygame.draw.rect(screen, self.__color, self.__rect)
