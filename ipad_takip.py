import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

# Mail ayarları (GitHub Secrets'tan gelecek)
ALICI_EMAIL = "Eskici142@gmail.com"
GONDEREN_EMAIL = os.environ.get('GMAIL_USER')
GMAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD')

def mediamarkt_fiyat_kontrol():
    print("🔍 Media Markt kontrolü başlatılıyor...")
  
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
  
    urunler = []
  
    try:
        url = "https://www.mediamarkt.com.tr/tr/search.html?query=iPad%20Air%20M4"
        response = requests.get(url, headers=headers, timeout=30)
      
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            product_cards = soup.find_all('div', {'data-test': 'mms-search-srp-productlist-item'})
          
            print(f"✅ {len(product_cards)} ürün bulundu")
          
            for card in product_cards:
                try:
                    title_element = card.find('h2')
                    price_element = card.find('div', {'data-test': 'mms-product-price-box'})
                  
                    if title_element and price_element:
                        title = title_element.get_text(strip=True)
                        price = price_element.get_text(strip=True).split('\n')[0]
                      
                        if 'iPad Air' in title and 'M4' in title and 'Wi-Fi' in title:
                            kapasite = '128 GB' if '128' in title else '256 GB' if '256' in title else '512 GB' if '512' in title else 'Bilinmiyor'
                            boyut = '11 inç' if '11' in title else '13 inç' if '13' in title else 'Bilinmiyor'
                          
                            kampanya = ""
                            badge = card.find('div', class_=lambda x: x and 'badge' in x.lower())
                            if badge:
                                kampanya = badge.get_text(strip=True)
                          
                            urunler.append({
                                'baslik': title,
                                'fiyat': price,
                                'boyut': boyut,
                                'kapasite': kapasite,
                                'kampanya': kampanya
                            })
                          
                            print(f"📱 {boyut} {kapasite}: {price}")
                except:
                    continue
    except Exception as e:
        print(f"❌ Hata: {e}")
  
    return urunler

def mail_gonder(urunler):
    print("📧 Mail hazırlanıyor...")
  
    tarih = datetime.now().strftime("%d %B %Y, %H:%M")
  
    ipad_11_128 = next((u for u in urunler if u['boyut'] == '11 inç' and u['kapasite'] == '128 GB'), None)
    ipad_11_256 = next((u for u in urunler if u['boyut'] == '11 inç' and u['kapasite'] == '256 GB'), None)
    ipad_11_512 = next((u for u in urunler if u['boyut'] == '11 inç' and u['kapasite'] == '512 GB'), None)
    ipad_13_128 = next((u for u in urunler if u['boyut'] == '13 inç' and u['kapasite'] == '128 GB'), None)
    ipad_13_256 = next((u for u in urunler if u['boyut'] == '13 inç' and u['kapasite'] == '256 GB'), None)
    ipad_13_512 = next((u for u in urunler if u['boyut'] == '13 inç' and u['kapasite'] == '512 GB'), None)
  
    body = f"""Merhaba,

Media Markt'tan güncel iPad Air M4 fiyatları:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📱 iPad Air 11 inç M4 Wi-Fi
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{'✅ 128 GB: ' + ipad_11_128['fiyat'] if ipad_11_128 else '❌ 128 GB: Stokta yok'}
{f"   🎉 {ipad_11_128['kampanya']}" if ipad_11_128 and ipad_11_128.get('kampanya') else ''}

{'✅ 256 GB: ' + ipad_11_256['fiyat'] if ipad_11_256 else '❌ 256 GB: Stokta yok'}
{f"   🎉 {ipad_11_256['kampanya']}" if ipad_11_256 and ipad_11_256.get('kampanya') else ''}

{'✅ 512 GB: ' + ipad_11_512['fiyat'] if ipad_11_512 else '❌ 512 GB: Stokta yok'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📱 iPad Air 13 inç M4 Wi-Fi
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{'✅ 128 GB: ' + ipad_13_128['fiyat'] if ipad_13_128 else '❌ 128 GB: Stokta yok'}
{f"   🎉 {ipad_13_128['kampanya']}" if ipad_13_128 and ipad_13_128.get('kampanya') else ''}

{'✅ 256 GB: ' + ipad_13_256['fiyat'] if ipad_13_256 else '❌ 256 GB: Stokta yok'}
{f"   🎉 {ipad_13_256['kampanya']}" if ipad_13_256 and ipad_13_256.get('kampanya') else ''}

{'✅ 512 GB: ' + ipad_13_512['fiyat'] if ipad_13_512 else '❌ 512 GB: Stokta yok'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔗 https://www.mediamarkt.com.tr/tr/search.html?query=iPad%20Air%20M4

🌩️ Otomatik bulut servisi
📅 {tarih}

İyi alışverişler! 🛒"""
  
    try:
        msg = MIMEMultipart()
        msg['From'] = GONDEREN_EMAIL
        msg['To'] = ALICI_EMAIL
        msg['Subject'] = f"📱 iPad Air M4 Fiyat Raporu - {datetime.now().strftime('%d.%m.%Y')}"
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
      
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GONDEREN_EMAIL, GMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
      
        print("✅ Mail gönderildi!")
        return True
    except Exception as e:
        print(f"❌ Mail hatası: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("📱 iPad Air M4 Fiyat Takip")
    print("🌩️ GitHub Actions Bulut Servisi")
    print("=" * 50)
  
    urunler = mediamarkt_fiyat_kontrol()
  
    if urunler:
        print(f"\n✅ {len(urunler)} ürün bulundu")
        mail_gonder(urunler)
    else:
        print("\n❌ Ürün bulunamadı")
  
    print("\n✅ Tamamlandı")
