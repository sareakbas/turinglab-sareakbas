import pytest
from turinglab.tm_engine import SingleTapeTM

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