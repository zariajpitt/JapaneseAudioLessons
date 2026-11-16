import io, os, shutil
from DataBase import DataBase
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from audioexport import AudioExport
import pandas as pd, tempfile
app = Flask(__name__)
CORS(app)
db = DataBase()

@app.route("/<language>", methods=["GET", "POST"])
def index(language):
    
    text = db.loadCards(language) 
    return jsonify(text), 200

@app.route("/api/cards/submit", methods=["POST"])
def submitEntry():
    data = request.get_json()
    english = data.get("english_text") + data.get("politeness")
    target = data.get("target_text")
    language = data.get("language")
    level = data.get("level")
    grammar = data.get("grammar_point")
    db.entry(english, target, language, level, grammar)
    return jsonify({"message": "Card added"}), 200

@app.route("/api/cards/<int:card_id>/decision", methods=["POST"])
def saveCardDecision(card_id):

    try:
        data = request.get_json()
        user_id = 5 #temporary id until we set up individual user sessions

        decision = data.get("decision")
        if decision not in ["like", "skip"]:
            return jsonify({"error": "Invalid decision"}), 400

        #save decision to postgresql
        db.saveDecision(user_id, card_id, decision)

        return jsonify({"message": "Decision saved"}), 200

    except Exception as error:
        print("ERROR SAVING DECISION:", error)

        return jsonify({"error": str(error)}), 500

@app.route("/api/cards/makeLesson", methods=["POST"])
def makeLesson():
    
    data = request.get_json()
    language = data.get("language").lower()
    user_id = 5
    lessonCards = db.getLessonCards(user_id, language)
    if language == "japanese":
        for i in range(len(lessonCards)):
            lessonCards[i]["target_text"] = lessonCards[i]["target_text"].split("|")[-1]
    if not lessonCards:
        return jsonify({"error": "No liked cards yet"}), 400
    
    temp_dir = tempfile.mkdtemp(prefix="output_")
    csv_path = os.path.join(temp_dir, "cards.csv")   # a file inside the folder
    pd.DataFrame(lessonCards).to_csv(csv_path, index=False)
    
    audioExport = AudioExport(csv_path)
    output_path, audio_temp_dir = audioExport.generate(language)
    print("OUTPUT:", output_path, os.path.getsize(output_path), "bytes")
    #tuple [output_path, temp_dir]

    # read into memory first, then clean up the temp files
    with open(output_path, "rb") as f:
        audio_bytes = io.BytesIO(f.read())
    shutil.rmtree(temp_dir, ignore_errors=True)
    shutil.rmtree(audio_temp_dir, ignore_errors=True)

    return send_file(audio_bytes, mimetype="audio/wav", download_name="lesson.wav")
            
    

if __name__ == "__main__":
    app.run(debug=True, port=5000)
    