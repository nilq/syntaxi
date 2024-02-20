"""Shift token behaviour."""

import regex

from syntaxi.tokens import Token

capital_word_pattern = regex.compile(r"\b\p{Lu}\p{Ll}*\b")


def convert_to_shift_tokens(text: str, shift_token=Token.SHIFT):
    """Convert text to use shift tokens for capitalised words.

    Example:
        >>> convert_to_shift_tokens("Words including Århus and Æble.")
        '[SHIFT] words including [SHIFT] århus and [SHIFT] æble.'

    Note:
        This won't convert tokens with capitalised letters within
        the actual word, e.g. "LoRA".

    Args:
        text (str): Text to convert.
        shift_token (Token, optional): Shift token to use.
            Defaults to `syntaxi.tokens.Token.SHIFT`

    Returns:
        str: Converted text.
    """
    def replace_with_shift_token(match: regex.Match) -> str:
        """Replace match with shift token and lowercased word.

        Args:
            match (regex.Match): Regex match.

        Returns:
            str: Match converted to use shift tokens.
        """
        word = match.group()
        return f"{shift_token} {word[0].lower()}{word[1:]}"

    return regex.sub(capital_word_pattern, replace_with_shift_token, text)


def convert_from_shift_tokens(text: str, shift_token=Token.SHIFT):
    """Convert text from using explicit shift tokens to just regular text.

    Example:
        >>> convert_to_shift_tokens("[SHIFT] words including [SHIFT] århus and [SHIFT] æble.")
        'Words including Århus and Æble.'

    Args:
        text (str): Text to convert.
        shift_token (Token, optional): Shift token to use.
            Defaults to `syntaxi.tokens.Token.SHIFT`

    Returns:
        str: Converted text.
    """
    shift_token_pattern = regex.compile(regex.escape(shift_token) + r" (\p{Ll})")
    def to_just_capital(match: regex.Match) -> str:
        return match.group(1).upper()
    return shift_token_pattern.sub(to_just_capital, text)
