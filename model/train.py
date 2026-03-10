"""
Smart Email Classifier - Model Training
Trains a Naive Bayes + TF-IDF pipeline on synthetic email data.
"""

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import re


# ─────────────────────────────────────────────
# 1. Synthetic Dataset Generation
# ─────────────────────────────────────────────

EMAILS = {
    "spam": [
        "Congratulations! You've won a $1000 gift card. Click here to claim now!",
        "FREE MONEY! Limited time offer. Act now before it expires!",
        "You have been selected for a cash prize. Verify your account today.",
        "Earn $500 a day working from home. No experience needed!",
        "URGENT: Your account will be suspended. Confirm your details immediately.",
        "Buy cheap medications online. No prescription required. Best prices!",
        "Nigerian prince needs your help transferring $5 million. Reply now.",
        "You are the lucky winner of our weekly lottery. Claim your prize.",
        "Make money fast! Investment opportunity of a lifetime. Join today.",
        "Lose 20 pounds in 2 weeks with this one weird trick!",
        "Hot singles in your area want to meet you tonight!",
        "Exclusive deal: Get iPhone 15 for free. Limited stocks available!",
        "Your PayPal account has been compromised. Click link to secure it.",
        "Work from home opportunity. Earn $2000 weekly with no skills needed.",
        "Congratulations! You qualify for a personal loan of $50,000.",
        "Double your Bitcoin investment in 24 hours. Guaranteed returns!",
        "You've been pre-approved for a credit card with 0% interest.",
        "FINAL NOTICE: Claim your prize or it will be forfeited.",
        "Click here to unsubscribe from debt. Instant relief guaranteed.",
        "Meet hot local singles. Sign up for free today!",
        "Get rich quick with our proven system. Thousands already earning!",
        "Your computer has a virus! Call this number immediately.",
        "Special promotion: Buy 1 get 10 free. Today only!",
        "You owe taxes. Pay immediately to avoid arrest.",
        "Extend your car warranty before it's too late!",
    ],
    "promotion": [
        "Flash sale! 50% off all items this weekend only. Shop now!",
        "Your exclusive coupon inside: 20% off your next purchase.",
        "New arrivals just dropped. Discover our latest collection.",
        "Don't miss out — sale ends Sunday. Up to 70% off.",
        "You have reward points expiring soon. Use them before they're gone.",
        "Introducing our new product line. Be the first to try it.",
        "Members-only sale starts tomorrow. Early access for you!",
        "Weekly deals are here. Grab the best offers before they sell out.",
        "We miss you! Here's 15% off to welcome you back.",
        "Summer sale is on! Free shipping on orders above $50.",
        "New season, new styles. Shop the latest trends now.",
        "Your wishlist items are on sale. Grab them today!",
        "Black Friday preview: Get early access to our biggest sale.",
        "Loyalty reward: You've earned a $10 voucher. Redeem today.",
        "Limited edition launch — pre-order now and save 25%.",
        "Back in stock! Your favorite items are available again.",
        "Exclusive offer for newsletter subscribers: Free gift on orders over $30.",
        "End of season clearance. Prices slashed up to 80%.",
        "Upgrade your subscription and get 3 months free.",
        "Holiday gift guide is here. Find the perfect present.",
        "Two for one deal this week only. Don't miss out.",
        "Refer a friend and both get $20 off your next order.",
        "Your cart is waiting! Complete your purchase and get 10% off.",
        "New restaurant deals in your area. Order now and save.",
        "Special birthday offer just for you. Celebrate with savings!",
    ],
    "important": [
        "Your invoice for this month is attached. Payment due by end of month.",
        "Meeting scheduled for Monday at 10 AM. Please confirm attendance.",
        "Action required: Please review and sign the attached document.",
        "Your subscription renewal is coming up. Review your plan details.",
        "Project update: Milestone 2 has been completed successfully.",
        "Reminder: Annual performance review scheduled for next week.",
        "Your order has been shipped. Expected delivery in 2-3 business days.",
        "Account statement for October is now available. Please review.",
        "Team meeting agenda for Thursday. Please review and add items.",
        "Quarterly report is ready for your review. See attached.",
        "Your flight booking confirmation. Check-in opens 24 hours before.",
        "Password changed successfully on your account.",
        "New policy update effective next month. Please read carefully.",
        "Your tax documents are ready for download.",
        "Interview confirmation: Thursday at 2 PM via Zoom.",
        "Your application has been received. We will be in touch.",
        "Lease renewal notice: Your lease expires in 60 days.",
        "Health insurance enrollment deadline is approaching.",
        "Your delivery was attempted. Reschedule at your convenience.",
        "Contract renewal: Please review the updated terms.",
        "New security update available for your device.",
        "Your direct deposit has been processed successfully.",
        "Appointment reminder: Dental checkup tomorrow at 3 PM.",
        "Budget report submitted by finance team for Q3.",
        "System maintenance scheduled this Saturday from 2-4 AM.",
    ],
    "urgent": [
        "URGENT: Server is down. Production environment affected. Immediate action needed.",
        "Critical security breach detected. All passwords must be reset now.",
        "Emergency meeting in 15 minutes. Board room. All managers required.",
        "ASAP: Client escalation — CEO is requesting immediate response.",
        "Data loss alert! Backup failed last night. Investigate immediately.",
        "CRITICAL: Payment processing system offline. Revenue impact ongoing.",
        "Immediate response needed: Legal deadline is today at 5 PM.",
        "SOS: Team member hospitalized. Need coverage for today's shift urgently.",
        "ALERT: Unauthorized login attempt on your admin account detected.",
        "Time-sensitive: Offer expires in 2 hours. Requires your approval.",
        "Emergency: Office flooded. All staff please report to backup location.",
        "CRITICAL BUG: App crashing for all users. Fix required immediately.",
        "Urgent recall notice: Product defect identified. Stop distribution now.",
        "Final warning: Account will be permanently deleted in 24 hours.",
        "Hospital billing error needs correction before end of business today.",
        "DEADLINE TODAY: Submit your quarterly tax filing before midnight.",
        "Power outage at HQ. Emergency generators running. IT on standby.",
        "Urgent: Visa application requires additional document by tomorrow.",
        "BREAKING: Major client threatening to cancel contract. Call required now.",
        "System alert: Disk space critically low. Immediate cleanup required.",
        "Employee complaint filed. HR requires your statement by end of day.",
        "Urgent: Child school called — please contact them immediately.",
        "Production database corrupted. All hands on deck required.",
        "Urgent medical prescription needs authorization within the hour.",
        "Network intrusion detected in real time. Security team alerted.",
    ]
}


