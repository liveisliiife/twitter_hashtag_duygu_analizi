import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from textblob import TextBlob
import matplotlib.pyplot as plt

print("Eğer hata alıyorsanız time.sleep() kısmındaki süreyi arttırın")
kullanici_adi = input("Kullanıcı adınız: ")
kullanici_sifresi = input("Şifreniz: ")
hedef = input("Hangi hashtag üzerinde işlem yapmak istiyorsanız başında # olmadan giriniz.Mesela btcusdt gibi: ")
if hedef[0] == "#":
    hedef = hedef[1:]

tweet_sayisi = int(input("En son atılan kaç tweeti görmek istiyorsunuz: "))
if (type(tweet_sayisi) != int) or (tweet_sayisi < 1):
    print("Tweet sayisi pozitif tam sayı olmak zorundadır")
    exit()

driver = webdriver.Chrome(".../chromedriver.exe")
url = "https://twitter.com/login"
driver.get(url)
time.sleep(5)

driver.maximize_window()
time.sleep(5)

giris = driver.find_element(By.XPATH,"//input[@autocomplete='username']")
giris.send_keys(kullanici_adi)
time.sleep(5)
giris.send_keys(Keys.ENTER)
time.sleep(5)

sifre = driver.find_element(By.XPATH,"//input[@autocomplete='current-password']")
sifre.send_keys(kullanici_sifresi)
time.sleep(5)
sifre.send_keys(Keys.ENTER)
time.sleep(5)

url2 = "https://twitter.com/search?q=%23{}&src=typed_query&f=live".format(hedef)
driver.get(url2)
time.sleep(5)

bilgi = []
profil = driver.find_elements(By.CSS_SELECTOR,".css-1dbjc4n.r-1iusvr4.r-16y2uox.r-1777fci.r-kzbkwu")
for i in profil:
    bilgi.append(i.text)

while True:
    driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")
    time.sleep(5)
    profil2 = driver.find_elements(By.CSS_SELECTOR, ".css-1dbjc4n.r-1iusvr4.r-16y2uox.r-1777fci.r-kzbkwu")
    for i in profil2:
        x = i.text
        if x not in bilgi:
            bilgi.append(x)
    if len(bilgi) >= tweet_sayisi:
        break

kisi_adi = []
kisi_tweeti = []
for i in range(0,tweet_sayisi):
    kisi_adi.append(bilgi[i].split("\n")[1])
    kisi_tweeti.append(bilgi[i].split("\n")[4])

total = 0
takipci_sayisi = []
for username in kisi_adi:
    driver.get(f"https://twitter.com/{username[1:]}")
    time.sleep(5)
    temp = driver.find_element(By.XPATH,"//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[2]").find_element(By.CSS_SELECTOR,".css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0")
    temp = temp.text
    parts = temp.replace(",", ".").split(" ")
    if len(parts) == 2:
        numeric_part = float(parts[0])
        unit = parts[1]
        if unit == "Mn":
            numeric_part = float(numeric_part) * 1000000
        if unit == "B":
            numeric_part = float(numeric_part) * 1000
    else:
        if "." in temp:
            numeric_part = float(temp) * 1000
        else:
            numeric_part = int(temp)
    takipci_sayisi.append(numeric_part)
    total += numeric_part

positive_tweets = 0
negative_tweets = 0
neutral_tweets = 0
j = 0
for tweet in kisi_tweeti:
    analysis = TextBlob(tweet)
    sentiment = analysis.sentiment.polarity
    if sentiment > 0:
        positive_tweets += (takipci_sayisi[j]/total)
    elif sentiment < 0:
        negative_tweets += (takipci_sayisi[j]/total)
    else:
        neutral_tweets += (takipci_sayisi[j]/total)
    j += 1

labels = ['Pozitif', 'Negatif', 'Nötr']
values = [positive_tweets, negative_tweets, neutral_tweets]

fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(labels, values, color=['green', 'red', 'grey'])

for i, v in enumerate(values):
    ax.text(i, v+0.01, f'{round(v*100,2)}%', ha='center')

ax.set_title('{} Duygu Analizi Sütun Grafiği'.format(hedef))
ax.set_ylabel('Oran')
ax.set_ylim([0,1])

plt.show()

input("Çıkmak için bir tuşa basınız")
driver.close()
exit()







