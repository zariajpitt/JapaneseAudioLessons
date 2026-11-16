
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import CardDisplay from './CardDisplay'
import './App.css'
import Home from "./Home";
import MakeCard from "./MakeCard";
import Player from "./Player"

function App() {
  

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home/>}/>
        <Route path="/lesson/:language" element={<CardDisplay/>}/>
        <Route path="/lesson/:language/makecard" element={<MakeCard />} />
        <Route path="/lesson/:language/player" element={<Player/>}/>
      </Routes>
      
      
    </BrowserRouter>
  )
}

export default App
