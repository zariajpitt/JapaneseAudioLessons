import { useNavigate } from "react-router-dom";
export default function Home() {
    const navigate = useNavigate();
    return (
        <div className="main main-home">
            <h1>Pick a Language</h1><br></br>
            <div className="home-buttons">
            <button className="btn" onClick={() => navigate("/lesson/Japanese")}>
                Japanese
            </button>
            <button className="btn" onClick={() => navigate("/lesson/Spanish")}>
                Spanish
            </button>
            </div>
        </div>
    )
}