'''
Created on 16 Ara 2019

@author: muura
'''
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import nltk
import jpype
nltk.download('stopwords')

jvmDLLpath = r"C:\Program Files\Java\jdk-13\bin\server\jvm.dll"                    
jpype.startJVM(jvmDLLpath,"-Djava.class.path=zemberek-tum-2.0.jar", "-ea")       

TR = jpype.JClass("net.zemberek.tr.yapi.TurkiyeTurkcesi")
tr = TR()

Z = jpype.JClass("net.zemberek.erisim.Zemberek")
z = Z(tr)

def Zemberek(makale):      
    yenidepo = []
    makale = makale.split()
    for line in makale:
        try:
            kok = z.kelimeCozumle(line)[0].kok().icerik()
            if kok:
                yenidepo.append(kok)
        except:
            pass
    
    return yenidepo    

egitim = []
file = open("Makaleler.txt")
for satır in file:
    satır = satır.strip()
    temizle = Zemberek(satır)
    temizle = ' '.join(temizle)
    egitim.append(temizle)
    
vectorizer = TfidfVectorizer(min_df = 0., max_df = 1., use_idf = True)
egitim = vectorizer.fit_transform(egitim)

egitim_y = np.zeros(218) 
egitim_y[57:119] = 1 
egitim_y[119:159] = 2
egitim_y[159:218] = 3

mkneighbors = KNeighborsClassifier(n_neighbors=15)
mkneighbors.fit(egitim,egitim_y)
DogruEtiketler = ['Popüler Kültür','Otomobil', 'Müzik/Piyano', 'Ekonomi']

testDokumani = open("TestDokumanlari.txt")

Dokumani_Temizle = []
for line in testDokumani:
    line = line.strip()
    temizle = Zemberek(line)
    temizle = ' '.join(temizle)
    Dokumani_Temizle.append(temizle)
Test_Dokumani = vectorizer.transform(Dokumani_Temizle)

YuklemEtiketleriKneigbors = mkneighbors.predict(Test_Dokumani)

YuklemEtiketleriKneigbors = YuklemEtiketleriKneigbors.astype(int)
YuklemEtiketleriKneigbors = ''.join(str(v) for v in YuklemEtiketleriKneigbors)
sayac = 0
for i in YuklemEtiketleriKneigbors:
    MevcutSayac = YuklemEtiketleriKneigbors.count(i)
    if(MevcutSayac > sayac):
        sayac = MevcutSayac
        Etiket = i
        
print("\nDokümanın sinifi: ", DogruEtiketler[np.int(Etiket)], "\n\n\n\n")

jpype.shutdownJVM()                                     