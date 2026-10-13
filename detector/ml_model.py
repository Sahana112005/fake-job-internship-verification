
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

TRAINING_DATA = [
    ("Apply through the official company careers website and attend the scheduled interview.", 0),
    ("Software developer internship with mentoring and technical assessment.", 0),
    ("Submit your resume through the recruitment portal.", 0),
    ("The company provides an offer letter after interviews.", 0),
    ("Python developer role with defined responsibilities.", 0),
    ("Apply through our careers page for an internship.", 0),
    ("Pay a registration fee immediately to guarantee your job.", 1),
    ("Pay a refundable security deposit to confirm the offer.", 1),
    ("Send your OTP and bank password to receive your salary.", 1),
    ("Pay a processing fee today or lose your job offer.", 1),
    ("Guaranteed placement after paying the job confirmation fee.", 1),
    ("Transfer money to secure your internship.", 1),
    ("Send your payment screenshot to receive your offer letter.", 1),
    ("Pay for the interview slot. Selection is guaranteed.", 1),
]


def train_model():
    texts = [item[0] for item in TRAINING_DATA]
    labels = [item[1] for item in TRAINING_DATA]

    model = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
        ("classifier", LogisticRegression(max_iter=1000))
    ])

    model.fit(texts, labels)
    return model


model = train_model()


def predict_suspicion(text):
    probabilities = model.predict_proba([text])[0]
    class_index = list(model.classes_).index(1)

    return round(float(probabilities[class_index]) * 100)
