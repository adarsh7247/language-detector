import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
import joblib
import re


# LOAD DATASET 
DATA_FILE = 'language.csv'
print(f"Loading dataset '{DATA_FILE}'...")

try:
    df = pd.read_csv(DATA_FILE)
except FileNotFoundError:
    print(f"ERROR: '{DATA_FILE}' not found!")
    sys.exit()

print(f"Original total rows: {len(df)}")

df['Text'] = df['Text'].astype(str).fillna('')

#  CLEAN MISLABELS
print("\nCleaning mislabeled or contaminated rows...")

non_latin_languages = [
    'Arabic', 'Hindi', 'Korean', 'Persian', 'Pushto',
    'Russian', 'Tamil', 'Thai', 'Urdu'
]

def contains_latin(text):
    return bool(re.search(r'[a-zA-Z]', text))

bad_indices = df[
    (df['language'].isin(non_latin_languages)) &
    (df['Text'].apply(contains_latin))
].index

print(f"Removed {len(bad_indices)} mislabeled rows")
df = df.drop(bad_indices)

#  REMOVE CHINESE & JAPANESE 
before = len(df)
df = df[~df['language'].isin(['Chinese', 'Japanese'])]
print(f"Removed {before - len(df)} rows")
print(f"Final dataset size: {len(df)}")

# TRAIN/TEST SPLIT 
X = df['Text']
y = df['language']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\nTraining samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")

#  BUILD MODEL
print("\nBuilding Linear SVM Model with hybrid TF-IDF...")

pipeline = Pipeline([
    ('vectorizer', TfidfVectorizer(
        analyzer='char_wb',
        ngram_range=(3, 6),
        max_features=160000
    )),
    ('classifier', LinearSVC())
])

# TRAIN 
print("\nTraining model...")
pipeline.fit(X_train, y_train)
print("✅ Training complete!")

# EVALUATE 
print("\nEvaluating model...\n")

y_pred = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"✅ Model Accuracy: {accuracy * 100:.2f}%\n")
print(classification_report(y_test, y_pred))

# SAVE MODEL 
MODEL_NAME = "my_own_language_model.joblib"
joblib.dump(pipeline, MODEL_NAME)
print(f"\n✅ Model saved to: {MODEL_NAME}\n")

# SIMPLE PREDICTION FUNCTION 
def detect_language(text):
    if len(text.strip()) < 3:
        return "Not enough text to detect language"
    return pipeline.predict([text])[0]

# BIG SAMPLE TESTING 

print("\n--- BIG LONG SAMPLE TESTING ---\n")

