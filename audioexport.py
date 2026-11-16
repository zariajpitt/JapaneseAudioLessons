import csv
import os
import edge_tts, shutil, tempfile
from pydub import AudioSegment

class AudioExport:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.english_voice = "en-US-SteffanNeural"
        self.language_voices = {
            "japanese": "ja-JP-NanamiNeural",
            "spanish": "es-MX-JorgeNeural"
        }

    def generate(self, language):
        # Make sure the requested language is supported.
        language = language.lower()
        if language not in self.language_voices:
            raise ValueError("Unsupported language")

        # Create a unique folder for this particular lesson.
        temp_dir = tempfile.mkdtemp(prefix="audio_lesson_")

        try:
            # Read the lesson phrases from the CSV.
            english_list = []
            target_list = []
            with open(self.csv_path, newline="", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    english_list.append(row["english_text"])
                    target_list.append(row["target_text"])
            print("LISTS:", len(english_list), len(target_list), english_list, target_list)
            full_lesson = AudioSegment.empty()

            # Temporary audio files belonging only to this lesson.
            english_path = os.path.join(temp_dir, "english.mp3")
            target_path = os.path.join(temp_dir, "target.mp3")

            for i in range(len(english_list)):

                # Generate the English prompt.
                edge_tts.Communicate(
                    "How do you say " + english_list[i],
                    self.english_voice,
                    rate="-10%"
                ).save_sync(english_path)

                english_audio = AudioSegment.from_file(english_path)

                # Generate the target-language response.
                edge_tts.Communicate(
                    target_list[i],
                    self.language_voices[language],
                    rate="-25%"
                ).save_sync(target_path)

                target_audio = AudioSegment.from_file(target_path)
                print("CLIP SIZES:", os.path.getsize(english_path), os.path.getsize(target_path))
                print("CLIP LENGTHS (ms):", len(english_audio), len(target_audio))
                # Add pauses between the English and target phrases.
                long_pause = AudioSegment.silent(duration=3000)
                short_pause = AudioSegment.silent(duration=800)

                lesson = (
                    english_audio
                    + long_pause
                    + target_audio
                    + short_pause
                    + target_audio
                )

                full_lesson += lesson
                
                # Delete intermediate files after combining the audio.
                os.remove(english_path)
                os.remove(target_path)
            print("FULL LESSON (ms):", len(full_lesson))
            # Export the complete lesson.
            output_path = os.path.join(temp_dir, "fullLesson.wav")
            full_lesson.export(output_path, format="wav").close()
            print("EXPORTED SIZE:", os.path.getsize(output_path))
            # Return both the MP3 path and its temporary folder.
            return output_path, temp_dir

        except Exception:
            # Clean up if audio generation fails.
            shutil.rmtree(temp_dir, ignore_errors=True)
            raise


#en-US-SteffanNeural for male voice
#en-US-AvaMultilingualNeural for female voice
#ja-JP-NanamiNeural for jp female best
#ja-JP-AoiNeural second female jp
#ja-JP-KeitaNeural male jp
#"es-MX-JorgeNeural"

        

        