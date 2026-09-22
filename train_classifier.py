import json
import os
import joblib
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, classification_report
from utils.preprocessing import clean_and_normalize_text

def run_model_training_and_comparison():
    data_path = os.path.join("data", "documents_dataset.json")
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    texts = [clean_and_normalize_text(item["text"]) for item in data]
    labels = [item["label"] for item in data]
    unique_labels = sorted(list(set(labels)))

    # Enhanced TF-IDF with sublinear tf and character n-grams alongside word n-grams
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)
    X = vectorizer.fit_transform(texts)
    y = np.array(labels)

    # Models: using stronger regularization C=5.0 for Logistic Regression
    models = {
        "Logistic Regression": LogisticRegression(C=5.0, max_iter=300, random_state=42),
        "Linear SVM": CalibratedClassifierCV(LinearSVC(C=2.0, random_state=42)),
        "Multinomial Naive Bayes": MultinomialNB(alpha=0.5)
    }

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    comparison_results = {}

    for name, model in models.items():
        scoring = ['accuracy', 'precision_weighted', 'recall_weighted', 'f1_weighted']
        scores = cross_validate(model, X, y, cv=cv, scoring=scoring)
        comparison_results[name] = {
            "Accuracy": float(scores['test_accuracy'].mean()),
            "Precision": float(scores['test_precision_weighted'].mean()),
            "Recall": float(scores['test_recall_weighted'].mean()),
            "F1-Score": float(scores['test_f1_weighted'].mean())
        }

    # Held-out split evaluation
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(
        texts, labels, test_size=0.3, random_state=42, stratify=labels
    )
    
    test_vec = TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)
    X_train_vec = test_vec.fit_transform(X_train_raw)
    X_test_vec = test_vec.transform(X_test_raw)

    eval_clf = LogisticRegression(C=5.0, max_iter=300, random_state=42)
    eval_clf.fit(X_train_vec, y_train)
    y_pred = eval_clf.predict(X_test_vec)

    acc = float(accuracy_score(y_test, y_pred))
    prec, rec, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted')
    report = classification_report(y_test, y_pred, target_names=unique_labels, digits=4)
    cm = confusion_matrix(y_test, y_pred, labels=unique_labels)

    # Final production model
    final_vec = TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)
    X_full = final_vec.fit_transform(texts)
    
    final_model = LogisticRegression(C=5.0, max_iter=300, random_state=42)
    final_model.fit(X_full, labels)

    os.makedirs("models", exist_ok=True)
    joblib.dump(final_model, os.path.join("models", "classifier_model.pkl"))
    joblib.dump(final_vec, os.path.join("models", "tfidf_vectorizer.pkl"))

    eval_summary = {
        "comparison": comparison_results,
        "classes": unique_labels,
        "test_metrics": {
            "accuracy": round(acc, 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "f1_score": round(float(f1), 4)
        },
        "confusion_matrix": cm.tolist(),
        "classification_report_str": report
    }

    with open(os.path.join("models", "evaluation_metrics.json"), "w", encoding="utf-8") as f:
        json.dump(eval_summary, f, indent=2)

    print("Model retrained with C=5.0 successfully!")

if __name__ == "__main__":
    run_model_training_and_comparison()
