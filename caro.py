import pygame
import random
import math 
# Kích thước cửa sổ trò chơi
WIDTH = 600 # Tăng chiều rong cửa sổ, 100 pixel cho vùng mở rộng
ROWS, COLS = 15, 15
SQUARE_SIZE = WIDTH // COLS     #マス目のサイズ
FOOTER_HEIGHT = 50  # Chiều cao vùng mở rộng phía dưới
HEIGHT = 700 + FOOTER_HEIGHT
Font = 'NotoSansJP-Light.ttf'  # Đảm bảo font này tồn tại trong thư mục

# Kích thước vùng mở rộng
EXTENSION_HEIGHT = 100  # Chiều cao vùng mở rộng

# Màu sắc
GREEN = (84, 255, 159)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
SKYBLUE = (0,191,255)
SKYBLUE1 = (176, 226, 255)
# Khởi tạo Pygame
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))# vẽ màn hình.,
pygame.display.set_caption('Caro 15x15')# ゲームの名前
cup_image = pygame.image.load('cup_1.png')# import anhr
cup_image = pygame.transform.scale(cup_image, (100, 100))

# Khởi tạo bảng trò chơi (0 là ô trống, 1 là X, -1 là O)
board = [[0 for _ in range(COLS)] for _ in range(ROWS)]


def reset_board():
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]


board = reset_board()

# Người chơi hiện tại (1 cho X, -1 cho O)
current_player = 1
x_kachi = 0
o_kachi = 0
games_played = 0
winner = None
final_winner = None
click = False
turn_time = 40  # Thời gian tối đa cho mỗi lượt (giây)
time_remaining = turn_time
turn_start_time = None
    

