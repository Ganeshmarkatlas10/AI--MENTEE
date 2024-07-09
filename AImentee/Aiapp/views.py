from django.shortcuts import render, redirect
from .models import SpeechRecognition, Translation
import json


# def load_data(request):
#     print(request.body.decode('utf-8'))
#     if request.method == "POST":
#         payload = json.loads(request.body.decode('utf-8'))
#         selected_language = payload["language"]
#         speech_data = payload["speech"]
#         return render(request, "resume.html", speech_data)
#     resume_data = {
#         "name": "markatlas",
#         "Career_Focus": "working as apython developer",
#         "Objective": "I am seeking employment with a company where I can grow professionally and personally. I seek challenging opportunities where I can fully use my skills for the success of the organization. I want to succeed in a stimulating and challenging environment that will provide me with advancement opportunities.",
#         "Job_Title": "software_developer",
#         "company_name": "Markatlas",
#         "start_end_date": "03-07-2024 - Present",
#         "Job_responsibilities": "Communicate with customers and meet their various needs",
#         "Accomplishments": "Making or saving the company money Exceeding expectations Improving customer experience",
#         "School_Name": "Sri chaitanya",
#         "school_details": "ssc-2018",
#         "Skills": "Python,django"      
        
#         }
#     return render(request, "resume.html", resume_data)


def load_home_page(request):
    return render(request, "index.html")
# def resume_view(request):
#     resume = Resume.objects.first()
#     return render(request, "Aiapp/resume.html", {"resume": resume})

# def update_resume(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         summary = request.POST.get("summary")
#         Resume.objects.update_or_create(id=1, defaults={"name": name, "summary": summary})
#         return redirect("resume_view")
#     return render(request, "Aiapp/resume.html", {"resume": Resume.objects.first()})

import speech_recognition as sr
from googletrans import Translator
from docx import Document

def recognize_speech(language_code="en-US", wait_time="60"):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio, language=language_code)
        return text
    except sr.UnknownValueError:
        return "Sorry, I did not understand that."
    except sr.RequestError:
        return "Sorry, I am unable to access the speech recognition service."

def translate_text(text, target_language):
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    return translated.text

def save_to_docx(text, filename):
    doc = Document()
    doc.add_paragraph(text)
    doc.save(filename)
    print(f"Saved to {filename}")

if __name__== "__main__":
    language_options = {
        "hindi": "hi-IN",    # Hindi
        "telugu": "te-IN",   # Telugu
        "tamil": "ta-IN"     # Tamil
    }

    print("Please say the language you want to use: Hindi, Telugu, or Tamil.")
    recognized_text = recognize_speech("en-US")

    print(f"You said: {recognized_text}")

    chosen_language = recognized_text.lower().strip()

    if chosen_language in language_options:
        language_code = language_options[chosen_language]
        print(f"Selected language: {language_code}")
        print("You can start speaking now...")
        recognized_text = recognize_speech(language_code)
        print("Recognized Speech:", recognized_text)

        if recognized_text not in ["Sorry, I did not understand that.", "Sorry, I am unable to access the speech recognition service."]:
            print("Would you like to translate this to another language? (Options: Hindi, Telugu, Tamil, English)")
            target_language_choice = recognize_speech("en-US").lower().strip()

            translation_options = {
                "hindi": "hi",
                "telugu": "te",
                "tamil": "ta",
                "english": "en"
            }

            if target_language_choice in translation_options:
                target_language_code = translation_options[target_language_choice]
                translated_text = translate_text(recognized_text, target_language_code)
                print(f"Translated Text: {translated_text}")
                save_to_docx(translated_text, f"translated_{target_language_choice}.docx")
            else:
                print("Invalid choice. Please restart and choose a valid translation language.")
    else:
        print("Invalid choice. Please restart and choose a valid language.")

