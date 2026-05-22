import pytest
from turinglab.tm_engine import SingleTapeTM
from turinglab.multi_tape import MultiTapeTM 
from turinglab.ntm import NonDeterministicTM


@pytest.fixture
def tm_unary_to_binary():
    return SingleTapeTM.from_yaml("machines/unary_to_binary.yaml")

# 1. Kabul Testi: 3 Sayısı
def test_tm1_kabul_3(tm_unary_to_binary):
    result = tm_unary_to_binary.run("111")
    assert result.accepted is True
    # Şeritteki [ ] ve B'leri temizleyince elimizde 11 kalmalı
    temiz_serit = result.final_tape.replace("[", "").replace("]", "").replace("B", "")
    assert "11" in temiz_serit

# 2. Kabul Testi: 5 Sayısı
def test_tm1_kabul_5(tm_unary_to_binary):
    result = tm_unary_to_binary.run("11111")
    assert result.accepted is True
    temiz_serit = result.final_tape.replace("[", "").replace("]", "").replace("B", "")
    assert "101" in temiz_serit

# 3. Ret Testi: Geçersiz Harf
def test_tm1_ret_gecersiz_harf(tm_unary_to_binary):
    result = tm_unary_to_binary.run("11A")
    assert result.accepted is False

# 4. Ret Testi: Unary Sistemde 0 Olmaz
def test_tm1_ret_icinde_sifir_var(tm_unary_to_binary):
    result = tm_unary_to_binary.run("101")
    assert result.accepted is False

# 5. Kenar Durum: Boş Girdi (0 Sayısı)
def test_tm1_kenar_durum_bos(tm_unary_to_binary):
    result = tm_unary_to_binary.run("")
    assert result.accepted is True
    temiz_serit = result.final_tape.replace("[", "").replace("]", "").replace("B", "")
    assert "0" in temiz_serit

@pytest.fixture
def tm_binary_compare():
    return SingleTapeTM.from_yaml("machines/binary_compare.yaml")

# 1. Kabul Testi: Sol Büyük (3 > 2)
def test_tm2_kabul_sol_buyuk(tm_binary_compare):
    assert tm_binary_compare.run("11#10").accepted is True

# 2. Kabul Testi: Sol Büyük (5 > 4)
def test_tm2_kabul_sol_daha_buyuk(tm_binary_compare):
    assert tm_binary_compare.run("101#100").accepted is True

# 3. Ret Testi: Sağ Büyük (2 < 3)
def test_tm2_ret_sag_buyuk(tm_binary_compare):
    assert tm_binary_compare.run("10#11").accepted is False

# 4. Ret Testi: Sağ Büyük (1 < 2)
def test_tm2_ret_sag_daha_buyuk(tm_binary_compare):
    assert tm_binary_compare.run("01#10").accepted is False

# 5. Kenar Durum: Eşitlik (3 == 3) -> Büyük olmadığı için reddetmeli
def test_tm2_kenar_durum_esit(tm_binary_compare):
    assert tm_binary_compare.run("11#11").accepted is False



# TM-3: DİZGİ KOPYALAYICI 
@pytest.fixture
def tm_string_copy():
    return SingleTapeTM.from_yaml("machines/string_copy.yaml")

# 1. Kabul Testi: Uzun Kelime
def test_tm3_kabul_uzun(tm_string_copy):
    result = tm_string_copy.run("abba")
    assert result.accepted is True
    temiz_serit = result.final_tape.replace("[", "").replace("]", "")
    assert "abba#abba" in temiz_serit

# 2. Kabul Testi: Kısa Kelime
def test_tm3_kabul_kisa(tm_string_copy):
    result = tm_string_copy.run("ab")
    assert result.accepted is True
    temiz_serit = result.final_tape.replace("[", "").replace("]", "")
    assert "ab#ab" in temiz_serit

# 3. Ret Testi: Geçersiz Alfabe (c harfi var)
def test_tm3_ret_gecersiz_harf(tm_string_copy):
    result = tm_string_copy.run("abc")
    assert result.accepted is False

# 4. Ret Testi: İçinde Zaten '#' Olan Girdi
def test_tm3_ret_icinde_ayirici_var(tm_string_copy):
    result = tm_string_copy.run("a#b")
    assert result.accepted is False

# 5. Kenar Durum: Boş Girdi (Sadece '#' bırakmalı)
def test_tm3_kenar_durum_bos(tm_string_copy):
    result = tm_string_copy.run("")
    assert result.accepted is True
    assert "#" in result.final_tape


