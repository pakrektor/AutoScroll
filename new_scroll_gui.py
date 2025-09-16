import customtkinter
import pyautogui
import threading
import time

# --- Variabel Global ---
is_scrolling = False
scroll_speed = -1
# Variabel baru untuk pesan error dari thread
error_message = ""

# --- Fungsi Inti untuk Scrolling ---
def scroller():
    """Fungsi ini akan berjalan di thread terpisah untuk melakukan scroll."""
    global scroll_speed, is_scrolling, error_message
    while True:
        if is_scrolling:
            try:
                # Mencoba melakukan scroll
                pyautogui.scroll(int(scroll_speed))
                time.sleep(0.100)
            except Exception as e:
                # Jika terjadi error, tangkap pesannya dan berhenti scroll
                print(f"Error terdeteksi: {e}")
                error_message = str(e)
                is_scrolling = False
        else:
            time.sleep(0.1)

# --- Fungsi untuk Kontrol GUI ---
def update_status_indicator():
    """
    Memperbarui SEMUA indikator status: label teks, warna, dan teks tombol.
    Fungsi ini sekarang menjadi pusat kendali tampilan status.
    """
    if is_scrolling:
        # Status saat Berjalan
        status_label.configure(text="Status: Berjalan", text_color="green")
        start_stop_button.configure(text="Stop Scroll")
    else:
        # Status saat Berhenti
        status_label.configure(text="Status: Berhenti", text_color="red")
        start_stop_button.configure(text="Start Scroll")

def toggle_scrolling():
    """
    Hanya mengubah status (True/False) dan memanggil fungsi update.
    Fungsi ini sekarang lebih sederhana.
    """
    global is_scrolling, error_message
    # Hapus pesan error lama saat memulai
    error_message = ""
    error_label.configure(text="")
    
    # Balik status scrolling (dari True ke False, atau sebaliknya)
    is_scrolling = not is_scrolling
    
    # Panggil satu fungsi untuk memperbarui semua tampilan
    update_status_indicator()

def update_speed(value):
    """Dipanggil saat slider digerakkan."""
    global scroll_speed
    scroll_speed = -value
    speed_label.configure(text=f"Speed: {int(value)}")

# --- Fungsi Baru untuk Memeriksa Error ---
def check_for_errors():
    """Memeriksa apakah ada pesan error dari thread scroller."""
    global error_message
    if error_message:
        # Jika ada error, tampilkan di label dan update status
        error_label.configure(text=f"Error: {error_message[:30]}...")
        update_status_indicator()
        error_message = "" # Kosongkan kembali setelah ditampilkan
    
    # Jalankan pemeriksaan ini setiap 200ms
    app.after(200, check_for_errors)

def exit_app():
    """Menutup aplikasi."""
    global is_scrolling
    is_scrolling = False
    app.destroy()

# --- Pengaturan Tampilan GUI ---
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")
app = customtkinter.CTk()
app.title("Auto Scroll")
app.geometry("250x250") # Sedikit diperbesar
app.attributes("-topmost", True)

# --- Membuat Widget ---
title_label = customtkinter.CTkLabel(app, text="Auto Scroll", font=("Roboto", 16))
title_label.pack(pady=5, padx=10)

# 1. Label Status Baru
status_label = customtkinter.CTkLabel(app, text="Status: Berhenti", text_color="gray")
status_label.pack()

speed_label = customtkinter.CTkLabel(app, text="Speed: 1")
speed_label.pack(pady=(10, 0))

speed_slider = customtkinter.CTkSlider(app, from_=1, to=20, command=update_speed)
speed_slider.set(1)
speed_slider.pack(pady=10, padx=20)

start_stop_button = customtkinter.CTkButton(app, text="Start Scroll", command=toggle_scrolling)
start_stop_button.pack(pady=5)

exit_button = customtkinter.CTkButton(app, text="Exit", command=exit_app, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
exit_button.pack(pady=5)

# 2. Label Error Baru
error_label = customtkinter.CTkLabel(app, text="", text_color="red")
error_label.pack(pady=(5, 0))

# --- Menjalankan Thread dan Aplikasi ---
scroll_thread = threading.Thread(target=scroller, daemon=True)
scroll_thread.start()

# Memulai fungsi pemeriksaan error
check_for_errors()

app.mainloop()