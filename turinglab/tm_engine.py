import yaml
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class StepConfig:
    """Makinenin her bir adımındaki anlık durumunu tutar."""
    state: str
    tape: dict
    head_position: int

@dataclass
class RunResult:
    accepted: bool
    final_tape: str
    steps: int
    history: List[StepConfig] 
    reason: str

class Tape:
    def __init__(self, initial_content="", blank_symbol="B"):
        self.tape = {}
        self.blank_symbol = blank_symbol
        
        self.head_position = 0
        for i, char in enumerate(initial_content):
            self.tape[i] = char

    def read(self) -> str:
        return self.tape.get(self.head_position, self.blank_symbol)

    def write(self, char: str):
        self.tape[self.head_position] = char

    def move(self, direction: str):
        if direction == 'R':
            self.head_position += 1
        elif direction == 'L':
            self.head_position -= 1
        else:
            raise ValueError(f"Geçersiz hareket yönü: {direction}. Sadece 'R' veya 'L' olmalıdır.")

    def get_tape_string(self) -> str:
        """Şeridin o anki durumunu, pointer pozisyonunu [x] şeklinde belirterek döndürür."""
        if not self.tape:
            return f"[{self.blank_symbol}]"
            
        min_index = min(self.tape.keys())
        max_index = max(self.tape.keys())
        min_index = min(min_index, self.head_position)
        max_index = max(max_index, self.head_position)

        tape_string = ""
        for i in range(min_index, max_index + 1):
            symbol = self.tape.get(i, self.blank_symbol)
            if i == self.head_position:
                tape_string += f"[{symbol}]"
            else:
                tape_string += symbol
                
        return tape_string    
        


class SingleTapeTM:
    def __init__(self, config: Dict[str, Any]):
        """Makineyi, sözlük olarak verilen YAML ayarlarıyla kurar."""
        self.name = config.get('name', 'Bilinmeyen TM')
        self.states = config.get('states', [])
        self.blank_symbol = config.get('blank', 'B')
        self.start_state = config.get('start_state', '')
        self.accept_states = config.get('accept_states', [])
        
        
        self.reject_states = config.get('reject_states', [])
        
       
        self.transitions = {}
        for t in config.get('transitions', []):
            key = (t['state'], str(t['read']))
            self.transitions[key] = t

    @classmethod
    def from_yaml(cls, file_path: str):
        """Hocanın test sisteminin kullanacağı, YAML dosyasından nesne üreten metot."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                if not config:
                    raise ValueError(f"YAML dosyası boş veya okunamadı: {file_path}")
                return cls(config)
        except Exception as e:
            raise ValueError(f"Geçersiz YAML formatı: {e}")
        
    def run(self, input_string: str, max_steps: int = 1000, verbose: bool = False) -> RunResult:
        """Makineyi verilen kelimeyle çalıştırır ve sonucu döndürür."""
        
        tape = Tape(initial_content=input_string, blank_symbol=self.blank_symbol)
        current_state = self.start_state
        steps = 0
        history = []
        
       
        while steps < max_steps:
            current_char = tape.read()
            
            
            adim_kaydi = StepConfig(
                state=current_state,
                tape=tape.tape.copy(), 
                head_position=tape.head_position
            )
            history.append(adim_kaydi)
            
            
            if current_state in self.accept_states:
                if verbose:
                    print(f"Adım {steps} | Durum: {current_state} | Şerit: {tape.get_tape_string()}")
                # RUBRİK KURALI: reason="accept"
                return RunResult(True, tape.get_tape_string(), steps, history, "accept")
                
            
            if current_state in self.reject_states:
                if verbose:
                    print(f"Adım {steps} | Durum: {current_state} | Şerit: {tape.get_tape_string()}")
                # RUBRİK KURALI: reason="reject"
                return RunResult(False, tape.get_tape_string(), steps, history, "reject")
                
            
            transition = self.transitions.get((current_state, current_char))
            
            if transition is None:
                if verbose:
                    print(f"Adım {steps} | Durum: {current_state} | Şerit: {tape.get_tape_string()}")
                
                return RunResult(False, tape.get_tape_string(), steps, history, "no_transition")
                
           
            move_dir = transition['move']
            if verbose:
                print(f"Adım {steps} | Durum: {current_state} | Şerit: {tape.get_tape_string()} | Hareket: {move_dir}")
                
            
            tape.write(transition['write'])
            tape.move(move_dir)
            current_state = transition['next']
            
            steps += 1
            
        
        return RunResult(False, tape.get_tape_string(), steps, history, "timeout")


    
    