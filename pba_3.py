import streamlit as st
import re
from collections import Counter
import time

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

# Fungsi untuk mendapatkan semua edit satu langkah dari kata
def edits1(word):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

# Fungsi untuk mendapatkan semua edit dua langkah dari kata
def edits2(word):
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

# Streamlit UI
st.title("Indonesian Spell Checker using Norvig's Algorithm")

input_words = st.text_input("Masukkan kata-kata yang dipisahkan dengan koma:", "")

if st.button("Periksa Ejaan"):
    test_words = input_words.split(',')
    
    start = time.time()
    corrected_words = {w: correction(w.strip()) for w in test_words}
    end = time.time()
    
    st.write(f'Waktu yang diperlukan: {end - start:.4f} detik')
    
    st.write("Koreksi Kata:")
    for word, correction in corrected_words.items():
        st.write(f"'{word.strip()}' -> '{correction}'")
