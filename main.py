import re
import sys

import ebooklib
from bark import SAMPLE_RATE, generate_audio, preload_models
from bs4 import BeautifulSoup
from ebooklib import epub
from scipy.io.wavfile import write as write_wav


def extract_text_from_epub(file_path):
    try:
        book = epub.read_epub(file_path)
        text_content = []

        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.content, "html.parser")
                text = soup.get_text()

                cleaned_text = " ".join(text.split())  # Normalize whitespace
                cleaned_text = re.sub(
                    r"\bpart\d+\b", "", cleaned_text, flags=re.IGNORECASE
                )
                text_content.append(cleaned_text)

        return "\n".join(text_content).strip()

    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""


def gen_speech_file(text_input: str, output_file: str):
    preload_models()
    audio_array = generate_audio(text_input)
    write_wav(f"{output_file}.wav", SAMPLE_RATE, audio_array)


if __name__ == "__main__":
    args = sys.argv[1:]
    extracted_text = extract_text_from_epub(args[0])
    gen_speech_file(extracted_text, args[1])
