import { useState, useEffect } from 'react'
import { useParams, useNavigate } from "react-router-dom";

export default function Player(){
    const [audioUrl, setAudioUrl] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const {language} = useParams<{ language: string }>();
    const [error, setError] = useState<string>("");
    const navigate = useNavigate();

    useEffect(() => {
        return () => {
            if (audioUrl){ URL.revokeObjectURL(audioUrl)}
        }
    },[audioUrl]);

    async function makeLesson() {
        setLoading(true);
        setError("");
        try{
            const response = await fetch(
                "http://localhost:5000/api/cards/makeLesson",
                {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({
                        "language": language
                    })
                })
                if(!response.ok){throw new Error("Could not create lesson.");}
                const audioBlob = await response.blob();
                setAudioUrl(URL.createObjectURL(audioBlob))
        }
        catch (error) {
            setError("Could not generate the lesson audio.")
            console.error(error);
        } finally {
            setLoading(false);
        }
    }
        return(
            <div className="main">
                <h1>Your Personal Lesson</h1>
                <button className="btn" onClick={makeLesson} disabled={loading}>
                    {loading ? "Generating..." : "Make Lesson"}
                </button>
                {error && <p>{error}</p>}
                {audioUrl && (
                    <>
                        <div className="audio"><audio controls src={audioUrl} /></div>
                        <a href={audioUrl} download="lesson.mp3" className="btn btn-download">Download</a>
                    </>
                )}
                <button className="btn" onClick={() => navigate(`/lesson/${language}`)}>Back</button>
            </div>

    );
}