# Vietnamese Lotto Card Generator

Generate Vietnamese-style lotto cards with decorative lion frame.

## Features

- **40 cards (20 sets of 2 cards each)**
- **20 obviously different color schemes**
- All 90 numbers (1-90) distributed across each set
- Exactly 5 numbers per row
- **NEW: Max 2 consecutive empty cells per row**
- Numbers organized by column ranges (1-9, 10-19, ..., 80-90)
- Decorative lion frame with golden scroll rods
- "LÔ TÔ" and "TY Family" text in matching colors

## Rules

1. **Column Distribution**: Numbers are placed in columns based on their value:
   - Column 0: 1-9
   - Column 1: 10-19
   - Column 2: 20-29
   - ...
   - Column 8: 80-90

2. **Row Balance**: Each row has exactly 5 numbers and 4 empty cells

3. **Empty Cell Pattern**: No more than 2 consecutive empty cells in any row (prevents long gaps)

4. **Complete Set**: Each pair of cards contains all numbers 1-90 exactly once

## Usage

```bash
python3 generate_lotto_cards.py
```

## Output

- Generates 40 PNG files (lotto_card_01.png to lotto_card_40.png)
- Each pair forms a complete set with all numbers 1-90
- Card dimensions: 2480x3508 pixels

## Sample Cards

See `sample_cards/` directory for examples showing different color schemes.
