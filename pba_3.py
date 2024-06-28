import streamlit as st
import re
from collections import Counter

# Fungsi untuk memuat korpus
def load_corpus(path):
    with open(path, 'r') as file:
        return file.read()

# Fungsi untuk mendapatkan daftar kata
def words(text):
    return re.findall(r'\w+', text.lower())

# Load korpus
path_corpus = "01-kbbi3-2001-sort-alpha.lst"
WORDS = Counter(words(load_corpus(path_corpus)))

# Fungsi untuk menghitung probabilitas kata
def P(word, N=sum(WORDS.values())):
    return WORDS[word] / N

# Fungsi untuk mendapatkan koreksi kata
def correction(word):
    return max(candidates(word), key=P)

# Fungsi untuk mendapatkan kandidat koreksi
def candidates(word):
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

# Fungsi untuk mendapatkan kata-kata yang dikenal
def known(words):
    return set(w for w in words if w in WORDS)

# Fungsi untuk menghasilkan semua kata yang berjarak satu edit dari kata yang diberikan
def edits1(word):
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

# Fungsi untuk menghasilkan semua kata yang berjarak dua edit dari kata yang diberikan
def edits2(word):
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

# Judul aplikasi
st.title("Indonesian Spell Checker using Norvig's Algorithm")

# Input teks dari pengguna
input_text = st.text_area("Masukkan kata yang ingin diperiksa (pisahkan dengan koma):")

if st.button("Periksa"):
    if input_text:
        test_words = input_text.split(',')
        results = {}
        correct_count = 0
        total_words = len(test_words)
        
        for w in test_words:
            original_word = w.strip()
            corrected_word = correction(original_word)
            results[original_word] = corrected_word
            if original_word == corrected_word:
                correct_count += 1
        
        accuracy = correct_count / total_words
        
        # Tampilkan hasil
        st.write("Hasil Koreksi:")
        for w, corrected in results.items():
            st.write(f"'{w.strip()}' -> '{corrected}'")
        
        st.write(f"Akurasi: {accuracy:.2%}")
        
        # Tampilkan known edits1 dari kata 'kcing'
        st.write("Kandidat koreksi untuk 'kcing':")
        st.write(known(edits1('kcing')))
        
        # Hitung probabilitas dari daftar kata tertentu
        st.write("Probabilitas kata:")
        words_list = ['cing', 'kaing', 'king', 'kling', 'kring', 'kucing', 'kuing']
        for c in words_list:
            st.write(f"P({c}) = {P(c):.6f}")
    else:
        st.write("Mohon masukkan kata untuk diperiksa.")
