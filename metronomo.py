import pygame
import os
import sys

class Metronomo:
    def __init__(self, callback_visual=None):
        pygame.mixer.init()
        self.bpm = 120
        self.compasso = 4
        self.volume = 0.5
        self.is_running = False
        self.current_tempo = 0
        self.callback_visual = callback_visual

        # Caminho base: script ou exe
        if getattr(sys, "frozen", False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(__file__)

        # Caminho para a pasta sons
        caminho_sons = os.path.join(base_path, "sons")

        # Carrega sons padrão
        self.som_tempo1 = pygame.mixer.Sound(os.path.join(caminho_sons, "metronomo0_forte.wav"))
        self.som_outros = pygame.mixer.Sound(os.path.join(caminho_sons, "metronomo0_fraco.wav"))
        self.set_volume(self.volume)

    def set_som_tempo1(self, path):
        if os.path.exists(path):
            self.som_tempo1 = pygame.mixer.Sound(path)
            self.set_volume(self.volume)

    def set_som_outros(self, path):
        if os.path.exists(path):
            self.som_outros = pygame.mixer.Sound(path)
            self.set_volume(self.volume)

    def set_bpm(self, bpm: int):
        self.bpm = bpm

    def set_compasso(self, compasso: int):
        self.compasso = compasso

    def set_volume(self, volume: float):
        self.volume = volume
        self.som_tempo1.set_volume(volume)
        self.som_outros.set_volume(volume)

    def start(self, root):
        if not self.is_running:
            self.is_running = True
            self.current_tempo = 0
            self._tick(root)

    # dentro da classe Metronomo
    def reset_tempo(self):
        self.current_tempo = 0


    def stop(self):
        self.is_running = False

    def _tick(self, root):
        if not self.is_running:
            return

        self.current_tempo += 1
        if self.current_tempo > self.compasso:
            self.current_tempo = 1

        # Escolhe som
        if self.current_tempo == 1:
            self.som_tempo1.play()
        else:
            self.som_outros.play()

        # Callback visual
        if self.callback_visual:
            self.callback_visual(self.current_tempo)

        # Próximo tick
        intervalo = int((60 / self.bpm) * 1000)
        root.after(intervalo, lambda: self._tick(root))
