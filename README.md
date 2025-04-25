

# Professional Summary Generator with Meeting Transcription and Encryption

This project is a **Professional Summary Generator** that provides a user-friendly interface to generate personalized summaries for individuals based on their name, organization, and type of organization. It also integrates a **Meeting Transcription** feature that records and transcribes conversations between multiple speakers, and it includes encryption functionality for securely storing and sharing data.

## Key Features:

1. **Professional Summary Generation**:
   - The app collects a person's name, their organization, and the type of organization they are associated with.
   - It uses a combination of Google and LinkedIn search results to gather relevant information.
   - A summary is generated based on the collected data using the Gemini model (Google's generative AI).
   - The summary can be exported in different formats (PDF or TXT).
   - The summary can also be encrypted for secure storage or sharing.

2. **Meeting Transcription**:
   - The app listens to audio from two speakers, automatically switching between them based on voice activity.
   - It transcribes the audio into a readable format, assigning each part of the transcript to either Speaker A or Speaker B.
   - After the meeting, the transcript is saved as a text file, and a summary of the conversation is generated using Gemini.
   - Users can download the transcript and the meeting summary.

3. **File Encryption & Decryption**:
   - The app supports encrypting the generated summaries (or any other files) using **Fernet encryption**.
   - Encrypted files can be safely shared and later decrypted by the user.
   - The decryption process can be done by uploading the encrypted file, which will reveal the original summary.

4. **Gradio Interface**:
   - The application uses Gradio to create an interactive web interface where users can input data (such as name, organization, etc.) and interact with the generated summary and transcription.
   - It also provides buttons for exporting, encrypting, and decrypting files.

## How It Works:

1. **Generate Professional Summary**:
   - The user inputs their name, organization, and organization type.
   - The app uses Google and LinkedIn search to gather details about the person and the organization.
   - The collected information is processed into a professional summary using Gemini AI.
   - The user can export the summary in a format of their choice (PDF or TXT), and optionally encrypt the file.

2. **Transcribe Meetings**:
   - The app listens to audio input from two speakers, processes the audio in real-time, and creates a transcript.
   - The transcript is automatically divided into sections, labeled by the speaker.
   - After the meeting, the user can download the transcript and a summary of the discussion, which is generated using Gemini AI.

3. **Encrypt and Decrypt Files**:
   - The app allows users to export summaries or transcripts as encrypted files.
   - The encrypted file can later be decrypted, revealing the original content.

## Requirements:
- Python 3.12+
- Gradio
- Google Generative AI (Gemini) API
- Google Search API (SerpAPI)
- FPDF (for generating PDFs)
- `cryptography` library for file encryption
- `speechrecognition` library for audio transcription
- `python-dotenv` for environment variable management

## Installation:
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file and add your **Gemini API Key** and **SerpAPI Key**.

4. Run the application:
   ```bash
   python app.py
   ```

## Usage:
1. **Generate Professional Summary**:
   - Input the person's name, organization, and organization type.
   - Click **Generate Summary** to get the professional profile.
   - Export the summary as PDF or TXT and optionally encrypt it.

2. **Transcribe Meetings**:
   - Start the transcription by clicking the **Start Transcription** button.
   - The app will transcribe the meeting audio and switch speakers as needed.
   - After the meeting, you can download the transcript and summary.

3. **Encrypt & Decrypt Files**:
   - Export summaries/transcripts as encrypted files.
   - Upload encrypted files to decrypt and view the original summary.

## Example Usage:
- **Professional Summary Generator**: Generate a summary of a person's profile using data from the web and LinkedIn.
- **Meeting Transcriber**: Record and transcribe a meeting with automatic speaker identification.
- **File Encryption**: Securely store and share summaries with encryption.

## License:
This project is licensed under the MIT License.
