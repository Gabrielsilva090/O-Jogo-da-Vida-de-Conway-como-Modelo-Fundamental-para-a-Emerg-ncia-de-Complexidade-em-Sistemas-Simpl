import pygame
import numpy as np
import time
import os
import matplotlib.pyplot as plt 

# Pygame setup
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)

live_cells_data = []
generation_count = 0


def create_grid():
    """Cria uma grade inicial aleatória."""
    global live_cells_data, generation_count 
    live_cells_data = [] 
    generation_count = 0 
    return np.random.choice([0, 1], size=(GRID_HEIGHT, GRID_WIDTH), p=[0.8, 0.2])

def update_grid(grid):
    
    new_grid = np.copy(grid)
    for r in range(GRID_HEIGHT):
        for c in range(GRID_WIDTH):
            live_neighbors = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (i, j) == (0, 0):
                        continue 

                    neighbor_r, neighbor_c = (r + i), (c + j)

                    effective_r = neighbor_r % GRID_HEIGHT
                    effective_c = neighbor_c % GRID_WIDTH
                    live_neighbors += grid[effective_r, effective_c]

            if grid[r, c] == 1:
                if live_neighbors < 2 or live_neighbors > 3:
                    new_grid[r, c] = 0
            else:
                if live_neighbors == 3:
                    new_grid[r, c] = 1

    return new_grid

def draw_grid(screen, grid):
    """Desenha a grade na tela."""
    screen.fill(BLACK)
    for r in range(GRID_HEIGHT):
        for c in range(GRID_WIDTH):
            if grid[r, c] == 1:
                pygame.draw.rect(screen, WHITE, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GRAY, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
    pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jogo da Vida de Conway com Dados")

    grid = create_grid() 
    running = True
    paused = False 

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused 
                    if paused:
                        print("Simulação pausada. Pressione ESPAÇO para continuar.")
                    else:
                        print("Simulação retomada.")
                if event.key == pygame.K_r:
                    grid = create_grid()
                    print("Grade reiniciada.")

        if not paused:
            grid = update_grid(grid)
            num_live_cells = np.sum(grid)
            live_cells_data.append(num_live_cells)
            global generation_count
            generation_count += 1

        draw_grid(screen, grid)

        time.sleep(0.05)

    pygame.quit() 
    print("Simulação encerrada.")

    # --- Plotar os dados após a simulação encerrar ---
    if generation_count > 0:
        plt.figure(figsize=(10, 6))
        plt.plot(range(generation_count), live_cells_data, color='blue')
        plt.title('Número de Células Vivas ao Longo das Gerações', fontsize=16)
        plt.xlabel('Geração', fontsize=12)
        plt.ylabel('Número de Células Vivas', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout() 
        plt.show()   
    else:
        print("Nenhum dado de células vivas foi coletado para plotar.")

if __name__ == "__main__":
    main()