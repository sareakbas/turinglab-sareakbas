import yaml
from collections import deque

class NTMResult:
    def __init__(self, accepting_paths, rejected, max_depth_reached):
        self.accepting_paths = accepting_paths
        self.rejected = rejected
        self.max_depth_reached = max_depth_reached

class NonDeterministicTM:
    def __init__(self, config):
        self.name = config.get("name", "ntm")
        self.blank = config.get("blank", "B")
        self.start_state = config["start_state"]
        self.accept_states = set(config["accept_states"])
        self.reject_states = set(config.get("reject_states", []))
        
        # El Kitabı Şartı: Koruma Parametreleri
        self.max_depth = config.get("max_depth", 100)
        self.max_branches = config.get("max_branches", 1000)

        # NTM Geçişleri: Aynı key için birden fazla hedef olabilir, bu yüzden liste kullanıyoruz.
        self.transitions = {}
        for t in config["transitions"]:
            key = (t["state"], t["read"])
            if key not in self.transitions:
                self.transitions[key] = []
            self.transitions[key].append((t["next"], t["write"], t["move"]))

    @classmethod
    def from_yaml(cls, path):
        with open(path, "r", encoding="utf-8") as f:
            return cls(yaml.safe_load(f))

    def run(self, input_string):
        # Şeridi sözlük olarak başlat
        initial_tape = {i: char for i, char in enumerate(input_string)}
        
        # BFS Kuyruğu: (şerit_sözlüğü, kafa_pozisyonu, mevcut_durum, yol_geçmişi, derinlik)
        queue = deque([(initial_tape, 0, self.start_state, [], 0)])
        
        accepting_paths = []
        branches_explored = 0
        max_depth_reached = False

        while queue:
            # Koruma mekanizması: Maksimum dal sayısını aştık mı?
            if branches_explored >= self.max_branches:
                break
                
            tape, head, state, path, depth = queue.popleft()
            branches_explored += 1

            # Koruma mekanizması: Maksimum derinliği aştık mı?
            if depth > self.max_depth:
                max_depth_reached = True
                continue

            # Eğer makine kabul durumuna ulaştıysa bu başarılı paralel evreni (yolu) kaydet
            if state in self.accept_states:
                accepting_paths.append({
                    "tape": self._get_tape_string(tape),
                    "path": path + [state]
                })
                continue

            # Reddedilen durumlarda bu dalı öldür (kuyruğa ekleme)
            if state in self.reject_states:
                continue

            current_symbol = tape.get(head, self.blank)
            key = (state, current_symbol)

            if key in self.transitions:
                # Olası tüm yollar için paralel dallar (evrenler) yarat
                for next_state, write_sym, move_dir in self.transitions[key]:
                    new_tape = tape.copy() # Her dalın kendi bağımsız şeridi olmalı!
                    new_tape[head] = write_sym
                    
                    new_head = head + 1 if move_dir == 'R' else (head - 1 if move_dir == 'L' else head)
                    
                    # Geçmişi kaydet (Örn: q0(a->X,R))
                    new_path = path + [f"{state}({current_symbol}->{write_sym},{move_dir})"]
                    
                    queue.append((new_tape, new_head, next_state, new_path, depth + 1))

        return NTMResult(accepting_paths, len(accepting_paths) == 0, max_depth_reached)

    def _get_tape_string(self, tape):
        if not tape: return ""
        min_idx, max_idx = min(tape.keys()), max(tape.keys())
        return "".join(tape.get(i, self.blank) for i in range(min_idx, max_idx + 1))