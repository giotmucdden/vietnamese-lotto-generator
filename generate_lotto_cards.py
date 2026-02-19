#!/usr/bin/env python3
"""
Vietnamese Lotto Card Generator
Generates 30 lotto cards (15 sets of 2) with decorative lion frame
- Each set contains all numbers 1-90
- Exactly 5 numbers per row
- Numbers distributed by column ranges
"""

from PIL import Image, ImageDraw, ImageFont
import random
import os

# 15 color schemes for the 15 sets
COLOR_SCHEMES = [
    ('#FFB6C1', '#C71585'),  # 1. Pink
    ('#FFE4B5', '#FF8C00'),  # 2. Orange
    ('#E0FFE0', '#228B22'),  # 3. Green
    ('#E0F0FF', '#1E90FF'),  # 4. Blue
    ('#FFE4E1', '#DC143C'),  # 5. Red
    ('#F0E68C', '#DAA520'),  # 6. Gold
    ('#E6E6FA', '#9370DB'),  # 7. Purple
    ('#FFE4CC', '#D2691E'),  # 8. Brown
    ('#E0FFFF', '#00CED1'),  # 9. Cyan
    ('#FFE4F0', '#FF1493'),  # 10. Deep Pink
    ('#F5F5DC', '#8B4513'),  # 11. Beige/Brown
    ('#F0FFF0', '#32CD32'),  # 12. Lime Green
    ('#FFF0F5', '#C71585'),  # 13. Lavender Pink
    ('#FFFACD', '#FFD700'),  # 14. Lemon Yellow
    ('#F0F8FF', '#4169E1'),  # 15. Alice Blue
]

# Card layout coordinates (adjust to match your frame)
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
        
        # Distribute by column ranges
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
            else:
                by_column[8].append(num)
        
        # Place randomly in rows
        for col in range(9):
            nums = by_column[col]
            available_rows = list(range(9))
            random.shuffle(available_rows)
            
            for i, num in enumerate(nums):
                if i < len(available_rows):
                    row = available_rows[i]
                    card[row][col] = num
        
        # Rebalance to exactly 5 per row
        max_iterations = 100
        for iteration in range(max_iterations):
            all_correct = True
            
            for row in range(9):
                count = sum(1 for cell in card[row] if cell is not None)
                
                if count < 5:
                    needed = 5 - count
                    all_correct = False
                    empty_cols = [c for c in range(9) if card[row][c] is None]
                    
                    for col in empty_cols:
                        if needed == 0:
                            break
                        for other_row in range(9):
                            if other_row == row:
                                continue
                            other_count = sum(1 for cell in card[other_row] if cell is not None)
                            if other_count > 5 and card[other_row][col] is not None:
                                card[row][col] = card[other_row][col]
                                card[other_row][col] = None
                                needed -= 1
                                break
                
                elif count > 5:
                    excess = count - 5
                    all_correct = False
                    filled_cols = [c for c in range(9) if card[row][c] is not None]
                    random.shuffle(filled_cols)
                    
                    for col in filled_cols:
                        if excess == 0:
                            break
                        num_to_move = card[row][col]
                        for other_row in range(9):
                            if other_row == row:
                                continue
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
    """Create a single lotto card with the given grid and color scheme"""
    empty_color, grid_color = color_scheme
    
    # Load frame
    frame = Image.open(frame_path)
    frame = frame.resize((2480, 3508), Image.Resampling.LANCZOS)
    
    card_width = CARD_RIGHT - CARD_LEFT
    card_height = CARD_BOTTOM - CARD_TOP
    
    cell_height = card_height // 10
    gap_height = (card_height - (9 * cell_height)) // 2
    cell_width = card_width // 9
    
    card_img = Image.new('RGB', (card_width, card_height), '#FFFFFF')
    draw = ImageDraw.Draw(card_img)
    
    # Load fonts
    try:
        number_font = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf', 120)
        text_font = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf', 80)
        text_font_italic = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf', 80)
    except:
        number_font = text_font = text_font_italic = ImageFont.load_default()
    
    # Draw grid
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
    
    # Add "LÔ TÔ" text in first gap
    gap1_y = 3 * cell_height + gap_height // 2
    text1 = "LÔ TÔ"
    bbox1 = draw.textbbox((0, 0), text1, font=text_font)
    draw.text(((card_width - (bbox1[2] - bbox1[0])) // 2, gap1_y - (bbox1[3] - bbox1[1]) // 2), 
             text1, fill=grid_color, font=text_font)
    
    # Add "TY Family" text in second gap
    gap2_y = 6 * cell_height + gap_height + gap_height // 2
    ty_bbox = draw.textbbox((0, 0), "TY ", font=text_font)
    fam_bbox = draw.textbbox((0, 0), "Family", font=text_font_italic)
    total_w = (ty_bbox[2] - ty_bbox[0]) + (fam_bbox[2] - fam_bbox[0])
    start_x = (card_width - total_w) // 2
    draw.text((start_x, gap2_y - max(ty_bbox[3] - ty_bbox[1], fam_bbox[3] - fam_bbox[1]) // 2), 
             "TY ", fill=grid_color, font=text_font)
    draw.text((start_x + (ty_bbox[2] - ty_bbox[0]), gap2_y - max(ty_bbox[3] - ty_bbox[1], fam_bbox[3] - fam_bbox[1]) // 2), 
             "Family", fill=grid_color, font=text_font_italic)
    
    # Paste card onto frame
    frame.paste(card_img, (CARD_LEFT, CARD_TOP))
    frame.save(filename)

def main():
    """Generate all 30 lotto cards"""
    frame_path = 'lion_frame_APPROVED_FINAL.png'
    
    if not os.path.exists(frame_path):
        print(f"❌ Error: Frame image '{frame_path}' not found!")
        print("Please place the lion frame image in the same directory as this script.")
        return
    
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    
    print("🎨 Generating 30 Vietnamese Lotto Cards")
    print("=" * 60)
    
    card_num = 1
    for set_num, color_scheme in enumerate(COLOR_SCHEMES, 1):
        c1, c2 = generate_set_numbers()
        
        # Verify all 90 numbers present
        all_nums = []
        for r in range(9):
            for c in range(9):
                if c1[r][c]: all_nums.append(c1[r][c])
                if c2[r][c]: all_nums.append(c2[r][c])
        
        status = "✅" if sorted(all_nums) == list(range(1, 91)) else "❌"
        
        # Generate both cards in the set
        filename1 = f'{output_dir}/lotto_card_{card_num:02d}.png'
        create_lotto_card(c1, color_scheme, filename1, frame_path)
        card_num += 1
        
        filename2 = f'{output_dir}/lotto_card_{card_num:02d}.png'
        create_lotto_card(c2, color_scheme, filename2, frame_path)
        
        print(f"Set {set_num:02d}: Cards {card_num-1:02d} & {card_num:02d} {status}")
        card_num += 1
    
    print("=" * 60)
    print(f"✅ All 30 cards generated successfully!")
    print(f"📁 Output directory: {output_dir}/")

if __name__ == '__main__':
    main()
