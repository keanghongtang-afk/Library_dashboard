import Auth from "./pages/Auth";
import Navbar from "./component/navbar";
import Home from "./pages/home";
import "../src/styles.css";
import { BrowserRouter,Routes, Route } from "react-router-dom";
import { useState } from "react";

export default function App() {
  const [islogin, Setislogin] = useState(true);

  return (
    <BrowserRouter>
    <Navbar islogin={islogin}/>
      <Routes>
        <Route path="/" element={<Home islogin={islogin}/>}/>
        <Route path="/auth-page" element={<Auth />}/>
      </Routes>
    </BrowserRouter>
  );
}