import pandas as pd
from sklearn.metrics import accuracy_score, f1_score
from app.models.intent_pipeline import IntentPipeline
from app.config import TEST_PATH
from tqdm import tqdm


def evaluate():
    pipeline = IntentPipeline()
    df = pd.read_csv(TEST_PATH)

    y_true = []
    y_pred = []
    rejected = 0

    for _, row in tqdm(df.iterrows(), total=len(df)):
        result = pipeline.predict(row["text"])

        true_label = row["label"]
        predicted_intent = result["intent"]

        if result["escalate"]:
            rejected += 1
            continue

        y_true.append(true_label)
        y_pred.append(
            pipeline.df.iloc[row.name]["label"]
        )

    acc = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, average="macro")

    print(f"Accuracy: {acc:.4f}")
    print(f"Macro F1: {f1:.4f}")
    print(f"Rejection Rate: {rejected/len(df):.4f}")


if __name__ == "__main__":
    evaluate()