def generate_dataset():
    records = []
    for label, emails in EMAILS.items():
        for email in emails:
            records.append({"text": email, "label": label})
    df = pd.DataFrame(records)
    # Shuffle
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    return df


# ─────────────────────────────────────────────
# 2. Text Preprocessing
# ─────────────────────────────────────────────

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', '', text)       # Remove URLs
    text = re.sub(r'\S+@\S+', '', text)               # Remove emails
    text = re.sub(r'[^a-z\s]', ' ', text)             # Keep only letters
    text = re.sub(r'\s+', ' ', text).strip()           # Normalize whitespace
    return text


# ─────────────────────────────────────────────
# 3. Train Model
# ─────────────────────────────────────────────

def train_model():
    df = generate_dataset()
    df["clean_text"] = df["text"].apply(preprocess_text)

    X = df["clean_text"]
    y = df["label"]

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            stop_words="english",
            min_df=1
        )),
        ("clf", MultinomialNB(alpha=0.5))
    ])

    # 5-fold cross-validation
    cv_scores = cross_val_score(pipeline, X, y, cv=5, scoring="accuracy")

    # Final train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    report = classification_report(y_test, y_pred, output_dict=True)
    cm = confusion_matrix(y_test, y_pred, labels=["spam", "promotion", "important", "urgent"])

    # Save model
    os.makedirs("model", exist_ok=True)
    with open("model/email_classifier.pkl", "wb") as f:
        pickle.dump(pipeline, f)

    print(f"✅ Model trained successfully!")
    print(f"   CV Accuracy: {cv_scores.mean():.2%} ± {cv_scores.std():.2%}")
    print(f"   Test Accuracy: {report['accuracy']:.2%}")

    return pipeline, cv_scores, report, cm, df


if __name__ == "__main__":
    train_model()
