# 🚕 syntaxi

Make your tokenizer more syntax-friendly.

Syntaxi will encode capital words using a special shift-token, allowing words to be effectively capital-invariant. "Dog" and "dog" are the same word. Without Syntaxi, your language model need to learn these words as if they were not the same.

Let your language model learn to think in terms of shift tokens, rather than learning words twice.

## Getting started

Load an existing, pre-trained HuggingFace tokenizer to be patched by Syntaxi.

**Create directly using `Tokenizer.from_pretrained`**
```py
import syntaxi

tokenizer = syntaxi.huggingface_tokenizer("nilq/baby-tokenizer")
encoded = tokenizer.encode("My dog is a Dog, and my Dog is a dog.")

encoded.tokens
# ['[SHIFT]', '▁my', '▁dog', '▁is', '▁a', '▁', '[SHIFT]', '▁dog,', '▁and', '▁my', '▁', '[SHIFT]', '▁dog', '▁is', '▁a', '▁dog.']

tokenizer.decode(encoded.ids)
# "My dog is a Dog, and my Dog is a dog."
```

**Manually patch tokenizer**
```py
import syntaxi

tokenizer = ...

# Original `tokenizer` stays the same.
syntaxi_tokenizer = syntaxi.patched_tokenizer(tokenizer)
```
