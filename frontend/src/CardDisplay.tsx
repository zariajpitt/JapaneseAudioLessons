import React from 'react';
import { useState, useEffect } from 'react'
import { useParams, useNavigate} from "react-router-dom";

type Card = {
    id: number;
    english_text: string;
    target_text: string;
    language: string;
    level: string;
    grammar_point: string;
};

export default function CardDisplay(){

    const navigate = useNavigate();
    const { language } = useParams<{ language: string }>();
    const [cards, setCards] = React.useState<Card[]>([]);
    const [swipeDirection, setSwipeDirection] = 
    React.useState<"left" | "right" | null>(null);
    const [isAnimating, setIsAnimating] = React.useState<boolean>(false);
    const [currentIndex, setCurrentIndex] = React.useState<number>(0);
    const [error, setError] = useState("");
    const [showKanji, setShowKanji] = useState<boolean>(false);

    function pickText(text: string): string {
        const [kanji, kana] = text.split("|");
        if (!kana) return kanji;            // old cards with no "|" just show as-is
        return showKanji ? kanji : kana;
      }
    useEffect(() => {
        async function loadCards(){
            try{
                const response =  await fetch(`http://localhost:5000/${language}`);

                if(!response.ok){ throw new Error("Could not load cards");
                }
                const data : Card[] = await response.json();
                setCards(data);
            }
            catch (error) {
                setError("Unable to load cards from server.")
                console.error(error);
            }
        }

        loadCards();
    }, []);

    async function handleSwipe(decision: "like" | "skip"){

        if(isAnimating) return;

        const currentCard = cards[currentIndex]
        if (!currentCard) return;
        
        setIsAnimating(true);
        setError("");

        setSwipeDirection(decision === "like" ? "right": "left");
        

        try {
            await new Promise(resolve => setTimeout(resolve, 300));
            // Send the user's decision to Flask.
            const response = await fetch(
                `http://localhost:5000/api/cards/${currentCard.id}/decision`,
                {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({decision: decision})
                }
            );
            if(!response.ok){
                throw new Error("Could not save decision");
            }

            // Move to the next card.
            setCurrentIndex(previousIndex => previousIndex + 1);
            
        }
        catch (error) {
            setError("Could not save your decison. Try Again");
            console.error(error);
        }
        finally {
            setSwipeDirection(null);
            setIsAnimating(false);
        }
    }
    const currentCard = cards[currentIndex];
    return(
        <>
           
            <div>
                <button className="btn" onClick={() => navigate("/")}>Back</button>
            </div>
            {language === "Japanese" ? 
            <label className="switch">
                <input
                type="checkbox" checked={showKanji}
                onChange={(e) => setShowKanji(e.target.checked)}
                />Kanji
                </label> : <></>}
            <main className="card-container">

                <h1>{language} Lesson Creator</h1>

                {error && <p>{error}</p>}
                {/* Display the current card if one exists. */}
                {currentCard ? (

                    <article key={currentCard.id} 
                    className={`card ${swipeDirection ? `card-${swipeDirection}` : ""}`}>
                        <h3>{currentCard.english_text}</h3>
                        <p>{currentCard.level} {currentCard.language}: {pickText(currentCard.target_text)}</p>
                        <p>{currentCard.grammar_point}</p>
                    </article>)
                : (<p>No more cards available!</p>)
                }
                {currentCard && (
                    <div>
                        <button className="btn" onClick={() => handleSwipe("skip")}
                            disabled={isAnimating}>skip</button>
                            <button className="btn" onClick={() => handleSwipe("like")}
                            disabled={isAnimating}>like</button>
                    </div>
                    )
                }
            </main>
            <div>
                <button className="btn" className="btn" onClick={() => navigate(`/lesson/${language}/makecard`)}>Create Card</button>
                <button className="btn" className="btn" onClick={() => navigate(`/lesson/${language}/player`)}>Make Lesson</button>
            </div>
        </>
    )
    }

