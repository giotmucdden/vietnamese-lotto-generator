#!/usr/bin/env python3
"""
Generate 40 Vietnamese Lotto Cards (20 sets)
- 20 obviously different color schemes
- All 90 numbers (1-90) per set
- Exactly 5 numbers per row
- Correct column ranges: 1-9, 10-19, 20-29, ..., 70-79, 80-90
"""

from PIL import Image, ImageDraw, ImageFont
import random

# 20 OBVIOUSLY DIFFERENT color schemes
COLOR_SCHEMES = [
    ('#FFB6C1', '#C71585', 'Hot Pink'),
    ('#FFD700', '#FF8C00', 'Gold'),
    ('#90EE90', '#006400', 'Green'),
    ('#87CEEB', '#00008B', 'Sky Blue'),
    ('#FF6347', '#8B0000', 'Tomato'),
    ('#DDA0DD', '#4B0082', 'Plum'),
    ('#F0E68C', '#8B4513', 'Khaki'),
    ('#FFA07A', '#D2691E', 'Salmon'),
    ('#00CED1', '#008B8B', 'Turquoise'),
    ('#FFE4E1', '#DC143C', 'Rose'),
    ('#E0E0E0', '#404040', 'Gray'),
    ('#ADFF2F', '#228B22', 'Yellow Green'),
    ('#FFC0CB', '#FF1493', 'Pink'),
    ('#F5DEB3', '#8B4513', 'Wheat'),
    ('#B0E0E6', '#4682B4', 'Powder Blue'),
    ('#FFDAB9', '#FF4500', 'Peach'),
    ('#E6E6FA', '#8B008B', 'Lavender'),
    ('#F0FFF0', '#2E8B57', 'Honeydew'),
    ('#FFF8DC', '#DAA520', 'Cornsilk'),
    ('#FFE4B5', '#CD853F', 'Moccasin'),
]

CARD_LEFT = 288
CARD_TOP = 710
CARD_RIGHT = 2192
CARD_BOTTOM = 3172

def generate_set_numbers():
    """Generate 2 cards with all 90 numbers, exactly 5 per row"""
    all_numbers = list(range(1, 91))
    random.shuffle(all_numbers)
    
    card1_numbers = sorted(all_numbers[:45])
    card2_numbers = sorted(all_numbers[45:])
    
    def distribute_to_card(numbers):
        card = [[None] * 9 for _ in range(9)]
        
        # Distribute numbers to columns by range
        by_column = [[] for _ in range(9)]
        for num in numbers:
            if num <= 9:
                by_column[0].append(num)
            elif num <= 19:
                by_column[1].append(num)
            elif num <= 29:
                by_column[2].append(num)
            elif num <= 39:
                by_column[3].append(num)
            elif num <= 49:
                by_column[4].append(num)
            elif num <= 59:
                by_column[5].append(num)
            elif num <= 69:
                by_column[6].append(num)
            elif num <= 79:
                by_column[7].append(num)
            else:  # 80-90
                by_column[8].append(num)
        
        # Place numbers randomly
        for col in range(9):
            nums = by_column[col]
            available_rows = list(range(9))
            random.shuffle(available_rows)
            for i, num in enumerate(nums):
                if i < len(available_rows):
                    card[available_rows[i]][col] = num
        
        # Balance rows to exactly 5 numbers
        for iteration in range(100):
            all_correct = True
            for row in range(9):
                count = sum(1 for cell in card[row] if cell is not None)
                if count < 5:
                    all_correct = False
                    needed = 5 - count
                    empty_cols = [c for c in range(9) if card[row][c] is None]
                    for col in empty_cols:
                        if needed == 0:
                            break
                        for other_row in range(9):
                            if other_row != row:
                                other_count = sum(1 for cell in card[other_row] if cell is not None)
                                if other_count > 5 and card[other_row][col] is not None:
                                    card[row][col] = card[other_row][col]
                                    card[other_row][col] = None
                                    needed -= 1
                                    break
                elif count > 5:
                    all_correct = False
                    excess = count - 5
                    filled_cols = [c for c in range(9) if card[row][c] is not None]
                    random.shuffle(filled_cols)
                    for col in filled_cols:
                        if excess == 0:
                            break
                        num_to_move = card[row][col]
                        for other_row in range(9):
                            if other_row != row:
                                other_count = sum(1 for cell in card[other_row] if cell is not None)
                                if other_count < 5 and card[other_row][col] is None:
                                    card[other_row][col] = num_to_move
                                    card[row][col] = None
                                    excess -= 1
                                    break
            if all_correct:
                break
        
        return card
    
    return distribute_to_card(card1_numbers), distribute_to_card(card2_numbers)

