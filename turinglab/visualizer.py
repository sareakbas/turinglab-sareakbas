import os
from PIL import Image, ImageDraw

class TMVisualizer:
    def __init__(self, tm):
        self.tm = tm
        self.blank_sym = getattr(tm, 'blank', getattr(tm, 'blank_symbol', 'B'))

    def run_and_create_gif(self, input_string, output_file="docs/images/tm_animation.gif"):
        frames = []
        tape = {i: char for i, char in enumerate(input_string)}
        head = 0
        state = self.tm.start_state
        
        print("Kareler çiziliyor, lütfen bekleyin...")
        
        while state not in getattr(self.tm, 'accept_states', set()) and state not in getattr(self.tm, 'reject_states', set()):
            frames.append(self._draw_frame(tape, head, state))
            
            symbol = tape.get(head, self.blank_sym)
            key = (state, symbol)
            
            if key not in self.tm.transitions:
                break
            
        
            trans = self.tm.transitions[key]
            
            if isinstance(trans, dict):
                next_state = trans.get("next")
                write_sym = trans.get("write")
                move_dir = trans.get("move")
            else:
                
                next_state, write_sym, move_dir = trans[:3]
            
            
            tape[head] = write_sym
            head += 1 if move_dir == 'R' else (-1 if move_dir == 'L' else 0)
            state = next_state
            
       
        frames.append(self._draw_frame(tape, head, state))
        
        
        if frames:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            frames[0].save(
                output_file, 
                save_all=True, 
                append_images=frames[1:], 
                duration=600, 
                loop=0
            )
            print(f"🎉 Animasyon başarıyla oluşturuldu: {output_file}")
            
        accept_states = getattr(self.tm, 'accept_states', set())
        return state in accept_states

    def _draw_frame(self, tape, head, state):
        width, height = 700, 200
        img = Image.new("RGB", (width, height), "#f8f9fa")
        draw = ImageDraw.Draw(img)
        
        cell_w = 50
        start_y = 80
        
        min_idx = min(tape.keys()) if tape else 0
        max_idx = max(tape.keys()) if tape else 0
        
        min_idx = min(min_idx, head - 5)
        max_idx = max(max_idx, head + 5)
        
        draw.text((20, 20), f"Mevcut Durum: {state}", fill="#d90429")
        
        for i in range(min_idx, max_idx + 1):
            x = (width // 2) + (i - head) * cell_w - (cell_w // 2)
            char = tape.get(i, self.blank_sym)
            
            draw.rectangle([x, start_y, x + cell_w, start_y + cell_w], outline="#343a40", width=2)
            draw.text((x + 20, start_y + 18), str(char), fill="black")
            
            if i == head:
                poly = [x + 25, start_y + cell_w + 5, x + 10, start_y + cell_w + 20, x + 40, start_y + cell_w + 20]
                draw.polygon(poly, fill="#d90429")
                
        return img