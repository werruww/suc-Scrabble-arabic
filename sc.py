import tkinter as tk
from tkinter import messagebox, font
import random
from collections import Counter

# إعدادات اللعبة
ARABIC_LETTERS = {
    'ا': 1, 'ب': 3, 'ت': 1, 'ث': 4, 'ج': 2, 'ح': 3, 'خ': 5, 'د': 1, 'ذ': 4,
    'ر': 1, 'ز': 4, 'س': 1, 'ش': 5, 'ص': 3, 'ض': 5, 'ط': 3, 'ظ': 6, 'ع': 2,
    'غ': 6, 'ف': 3, 'ق': 6, 'ك': 2, 'ل': 1, 'م': 1, 'ن': 1, 'ه': 2, 'و': 2,
    'ي': 2, 'ة': 3, 'ء': 6, 'أ': 1, 'إ': 1, 'آ': 4, 'ى': 1, 'ؤ': 5, 'ئ': 5
}

BOARD_SIZE = 15
TILE_SIZE = 40  # حجم كل خانة بالبكسل

class ArabicScrabbleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("سكرابل العربية")
        self.root.geometry("1200x800")

        # --- إضافة جديدة: تحميل القاموس ---
        self.valid_words = self.load_words()
        
        # إعدادات اللاعبين
        self.players = ["اللاعب 1", "اللاعب 2"]
        self.scores = [0, 0]
        self.current_player = 0
        
        # إنشاء الحقيبة
        self.tile_bag = self.create_tile_bag()
        self.player_tiles = [[], []]
        
        # اللوحة (15x15)
        self.board = [['' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.board_multipliers = [
            ['3W', '1', '1', '2L', '1', '1', '1', '3W', '1', '1', '1', '2L', '1', '1', '3W'],
            ['1', '2W', '1', '1', '1', '3L', '1', '1', '1', '3L', '1', '1', '1', '2W', '1'],
            ['1', '1', '2W', '1', '1', '1', '2L', '1', '2L', '1', '1', '1', '2W', '1', '1'],
            ['2L', '1', '1', '2W', '1', '1', '1', '2L', '1', '1', '1', '2W', '1', '1', '2L'],
            ['1', '1', '1', '1', '2W', '1', '1', '1', '1', '1', '2W', '1', '1', '1', '1'],
            ['1', '3L', '1', '1', '1', '3L', '1', '1', '1', '3L', '1', '1', '1', '3L', '1'],
            ['1', '1', '2L', '1', '1', '1', '2L', '1', '2L', '1', '1', '1', '2L', '1', '1'],
            ['3W', '1', '1', '2L', '1', '1', '1', '2W', '1', '1', '1', '2L', '1', '1', '3W'],
            ['1', '1', '2L', '1', '1', '1', '2L', '1', '2L', '1', '1', '1', '2L', '1', '1'],
            ['1', '3L', '1', '1', '1', '3L', '1', '1', '1', '3L', '1', '1', '1', '3L', '1'],
            ['1', '1', '1', '1', '2W', '1', '1', '1', '1', '1', '2W', '1', '1', '1', '1'],
            ['2L', '1', '1', '2W', '1', '1', '1', '2L', '1', '1', '1', '2W', '1', '1', '2L'],
            ['1', '1', '2W', '1', '1', '1', '2L', '1', '2L', '1', '1', '1', '2W', '1', '1'],
            ['1', '2W', '1', '1', '1', '3L', '1', '1', '1', '3L', '1', '1', '1', '2W', '1'],
            ['3W', '1', '1', '2L', '1', '1', '1', '3W', '1', '1', '1', '2L', '1', '1', '3W']
        ]
        
        # --- تعديلات: لتتبع حالة اللعبة ---
        self.selected_tile_button = None
        self.current_move_tiles = [] # يخزن (الحرف, الصف, العمود) للحركة الحالية

        # تهيئة الواجهة
        self.setup_ui()
        self.start_game()
    
    def load_words(self):
        try:
            with open('arabic_words.txt', 'r', encoding='utf-8') as f:
                words = set()
                for line in f:
                    # القاموس الجديد يحتوي على الكلمة وعدد تكرارها، نحن نحتاج الكلمة فقط
                    word = line.split()[0]
                    words.add(word.strip())
                return words
        except FileNotFoundError:
            messagebox.showerror("خطأ ملف", "لم يتم العثور على ملف القاموس 'arabic_words.txt'.\nسيتم استخدام قائمة كلمات افتراضية صغيرة.")
            return {'سلام', 'مرحبا', 'كتاب', 'بيت', 'شمس'}

    def is_valid_word(self, word):
        return word in self.valid_words
    
    def create_tile_bag(self):
        distribution = {
            'ا': 14, 'ب': 4, 'ت': 6, 'ث': 2, 'ج': 3, 'ح': 3, 'خ': 2, 'د': 6, 'ذ': 2,
            'ر': 8, 'ز': 2, 'س': 6, 'ش': 2, 'ص': 2, 'ض': 1, 'ط': 2, 'ظ': 1, 'ع': 5,
            'غ': 1, 'ف': 3, 'ق': 1, 'ك': 4, 'ل': 8, 'م': 5, 'ن': 7, 'ه': 4, 'و': 5,
            'ي': 5, 'ة': 2, 'ء': 1, 'أ': 2, 'إ': 2, 'آ': 1, 'ى': 2, 'ؤ': 1, 'ئ': 1
        }
        bag = []
        for letter, count in distribution.items():
            bag.extend([letter] * count)
        random.shuffle(bag)
        return bag
    
    def setup_ui(self):
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(side=tk.LEFT, padx=20, pady=20)
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.Y)
        self.canvas = tk.Canvas(self.board_frame, width=BOARD_SIZE*TILE_SIZE, height=BOARD_SIZE*TILE_SIZE)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_board_click)
        self.draw_board()
        self.player_labels = []
        for i in range(2):
            label = tk.Label(self.control_frame, text=f"{self.players[i]}: 0 نقطة", font=("Arial", 14))
            label.pack(pady=5)
            self.player_labels.append(label)
        
        tk.Button(self.control_frame, text="تسليم الكلمة", command=self.submit_word, bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).pack(pady=10, fill=tk.X)
        tk.Button(self.control_frame, text="تراجع عن الحركة", command=self.reset_move, bg="#f44336", fg="white", font=("Arial", 12)).pack(pady=5, fill=tk.X)
        tk.Button(self.control_frame, text="تخطي الدور", command=self.skip_turn, bg="#FFC107", fg="black", font=("Arial", 12)).pack(pady=5, fill=tk.X)
        
        self.tile_frames = []
        for i in range(2):
            frame = tk.Frame(self.control_frame)
            frame.pack(pady=10, expand=True)
            self.tile_frames.append(frame)
        
        self.status_label = tk.Label(self.root, text=f"دور: {self.players[self.current_player]}", font=("Arial", 16, "bold"), bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                x1, y1 = j * TILE_SIZE, i * TILE_SIZE
                x2, y2 = x1 + TILE_SIZE, y1 + TILE_SIZE
                multiplier = self.board_multipliers[i][j]
                
                color_map = {'2L': "#a0d8ef", '3L': "#4CAF50", '2W': "#FFC107", '3W': "#f44336", '1': "#f5f5dc"}
                color = color_map.get(multiplier, "#f5f5dc")
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="grey")
                if multiplier != '1':
                    self.canvas.create_text(x1 + TILE_SIZE/2, y1 + TILE_SIZE/2, text=multiplier, font=("Arial", 8), fill="black")
                
                if self.board[i][j]:
                    self.canvas.create_text(x1 + TILE_SIZE/2, y1 + TILE_SIZE/2, text=self.board[i][j], font=("Arial", 16, "bold"))
        
        for letter, r, c in self.current_move_tiles:
            x1, y1 = c * TILE_SIZE, r * TILE_SIZE
            self.canvas.create_text(x1 + TILE_SIZE/2, y1 + TILE_SIZE/2, text=letter, font=("Arial", 16, "bold"), fill="blue")

    def start_game(self):
        for i in range(2):
            self.draw_player_tiles(i, 7)
        self.update_tile_display()

    def draw_player_tiles(self, player, num):
        for _ in range(num):
            if self.tile_bag:
                self.player_tiles[player].append(self.tile_bag.pop(0))

    def update_tile_display(self):
        for i in range(2):
            for widget in self.tile_frames[i].winfo_children():
                widget.destroy()

            is_current = (i == self.current_player)
            tk.Label(self.tile_frames[i], text=f"حروف {self.players[i]}", font=("Arial", 12, "underline" if is_current else "normal")).pack()
            
            button_frame = tk.Frame(self.tile_frames[i])
            button_frame.pack()

            for tile in self.player_tiles[i]:
                state = tk.NORMAL if is_current else tk.DISABLED
                
                btn = tk.Button(button_frame, text=tile, width=3, height=1, font=("Arial", 14),
                                state=state, relief=tk.RAISED)
                btn.config(command=lambda b=btn: self.select_tile(b))
                
                btn.pack(side=tk.LEFT, padx=2)
    
    def select_tile(self, button):
        if self.selected_tile_button:
            self.selected_tile_button.config(relief=tk.RAISED, bg='SystemButtonFace')
        
        self.selected_tile_button = button
        self.selected_tile_button.config(relief=tk.SUNKEN, bg='lightblue')

    def on_board_click(self, event):
        if not self.selected_tile_button:
            messagebox.showwarning("خطأ", "الرجاء اختيار حرف أولاً!")
            return

        c = event.x // TILE_SIZE
        r = event.y // TILE_SIZE

        if r >= BOARD_SIZE or c >= BOARD_SIZE: return

        if self.board[r][c] or any(row == r and col == c for _, row, col in self.current_move_tiles):
            messagebox.showerror("خطأ", "هذه الخانة مشغولة!")
            return

        letter = self.selected_tile_button['text']
        self.current_move_tiles.append((letter, r, c))
        
        self.selected_tile_button.pack_forget()
        self.selected_tile_button = None
        self.draw_board()

    def reset_move(self):
        self.current_move_tiles.clear()
        self.update_tile_display()
        self.draw_board()

    def submit_word(self):
        if not self.current_move_tiles:
            messagebox.showerror("خطأ", "يجب وضع حرف واحد على الأقل!")
            return
        
        rows = {r for _, r, _ in self.current_move_tiles}
        cols = {c for _, _, c in self.current_move_tiles}

        is_horizontal = len(rows) == 1
        is_vertical = len(cols) == 1

        if not (is_horizontal or is_vertical):
            messagebox.showerror("كلمة غير صالحة", "يجب أن تكون الحروف في صف أو عمود واحد!")
            return

        if is_horizontal:
            r = list(rows)[0]
            min_c = min(c for _, _, c in self.current_move_tiles)
            max_c = max(c for _, _, c in self.current_move_tiles)
            # Extend to connect to existing letters
            while min_c > 0 and self.board[r][min_c - 1]: min_c -= 1
            while max_c < BOARD_SIZE - 1 and self.board[r][max_c + 1]: max_c += 1
            
            word = ""
            for c in range(min_c, max_c + 1):
                placed_letter = next((letter for letter, row, col in self.current_move_tiles if row == r and col == c), None)
                if placed_letter:
                    word += placed_letter
                elif self.board[r][c]:
                    word += self.board[r][c]
                else:
                    messagebox.showerror("كلمة غير صالحة", "لا يمكن ترك فراغات في الكلمة.")
                    return
        else: # is_vertical
            c = list(cols)[0]
            min_r = min(r for _, r, _ in self.current_move_tiles)
            max_r = max(r for _, r, _ in self.current_move_tiles)
            # Extend to connect to existing letters
            while min_r > 0 and self.board[min_r - 1][c]: min_r -= 1
            while max_r < BOARD_SIZE - 1 and self.board[max_r + 1][c]: max_r += 1

            word = ""
            for r in range(min_r, max_r + 1):
                placed_letter = next((letter for letter, row, col in self.current_move_tiles if row == r and col == c), None)
                if placed_letter:
                    word += placed_letter
                elif self.board[r][c]:
                    word += self.board[r][c]
                else:
                    messagebox.showerror("كلمة غير صالحة", "لا يمكن ترك فراغات في الكلمة.")
                    return
        
        if self.is_valid_word(word):
            score = 0
            word_multiplier = 1
            for letter, r, c in self.current_move_tiles:
                letter_score = ARABIC_LETTERS.get(letter, 0)
                multiplier_str = self.board_multipliers[r][c]
                if multiplier_str == '2L': letter_score *= 2
                elif multiplier_str == '3L': letter_score *= 3
                elif multiplier_str == '2W': word_multiplier *= 2
                elif multiplier_str == '3W': word_multiplier *= 3
                score += letter_score
            
            final_score = score * word_multiplier
            self.scores[self.current_player] += final_score

            messagebox.showinfo("كلمة صحيحة!", f"كلمة '{word}' صحيحة!\nحصلت على {final_score} نقطة.")
            
            for letter, r, c in self.current_move_tiles:
                self.board[r][c] = letter
                self.player_tiles[self.current_player].remove(letter)

            self.draw_player_tiles(self.current_player, len(self.current_move_tiles))
            self.current_move_tiles.clear()
            self.end_turn()
        else:
            messagebox.showerror("كلمة خاطئة", f"الكلمة '{word}' غير موجودة في القاموس.")

    def skip_turn(self):
        self.reset_move()
        self.end_turn()

    def end_turn(self):
        self.current_player = 1 - self.current_player
        self.draw_board()
        self.update_tile_display()
        self.update_scores()
        self.status_label.config(text=f"دور: {self.players[self.current_player]}")

    def update_scores(self):
        for i in range(2):
            self.player_labels[i].config(text=f"{self.players[i]}: {self.scores[i]} نقطة")

if __name__ == "__main__":
    root = tk.Tk()
    app = ArabicScrabbleGUI(root)
    root.mainloop()