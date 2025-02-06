from pydub import AudioSegment
from pydub.playback import play

def load_audio(audio_path):
    """Load an audio file."""
    try:
        audio = AudioSegment.from_file(audio_path)
        print(f"Audio loaded successfully: {audio_path}")
        return audio
    except FileNotFoundError:
        print("Audio file does not exist.")
        return None

def play_audio(audio):
    """Play the audio."""
    if audio:
        print("Playing audio...")
        play(audio)

def change_speed(audio, speed=1.0):
    """Change the speed of the audio."""
    if audio:
        print(f"Changing speed to {speed}x...")
        new_audio = audio._spawn(audio.raw_data, overrides={
            "frame_rate": int(audio.frame_rate * speed)
        }).set_frame_rate(audio.frame_rate)
        return new_audio
    else:
        print("No audio to change speed.")
        return None

def reverse_audio(audio):
    """Reverse the audio."""
    if audio:
        print("Reversing audio...")
        return audio.reverse()
    else:
        print("No audio to reverse.")
        return None

def save_audio(audio, output_path):
    """Save the manipulated audio."""
    if audio:
        audio.export(output_path, format="wav")
        print(f"Audio saved successfully: {output_path}")
    else:
        print("No audio to save.")

# Example usage
if __name__ == "__main__":
    # Load the audio file
    audio_path = "sample.wav"  # Replace with your actual audio file path
    audio = load_audio(audio_path)
    
    if audio:
        # Play the original audio
        play_audio(audio)

        # Apply transformations
        faster_audio = change_speed(audio, 1.5)  # 1.5x speed
        reversed_audio = reverse_audio(audio)

        # Save transformed audios
        save_audio(faster_audio, "faster_sample.wav")
        save_audio(reversed_audio, "reversed_sample.wav")