def draw_extension_area():
    """
    Vẽ vùng mở rộng phía trên khu vực chơi chính.
    """
    pygame.draw.rect(WIN, SKYBLUE, (0, 0, WIDTH, EXTENSION_HEIGHT))  # Vẽ nền màu xanh

    # Hiển thị thông tin
    font = pygame.font.Font(Font, 24)
    turn_text = f"出番: {'X' if current_player == 1 else 'O'}"
    x_score_text = f"X 勝ち: {x_kachi}"
    o_score_text = f"O 勝ち: {o_kachi}"

    turn_label = font.render(turn_text, True, BLACK)
    x_score_label = font.render(x_score_text, True, BLACK)
    o_score_label = font.render(o_score_text, True, BLACK)

    WIN.blit(turn_label, (260, 60))  # Hiển thị lượt chơi
    WIN.blit(x_score_label, (100, 10))  # Hiển thị số lần thắng của X
    WIN.blit(o_score_label, (400, 10))  # Hiển thị số lần thắng của O
    # ve vach ngan
    pygame.draw.line(WIN, GREEN, (0, EXTENSION_HEIGHT - 40), (WIDTH, EXTENSION_HEIGHT - 40), 5)
    pygame.draw.line(WIN, GREEN, (WIDTH // 2, 0), (WIDTH // 2, EXTENSION_HEIGHT - 40), 5)  # Vẽ vạch dọc
    
    #Ve nut quay tro lai man hinh chinh 
    global back_button_rect
    back_button_rect = pygame.Rect(WIDTH - 55 , 0, 55, 30)  # Tọa độ và kích thước nút
    pygame.draw.rect(WIN, WHITE, back_button_rect)  # Vẽ nút màu trắng
    pygame.draw.rect(WIN, BLACK, back_button_rect, 2)  # Vẽ viền nút

    back_label = font.render("戻り", True, BLACK) # ve nut quay tro lai
    WIN.blit(back_label, (back_button_rect.x + (back_button_rect.width - back_label.get_width()) // 2,
                          back_button_rect.y + (back_button_rect.height - back_label.get_height()) // 2))
    
def draw_footer_area():
    """
    Vẽ vùng mở rộng phía dưới khu vực chơi.
    """
    pygame.draw.rect(WIN, SKYBLUE, (0, HEIGHT - FOOTER_HEIGHT, WIDTH, FOOTER_HEIGHT))  # Vẽ nền màu xanh
    # Hiển thị thông tin
    font = pygame.font.Font(Font, 16)
    message_text = "The game is created by NGUYENSYPHIEU"
    message_label = font.render(message_text, True, BLACK)
    WIN.blit(
        message_label,
        ((WIDTH - message_label.get_width()) // 2, HEIGHT - FOOTER_HEIGHT + (FOOTER_HEIGHT - message_label.get_height()) // 2),
    )

def display_start_screen():
    waiting = True
    
    base_font_size = 36  # Kích thước cơ bản
    hover_font_size = 43  # Kích thước khi hover
    font_growth_speed = 0.3 # Tốc độ tăng kích thước font
    font_sizes = [base_font_size, base_font_size, base_font_size]  # Kích thước font cho từng tùy chọn
    options = ["人と対戦", "コンピューターと対戦","Exit"]
    font = pygame.font.Font(Font, base_font_size)
    

    image = pygame.image.load('anh_nen1.png')
    image = pygame.transform.scale(image, (600, 800))
    # Tính toán vị trí y bắt đầu và khoảng cách giữa các dòng
    start_y = HEIGHT // 2 - len(options) * 40  # Đặt dòng đầu tiên vào giữa màn hình
    line_spacing = 70  # Khoảng cách giữa các dòng
    
    
    while waiting:
        WIN.fill(WHITE)
        WIN.blit(image, ((WIDTH - image.get_width()) // 2, (HEIGHT - image.get_height()) // 2))
        mouse_pos = pygame.mouse.get_pos()
        selected_option = -1
        
        for i, option in enumerate(options):
            # Tính toán vị trí của từng dòng
            option_x = (WIDTH - 300) // 2
            option_y = start_y + i * line_spacing

            # Kiểm tra nếu chuột hover lên tùy chọn
            option_rect = pygame.Rect(option_x, option_y, 300, 50)
            if option_rect.collidepoint(mouse_pos):
                selected_option = i
                # Tăng dần kích thước font nếu hover
                if font_sizes[i] < hover_font_size:
                    font_sizes[i] += font_growth_speed
            else:
                # Giảm dần kích thước font nếu không hover
                if font_sizes[i] > base_font_size:
                    font_sizes[i] -= font_growth_speed

            # Vẽ chữ với kích thước và màu sắc tương ứng
            dynamic_font = pygame.font.Font(Font, int(font_sizes[i]))
            text_color = RED if option_rect.collidepoint(mouse_pos) else BLACK
            option_text = dynamic_font.render(option, True, text_color)
            WIN.blit(option_text, ((WIDTH - option_text.get_width()) // 2, option_y))

        
        pygame.display.update()

        # Kiểm tra sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and selected_option != -1:
                if options[selected_option] == "Exit":
                    pygame.quit()
                    quit()  # Đảm bảo thoát trò chơi ngay lập tức
                return selected_option  # Trả về sự lựa chọn của người chơi

        pygame.display.update()
             
        

        
def draw_grid():
    """
    Vẽ lưới khu vực chơi chính.
    """
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(
                WIN, SKYBLUE1, (col * SQUARE_SIZE, EXTENSION_HEIGHT + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1
            )


def draw_board(board):
    """
    Vẽ các ô X hoặc O trong khu vực chơi.
    Nếu có chuỗi chiến thắng, 5 ô đó sẽ được đổi màu nền và có đường gạch ngang qua.
    """
    def get_winning_positions(board, player):
        for row in range(ROWS):
            for col in range(COLS):
                # Kiểm tra các hướng
                for dr, dc in [(1, 0), (0, 1), (1, 1), (1, -1)]:
                    positions = []
                    for i in range(5):
                        r, c = row + i * dr, col + i * dc
                        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
                            positions.append((r, c))
                        else:
                            break
                    if len(positions) == 5:  # Nếu tìm được 5 ô liên tiếp
                        return positions
        return None

    # Lấy các vị trí thắng của X hoặc O
    winning_positions = get_winning_positions(board, 1) or get_winning_positions(board, -1)

    # Vẽ bàn cờ
    for row in range(ROWS):
        for col in range(COLS):
            # Nếu là ô thuộc chuỗi chiến thắng, đổi màu nền
            if winning_positions and (row, col) in winning_positions:
                pygame.draw.rect(
                    WIN, (0, 255, 0),  # Màu xanh lá cho nền
                    pygame.Rect(col * SQUARE_SIZE, EXTENSION_HEIGHT + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                )

            # Vẽ X hoặc O trên nền
            if board[row][col] == 1:  # Vẽ X
                pygame.draw.line(
                    WIN, BLUE, (col * SQUARE_SIZE + 10, EXTENSION_HEIGHT + row * SQUARE_SIZE + 10),
                    ((col + 1) * SQUARE_SIZE - 10, EXTENSION_HEIGHT + (row + 1) * SQUARE_SIZE - 10), 3)
                pygame.draw.line(
                    WIN, BLUE, ((col + 1) * SQUARE_SIZE - 10, EXTENSION_HEIGHT + row * SQUARE_SIZE + 10),
                    (col * SQUARE_SIZE + 10, EXTENSION_HEIGHT + (row + 1) * SQUARE_SIZE - 10), 3)
            elif board[row][col] == -1:  # Vẽ O
                pygame.draw.circle(
                    WIN, RED,
                    (col * SQUARE_SIZE + SQUARE_SIZE // 2, EXTENSION_HEIGHT + row * SQUARE_SIZE + SQUARE_SIZE // 2),
                    SQUARE_SIZE // 3, 3)

    # Vẽ đường gạch qua 5 ô thắng
    if winning_positions:
        start_row, start_col = winning_positions[0]
        end_row, end_col = winning_positions[-1]
        start_pos = (start_col * SQUARE_SIZE + SQUARE_SIZE // 2,
                     EXTENSION_HEIGHT + start_row * SQUARE_SIZE + SQUARE_SIZE // 2)
        end_pos = (end_col * SQUARE_SIZE + SQUARE_SIZE // 2,
                   EXTENSION_HEIGHT + end_row * SQUARE_SIZE + SQUARE_SIZE // 2)
        pygame.draw.line(WIN, (0, 0, 0), start_pos, end_pos, 2)  # Màu đỏ, độ dày 5 pixel
def reset_game():
    "dat lai trang thai tro choi khi bam nut 戻る"
    
    global board, current_player, winner, x_kachi, o_kachi,games_played,final_winner, click
    board = reset_board()
    current_player = 1
    winner = None
    x_kachi = o_kachi = games_played = 0
    final_winner = None
    click = False
    
  # Đặt lại thời gian bắt đầu lượt
def handle_click(pos):
    """
    Xử lý click trong khu vực chơi.
    """
    
    global turn_start_time, current_player, winner, board, click
    if back_button_rect.collidepoint(pos):
        reset_game()
        click = False
        return "メニューに戻る"

    if winner or final_winner:  # Sau khi thắng thì không tăng số lần thắng nữa
        return
    
    x, y = pos
    
    if y < EXTENSION_HEIGHT:  # Bỏ qua khu vực mở rộng
        return
    
    row = (y - EXTENSION_HEIGHT) // SQUARE_SIZE
    col = x // SQUARE_SIZE
    
    if board[row][col] == 0:  # Nếu ô trống thì mới cho phép đánh
        board[row][col] = current_player
        current_player *= -1  # Đổi lượt chơi
        turn_start_time = pygame.time.get_ticks()  # Đặt lại thời gian bắt đầu lượt mới
def check_win(board, player):
    for row in range(ROWS):
        for col in range(COLS):
            if check_line(board, player, row, col, 1, 0) or \
               check_line(board, player, row, col, 0, 1) or \
            check_line(board, player, row, col, 1, 1) or \
               check_line(board, player, row, col, 1, -1):
                return True
            
    return False
def check_line(board, player, row, col, dx, dy):
    count = 0
    for i in range(5):
        r = row + i * dx
        c = col + i * dy
        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
        else:
            break
    return count == 5
def find_double_threat(player):
    """
    Tìm các ô có thể tạo 2 đường thắng đồng thời.
    """
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == 0:  # Chỉ xét ô trống
                threats = 0
                # Kiểm tra các hướng
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    count = 1
                    for i in range(1, 4):
                        r, c = row + i * dr, col + i * dc
                        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
                            count += 1
                        else:
                            break
                    if count >= 3:  # Nếu tìm thấy chuỗi tiềm năng
                        threats += 1
                if threats >= 2:  # Double Threat
                    return row, col
    return None
def find_block_or_win(player, count_needed):
   
        for row in range(ROWS):
            for col in range(COLS):
                if board[row][col] == 0:  # Chỉ kiểm tra ô trống
                    # Kiểm tra tất cả các hướng (ngang, dọc, chéo)
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                        count = 1  # Đếm số quân của player ở vị trí này (bắt đầu từ 1 vì ô hiện tại là ô trống)
                        for i in range(1, count_needed):  # Kiểm tra đến số lượng quân cần thiết (3 hoặc 4)
                            r, c = row + i * dr, col + i * dc
                            if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
                                count += 1
                            else:
                                break
                        # Nếu có đủ quân liên tiếp, chặn ở ô trống hoặc thắng
                        if count == count_needed:
                            return row, col
        return None
def find_3_in_4_to_block(player):
    """
    Tìm chuỗi 4 ô liên tiếp có 3 quân của player và 1 ô trống:
    - Chặn ô trống ở giữa nếu có.
    - Chặn ô đầu hoặc cuối nếu chưa bị chặn bởi quân đối phương.
    """
    for row in range(ROWS):
        for col in range(COLS):
            # Kiểm tra tất cả các hướng (ngang, dọc, chéo)
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                count = 0       # Đếm quân player
                empty_count = 0 # Đếm ô trống
                empty_positions = [] # Vị trí ô trống
                blocked = False  # Kiểm tra có bị chặn bởi quân đối phương không

                for i in range(4):  # Duyệt qua 4 ô liên tiếp
                    r, c = row + i * dr, col + i * dc
                    if 0 <= r < ROWS and 0 <= c < COLS:
                        if board[r][c] == player:
                            count += 1
                        elif board[r][c] == 0:
                            empty_count += 1
                            empty_positions.append((r, c))
                        else:  # Nếu ô bị chặn bởi đối phương
                            blocked = True
                            break
                    else:
                        blocked = True
                        break

                # Nếu có 3 quân player và 1 ô trống, xử lý
                if count == 3 and empty_count == 1 and not blocked:
                    return empty_positions[0]  # Trả về ô trống giữa

                # Nếu có 3 quân player và 1 ô trống ở đầu hoặc cuối, không bị chặn
                if count == 3 and empty_count == 2 and not blocked:
                    return empty_positions[0] if empty_positions else None  # Trả về ô đầu/cuối

    return None
def ai_move():
    global board, current_player
    """

    1. Đánh để thắng nếu AI có nước thắng.
    2. Chặn đối phương thắng.
    3. Tạo Double Threat (2 nước thắng).
    4. Chặn Double Threat của đối phương.
    5. Chặn 3 quân liên tiếp của đối phương.
    6. Mở rộng chuỗi tấn công của AI.
    7. Kiểm soát khu vực trung tâm.
    8. Đánh gần các quân cờ đã có.
    9. Đánh ngẫu nhiên nếu không còn lựa chọn.
    """
    def is_valid_cell(row, col):
        return 0 <= row < ROWS and 0 <= col < COLS and board[row][col] == 0

    def get_center_priority():
        center = (ROWS // 2, COLS // 2)
        empty_cells = [(row, col) for row in range(ROWS) for col in range(COLS) if board[row][col] == 0]
        empty_cells.sort(key=lambda x: abs(x[0] - center[0]) + abs(x[1] - center[1]))
        return empty_cells
     # 2. Chặn đối phương thắng nếu họ có 4 quân liên tiếp
    block_move = find_block_or_win(1, 4)
    if block_move:
        row, col = block_move
        board[row][col] = -1
        return True
    # 1. Đánh để thắng ngay nếu có thể
    winning_move = find_block_or_win(-1, 4)
    if winning_move:
        row, col = winning_move
        board[row][col] = -1
        return True
    # 4. Chặn X nếu họ có 3 quân trong 4 ô liên tiếp (bao gồm ô trống ở giữa hoặc hai đầu)
    block_3_in_4 = find_3_in_4_to_block(1)
    if block_3_in_4:
        row, col = block_3_in_4
        board[row][col] = -1
        return True
   # 5. Chặn 3 quân liên tiếp của đối phương
    block_3 = find_block_or_win(1, 3)
    if block_3:
        row, col = block_3
        board[row][col] = -1
        return True

    # 3. Tạo Double Threat (2 đường thắng đồng thời)
    double_threat_move = find_double_threat(-1)
    if double_threat_move:
        row, col = double_threat_move
        board[row][col] = -1
        return True

    # 4. Chặn Double Threat của đối phương
    block_double_threat = find_double_threat(1)
    if block_double_threat:
        row, col = block_double_threat
        board[row][col] = -1
        return True
   
    # 6. Mở rộng chuỗi tấn công của AI (ưu tiên tạo 3 quân)
    expand_attack = find_block_or_win(-1, 3)
    if expand_attack:
        row, col = expand_attack
        board[row][col] = -1
        return True

    # 7. Kiểm soát khu vực trung tâm
    center_priority_cells = get_center_priority()
    if center_priority_cells:
        row, col = center_priority_cells[0]
        board[row][col] = -1
        return True

    # 8. Đánh gần các quân cờ đã có
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == -1:  # Gần các quân của AI
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    nr, nc = row + dr, col + dc
                    if is_valid_cell(nr, nc):
                        board[nr][nc] = -1
                        return True

    # 9. Đánh ngẫu nhiên nếu không có lựa chọn nào khác
    empty_cells = [(row, col) for row in range(ROWS) for col in range(COLS) if board[row][col] == 0]
    if empty_cells:
        row, col = random.choice(empty_cells)
        board[row][col] = -1
        return True

    return False



def main():
    game_mode = display_start_screen()
    global board, current_player, winner, x_kachi, o_kachi, games_played, final_winner, click
    run = True
    blink = True
    blink_timer = pygame.time.get_ticks()
    show_restart_message = False
    winner_display_time = None
    # Thời gian cho mỗi lượt
    turn_time = 40  # Thời gian tối đa cho mỗi lượt (giây)
    time_remaining = turn_time  # Thời gian còn lại của lượt hiện tại
    turn_start_time = None  # Thời gian bắt đầu của lượt hiện tại

    while run:
        # Khởi tạo thời gian bắt đầu lượt
        if turn_start_time is None and not winner and not final_winner:
            turn_start_time = pygame.time.get_ticks()

        # Tính toán thời gian còn lại
        if turn_start_time:
            elapsed_time = (pygame.time.get_ticks() - turn_start_time) // 1000  # Thời gian đã trôi qua (giây)
            time_remaining = max(turn_time - elapsed_time, 0)

        # Kiểm tra nếu hết thời gian
        if time_remaining <= 0 and not winner and not final_winner:
            if current_player == 1:
                winner = 'O が勝ち!'
                o_kachi += 1
            else:
                winner = 'X が勝ち!'
                x_kachi += 1
            games_played += 1
            turn_start_time = None  # Reset thời gian cho lượt tiếp theo
            time_remaining = turn_time
            current_player *= -1  # Đổi lượt
            if x_kachi == 2 or o_kachi == 2:  # Nếu một trong hai người thắng đủ 2 ván
                final_winner = f"{'X' if x_kachi == 2 else 'O'} が優勝"
                show_restart_message = True
            else:
                show_restart_message = True
                click = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                turn_start_time = pygame.time.get_ticks()  # Đặt lại thời gian sau mỗi nước đi
                if back_button_rect.collidepoint(pos):
                    reset_game()
                    game_mode = display_start_screen()
                    click = False
                if game_mode == 0:
                    handle_click(pos)  # Xử lý click cho người chơi
                    
                if game_mode == 1:
                    if current_player == 1 and not winner and not final_winner:  # Lượt của nguoi (X)
                        handle_click(pos)
                        
                    if current_player == -1 and not winner and not final_winner:  # Lượt của máy (O)
                        current_player = 1
                        ai_move()  # AI tự động đánh
                
                        
                        
                        
                            
                                
                        
                if final_winner:
                    continue  # Không xử lý thêm sự kiện nếu đã có người thắng

                # Kiểm tra lại nếu có người thắng và chưa có người thắng chung cuộc
                if winner and not final_winner:
                    board = reset_board()
                    current_player = 1  # Khởi động lại lượt chơi
                    winner = None
                    click = True
                    show_restart_message = False  # Tắt thông báo restart
                    turn_start_time = pygame.time.get_ticks()  # Đặt lại thời gian bắt đầu lượt
                elif not winner:
                    handle_click(pos)  # Chỉ cho phép người chơi click nếu chưa có người thắng
                # Kiểm tra thắng sau khi click (X hoặc O)
                if check_win(board, 1):
                    winner = 'X が勝ち'
                    x_kachi += 1
                    games_played += 1
                    winner_display_time = pygame.time.get_ticks()
                    turn_start_time = None  # Reset thời gian cho lượt tiếp theo
                elif check_win(board, -1):
                    winner = 'O が勝ち!'
                    o_kachi += 1
                    games_played += 1
                    winner_display_time = pygame.time.get_ticks()
                    turn_start_time = None  # Reset thời gian cho lượt tiếp theo

                if x_kachi == 2 or o_kachi == 2:
                    final_winner = f"{'X' if x_kachi == 2 else 'O'} が優勝"
                    show_restart_message = True
                    click = False
                    turn_start_time = None  # Không cần thiết phải tiếp tục đếm thời gian khi có người chiến thắng

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and final_winner:
                # Reset tất cả nếu bấm ESC khi có người thắng chung cuộc
                board = reset_board()
                current_player = 1
                winner = None
                x_kachi = o_kachi = games_played = 0
                final_winner = None
                show_restart_message = False
                click = False

        WIN.fill(WHITE)
        draw_footer_area()
        draw_extension_area()  # Vẽ vùng mở rộng
        draw_grid()  # Vẽ lưới khu vực chơi
        draw_board(board)  # Vẽ bàn cờ
        # Hiển thị thời gian còn lại
        if not final_winner:
            font = pygame.font.Font('NotoSansJP-Light.ttf', 24)
            timer_text = f"Time: {time_remaining}s"
            timer_label = font.render(timer_text, True, RED)
            WIN.blit(timer_label, (10, 60))
        if final_winner:
            font = pygame.font.Font(Font, 36)
            text = font.render(final_winner, True, BLACK)
            WIN.blit(text, ((WIDTH - text.get_width()) // 2, (HEIGHT - text.get_height()) // 2 - 50))
            WIN.blit(cup_image, ((WIDTH - cup_image.get_width()) // 2, (HEIGHT // 2)))  # Hiển thị hình cúps
        elif winner:
            font = pygame.font.Font(Font, 36)
            text = font.render(winner, True, BLACK)
            WIN.blit(text, ((WIDTH - text.get_width()) // 2, (HEIGHT - text.get_height()) // 2 - 50))   
            if winner_display_time and pygame.time.get_ticks() - winner_display_time > 1500:
                show_restart_message = True
                click = True
        if show_restart_message:
            if pygame.time.get_ticks() - blink_timer > 550:
                blink = not blink
                blink_timer = pygame.time.get_ticks()

            if blink:
                if final_winner:
                    reset_text = font.render("Press ESC to Restart", True, BLACK)
                    WIN.blit(reset_text, ((WIDTH - reset_text.get_width()) // 2, HEIGHT // 2 + cup_image.get_height() + 20))
                elif winner:
                    reset_text = font.render('Click to Start', True, BLACK)
                    
                    WIN.blit(reset_text, ((WIDTH - reset_text.get_width()) // 2, (HEIGHT - reset_text.get_height()) // 2))
                else:
                    reset_text = False

        pygame.display.update()

    pygame.quit()
main()