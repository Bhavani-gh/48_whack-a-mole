import pygame
from game.game_engine import GameEngine

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 500, 560
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Whack-a-Mole - Pygame Version")

# Colors
GRASS_GREEN = (120, 170, 90)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Create first game
engine = GameEngine(WIDTH, HEIGHT)


def show_difficulty_screen():
    """Display difficulty selection and return the selected difficulty."""

    selecting = True
    font = pygame.font.SysFont("Arial", 28)

    while selecting:
        SCREEN.fill(GRASS_GREEN)

        title = font.render(
            "SELECT DIFFICULTY",
            True,
            BLACK
        )

        easy = font.render(
            "1 - Easy",
            True,
            BLACK
        )

        medium = font.render(
            "2 - Medium",
            True,
            BLACK
        )

        hard = font.render(
            "3 - Hard",
            True,
            BLACK
        )

        SCREEN.blit(
            title,
            title.get_rect(
                center=(WIDTH // 2, 180)
            )
        )

        SCREEN.blit(
            easy,
            easy.get_rect(
                center=(WIDTH // 2, 250)
            )
        )

        SCREEN.blit(
            medium,
            medium.get_rect(
                center=(WIDTH // 2, 300)
            )
        )

        SCREEN.blit(
            hard,
            hard.get_rect(
                center=(WIDTH // 2, 350)
            )
        )

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1:
                    return "easy"

                elif event.key == pygame.K_2:
                    return "medium"

                elif event.key == pygame.K_3:
                    return "hard"

        clock.tick(FPS)


def create_new_game(difficulty):
    """Create a new game using the selected difficulty."""

    new_engine = GameEngine(WIDTH, HEIGHT)

    if difficulty == "easy":
        new_engine.spawn_chance = 0.01
        new_engine.mole_up_frames = 60

    elif difficulty == "medium":
        new_engine.spawn_chance = 0.02
        new_engine.mole_up_frames = 45

    elif difficulty == "hard":
        new_engine.spawn_chance = 0.04
        new_engine.mole_up_frames = 30

    return new_engine


def main():
    global engine

    running = True

    while running:

        SCREEN.fill(GRASS_GREEN)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # Normal game controls
            if not engine.game_over:
                engine.handle_event(event)

            # Game Over controls
            else:

                if event.type == pygame.KEYDOWN:

                    # Replay
                    if event.key == pygame.K_r:

                        difficulty = show_difficulty_screen()

                        if difficulty is None:
                            running = False
                        else:
                            engine = create_new_game(
                                difficulty
                            )

                    # Quit
                    elif event.key == pygame.K_q:
                        running = False

        if not engine.game_over:
            engine.handle_input()
            engine.update()

        engine.render(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()