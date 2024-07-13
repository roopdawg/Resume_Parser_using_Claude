from transformers import Trainer, TrainingArguments, AutoModelForSequenceClassification, AutoTokenizer
from datasets import Dataset

def fine_tune_model(train_texts, train_labels, model_name='bert-base-uncased', num_labels=2):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)

    def tokenize_function(examples):
        return tokenizer(examples['text'], padding="max_length", truncation=True)

    dataset = Dataset.from_dict({'text': train_texts, 'label': train_labels})
    tokenized_datasets = dataset.map(tokenize_function, batched=True)

    training_args = TrainingArguments(
        output_dir="./results",
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=3,
        weight_decay=0.01,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets,
        eval_dataset=tokenized_datasets,  # Use a separate validation set if available
    )

    trainer.train()
    return model, tokenizer

