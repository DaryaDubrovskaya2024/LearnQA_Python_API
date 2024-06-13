import pytest

def test_length_phrase():
    phrase = input("Enter phrase: ")

    assert len(phrase) < 15, f"Phrase is too long: {len(phrase)} characters"