big_samples = {
    "English_long": """Language detection models are widely used in modern systems 
to automatically identify the language being written or spoken. This helps 
applications such as translation services, search engines, chatbots, and 
social media platforms process content more intelligently.""",

    "Hindi_long": """भाषा पहचान मॉडल आधुनिक सिस्टम में व्यापक रूप से उपयोग किए जाते हैं 
ताकि स्वचालित रूप से यह निर्धारित किया जा सके कि कौन सी भाषा लिखी या बोली जा रही है। 
यह अनुवाद सेवाओं, खोज इंजनों, चैटबॉट और सोशल मीडिया प्लेटफार्मों को सामग्री को 
अधिक स्मार्ट तरीके से प्रोसेस करने में मदद करता है।""",

    "Urdu_long": """زبان کی شناخت کرنے والے ماڈل جدید نظاموں میں وسیع پیمانے پر استعمال ہوتے ہیں 
تاکہ خود بخود یہ طے کیا جا سکے کہ کون سی زبان بولی یا لکھی جا رہی ہے۔ 
یہ ترجمہ سروسز، سرچ انجنز، چیٹ بوٹس اور سوشل میڈیا پلیٹ فارمز کو مواد 
کو زیادہ ذہانت کے ساتھ پروسیس کرنے میں مدد دیتا ہے۔""",

    "Arabic_long": """تُستخدم نماذج كشف اللغة على نطاق واسع في الأنظمة الحديثة لتحديد اللغة المكتوبة 
أو المنطوقة تلقائيًا. يساعد ذلك خدمات الترجمة ومحركات البحث وروبوتات الدردشة 
والمنصات الاجتماعية على معالجة المحتوى بشكل أكثر ذكاءً.""",

    "Spanish_long": """Los modelos de detección de idioma se utilizan ampliamente en los sistemas modernos 
para identificar automáticamente el idioma que se escribe o se habla. Esto ayuda 
a los servicios de traducción, motores de búsqueda, chatbots y plataformas de redes 
sociales a procesar el contenido de manera más inteligente.""",

    "French_long": """Les modèles de détection de la langue sont largement utilisés dans les systèmes modernes 
afin d’identifier automatiquement la langue écrite ou parlée. Cela aide les services 
de traduction, les moteurs de recherche, les chatbots et les plateformes sociales 
à traiter le contenu de manière plus intelligente.""",

    "Russian_long": """Модели определения языка широко используются в современных системах для автоматического 
распознавания языка, на котором пишут или говорят. Это помогает сервисам перевода, 
поисковым системам, чат-ботам и социальным платформам более интеллектуально 
обрабатывать информацию.""",

    "Turkish_long": """Dil tespit modelleri, yazılan veya konuşulan dili otomatik olarak belirlemek için modern 
sistemlerde yaygın olarak kullanılmaktadır. Bu, çeviri hizmetlerinin, arama motorlarının, 
sohbet botlarının ve sosyal medya платформlarının içeriği daha akıllıca işlemesine yardımcı olur.""",

    "Swedish_long": """Språkidentifieringsmodeller används ofta i moderna system för att automatiskt avgöra vilket 
språk som skrivs eller talas. Detta hjälper översättningstjänster, sökmotorer, chattbotar och 
sociala plattformar att hantera innehåll på ett smartare sätt. ÅÄÖ finns också här.""",

    "Estonian_long": """Keeletuvastusmudelid kasutatakse kaasaegsetes süsteemides selleks, et automaatselt kindlaks 
teha, mis keeles kirjutatakse või räägitakse. See aitab tõlketeenuseid, otsingumootoreid, 
vestlusroboteid ja sotsiaalmeedia platvorme sisu nutikamalt töödelda.""",

    "Tamil_long": """மொழி கண்டறிதல் மாதிரிகள் எழுதப்பட்ட அல்லது பேசப்படும் மொழியை தானாக அடையாளம் காண நவீன 
அமைப்புகளில் பரவலாக பயன்படுத்தப்படுகின்றன. இது மொழிபெயர்ப்பு சேவைகள், தேடுபொறிகள், 
அரட்டை ரோபோட்டுகள் மற்றும் சமூக ஊடக தளங்கள் உள்ளடக்கத்தை மேலும் புத்திசாலித்தனமாக 
செயலாக்க உதவுகிறது.""",

    "Korean_long": """언어 감지 모델은 작성되거나 말해지는 언어를 자동으로 식별하기 위해 현대 시스템에서 
널리 사용됩니다. 이는 번역 서비스, 검색 엔진, 챗봇 및 소셜 플랫폼이 콘텐츠를 
더 지능적으로 처리하는 데 도움이 됩니다.""",

    "Persian_long": """مدل‌های تشخیص زبان به طور گسترده‌ای در سیستم‌های مدرن برای شناسایی خودکار زبان نوشته 
یا گفته شده استفاده می‌شوند. این کار به خدمات ترجمه، موتورهای جستجو، چت‌بات‌ها و 
پلتفرم‌های اجتماعی کمک می‌کند محتوای خود را هوشمندانه‌تر پردازش کنند.""",

    "Pushto_long": """د ژبې د پېژندلو ماډلونه په عصري سیسټمونو کې پراخ کارول کېږي ترڅو په خپله وپېژني چې کومه 
ژبه لیکل کېږي یا ویل کېږي. دا د ژباړې خدمتونو، لټون انجنونو, چټ بوټانو او ټولنیزو 
پلیټفارمونو سره مرسته کوي چې منځپانګه هوښیارانه ډول پروسس کړي.""",

    "Portuguese_long": """Os modelos de detecção de idioma são amplamente utilizados em sistemas modernos para 
identificar automaticamente o idioma que está sendo escrito ou falado. Isso ajuda 
serviços de tradução, mecanismos de pesquisa, chatbots e plataformas sociais a 
processarem conteúdo de maneira mais inteligente.""",

    "Indonesian_long": """Model deteksi bahasa banyak digunakan dalam sistem modern untuk secara otomatis 
mengidentifikasi bahasa yang sedang ditulis atau diucapkan. Ini membantu layanan 
terjemahan, mesin pencari, chatbot, dan platform media sosial memproses konten 
dengan lebih cerdas.""",

    "Romanian_long": """Modelele de detectare a limbii sunt utilizate pe scară largă în sistemele moderne pentru 
a identifica automat limba în care se scrie sau se vorbește. Acest lucru ajută serviciile 
de traducere, motoarele de căutare, chatbot-urile și platformele sociale să proceseze 
conținutul mai inteligent.""",

    "Thai_long": """โมเดลตรวจจับภาษาถูกใช้งานอย่างกว้างขวางในระบบสมัยใหม่เพื่อตรวจสอบโดยอัตโนมัติว่ากำลังเขียน 
หรือพูดภาษาใด สิ่งนี้ช่วยให้บริการแปลภาษา เครื่องมือค้นหา แชทบอท และแพลตฟอร์มโซเชียลประมวลผล 
เนื้อหาอย่างชาญฉลาดมากขึ้น""",

    "Dutch_long": """Taalherkenningsmodellen worden veel gebruikt in moderne systemen om automatisch te bepalen 
welke taal wordt geschreven of gesproken. Dit helpt vertaalservices, zoekmachines, chatbots en 
sociale platforms om inhoud slimmer te verwerken.""",

    "Latin_long": """Modelli detectionis linguae in systematibus modernis late adhibentur ut linguam scriptam vel 
dictam automatice recognoscant. Hoc auxiliatur officiis interpretationis, machinis quaesitionum, 
nuntiariis colloquiorum et suggestis socialibus ad contenta sapientius tractanda."""
}

for label, text in big_samples.items():
    detected = detect_language(text)
    print(f"{label}: {detected}")

print("\n✅ DONE — Big sample testing completed!\n")
