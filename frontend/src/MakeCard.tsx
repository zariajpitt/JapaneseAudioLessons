import { useParams, useNavigate } from "react-router-dom";
import { useState } from "react";
export default function MakeCard(){
    const {language} = useParams<{ language: string }>();
    const [english, setEnglish] = useState<string>("");
    const [target, setTarget] = useState<string>("");
    const [level, setLevel] = useState<string>("A1");
    const [grammar, setGrammar] = useState<string>("");
    const [politeness, setPoliteness] = useState<string>("");
    const [status, setStatus] = useState<string>("");
    const navigate = useNavigate();
    async function submitEntry(e: React.SubmitEvent<HTMLFormElement>){
        e.preventDefault();               // stop the page from reloading
        setStatus("Saving...");
        try {
            const response = await fetch(`http://localhost:5000/api/cards/submit`,
            {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                english_text: english,
                target_text: target,
                language: language,
                level: level,
                grammar_point: grammar,
                politeness: politeness
                                    }),
            })
            if (!response.ok) throw new Error("Save failed");

            setStatus("Card added!");
            setEnglish("");                 // clear the form
            setTarget("");
            setGrammar("");
            setPoliteness("");
          } catch (err) {
            console.error(err);
            setStatus("Could not save the card.");
          }
        }

    return (
        <main className="main">
            <h1>Enter Card Information</h1>

            <form className="cardForm" onSubmit={submitEntry}>
                <label htmlFor="english_text">English:</label>
                <input type='text' id="english_text" name="english_text" 
                value={english} onChange={(e) => setEnglish(e.target.value)} required></input>
                <label htmlFor="target_text">{language}:</label>
                <input type='text' id="target_text" name="target_text"
                value={target} onChange={(e) => setTarget(e.target.value)} required></input>
                {/* Japanese Choices */}
                {language?.toLowerCase() === "japanese" &&
                    <>
                        <label htmlFor="level">Level:</label>
                        <select id="level" value={level} onChange={(e) => setLevel(e.target.value)}>
                            <option value="N5">N5</option>
                            <option value="N4">N4</option>
                            <option value="N3">N3</option>
                            <option value="N2">N2</option>
                            <option value="N1">N1</option>
                        </select>
                        <label htmlFor="politeness">Politeness</label>
                        <select id="politeness" value={politeness} onChange={(e) => setPoliteness(e.target.value)}>
                            <option value="Formally">Formally</option>
                            <option value="Informally">informally</option>
                            
                        </select>
                    </>}
                    {/* Spanish Choices */}
                {language?.toLowerCase() === "spanish" &&
                    <>
                        <label htmlFor="level">Level:</label>
                        <select id="level" value={level} onChange={(e) => setLevel(e.target.value)}>
                            <option value="A1">A1</option>
                            <option value="A2">A2</option>
                            <option value="B1">B1</option>
                            <option value="B2">B2</option>
                            <option value="C1">C1</option>
                            <option value="C2">C2</option>
                        </select>
                    </>}
                <label htmlFor="grammar_point">Grammer Point:</label>
                <input type='text' id="grammar_point" name="grammar_point"
                value={grammar} onChange={(e) => setGrammar(e.target.value)} required />
                <button className="btn" type="submit">Submit</button>
            </form>
            <br></br>
            <p>Please make sure your sentences are written correctly so that your lesson is generated with correct pronounciation.</p>
            <div>
                <button className="btn" onClick={() => navigate(`/lesson/${language}`)}>Back</button>
            </div>
        </main>
    )
}