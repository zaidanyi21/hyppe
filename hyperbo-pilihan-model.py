import requests
import time

# Daftar model yang tersedia
MODEL_OPTIONS = [
    "Qwen/QwQ-32B",
    "deepseek-ai/DeepSeek-R1",
    "deepseek-ai/DeepSeek-V3",
    "meta-llama/Llama-3.3-70B-Instruct",
    "Qwen/QwQ-32B-Preview",
    "Qwen/Qwen2.5-Coder-32B-Instruct",
    "meta-llama/Llama-3.2-3B-Instruct",
    "Qwen/Qwen2.5-72B-Instruct",
    "meta-llama/Meta-Llama-3-70B-Instruct",
    "NousResearch/Hermes-3-Llama-3.1-70B",
    "meta-llama/Meta-Llama-3.1-405B-Instruct",
    "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "meta-llama/Meta-Llama-3.1-70B-Instruct"
]

# Menampilkan opsi model kepada pengguna
def choose_model():
    print("Pilih model yang akan digunakan:")
    for i, model in enumerate(MODEL_OPTIONS, 1):
        print(f"{i}. {model}")
    
    while True:
        try:
            choice = int(input("Masukkan nomor model: "))
            if 1 <= choice <= len(MODEL_OPTIONS):
                return MODEL_OPTIONS[choice - 1]
            else:
                print("Pilihan tidak valid. Masukkan nomor yang sesuai.")
        except ValueError:
            print("Input tidak valid. Masukkan angka.")

# Memilih model sebelum menjalankan script
selected_model = choose_model()

# Membaca daftar akun dari file akun.txt
def get_accounts():
    try:
        with open("akun.txt", "r") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print("Error: File akun.txt tidak ditemukan.")
        exit(1)

# Membaca daftar proxy dari file proxy.txt
def get_proxies():
    try:
        with open("proxy.txt", "r") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print("Error: File proxy.txt tidak ditemukan. Tidak menggunakan proxy.")
        return []

# Membaca daftar prompt dari file prompt.txt
def get_prompts():
    try:
        with open("prompt.txt", "r") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print("Error: File prompt.txt tidak ditemukan.")
        exit(1)

# API Key dan URL
url = "https://api.hyperbolic.xyz/v1/chat/completions"
accounts = get_accounts()
proxies = get_proxies()
prompts = get_prompts()

# Fungsi untuk mendapatkan IP publik
def get_ip(proxy):
    try:
        response = requests.get("https://api64.ipify.org?format=json", proxies=proxy, timeout=5)
        return response.json().get("ip", "Tidak dapat mengambil IP")
    except:
        return "Gagal mengambil IP"

# Fungsi untuk mengirimkan prompt ke API
def send_prompt(text, token, proxy):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    data = {
        "messages": [
            {"role": "user", "content": text}
        ],
        "model": selected_model,
        "max_tokens": 512,
        "temperature": 0.1,
        "top_p": 0.9
    }
    
    proxy_dict = {"http": proxy, "https": proxy} if proxy else None
    ip_used = get_ip(proxy_dict) if proxy else "Tanpa Proxy"
    print(f"Menggunakan Proxy: {proxy} | IP: {ip_used}")
    
    response = requests.post(url, headers=headers, json=data, proxies=proxy_dict)
    
    if response.status_code == 200:
        try:
            print(f"Response untuk '{text}':")
            print(response.json())
        except ValueError as e:
            print("Error decoding JSON:", e)
            print("Respons teks:", response.text)
    else:
        print(f"Terjadi kesalahan saat mengirimkan prompt '{text}': {response.status_code}")
        print(response.text)

# Loop untuk mengirimkan permintaan ke API dengan multiple akun dan proxy
token_index = 0
proxy_index = 0

for text in prompts:
    token = accounts[token_index % len(accounts)]  # Gunakan akun secara bergantian
    proxy = proxies[proxy_index % len(proxies)] if proxies else None  # Gunakan proxy secara bergantian
    
    send_prompt(text, token, proxy)
    
    token_index += 1
    proxy_index += 1
    time.sleep(12)

print("Semua prompt telah diproses. Program berhenti.")