# TM-4: 4'E BÖLÜNEBİLİRLİK 

@pytest.fixture
def tm_divisible_by_4():
    return SingleTapeTM.from_yaml("machines/student_choice.yaml")

# 1. Kabul Testi: 12 (1100) -> Sonu 00 biter
def test_tm4_kabul_12(tm_divisible_by_4):
    assert tm_divisible_by_4.run("1100").accepted is True

# 2. Kabul Testi: 16 (10000) -> Sonu 00 biter
def test_tm4_kabul_16(tm_divisible_by_4):
    assert tm_divisible_by_4.run("10000").accepted is True

# 3. Ret Testi: 10 (1010) -> Sonu 10 biter
def test_tm4_ret_10(tm_divisible_by_4):
    assert tm_divisible_by_4.run("1010").accepted is False

# 4. Ret Testi: 7 (111) -> Sonu 11 biter
def test_tm4_ret_7(tm_divisible_by_4):
    assert tm_divisible_by_4.run("111").accepted is False

# 5. Kenar Durum Testi: Sadece 0 sayısı
def test_tm4_kenar_durum_sifir(tm_divisible_by_4):
    assert tm_divisible_by_4.run("0").accepted is True

# 6. Ekstra Kenar Durum: Boş Girdi (Reddedilmeli)
def test_tm4_kenar_durum_bos(tm_divisible_by_4):
    assert tm_divisible_by_4.run("").accepted is False



# ==========================================
# BONUS A: ÇOK ŞERİTLİ (MULTI-TAPE) TOPLAMA
# ==========================================

@pytest.fixture
def tm_multi_add():
    return MultiTapeTM.from_yaml("machines/binary_add_multi.yaml")

# 1. Test: 10 (2) + 11 (3) = 101 (5)
def test_bonus_a_add_simple(tm_multi_add):
    result = tm_multi_add.run(["10", "11"])
    assert result.accepted is True
    assert "101" in result.final_tapes[2] # 3. Şerit

# 2. Test: 111 (7) + 1 (1) = 1000 (8)
def test_bonus_a_add_carry(tm_multi_add):
    result = tm_multi_add.run(["111", "1"])
    assert result.accepted is True
    assert "1000" in result.final_tapes[2]

# 3. Test: Uzunluk farkı olan sayılar
def test_bonus_a_add_diff_len(tm_multi_add):
    result = tm_multi_add.run(["1000", "1"]) # 8 + 1 = 9
    assert result.accepted is True
    assert "1001" in result.final_tapes[2]

# 4. Test: Sıfır ile toplama
def test_bonus_a_add_zero(tm_multi_add):
    result = tm_multi_add.run(["101", "0"]) # 5 + 0 = 5
    assert result.accepted is True
    assert "101" in result.final_tapes[2]

# 5. Test: Çift elde (Double carry)
def test_bonus_a_double_carry(tm_multi_add):
    result = tm_multi_add.run(["11", "11"]) # 3 + 3 = 6
    assert result.accepted is True
    assert "110" in result.final_tapes[2]


# ==========================================
# BONUS B: NON-DETERMINISTIC TM (NTM)
# ==========================================

@pytest.fixture
def ntm_find_11():
    return NonDeterministicTM.from_yaml("machines/ntm_find_11.yaml")

# 1. Test: Sonda '11' var
def test_bonus_b_ntm_sonda(ntm_find_11):
    result = ntm_find_11.run("01011")
    assert len(result.accepting_paths) > 0 # Kabul edilen en az 1 paralel evren olmalı
    assert result.rejected is False

# 2. Test: Başta '11' var
def test_bonus_b_ntm_basta(ntm_find_11):
    result = ntm_find_11.run("11000")
    assert len(result.accepting_paths) > 0

# 3. Test: İçinde hiç '11' yok -> Reddedilmeli
def test_bonus_b_ntm_yok(ntm_find_11):
    result = ntm_find_11.run("01010")
    assert len(result.accepting_paths) == 0
    assert result.rejected is True

# 4. Test: Çakışan '1'ler (111)
def test_bonus_b_ntm_cakisan(ntm_find_11):
    result = ntm_find_11.run("111")
    assert len(result.accepting_paths) > 0

# 5. Kenar Durum: Boş girdi
def test_bonus_b_ntm_bos(ntm_find_11):
    result = ntm_find_11.run("")
    assert result.rejected is True