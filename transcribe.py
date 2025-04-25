import speech_recognition as sr
import threading
import time
import queue
from datetime import datetime
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MeetingTranscriber:
    def _init_(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.speakers = ("Speaker A", "Speaker B")
        self.current_speaker = 0
        self.audio_queue = queue.Queue()
        self.transcript = []
        self.is_running = False
        self.last_switch_time = time.time()
        self.silence_threshold = 1.5  # Switch after 3 seconds silence

        # Audio setup
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
        print("\n=== MEETING TRANSCRIBER ===")
        print(f"• Speakers: {self.speakers[0]} and {self.speakers[1]}")
        print("• Press Ctrl+C to end and save transcript")
        print("===========================\n")

    def start(self):
        self.is_running = True
        
        # Start background listener
        self.stop_listening = self.recognizer.listen_in_background(
            self.microphone,
            self._audio_callback,
            phrase_time_limit=8  # Longer phrases
        )
        
        # Start processing thread
        processor = threading.Thread(target=self._process_audio)
        processor.daemon = True
        processor.start()

        # Main loop
        try:
            while self.is_running:
                # Auto-switch on prolonged silence
                if time.time() - self.last_switch_time > self.silence_threshold:
                    self._switch_speaker()
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n\nStopping transcription...")
            self._shutdown()

    def _audio_callback(self, recognizer, audio):
        if self.is_running:
            self.audio_queue.put(audio)

    def _process_audio(self):
        while self.is_running:
            try:
                audio = self.audio_queue.get(timeout=1)
                text = self._recognize_speech(audio)
                
                if text:
                    self.last_switch_time = time.time()
                    entry = f"{self.speakers[self.current_speaker]}: {text}"
                    self.transcript.append(entry)
                    print(entry)  # Clean single-line output

            except queue.Empty:
                continue

    def _switch_speaker(self):
        """Switch speaker only if meaningful speech occurred"""
        if len(self.transcript) > 0 and len(self.transcript[-1].split()) > 3:
            self.current_speaker = 1 - self.current_speaker
            self.last_switch_time = time.time()

    def _recognize_speech(self, audio):
        try:
            return self.recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            print("\n[System] Could not request results")
            return None

    def _shutdown(self):
        """Clean shutdown procedure"""
        self.is_running = False
        
        # Stop background listening
        if hasattr(self, 'stop_listening'):
            self.stop_listening(wait_for_stop=False)
        
        # Save transcript
        self._save_transcript()

    def _save_transcript(self):
        """Save transcript to file and generate summary"""
        if not self.transcript:
            print("\nNo conversation recorded")
            return

        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"meeting_transcript_{timestamp}.txt"
        
        try:
            # Save transcript file
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=== MEETING TRANSCRIPT ===\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
                f.write("Participants: Speaker A, Speaker B\n\n")
                f.write("\n".join(self.transcript))
            
            print(f"\nTranscript saved to: {filename}")
            print("\n=== FINAL TRANSCRIPT ===")
            print("\n".join(self.transcript))
            
            # Generate summary using Gemini
            self._generate_gemini_summary(filename)
            
        except Exception as e:
            print(f"\n[Error] Could not save transcript: {str(e)}")

    def _generate_gemini_summary(self, transcript_file):
        """Generate summary using Gemini's free API"""
        try:
            # Configure Gemini
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
            model = genai.GenerativeModel('gemini-1.5-pro-001')
            
            # Read transcript content
            with open(transcript_file, 'r', encoding='utf-8') as f:
                transcript_content = f.read()
            
            # Create prompt
            prompt = """Please analyze this meeting transcript and provide:
            1. Brief 3-point summary
            2. Top 5 discussion points
            3. Action items (with responsible persons)
            4. Any decisions made

            Format the output with clear headings and bullet points.
            Keep it concise and business-appropriate.
            
            Transcript:\n""" + transcript_content
            
            # Generate response
            print("\nGenerating meeting summary... (Press Ctrl+C again to skip)")
            response = model.generate_content(prompt)
            
            # Save summary
            summary_filename = transcript_file.replace("transcript", "summary")
            with open(summary_filename, 'w', encoding='utf-8') as f:
                f.write("=== MEETING SUMMARY ===\n")
                f.write(response.text)
            
            print(f"\nSummary saved to: {summary_filename}")
            print("\n=== MEETING SUMMARY ===")
            print(response.text)
            
        except KeyboardInterrupt:
            print("\nSkipping summary generation")
        except Exception as e:
            print(f"\n[Error] Could not generate summary: {str(e)}")
            print("Note: Please ensure you have:")
            print("1. A valid Gemini API key in .env file")
            print("2. google-generativeai package installed")
            print("3. Active internet connection")

if _name_ == "_main_":
    transcriber = MeetingTranscriber()
    transcriber.start()