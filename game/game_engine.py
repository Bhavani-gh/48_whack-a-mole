import pygame
import random
import math
from array import array
from .hole import Hole


# Game Engine

DARK_BROWN = (60, 40, 20)
MOLE_BROWN = (140, 95, 55)
BLACK = (0, 0, 0)


class GameEngine:

    def __init__(self, width, height, rows=3, cols=3):
        self.width = width
        self.height = height

        self.holes = []

        spacing_x = width // (cols + 1)
        spacing_y = (height - 80) // (rows + 1)

        for r in range(rows):
            for c in range(cols):
                cx = spacing_x * (c + 1)
                cy = 80 + spacing_y * (r + 1)
                self.holes.append(Hole(cx, cy))

        # Difficulty settings
        self.spawn_chance = 0.02
        self.mole_up_frames = 45

        # Game timer
        self.round_seconds = 30
        self.time_left_frames = self.round_seconds * 60

        # Score
        self.score = 0
        self.misses = 0

        self.font = pygame.font.SysFont("Arial", 28)

        self.game_over = False

        # Prevent the game-over sound from playing repeatedly
        self.game_over_sound_played = False

        # Create sound effects
        self.hit_sound = self.create_tone(
            frequency=700,
            duration=0.08
        )

        self.miss_sound = self.create_tone(
            frequency=250,
            duration=0.10
        )

        self.game_over_sound = self.create_tone(
            frequency=150,
            duration=0.40
        )

    def create_tone(self, frequency, duration):
        """
        Creates a simple sound effect without needing
        external .wav files.
        """

        sample_rate = 44100
        amplitude = 8000

        number_of_samples = int(
            sample_rate * duration
        )

        samples = array("h")

        for i in range(number_of_samples):

            value = int(
                amplitude
                * math.sin(
                    2 * math.pi
                    * frequency
                    * i
                    / sample_rate
                )
            )

            samples.append(value)

        return pygame.mixer.Sound(
            buffer=samples.tobytes()
        )

    def handle_event(self, event):

        if self.game_over:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_click(event.pos)

    def _handle_click(self, pos):

        hit_something = False

        for hole in self.holes:

            if hole.rect().collidepoint(pos):

                if hole.whack():

                    self.score += 1
                    hit_something = True

                    # Successful whack sound
                    self.hit_sound.play()

                    # Only one mole can be hit
                    break

        if not hit_something:

            self.misses += 1

            # Miss sound
            self.miss_sound.play()

    def handle_input(self):
        # Reserved for continuously-held-key input.
        pass

    def update(self):

        if self.game_over:
            return

        self.time_left_frames -= 1

        if self.time_left_frames <= 0:

            self.game_over = True

            # Play round-ending sound only once
            if not self.game_over_sound_played:

                self.game_over_sound.play()

                self.game_over_sound_played = True

            return

        for hole in self.holes:

            hole.update()

            if (
                not hole.active
                and random.random() < self.spawn_chance
            ):
                hole.pop_up(
                    self.mole_up_frames
                )

    def render(self, screen):

        # Draw holes and moles
        for hole in self.holes:

            pygame.draw.circle(
                screen,
                DARK_BROWN,
                (
                    hole.center_x,
                    hole.center_y
                ),
                40
            )

            if hole.active:

                pygame.draw.circle(
                    screen,
                    MOLE_BROWN,
                    (
                        hole.center_x,
                        hole.center_y
                    ),
                    32
                )

        # Draw score
        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            BLACK
        )

        screen.blit(
            score_text,
            (10, 10)
        )

        # Draw timer
        seconds_left = max(
            0,
            self.time_left_frames // 60
        )

        timer_text = self.font.render(
            f"Time: {seconds_left}s",
            True,
            BLACK
        )

        screen.blit(
            timer_text,
            (self.width - 140, 10)
        )

        # Game Over screen
        if self.game_over:

            # Dark transparent overlay
            overlay = pygame.Surface(
                (self.width, self.height)
            )

            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))

            screen.blit(
                overlay,
                (0, 0)
            )

            # GAME OVER
            game_over_text = self.font.render(
                "GAME OVER",
                True,
                (255, 255, 255)
            )

            # Final score
            final_score_text = self.font.render(
                f"Final Score: {self.score}",
                True,
                (255, 255, 255)
            )

            # Misses
            misses_text = self.font.render(
                f"Misses: {self.misses}",
                True,
                (255, 255, 255)
            )

            # Replay / Quit
            replay_text = self.font.render(
                "R - Replay    Q - Quit",
                True,
                (255, 255, 255)
            )

            # GAME OVER
            screen.blit(
                game_over_text,
                game_over_text.get_rect(
                    center=(
                        self.width // 2,
                        self.height // 2 - 80
                    )
                )
            )

            # Final score
            screen.blit(
                final_score_text,
                final_score_text.get_rect(
                    center=(
                        self.width // 2,
                        self.height // 2 - 30
                    )
                )
            )

            # Misses
            screen.blit(
                misses_text,
                misses_text.get_rect(
                    center=(
                        self.width // 2,
                        self.height // 2 + 20
                    )
                )
            )

            # Replay / Quit
            screen.blit(
                replay_text,
                replay_text.get_rect(
                    center=(
                        self.width // 2,
                        self.height // 2 + 80
                    )
                )
            )