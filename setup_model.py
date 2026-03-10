"""
Run this once locally to generate model/email_classifier.pkl before deploying.
Or include in a setup step if deploying without a pre-built model.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from model.train import train_model

if __name__ == "__main__":
    print("Training Smart Email Classifier model...")
    pipeline, cv_scores, report, cm, df = train_model()
    print(f"\n✅ Done! Model saved to model/email_classifier.pkl")
    print(f"   CV Accuracy: {cv_scores.mean():.2%} ± {cv_scores.std():.2%}")
