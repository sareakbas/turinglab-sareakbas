import pytest
from turinglab.tm_engine import SingleTapeTM

# ==========================================
# 1. HATA YÖNETİMİ VE EDGE CASE TESTLERİ
# ==========================================

def test_hatali_yaml_okuma():
    with pytest.raises(ValueError):
        SingleTapeTM.from_yaml("var_olmayan_hayalet_dosya.yaml")

def test_timeout_sonsuz_dongu():
    config = {
        'states': ['q0'], 'start_state': 'q0', 'accept_states': ['q_kabul'], 'blank': 'B',
        'transitions': [
            {'state': 'q0', 'read': '1', 'write': '1', 'move': 'R', 'next': 'q0'},
            {'state': 'q0', 'read': 'B', 'write': 'B', 'move': 'R', 'next': 'q0'}
        ]
    }
    tm = SingleTapeTM(config)
    result = tm.run(input_string="111", max_steps=5)
    assert result.accepted is False
    assert result.reason == "timeout"

def test_verbose_modu_ciktisi(capsys):
    config = {
        'states': ['q0', 'q_kabul'], 'start_state': 'q0', 'accept_states': ['q_kabul'], 'blank': 'B',
        'transitions': [{'state': 'q0', 'read': '1', 'write': '0', 'move': 'R', 'next': 'q_kabul'}]
    }
    tm = SingleTapeTM(config)
    tm.run(input_string="1", verbose=True)
    captured = capsys.readouterr() 
    assert "Adım 0" in captured.out
    assert "Hareket: R" in captured.out

# ==========================================
# 2. FARKLI MAKİNELER VE GİRDİ TESTLERİ
# ==========================================

@pytest.fixture
def makine_silici():
    config = {
        'states': ['q0', 'q_kabul'], 'start_state': 'q0', 'accept_states': ['q_kabul'], 'blank': 'B',
        'transitions': [
            {'state': 'q0', 'read': '1', 'write': '0', 'move': 'R', 'next': 'q0'},
            {'state': 'q0', 'read': 'B', 'write': 'B', 'move': 'R', 'next': 'q_kabul'}
        ]
    }
    return SingleTapeTM(config)

def test_makine_silici_tek_girdi(makine_silici):
    result = makine_silici.run("1")
    assert result.accepted is True
    assert result.reason == "accept"

def test_makine_silici_coklu_girdi(makine_silici):
    result = makine_silici.run("1111")
    assert result.accepted is True
    assert "0000" in result.final_tape.replace("[", "").replace("]", "")

def test_makine_silici_bos_girdi(makine_silici): # KAYIP TEST 1 GERİ GELDİ
    result = makine_silici.run("")
    assert result.accepted is True

@pytest.fixture
def makine_sadece_A():
    config = {
        'states': ['q0', 'q_kabul'], 'start_state': 'q0', 'accept_states': ['q_kabul'], 'blank': 'B',
        'transitions': [
            {'state': 'q0', 'read': 'A', 'write': 'A', 'move': 'R', 'next': 'q_kabul'}
        ]
    }
    return SingleTapeTM(config)

def test_makine_sadece_A_dogru(makine_sadece_A): # KAYIP TEST 2 GERİ GELDİ
    assert makine_sadece_A.run("A").accepted is True

def test_makine_sadece_A_yanlis(makine_sadece_A):
    result = makine_sadece_A.run("X")
    assert result.accepted is False
    assert result.reason == "no_transition"

def test_makine_dogrudan_ret():
    config = {
        'states': ['q0', 'q_ret'], 'start_state': 'q0', 'accept_states': [], 'reject_states': ['q_ret'], 'blank': 'B',
        'transitions': [
            {'state': 'q0', 'read': '1', 'write': '1', 'move': 'R', 'next': 'q_ret'}
        ]
    }
    tm = SingleTapeTM(config)
    result = tm.run("1")
    assert result.accepted is False
    assert result.reason == "reject"