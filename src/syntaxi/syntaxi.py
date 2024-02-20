"""Monkey patching tokenizers."""

import copy

from syntaxi.tokens import Token
from syntaxi.shift import convert_to_shift_tokens, convert_from_shift_tokens

from tokenizers import Tokenizer


def patched_tokenizer(tokenizer):
    """Get Syntaxi-patched tokenizer.

    Args:
        tokenizer (Tokenizer): Tokenizer to patch.

    Returns:
        Tokenizer: Patched tokenizer.
    """
    new_tokenizer = copy.copy(tokenizer)
    new_tokenizer.add_special_tokens([Token.SHIFT.value])

    original_encode = new_tokenizer.encode
    original_decode = tokenizer.decode

    def patched_encode(self, text: str, **kwargs):
        processed_text = convert_to_shift_tokens(text=text)
        kwargs["add_special_tokens"] = True
        return original_encode(processed_text, **kwargs)

    def patched_decode(self, text: list[str]) -> str:
        return convert_from_shift_tokens(original_decode(text))

    new_tokenizer.encode = patched_encode.__get__(tokenizer)
    new_tokenizer.decode = patched_decode.__get__(tokenizer)

    return new_tokenizer

def huggingface_tokenizer(tokenizer_id: str) -> Tokenizer:
    """Get Syntaxi-patched HuggingFace tokenizer.

    Args:
        tokenizer_id (str): Identifier/path of tokenizer.

    Returns:
        Tokenizer: Tokenizer, but it's patched.
    """
    return patched_tokenizer(Tokenizer.from_pretrained(tokenizer_id))
