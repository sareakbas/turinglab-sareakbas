import yaml

class MultiTapeResult:
    def __init__(self, final_tapes, accepted):
        self.final_tapes = final_tapes
        self.accepted = accepted

class MultiTapeTM:
    def __init__(self, config):
        self.name = config.get("name", "multi_tape_tm")
        self.num_tapes = config.get("num_tapes", 2)
        self.blank = config.get("blank", "B")
        self.start_state = config["start_state"]
        self.accept_states = set(config["accept_states"])
        self.reject_states = set(config.get("reject_states", []))
        
        # Geçişleri sözlüğe (dict) kaydediyoruz.
        # Anahtar: (durum, (okunan1, okunan2, ...))
        # Değer: (yeni_durum, (yazilan1, yazilan2, ...), (hareket1, hareket2, ...))
        self.transitions = {}
        for t in config["transitions"]:
            key = (t["state"], tuple(t["read"]))
            self.transitions[key] = (t["next"], tuple(t["write"]), tuple(t["move"]))

    @classmethod
    def from_yaml(cls, path):
        with open(path, "r", encoding="utf-8") as f:
            return cls(yaml.safe_load(f))

    def run(self, initial_inputs):
        # initial_inputs: her şerit için başlangıç kelimelerinin listesi (Örn: ["101", "11"])
        tapes = []
        heads = [0] * self.num_tapes
        
        # Şeritleri hazırlıyoruz
        for i in range(self.num_tapes):
            tape_dict = {}
            if i < len(initial_inputs):
                for j, char in enumerate(initial_inputs[i]):
                    tape_dict[j] = char
            tapes.append(tape_dict)
            
        current_state = self.start_state
        
        # Makine çalışmaya başlıyor
        while current_state not in self.accept_states and current_state not in self.reject_states:
            # Tüm kafaların altındaki harfleri aynı anda oku
            current_symbols = tuple(tapes[i].get(heads[i], self.blank) for i in range(self.num_tapes))
            state_key = (current_state, current_symbols)
            
            # Eğer bu duruma uygun bir kural yoksa reddet ve çık
            if state_key not in self.transitions:
                break 
                
            next_state, writes, moves = self.transitions[state_key]
            
            # Tüm şeritlere yaz ve kafaları bağımsız hareket ettir
            for i in range(self.num_tapes):
                tapes[i][heads[i]] = writes[i]
                if moves[i] == 'R':
                    heads[i] += 1
                elif moves[i] == 'L':
                    heads[i] -= 1
                # 'S' (Stay/Sabit) ise hareket etmez
                    
            current_state = next_state
            
        # Şeritlerin son halini temiz bir listeye çeviriyoruz
        final_tape_strings = []
        for tape in tapes:
            if not tape:
                final_tape_strings.append("")
                continue
            min_idx = min(tape.keys())
            max_idx = max(tape.keys())
            s = "".join(tape.get(i, self.blank) for i in range(min_idx, max_idx + 1))
            final_tape_strings.append(s)
            
        return MultiTapeResult(final_tape_strings, current_state in self.accept_states)