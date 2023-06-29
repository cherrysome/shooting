import pygame
import random

# 초기화
pygame.init()

# 게임 창 설정
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

# 게임 제목 설정
pygame.display.set_caption("슈팅 게임")

# FPS 설정
clock = pygame.time.Clock()

# 배경 이미지 불러오기
background = pygame.image.load("background.png")

# 캐릭터(우주선) 설정
character = pygame.image.load("character.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height

# 이동 속도
character_speed = 5

# 총알 설정
bullet = pygame.image.load("bullet.png")
bullet_size = bullet.get_rect().size
bullet_width = bullet_size[0]
bullet_height = bullet_size[1]
bullet_x_pos = 0
bullet_y_pos = -1000
bullet_speed = 10
bullet_state = "ready"  # "ready": 발사 대기 상태, "fire": 발사 중

# 적(운석) 설정
enemy = pygame.image.load("enemy.png")
enemy_size = enemy.get_rect().size
enemy_width = enemy_size[0]
enemy_height = enemy_size[1]
enemy_x_pos = random.randint(0, screen_width - enemy_width)
enemy_y_pos = 0
enemy_speed = 3

# 점수 설정
score = 0
font = pygame.font.Font(None, 36)

# 게임 종료 여부
game_over = False
running = True
while running:
    # FPS 설정
    dt = clock.tick(60)

    # 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 창 닫기 버튼 이벤트
            running = False

        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # 스페이스바 키 이벤트
                    if bullet_state == "ready":
                        bullet_x_pos = character_x_pos + (character_width / 2) - (bullet_width / 2)
                        bullet_y_pos = character_y_pos
                        bullet_state = "fire"

    # 캐릭터 이동 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        character_x_pos -= character_speed
    if keys[pygame.K_RIGHT]:
        character_x_pos += character_speed

    # 경계 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 총알 이동 처리
    if bullet_state == "fire":
        bullet_y_pos -= bullet_speed
        if bullet_y_pos <= 0:
            bullet_state = "ready"

    # 적 이동 처리
    enemy_y_pos += enemy_speed
    if enemy_y_pos > screen_height:
        enemy_x_pos = random.randint(0, screen_width - enemy_width)
        enemy_y_pos = 0

    # 충돌 처리
    bullet_rect = bullet.get_rect()
    bullet_rect.left = bullet_x_pos
    bullet_rect.top = bullet_y_pos

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    if bullet_rect.colliderect(enemy_rect):
        bullet_state = "ready"
        enemy_x_pos = random.randint(0, screen_width - enemy_width)
        enemy_y_pos = 0
        score += 10

    if character_rect.colliderect(enemy_rect):
        game_over = True

    # 화면에 그리기
    screen.blit(background, (0, 0))
    screen.blit(character, (character_x_pos, character_y_pos))
    screen.blit(bullet, (bullet_x_pos, bullet_y_pos))
    screen.blit(enemy, (enemy_x_pos, enemy_y_pos))

    if game_over:
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over_text, (screen_width / 2 - game_over_text.get_width() / 2, screen_height / 2))

    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # 화면 업데이트
    pygame.display.update()

# 게임 종료
pygame.quit()