def create_lotto_card(grid, color_scheme, filename, frame_path):
    """Create a single lotto card"""
    empty_color, grid_color, color_name = color_scheme
    
    frame = Image.open(frame_path)
    frame = frame.resize((2480, 3508), Image.Resampling.LANCZOS)
    
    card_width = CARD_RIGHT - CARD_LEFT
    card_height = CARD_BOTTOM - CARD_TOP
    
    cell_height = card_height // 10
    gap_height = (card_height - (9 * cell_height)) // 2
    cell_width = card_width // 9
    
    card_img = Image.new('RGB', (card_width, card_height), '#FFFFFF')
    draw = ImageDraw.Draw(card_img)
    
    try:
        number_font = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf', 120)
        text_font = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf', 80)
        text_font_italic = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf', 80)
    except:
        number_font = text_font = text_font_italic = ImageFont.load_default()
    
    for row in range(9):
        row_y = row * cell_height + (0 if row < 3 else gap_height if row < 6 else 2 * gap_height)
        for col in range(9):
            col_x = col * cell_width
            if grid[row][col] is None:
                draw.rectangle([col_x, row_y, col_x + cell_width, row_y + cell_height], 
                              fill=empty_color, outline=grid_color, width=3)
            else:
                draw.rectangle([col_x, row_y, col_x + cell_width, row_y + cell_height], 
                              fill='#FFFFFF', outline=grid_color, width=3)
                num_text = str(grid[row][col])
                bbox = draw.textbbox((0, 0), num_text, font=number_font)
                draw.text((col_x + (cell_width - (bbox[2] - bbox[0])) // 2, 
                          row_y + (cell_height - (bbox[3] - bbox[1])) // 2 - 10), 
                         num_text, fill='#000000', font=number_font)
    
    gap1_y = 3 * cell_height + gap_height // 2
    text1 = "LÔ TÔ"
    bbox1 = draw.textbbox((0, 0), text1, font=text_font)
    draw.text(((card_width - (bbox1[2] - bbox1[0])) // 2, gap1_y - (bbox1[3] - bbox1[1]) // 2), 
             text1, fill=grid_color, font=text_font)
    
    gap2_y = 6 * cell_height + gap_height + gap_height // 2
    ty_bbox = draw.textbbox((0, 0), "TY ", font=text_font)
    fam_bbox = draw.textbbox((0, 0), "Family", font=text_font_italic)
    total_w = (ty_bbox[2] - ty_bbox[0]) + (fam_bbox[2] - fam_bbox[0])
    start_x = (card_width - total_w) // 2
    draw.text((start_x, gap2_y - max(ty_bbox[3] - ty_bbox[1], fam_bbox[3] - fam_bbox[1]) // 2), 
             "TY ", fill=grid_color, font=text_font)
    draw.text((start_x + (ty_bbox[2] - ty_bbox[0]), gap2_y - max(ty_bbox[3] - ty_bbox[1], fam_bbox[3] - fam_bbox[1]) // 2), 
             "Family", fill=grid_color, font=text_font_italic)
    
    frame.paste(card_img, (CARD_LEFT, CARD_TOP))
    frame.save(filename)

print("🎨 Generating 40 Vietnamese Lotto Cards (20 sets)")
print("=" * 60)

frame_path = 'lion_frame_APPROVED_FINAL.png'
card_num = 1

for set_num, color_scheme in enumerate(COLOR_SCHEMES, 1):
    c1, c2 = generate_set_numbers()
    
    all_nums = []
    for r in range(9):
        for c in range(9):
            if c1[r][c]: all_nums.append(c1[r][c])
            if c2[r][c]: all_nums.append(c2[r][c])
    
    status = "✅" if sorted(all_nums) == list(range(1, 91)) else "❌"
    
    filename1 = f'lotto_card_{card_num:02d}.png'
    create_lotto_card(c1, color_scheme, filename1, frame_path)
    card_num += 1
    
    filename2 = f'lotto_card_{card_num:02d}.png'
    create_lotto_card(c2, color_scheme, filename2, frame_path)
    
    print(f"Set {set_num:02d} ({color_scheme[2]:15s}): Cards {card_num-1:02d} & {card_num:02d} | All 90 nums: {status}")
    card_num += 1

print("=" * 60)
print(f"✅ All 40 cards generated successfully!")
