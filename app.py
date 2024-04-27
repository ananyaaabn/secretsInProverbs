# app.py

from flask import Flask, render_template, request, redirect, jsonify
import pandas as pd
import os
import google.generativeai as genai
import logging
from modules.translate_proverbs import generate_translation  

app = Flask(__name__)
#uncomment below line when run
#os.environ['GOOGLE_API_KEY'] = 'AIzaSyCnLpVtNOOacqif4bbi7u_Rt9QyDHzxPao' 
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

model = genai.GenerativeModel('gemini-pro')


def preprocess_text(text):
    return text.strip().lower()

def generate_explanation(proverb):
    explanation_prompt = f"Please provide a detailed explanation in a single paragraph of the proverb '{proverb}' in English."
    usage_prompt = f"Please provide a detailed usage in a single paragraph of the proverb '{proverb}' in English."

    try:
        explanation_response = model.generate_content(explanation_prompt)
        usage_response = model.generate_content(usage_prompt)

        explanationAI = ""
        usageAI = ""

        if explanation_response.parts:
            explanationAI = "\n".join([part.text.strip() for part in explanation_response.parts])
        else:
            logging.warning("No explanation generated.")

        if usage_response.parts:
            usageAI = "\n".join([part.text.strip() for part in usage_response.parts])
        else:
            logging.warning("No usage generated.")

        logging.info(f"Generated explanation: {explanationAI}")
        logging.info(f"Generated usage: {usageAI}")

        return explanationAI.strip(), usageAI.strip()
    except Exception as e:
        logging.error(f"Error generating explanation: {e}")
        return "", ""

def read_proverbs():
    proverbs = set()
    try:
        df = pd.read_excel('datasets/proverbs.xlsx', engine='openpyxl')
        for _, row in df.iterrows():
            try:
                proverb_id = str(row['Id'])
                proverb = preprocess_text(row['Proverb'])
                transliteration = preprocess_text(row['Transliteration'])
                translation = preprocess_text(row['Translation'])
                genre = preprocess_text(row['Genre'])
                meaning = preprocess_text(row['Meaning'])
                usage = preprocess_text(row['Usage'])
                language = preprocess_text(str(row['language']))

                proverb_entry = (proverb_id, proverb, transliteration, translation, genre, meaning, usage, language)

                proverbs.add(proverb_entry)
            except Exception as e:
                logging.error(f"Error processing row: {e}")
                continue
    except Exception as e:
        logging.error(f"Error reading Excel file: {e}")

    return proverbs

def get_genre_meaning_and_usage(proverb):
    return proverb[4], proverb[5], proverb[6]

def get_genres(proverbs):
    urdu_genres = set()
    kashmiri_genres = set()
    for proverb in proverbs:
        if proverb[7] == 'urdu':
            urdu_genres.add(proverb[4])
        elif proverb[7] == 'kashmiri':
            kashmiri_genres.add(proverb[4])
    return sorted(list(urdu_genres.intersection(kashmiri_genres)))

def get_languages(proverbs):
    valid_languages = {'urdu', 'kashmiri'}
    languages = set()
    for proverb in proverbs:
        language = proverb[7].strip().lower()
        if language in valid_languages:
            languages.add(language)
    return sorted(list(languages))

def get_proverbs_by_genre_and_language(proverbs, genre, language):
    filtered_proverbs = []
    for proverb in proverbs:
        if proverb[4].lower() == genre.lower() and proverb[7].strip().lower() == language.lower():
            filtered_proverbs.append(proverb)
    return filtered_proverbs

@app.route('/')
@app.route('/home')
def home():
    proverbs = read_proverbs()
    genres = get_genres(proverbs)
    languages = get_languages(proverbs)
    return render_template('home.html', genres=genres, languages=languages)

@app.route('/language', methods=['POST'])
def language():
    selected_genre = request.form.get('genre')
    proverbs = read_proverbs()
    languages = get_languages(proverbs)
    return render_template('language.html', genre=selected_genre, languages=languages)

@app.route('/proverbs', methods=['POST'])
def proverbs():
    selected_genre = request.form.get('genre')
    selected_language = request.form.get('language')
    proverbs = read_proverbs()
    filtered_proverbs = get_proverbs_by_genre_and_language(proverbs, selected_genre, selected_language)
    return render_template('proverbs.html', proverbs=filtered_proverbs, genre=selected_genre, language=selected_language)

@app.route('/aboutus')
def about_us():
    return render_template('aboutus.html')

@app.route('/get_proverb_details', methods=['GET'])
def get_proverb_details():
    proverb = request.args.get('proverb')
    translation = generate_translation(proverb)
    
    # Constructing a dictionary containing all the details
    proverb_details = {
        'proverb': proverb,
        'translation': translation,
    }
    return jsonify(proverb_details)


@app.route('/explanation')
def explanation():
    selected_proverb = request.args.get('proverb', '')

    proverbs = read_proverbs()
    for proverb in proverbs:
        if proverb[1] == selected_proverb:
            genre, meaning, usage = get_genre_meaning_and_usage(proverb)
            transliteration = proverb[2]
            break
    else:
        genre, meaning, usage, transliteration = "", "", "", ""

    detailed_explanation = generate_explanation(selected_proverb)
    model_translation = generate_translation(selected_proverb)

    return render_template('explanation.html', selected_proverb=selected_proverb,
                           genre=genre, meaning=meaning, usage=usage, transliteration=transliteration,
                           explanationAI=detailed_explanation[0],
                           usageAI=detailed_explanation[1],
                           model_translation=model_translation)
if __name__ == '__main__':
    
    app.run(debug=True)
