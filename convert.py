import json
import urllib.request
import re

URL = "https://raw.githubusercontent.com/ziizidavid/VSA/refs/heads/main/IPtv"
OUTPUT_FILE = "iptv.json"

def parse_m3u(url):
    try:
        # Mengambil data dari URL m3u
        with urllib.request.urlopen(url) as response:
            content = response.read().decode('utf-8')
    except Exception as e:
        print(f"Gagal mengambil data: {e}")
        return

    lines = content.split('\n')
    playlist = []
    current_item = {}

    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line.startswith("#EXTINF:"):
            current_item = {}
            # Mengambil properti seperti tvg-id, tvg-name, tvg-logo, group-title
            matches = re.findall(r'([a-zA-Z0-9\-]+)="([^"]*)"', line)
            for key, val in matches:
                current_item[key] = val
            
            # Mengambil nama channel (teks setelah koma terakhir)
            name_match = line.split(',')[-1]
            current_item['name'] = name_match.strip() if name_match else "Unknown"
            
        elif line.startswith("http") and current_item is not None:
            current_item['url'] = line
            playlist.append(current_item)
            current_item = {}

    # Menyimpan hasil ke file JSON
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(playlist, f, indent=4, ensure_ascii=False)
    print(f"Berhasil mengonversi dan menyimpan ke {OUTPUT_FILE}")

if __name__ == "__main__":
    parse_m3u(URL)
