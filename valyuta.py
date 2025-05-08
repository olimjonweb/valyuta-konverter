import requests
from pywebio.input import input, FLOAT, select
from pywebio.output import put_text, put_table, put_error, put_warning
from pywebio import start_server

def valyuta_kursini_ol(asosiy: str):
    """API orqali asosiy valyuta ma'lumotlarini olish"""
    # Haqiqiy API kalitini shu yerga kiriting
    API_KEY = "API kaliti u/n joy"
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{asosiy}"
    try:
        javob = requests.get(url, timeout=10)
        if javob.status_code == 200:
            data = javob.json()
            return data.get("conversion_rates", None)  # Valyutalar kurslari
        else:
            put_warning(f"API dan noto'g'ri javob : {javob.status_code}")
            return None
    except Exception as e:
        put_error(f"Requests xatosi: {e}")
        return None

def valyuta_konvertori():
    """Valyuta konvertori interfeysi"""
    asosiy = select("Asosiy valyuta", ["USD", "EUR", "UZS", "RUB", "GBP", "JPY", "CNY"])
    konvert = select("Konvertatsiya qilinadigan valyuta", ["USD", "EUR", "UZS", "RUB", "GBP", "JPY", "CNY"])
    summa = input("Miqdorni kiriting", type=FLOAT)

    # API orqali valyuta kurslarini olish
    kurslar = valyuta_kursini_ol(asosiy)
    if kurslar and konvert in kurslar:
        kurs = kurslar[konvert]
        natija = summa * kurs
        put_text(f"{summa} {asosiy} = {natija:.2f} {konvert}")
    else:
        put_error("Valyuta kurslarini olishda muammo yuzaga keldi!")

    # Barcha valyutalar uchun kurslarni ko'rsatish
    if kurslar:
        put_table([
            ["Valyuta", "Kurs"],
            *[[val, f"{qiymat:.2f}"] for val, qiymat in kurslar.items()]
        ])
    else:
        put_warning("Barcha valyutalar uchun kurslar topilmadi!")

if __name__ == "__main__":
    start_server(valyuta_konvertori, port=8080)
